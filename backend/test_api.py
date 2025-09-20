"""
Comprehensive API tests for AS/400 Legacy Modernization Assistant
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app
from models import DataSourceType

client = TestClient(app)

class TestLegacyModernizationAPI:
    """Test suite for the legacy modernization API"""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns correct information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "AS/400 Legacy Modernization Assistant" in data["message"]
        assert "endpoints" in data
    
    def test_upload_flat_file(self):
        """Test uploading a flat file"""
        # Create a test flat file content
        test_content = """CUST001JOHN DOE    123 MAIN ST    NEW YORK    NY10001 555-0123
CUST002JANE SMITH  456 OAK AVE   CHICAGO     IL60601 555-0456"""
        
        # Create a test file
        files = {"file": ("test_customers.txt", test_content, "text/plain")}
        
        response = client.post("/upload", files=files)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert "legacy_id" in data
        assert data["source_type"] == "flat_file"
        
        return data["legacy_id"]
    
    def test_upload_delimited_file(self):
        """Test uploading a delimited file"""
        test_content = """CUST_ID|CUST_NAME|ADDRESS|CITY|STATE|ZIP|PHONE
CUST001|JOHN DOE|123 MAIN ST|NEW YORK|NY|10001|555-0123
CUST002|JANE SMITH|456 OAK AVE|CHICAGO|IL|60601|555-0456"""
        
        files = {"file": ("test_customers_delimited.txt", test_content, "text/plain")}
        
        response = client.post("/upload", files=files)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert data["source_type"] == "flat_file"
        
        return data["legacy_id"]
    
    def test_upload_sql_file(self):
        """Test uploading a SQL file"""
        test_content = """CREATE TABLE CUSTOMER (
    CUSTID CHAR(10) NOT NULL,
    CUSTNAME VARCHAR(30) NOT NULL,
    ADDRESS VARCHAR(50),
    CITY VARCHAR(20),
    STATE CHAR(2),
    ZIPCODE CHAR(5),
    PHONE VARCHAR(12),
    PRIMARY KEY (CUSTID)
);"""
        
        files = {"file": ("customer.sql", test_content, "application/sql")}
        
        response = client.post("/upload", files=files)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert data["source_type"] == "db2_table"
        
        return data["legacy_id"]
    
    def test_ingest_legacy_data(self):
        """Test direct ingestion of legacy data"""
        test_content = "CUST001JOHN DOE    123 MAIN ST    NEW YORK    NY10001 555-0123"
        
        response = client.post("/ingest", json={
            "content": test_content,
            "source_type": "flat_file",
            "name": "test_ingest.txt"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "legacy_id" in data
        
        return data["legacy_id"]
    
    def test_transform_legacy_data(self):
        """Test transforming legacy data"""
        # First upload a file
        legacy_id = self.test_upload_flat_file()
        
        # Then transform it
        response = client.post(f"/transform/{legacy_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert "modernized_id" in data
        assert "api_count" in data
        assert "microservices_count" in data
        
        return data["modernized_id"]
    
    def test_get_legacy_data(self):
        """Test getting legacy data details"""
        legacy_id = self.test_upload_flat_file()
        
        response = client.get(f"/legacy/{legacy_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == legacy_id
        assert "source_type" in data
        assert "metadata" in data
    
    def test_get_modernized_data(self):
        """Test getting modernized data details"""
        modernized_id = self.test_transform_legacy_data()
        
        response = client.get(f"/modernized/{modernized_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == modernized_id
        assert "schema" in data
        assert "api_specs" in data
        assert "microservices" in data
    
    def test_query_modernized_data(self):
        """Test querying modernized data"""
        modernized_id = self.test_transform_legacy_data()
        
        response = client.post(f"/query/{modernized_id}", json={
            "table_name": "customers",
            "limit": 5
        })
        
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "total_count" in data
        assert "query_time" in data
    
    def test_get_microservices(self):
        """Test getting microservices architecture"""
        modernized_id = self.test_transform_legacy_data()
        
        response = client.get(f"/microservices/{modernized_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert "microservices" in data
        assert "architecture_diagram" in data
    
    def test_get_api_specs(self):
        """Test getting API specifications"""
        modernized_id = self.test_transform_legacy_data()
        
        response = client.get(f"/api-specs/{modernized_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
        assert "components" in data
    
    def test_dashboard(self):
        """Test dashboard endpoint"""
        response = client.get("/dashboard")
        assert response.status_code == 200
        
        data = response.json()
        assert "overview" in data
        assert "recent_legacy" in data
        assert "recent_modernized" in data
        
        overview = data["overview"]
        assert "total_legacy_files" in overview
        assert "total_modernized" in overview
        assert "processed_count" in overview
        assert "success_rate" in overview
    
    def test_websocket_connection(self):
        """Test WebSocket connection"""
        with client.websocket_connect("/ws") as websocket:
            # Send a test message
            websocket.send_text("test message")
            # Receive echo
            data = websocket.receive_text()
            assert "Echo: test message" in data
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        # Test invalid legacy ID
        response = client.get("/legacy/invalid-id")
        assert response.status_code == 404
        
        # Test invalid modernized ID
        response = client.get("/modernized/invalid-id")
        assert response.status_code == 404
        
        # Test transform with invalid legacy ID
        response = client.post("/transform/invalid-id")
        assert response.status_code == 404
    
    def test_file_type_detection(self):
        """Test automatic file type detection"""
        # Test RPG file
        rpg_content = """     FCUSTOMER  IF   E           K DISK
     D CustomerDS       DS
     D  CustID                10A"""
        
        files = {"file": ("test.rpg", rpg_content, "text/x-rpg")}
        response = client.post("/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        assert data["source_type"] == "rpg_program"
    
    def test_large_file_handling(self):
        """Test handling of large files"""
        # Create a large test file
        large_content = "\n".join([
            f"CUST{i:03d}CUSTOMER{i:03d} 123 MAIN ST    CITY{i:03d}    ST{i:02d}12345 555-{i:04d}"
            for i in range(1000)
        ])
        
        files = {"file": ("large_file.txt", large_content, "text/plain")}
        response = client.post("/upload", files=files)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert data["metadata"]["row_count"] == 1000

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
