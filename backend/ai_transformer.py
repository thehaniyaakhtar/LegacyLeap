import openai
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from models import LegacyData, ModernizedData, TableSchema, FieldMapping, APISpec, Microservice, DataSourceType

class AITransformationEngine:
    """AI-powered engine for transforming legacy AS/400 data to modern formats"""
    
    def __init__(self, api_key: str = None):
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        self.transformation_cache = {}
    
    async def transform_legacy_data(self, legacy_data: LegacyData) -> ModernizedData:
        """Transform legacy data using AI analysis"""
        transformation_log = []
        
        try:
            # Analyze the legacy data structure
            analysis = await self._analyze_legacy_structure(legacy_data)
            transformation_log.append(f"Analyzed {legacy_data.source_type} structure")
            
            # Generate modern schema
            modern_schema = await self._generate_modern_schema(legacy_data, analysis)
            transformation_log.append(f"Generated modern schema with {len(modern_schema.fields)} fields")
            
            # Generate API specifications
            api_specs = await self._generate_api_specs(legacy_data, modern_schema)
            transformation_log.append(f"Generated {len(api_specs)} API endpoints")
            
            # Suggest microservices architecture
            microservices = await self._suggest_microservices(legacy_data, modern_schema, api_specs)
            transformation_log.append(f"Suggested {len(microservices)} microservices")
            
            return ModernizedData(
                id=str(uuid.uuid4()),
                legacy_id=legacy_data.id,
                modern_schema=modern_schema,
                api_specs=api_specs,
                microservices=microservices,
                transformation_log=transformation_log,
                created_at=datetime.now()
            )
            
        except Exception as e:
            transformation_log.append(f"Error during transformation: {str(e)}")
            # Return a basic transformation even if AI fails
            return self._create_fallback_transformation(legacy_data, transformation_log)
    
    async def _analyze_legacy_structure(self, legacy_data: LegacyData) -> Dict[str, Any]:
        """Analyze legacy data structure using AI"""
        if not self.client:
            return self._fallback_analysis(legacy_data)
        
        try:
            prompt = self._create_analysis_prompt(legacy_data)
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            return self._parse_analysis_response(analysis_text)
            
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return self._fallback_analysis(legacy_data)
    
    async def _generate_modern_schema(self, legacy_data: LegacyData, analysis: Dict[str, Any]) -> TableSchema:
        """Generate modern database schema"""
        if not self.client:
            return self._fallback_schema(legacy_data)
        
        try:
            prompt = self._create_schema_prompt(legacy_data, analysis)
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            
            schema_text = response.choices[0].message.content
            return self._parse_schema_response(schema_text, legacy_data)
            
        except Exception as e:
            print(f"Schema generation failed: {e}")
            return self._fallback_schema(legacy_data)
    
    async def _generate_api_specs(self, legacy_data: LegacyData, schema: TableSchema) -> List[APISpec]:
        """Generate REST API specifications"""
        if not self.client:
            return self._fallback_api_specs(schema)
        
        try:
            prompt = self._create_api_prompt(legacy_data, schema)
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            api_text = response.choices[0].message.content
            return self._parse_api_response(api_text, schema)
            
        except Exception as e:
            print(f"API generation failed: {e}")
            return self._fallback_api_specs(schema)
    
    async def _suggest_microservices(self, legacy_data: LegacyData, schema: TableSchema, api_specs: List[APISpec]) -> List[Microservice]:
        """Suggest microservices architecture"""
        if not self.client:
            return self._fallback_microservices(schema)
        
        try:
            prompt = self._create_microservices_prompt(legacy_data, schema, api_specs)
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            
            microservices_text = response.choices[0].message.content
            return self._parse_microservices_response(microservices_text)
            
        except Exception as e:
            print(f"Microservices generation failed: {e}")
            return self._fallback_microservices(schema)
    
    def _create_analysis_prompt(self, legacy_data: LegacyData) -> str:
        """Create prompt for AI analysis"""
        return f"""
        Analyze this AS/400 legacy data structure and provide insights for modernization:
        
        Source Type: {legacy_data.source_type}
        Content: {legacy_data.content[:2000]}...
        Metadata: {json.dumps(legacy_data.metadata, indent=2)}
        
        Please analyze:
        1. Data structure patterns
        2. Field types and relationships
        3. Business logic implications
        4. Modernization challenges
        5. Recommended modern data types
        
        Respond in JSON format with analysis results.
        """
    
    def _create_schema_prompt(self, legacy_data: LegacyData, analysis: Dict[str, Any]) -> str:
        """Create prompt for schema generation"""
        return f"""
        Based on this AS/400 legacy data analysis, generate a modern database schema:
        
        Legacy Data: {legacy_data.content[:1000]}...
        Analysis: {json.dumps(analysis, indent=2)}
        
        Generate a modern schema with:
        1. Appropriate field names (camelCase)
        2. Modern data types (VARCHAR, INTEGER, TIMESTAMP, etc.)
        3. Primary keys and indexes
        4. Field constraints and validations
        5. Relationships if applicable
        
        Respond with JSON schema definition.
        """
    
    def _create_api_prompt(self, legacy_data: LegacyData, schema: TableSchema) -> str:
        """Create prompt for API generation"""
        return f"""
        Generate REST API specifications for this modernized schema:
        
        Schema: {json.dumps(schema.dict(), indent=2)}
        Legacy Source: {legacy_data.source_type}
        
        Create comprehensive API endpoints with:
        1. CRUD operations (GET, POST, PUT, DELETE)
        2. Query parameters and filtering
        3. Pagination support
        4. Error handling
        5. Response schemas
        6. OpenAPI 3.0 format
        
        Respond with JSON API specifications.
        """
    
    def _create_microservices_prompt(self, legacy_data: LegacyData, schema: TableSchema, api_specs: List[APISpec]) -> str:
        """Create prompt for microservices suggestions"""
        return f"""
        Suggest a microservices architecture for this modernized AS/400 system:
        
        Schema: {json.dumps(schema.dict(), indent=2)}
        APIs: {len(api_specs)} endpoints available
        Legacy Source: {legacy_data.source_type}
        
        Suggest microservices with:
        1. Service boundaries based on business domains
        2. API gateway configuration
        3. Database per service recommendations
        4. Inter-service communication patterns
        5. Docker containerization
        6. Scalability considerations
        
        Respond with JSON microservices definitions.
        """
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse AI analysis response"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback parsing
        return {
            "data_patterns": ["structured", "tabular"],
            "field_types": ["string", "numeric", "date"],
            "complexity": "medium",
            "recommendations": ["normalize", "add_constraints", "create_indexes"]
        }
    
    def _parse_schema_response(self, response: str, legacy_data: LegacyData) -> TableSchema:
        """Parse schema generation response"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                schema_data = json.loads(json_match.group())
                return self._build_schema_from_json(schema_data, legacy_data)
        except:
            pass
        
        return self._fallback_schema(legacy_data)
    
    def _parse_api_response(self, response: str, schema: TableSchema) -> List[APISpec]:
        """Parse API generation response"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                api_data = json.loads(json_match.group())
                return self._build_apis_from_json(api_data, schema)
        except:
            pass
        
        return self._fallback_api_specs(schema)
    
    def _parse_microservices_response(self, response: str) -> List[Microservice]:
        """Parse microservices response"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                microservices_data = json.loads(json_match.group())
                return self._build_microservices_from_json(microservices_data)
        except:
            pass
        
        return []
    
    def _build_schema_from_json(self, schema_data: Dict[str, Any], legacy_data: LegacyData) -> TableSchema:
        """Build TableSchema from JSON response"""
        table_name = schema_data.get('table_name', f"modernized_{legacy_data.source_type}")
        fields = []
        
        for field_data in schema_data.get('fields', []):
            field = FieldMapping(
                legacy_field=field_data.get('legacy_field', ''),
                modern_field=field_data.get('modern_field', ''),
                data_type=field_data.get('data_type', 'VARCHAR'),
                description=field_data.get('description', ''),
                transformation_rule=field_data.get('transformation_rule')
            )
            fields.append(field)
        
        return TableSchema(
            table_name=table_name,
            fields=fields,
            primary_key=schema_data.get('primary_key', []),
            indexes=schema_data.get('indexes', [])
        )
    
    def _build_apis_from_json(self, api_data: List[Dict[str, Any]], schema: TableSchema) -> List[APISpec]:
        """Build API specs from JSON response"""
        apis = []
        
        for api_info in api_data:
            api = APISpec(
                endpoint=api_info.get('endpoint', ''),
                method=api_info.get('method', 'GET'),
                description=api_info.get('description', ''),
                parameters=api_info.get('parameters', []),
                response_schema=api_info.get('response_schema', {})
            )
            apis.append(api)
        
        return apis
    
    def _build_microservices_from_json(self, microservices_data: List[Dict[str, Any]]) -> List[Microservice]:
        """Build microservices from JSON response"""
        microservices = []
        
        for service_data in microservices_data:
            service = Microservice(
                name=service_data.get('name', ''),
                description=service_data.get('description', ''),
                endpoints=[],
                dependencies=service_data.get('dependencies', []),
                dockerfile=service_data.get('dockerfile')
            )
            microservices.append(service)
        
        return microservices
    
    def _fallback_analysis(self, legacy_data: LegacyData) -> Dict[str, Any]:
        """Fallback analysis when AI is not available"""
        return {
            "data_patterns": ["structured"],
            "field_types": ["string", "numeric"],
            "complexity": "low",
            "recommendations": ["basic_normalization"]
        }
    
    def _fallback_schema(self, legacy_data: LegacyData) -> TableSchema:
        """Fallback schema generation"""
        fields = []
        
        if legacy_data.source_type == DataSourceType.FLAT_FILE:
            # Generate basic fields from flat file
            try:
                data = json.loads(legacy_data.content)
                if data and isinstance(data, list) and len(data) > 0:
                    sample_row = data[0]
                    for key, value in sample_row.items():
                        field = FieldMapping(
                            legacy_field=key,
                            modern_field=key.lower().replace('_', ''),
                            data_type=self._infer_data_type(value),
                            description=f"Field from {key}"
                        )
                        fields.append(field)
            except:
                pass
        
        if not fields:
            # Default field if no data
            fields.append(FieldMapping(
                legacy_field="FIELD_1",
                modern_field="field1",
                data_type="VARCHAR(255)",
                description="Default field"
            ))
        
        return TableSchema(
            table_name=f"modernized_{legacy_data.source_type}",
            fields=fields,
            primary_key=["id"],
            indexes=[]
        )
    
    def _fallback_api_specs(self, schema: TableSchema) -> List[APISpec]:
        """Fallback API generation"""
        return [
            APISpec(
                endpoint=f"/api/{schema.table_name}",
                method="GET",
                description=f"Get all {schema.table_name} records",
                parameters=[],
                response_schema={"type": "array", "items": {"type": "object"}}
            ),
            APISpec(
                endpoint=f"/api/{schema.table_name}",
                method="POST",
                description=f"Create new {schema.table_name} record",
                parameters=[],
                response_schema={"type": "object"}
            )
        ]
    
    def _fallback_microservices(self, schema: TableSchema) -> List[Microservice]:
        """Fallback microservices suggestion"""
        return [
            Microservice(
                name=f"{schema.table_name}-service",
                description=f"Microservice for {schema.table_name} operations",
                endpoints=[],
                dependencies=[]
            )
        ]
    
    def _create_fallback_transformation(self, legacy_data: LegacyData, transformation_log: List[str]) -> ModernizedData:
        """Create fallback transformation when AI fails"""
        schema = self._fallback_schema(legacy_data)
        api_specs = self._fallback_api_specs(schema)
        microservices = self._fallback_microservices(schema)
        
        return ModernizedData(
            id=str(uuid.uuid4()),
            legacy_id=legacy_data.id,
            modern_schema=schema,
            api_specs=api_specs,
            microservices=microservices,
            transformation_log=transformation_log,
            created_at=datetime.now()
        )
    
    def _infer_data_type(self, value: str) -> str:
        """Infer data type from value"""
        if not value:
            return "VARCHAR(255)"
        
        # Check for numeric
        try:
            float(value)
            if '.' in value:
                return "DECIMAL(10,2)"
            else:
                return "INTEGER"
        except:
            pass
        
        # Check for date
        if re.match(r'\d{4}-\d{2}-\d{2}', value):
            return "DATE"
        
        # Check for timestamp
        if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', value):
            return "TIMESTAMP"
        
        # Default to varchar
        length = min(len(value) * 2, 1000)
        return f"VARCHAR({length})"
