#!/usr/bin/env python3
"""
Demo script for AS/400 Legacy Modernization Assistant
"""

import requests
import json
import time
from backend.sample_data import get_sample_data

def demo_legacy_modernization():
    """Run a complete demo of the legacy modernization system"""
    
    print("🚀 AS/400 Legacy Modernization Assistant Demo")
    print("=" * 50)
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/")
        print("✅ Backend server is running")
    except requests.exceptions.ConnectionError:
        print("❌ Backend server is not running. Please start it first:")
        print("   cd backend && python main.py")
        return
    
    # Get sample data
    samples = get_sample_data()
    
    print("\n📁 Available Sample Data:")
    for name, content in samples.items():
        print(f"   - {name}: {len(content)} characters")
    
    # Demo 1: Upload and process a flat file
    print("\n🔄 Demo 1: Processing Flat File")
    print("-" * 30)
    
    flat_file_data = samples["flat_file_delimited"]
    response = requests.post("http://localhost:8000/ingest", json={
        "content": flat_file_data,
        "source_type": "flat_file",
        "name": "customer_data.txt"
    })
    
    if response.status_code == 200:
        result = response.json()
        legacy_id = result["legacy_id"]
        print(f"✅ Legacy data ingested: {legacy_id}")
        
        # Transform the data
        print("🤖 Transforming data with AI...")
        transform_response = requests.post(f"http://localhost:8000/transform/{legacy_id}")
        
        if transform_response.status_code == 200:
            transform_result = transform_response.json()
            modernized_id = transform_result["modernized_id"]
            print(f"✅ Data modernized: {modernized_id}")
            print(f"   - Generated {transform_result['api_count']} APIs")
            print(f"   - Suggested {transform_result['microservices_count']} microservices")
            
            # Demo 2: Query the modernized data
            print("\n🔍 Demo 2: Querying Modernized Data")
            print("-" * 30)
            
            query_response = requests.post(f"http://localhost:8000/query/{modernized_id}", json={
                "table_name": "customers",
                "limit": 5
            })
            
            if query_response.status_code == 200:
                query_result = query_response.json()
                print(f"✅ Query executed in {query_result['query_time']}s")
                print(f"   - Found {query_result['total_count']} records")
                print("   - Sample data:")
                for i, record in enumerate(query_result['data'][:3], 1):
                    print(f"     {i}. {record}")
            
            # Demo 3: Get microservices architecture
            print("\n🏗️ Demo 3: Microservices Architecture")
            print("-" * 30)
            
            microservices_response = requests.get(f"http://localhost:8000/microservices/{modernized_id}")
            
            if microservices_response.status_code == 200:
                microservices_result = microservices_response.json()
                print(f"✅ Generated {len(microservices_result['microservices'])} microservices:")
                
                for service in microservices_result['microservices']:
                    print(f"   - {service['name']}: {service['description']}")
                    print(f"     Endpoints: {len(service['endpoints'])}")
                    print(f"     Dependencies: {service['dependencies']}")
            
            # Demo 4: Get API specifications
            print("\n📋 Demo 4: API Specifications")
            print("-" * 30)
            
            api_specs_response = requests.get(f"http://localhost:8000/api-specs/{modernized_id}")
            
            if api_specs_response.status_code == 200:
                api_specs = api_specs_response.json()
                print(f"✅ Generated OpenAPI 3.0 specification")
                print(f"   - Title: {api_specs['info']['title']}")
                print(f"   - Endpoints: {len(api_specs['paths'])}")
                print(f"   - Schemas: {len(api_specs['components']['schemas'])}")
    
    # Demo 5: Process different file types
    print("\n📊 Demo 5: Processing Different File Types")
    print("-" * 30)
    
    # Process DDS file
    dds_data = samples["dds_file"]
    dds_response = requests.post("http://localhost:8000/ingest", json={
        "content": dds_data,
        "source_type": "db2_table",
        "name": "customer.dds"
    })
    
    if dds_response.status_code == 200:
        dds_result = dds_response.json()
        print(f"✅ DDS file processed: {dds_result['legacy_id']}")
        
        # Transform DDS data
        dds_transform = requests.post(f"http://localhost:8000/transform/{dds_result['legacy_id']}")
        if dds_transform.status_code == 200:
            print("✅ DDS data modernized successfully")
    
    # Process RPG program
    rpg_data = samples["rpg_program"]
    rpg_response = requests.post("http://localhost:8000/ingest", json={
        "content": rpg_data,
        "source_type": "rpg_program",
        "name": "customer.rpg"
    })
    
    if rpg_response.status_code == 200:
        rpg_result = rpg_response.json()
        print(f"✅ RPG program processed: {rpg_result['legacy_id']}")
        
        # Transform RPG data
        rpg_transform = requests.post(f"http://localhost:8000/transform/{rpg_result['legacy_id']}")
        if rpg_transform.status_code == 200:
            print("✅ RPG program modernized successfully")
    
    # Demo 6: Dashboard overview
    print("\n📈 Demo 6: Dashboard Overview")
    print("-" * 30)
    
    dashboard_response = requests.get("http://localhost:8000/dashboard")
    
    if dashboard_response.status_code == 200:
        dashboard_data = dashboard_response.json()
        overview = dashboard_data['overview']
        
        print(f"✅ Dashboard data retrieved:")
        print(f"   - Legacy files: {overview['total_legacy_files']}")
        print(f"   - Modernized: {overview['total_modernized']}")
        print(f"   - Processing: {overview['processed_count'] - overview['total_modernized']}")
        print(f"   - Success rate: {overview['success_rate']:.1f}%")
    
    print("\n🎉 Demo completed successfully!")
    print("\nNext steps:")
    print("1. Open http://localhost:3000 to see the web interface")
    print("2. Upload your own AS/400 files")
    print("3. Explore the generated APIs and microservices")
    print("4. Deploy to production using Docker or Kubernetes")

if __name__ == "__main__":
    demo_legacy_modernization()
