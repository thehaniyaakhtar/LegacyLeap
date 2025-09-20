from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import json
import os
from datetime import datetime
import asyncio

from models import *
from legacy_ingestion import AS400IngestionEngine
from ai_transformer import AITransformationEngine
from websocket_handler import manager

app = FastAPI(title="AS/400 Legacy Modernization Assistant", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
ingestion_engine = AS400IngestionEngine()
ai_engine = AITransformationEngine(api_key=os.getenv("OPENAI_API_KEY"))

# In-memory storage for demo (in production, use a database)
legacy_data_store: Dict[str, LegacyData] = {}
modernized_data_store: Dict[str, ModernizedData] = {}

@app.get("/")
async def root():
    return {
        "message": "AS/400 Legacy Modernization Assistant",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload",
            "ingest": "/ingest",
            "transform": "/transform/{legacy_id}",
            "query": "/query/{modernized_id}",
            "microservices": "/microservices/{modernized_id}",
            "dashboard": "/dashboard"
        }
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process AS/400 files"""
    try:
        content = await file.read()
        content_str = content.decode("utf-8")
        
        # Determine file type and process accordingly
        filename = file.filename.lower()
        
        if filename.endswith('.txt') or filename.endswith('.dat'):
            legacy_data = ingestion_engine.parse_flat_file(content_str, file.filename)
        elif filename.endswith('.sql') or 'create table' in content_str.lower():
            legacy_data = ingestion_engine.parse_db2_table(content_str, file.filename)
        elif 'screen' in filename or 'display' in filename:
            legacy_data = ingestion_engine.parse_green_screen(content_str, file.filename)
        elif filename.endswith('.rpg') or filename.endswith('.rpgle'):
            legacy_data = ingestion_engine.parse_rpg_program(content_str, file.filename)
        else:
            # Default to flat file
            legacy_data = ingestion_engine.parse_flat_file(content_str, file.filename)
        
        # Store the legacy data
        legacy_data_store[legacy_data.id] = legacy_data
        
        # Send real-time update
        await manager.send_processing_update(legacy_data.id, "uploaded", 25)
        
        return {
            "success": True,
            "legacy_id": legacy_data.id,
            "source_type": legacy_data.source_type,
            "metadata": legacy_data.metadata,
            "message": f"Successfully processed {file.filename}"
        }
        
    except Exception as e:
        await manager.send_error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@app.post("/ingest")
async def ingest_legacy_data(
    content: str,
    source_type: DataSourceType,
    name: str
):
    """Ingest legacy data directly"""
    try:
        if source_type == DataSourceType.FLAT_FILE:
            legacy_data = ingestion_engine.parse_flat_file(content, name)
        elif source_type == DataSourceType.DB2_TABLE:
            legacy_data = ingestion_engine.parse_db2_table(content, name)
        elif source_type == DataSourceType.GREEN_SCREEN:
            legacy_data = ingestion_engine.parse_green_screen(content, name)
        elif source_type == DataSourceType.RPG_PROGRAM:
            legacy_data = ingestion_engine.parse_rpg_program(content, name)
        else:
            raise HTTPException(status_code=400, detail="Invalid source type")
        
        legacy_data_store[legacy_data.id] = legacy_data
        
        return {
            "success": True,
            "legacy_id": legacy_data.id,
            "source_type": legacy_data.source_type,
            "metadata": legacy_data.metadata
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error ingesting data: {str(e)}")

@app.post("/transform/{legacy_id}")
async def transform_legacy_data(legacy_id: str):
    """Transform legacy data to modern format using AI"""
    try:
        if legacy_id not in legacy_data_store:
            raise HTTPException(status_code=404, detail="Legacy data not found")
        
        legacy_data = legacy_data_store[legacy_id]
        
        # Send progress updates
        await manager.send_processing_update(legacy_id, "analyzing", 50)
        
        modernized_data = await ai_engine.transform_legacy_data(legacy_data)
        
        # Store the modernized data
        modernized_data_store[modernized_data.id] = modernized_data
        
        # Mark legacy data as processed
        legacy_data.processed = True
        legacy_data_store[legacy_id] = legacy_data
        
        # Send completion notification
        await manager.send_transformation_complete(
            legacy_id, 
            modernized_data.id, 
            len(modernized_data.api_specs), 
            len(modernized_data.microservices)
        )
        
        # Send dashboard update
        dashboard_data = get_dashboard_data()
        await manager.send_dashboard_update(dashboard_data)
        
        return {
            "success": True,
            "modernized_id": modernized_data.id,
            "legacy_id": legacy_id,
            "schema": modernized_data.modern_schema.dict(),
            "api_count": len(modernized_data.api_specs),
            "microservices_count": len(modernized_data.microservices),
            "transformation_log": modernized_data.transformation_log
        }
        
    except Exception as e:
        await manager.send_error(f"Error transforming data: {str(e)}", legacy_id)
        raise HTTPException(status_code=500, detail=f"Error transforming data: {str(e)}")

@app.get("/legacy/{legacy_id}")
async def get_legacy_data(legacy_id: str):
    """Get legacy data details"""
    if legacy_id not in legacy_data_store:
        raise HTTPException(status_code=404, detail="Legacy data not found")
    
    legacy_data = legacy_data_store[legacy_id]
    return {
        "id": legacy_data.id,
        "source_type": legacy_data.source_type,
        "metadata": legacy_data.metadata,
        "processed": legacy_data.processed,
        "created_at": legacy_data.created_at
    }

@app.get("/modernized/{modernized_id}")
async def get_modernized_data(modernized_id: str):
    """Get modernized data details"""
    if modernized_id not in modernized_data_store:
        raise HTTPException(status_code=404, detail="Modernized data not found")
    
    modernized_data = modernized_data_store[modernized_id]
    return {
        "id": modernized_data.id,
        "legacy_id": modernized_data.legacy_id,
        "schema": modernized_data.modern_schema.dict(),
        "api_specs": [spec.dict() for spec in modernized_data.api_specs],
        "microservices": [ms.dict() for ms in modernized_data.microservices],
        "transformation_log": modernized_data.transformation_log,
        "created_at": modernized_data.created_at
    }

@app.post("/query/{modernized_id}")
async def query_modernized_data(modernized_id: str, query_request: QueryRequest):
    """Query modernized data"""
    try:
        if modernized_id not in modernized_data_store:
            raise HTTPException(status_code=404, detail="Modernized data not found")
        
        modernized_data = modernized_data_store[modernized_id]
        
        # Simulate query execution (in production, this would query the actual database)
        sample_data = _generate_sample_data(modernized_data.modern_schema, query_request)
        
        return QueryResponse(
            data=sample_data,
            total_count=len(sample_data),
            query_time=0.1
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying data: {str(e)}")

@app.get("/microservices/{modernized_id}")
async def get_microservices(modernized_id: str):
    """Get microservices architecture suggestions"""
    if modernized_id not in modernized_data_store:
        raise HTTPException(status_code=404, detail="Modernized data not found")
    
    modernized_data = modernized_data_store[modernized_id]
    return {
        "microservices": [ms.dict() for ms in modernized_data.microservices],
        "architecture_diagram": _generate_architecture_diagram(modernized_data.microservices)
    }

@app.get("/dashboard")
def get_dashboard_data():
    """Get dashboard overview data"""
    total_legacy = len(legacy_data_store)
    total_modernized = len(modernized_data_store)
    processed_count = sum(1 for data in legacy_data_store.values() if data.processed)
    
    recent_legacy = list(legacy_data_store.values())[-5:] if legacy_data_store else []
    recent_modernized = list(modernized_data_store.values())[-5:] if modernized_data_store else []
    
    return {
        "overview": {
            "total_legacy_files": total_legacy,
            "total_modernized": total_modernized,
            "processed_count": processed_count,
            "success_rate": (processed_count / total_legacy * 100) if total_legacy > 0 else 0
        },
        "recent_legacy": [{
            "id": data.id,
            "source_type": data.source_type,
            "created_at": data.created_at,
            "processed": data.processed
        } for data in recent_legacy],
        "recent_modernized": [{
            "id": data.id,
            "legacy_id": data.legacy_id,
            "api_count": len(data.api_specs),
            "microservices_count": len(data.microservices),
            "created_at": data.created_at
        } for data in recent_modernized]
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            # Echo back any received data (optional)
            await manager.send_personal_message(f"Echo: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api-specs/{modernized_id}")
async def get_api_specs(modernized_id: str):
    """Get OpenAPI specification for modernized data"""
    if modernized_id not in modernized_data_store:
        raise HTTPException(status_code=404, detail="Modernized data not found")
    
    modernized_data = modernized_data_store[modernized_id]
    
    # Generate OpenAPI 3.0 specification
    openapi_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": f"Modernized API for {modernized_data.modern_schema.table_name}",
            "version": "1.0.0",
            "description": "Generated from AS/400 legacy system"
        },
        "paths": {},
        "components": {
            "schemas": {
                modernized_data.modern_schema.table_name: {
                    "type": "object",
                    "properties": {}
                }
            }
        }
    }
    
    # Add field properties
    for field in modernized_data.modern_schema.fields:
        openapi_spec["components"]["schemas"][modernized_data.modern_schema.table_name]["properties"][field.modern_field] = {
            "type": _map_data_type_to_openapi(field.data_type),
            "description": field.description
        }
    
    # Add API endpoints
    for api_spec in modernized_data.api_specs:
        path = api_spec.endpoint
        method = api_spec.method.lower()
        
        if path not in openapi_spec["paths"]:
            openapi_spec["paths"][path] = {}
        
        openapi_spec["paths"][path][method] = {
            "summary": api_spec.description,
            "parameters": api_spec.parameters,
            "responses": {
                "200": {
                    "description": "Success",
                    "content": {
                        "application/json": {
                            "schema": api_spec.response_schema
                        }
                    }
                }
            }
        }
    
    return openapi_spec

def _generate_sample_data(schema: TableSchema, query_request: QueryRequest) -> List[Dict[str, Any]]:
    """Generate sample data for demonstration"""
    sample_data = []
    
    for i in range(min(query_request.limit, 10)):  # Generate up to 10 sample records
        record = {}
        for field in schema.fields:
            if field.data_type.startswith("VARCHAR"):
                record[field.modern_field] = f"Sample {field.modern_field} {i+1}"
            elif field.data_type.startswith("INTEGER"):
                record[field.modern_field] = (i + 1) * 100
            elif field.data_type.startswith("DECIMAL"):
                record[field.modern_field] = round((i + 1) * 10.5, 2)
            elif field.data_type.startswith("DATE"):
                record[field.modern_field] = "2024-01-01"
            elif field.data_type.startswith("TIMESTAMP"):
                record[field.modern_field] = "2024-01-01T10:00:00Z"
            else:
                record[field.modern_field] = f"Value {i+1}"
        
        sample_data.append(record)
    
    return sample_data

def _generate_architecture_diagram(microservices: List[Microservice]) -> str:
    """Generate Mermaid diagram for microservices architecture"""
    diagram = "graph TD\n"
    
    for i, service in enumerate(microservices):
        service_id = f"service_{i}"
        diagram += f'    {service_id}["{service.name}"]\n'
        
        for dep in service.dependencies:
            dep_id = f"service_{microservices.index(next(ms for ms in microservices if ms.name == dep))}"
            diagram += f"    {dep_id} --> {service_id}\n"
    
    return diagram

def _map_data_type_to_openapi(data_type: str) -> str:
    """Map database data type to OpenAPI type"""
    if data_type.startswith("VARCHAR") or data_type.startswith("TEXT"):
        return "string"
    elif data_type.startswith("INTEGER") or data_type.startswith("BIGINT"):
        return "integer"
    elif data_type.startswith("DECIMAL") or data_type.startswith("FLOAT"):
        return "number"
    elif data_type.startswith("DATE"):
        return "string"
    elif data_type.startswith("TIMESTAMP"):
        return "string"
    elif data_type.startswith("BOOLEAN"):
        return "boolean"
    else:
        return "string"

if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError:
        print("Uvicorn not installed. Please install with: pip install uvicorn")
        print("Or run with: uvicorn main:app --host 0.0.0.0 --port 8000")