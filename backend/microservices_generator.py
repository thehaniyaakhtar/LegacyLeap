"""
Microservices Architecture Generator for AS/400 Modernization
"""

import json
import uuid
from typing import List, Dict, Any
from datetime import datetime
from models import Microservice, APISpec, TableSchema

class MicroservicesArchitectureGenerator:
    """Generates microservices architecture recommendations"""
    
    def __init__(self):
        self.service_templates = {
            "api_gateway": self._generate_api_gateway,
            "data_service": self._generate_data_service,
            "business_service": self._generate_business_service,
            "notification_service": self._generate_notification_service,
            "audit_service": self._generate_audit_service,
            "integration_service": self._generate_integration_service
        }
    
    def generate_architecture(self, modernized_data: Dict[str, Any]) -> List[Microservice]:
        """Generate microservices architecture based on modernized data"""
        microservices = []
        
        # Extract schema information
        schema = modernized_data.get('schema', {})
        table_name = schema.get('table_name', 'unknown')
        fields = schema.get('fields', [])
        
        # Generate core services
        microservices.extend(self._generate_core_services(table_name, fields))
        
        # Generate domain-specific services
        microservices.extend(self._generate_domain_services(table_name, fields))
        
        # Generate supporting services
        microservices.extend(self._generate_supporting_services())
        
        return microservices
    
    def _generate_core_services(self, table_name: str, fields: List[Dict]) -> List[Microservice]:
        """Generate core microservices"""
        services = []
        
        # API Gateway
        services.append(self._generate_api_gateway())
        
        # Data Service
        services.append(self._generate_data_service(table_name, fields))
        
        # Business Logic Service
        services.append(self._generate_business_service(table_name, fields))
        
        return services
    
    def _generate_domain_services(self, table_name: str, fields: List[Dict]) -> List[Microservice]:
        """Generate domain-specific services based on table content"""
        services = []
        
        # Analyze table name and fields to determine domain
        domain = self._analyze_domain(table_name, fields)
        
        if domain == "customer":
            services.append(self._generate_customer_service())
        elif domain == "order":
            services.append(self._generate_order_service())
        elif domain == "product":
            services.append(self._generate_product_service())
        elif domain == "employee":
            services.append(self._generate_employee_service())
        elif domain == "financial":
            services.append(self._generate_financial_service())
        else:
            services.append(self._generate_generic_entity_service(table_name, fields))
        
        return services
    
    def _generate_supporting_services(self) -> List[Microservice]:
        """Generate supporting microservices"""
        services = []
        
        # Notification Service
        services.append(self._generate_notification_service())
        
        # Audit Service
        services.append(self._generate_audit_service())
        
        # Integration Service
        services.append(self._generate_integration_service())
        
        return services
    
    def _analyze_domain(self, table_name: str, fields: List[Dict]) -> str:
        """Analyze table to determine business domain"""
        table_lower = table_name.lower()
        
        if any(keyword in table_lower for keyword in ['cust', 'customer', 'client']):
            return "customer"
        elif any(keyword in table_lower for keyword in ['order', 'ord', 'purchase']):
            return "order"
        elif any(keyword in table_lower for keyword in ['prod', 'product', 'item', 'inventory']):
            return "product"
        elif any(keyword in table_lower for keyword in ['emp', 'employee', 'staff', 'worker']):
            return "employee"
        elif any(keyword in table_lower for keyword in ['acct', 'account', 'financial', 'finance']):
            return "financial"
        else:
            return "generic"
    
    def _generate_api_gateway(self) -> Microservice:
        """Generate API Gateway service"""
        endpoints = [
            APISpec(
                endpoint="/api/v1/health",
                method="GET",
                description="Health check endpoint",
                parameters=[],
                response_schema={"type": "object", "properties": {"status": {"type": "string"}}}
            ),
            APISpec(
                endpoint="/api/v1/routes",
                method="GET",
                description="List all available routes",
                parameters=[],
                response_schema={"type": "array", "items": {"type": "object"}}
            )
        ]
        
        dockerfile = """FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]"""
        
        return Microservice(
            name="api-gateway",
            description="API Gateway for routing and load balancing",
            endpoints=endpoints,
            dependencies=[],
            dockerfile=dockerfile
        )
    
    def _generate_data_service(self, table_name: str, fields: List[Dict]) -> Microservice:
        """Generate Data Service"""
        endpoints = [
            APISpec(
                endpoint=f"/api/v1/{table_name}",
                method="GET",
                description=f"Get all {table_name} records",
                parameters=[
                    {"name": "limit", "in": "query", "type": "integer", "required": False},
                    {"name": "offset", "in": "query", "type": "integer", "required": False}
                ],
                response_schema={"type": "array", "items": {"type": "object"}}
            ),
            APISpec(
                endpoint=f"/api/v1/{table_name}/{{id}}",
                method="GET",
                description=f"Get {table_name} record by ID",
                parameters=[{"name": "id", "in": "path", "type": "string", "required": True}],
                response_schema={"type": "object"}
            ),
            APISpec(
                endpoint=f"/api/v1/{table_name}",
                method="POST",
                description=f"Create new {table_name} record",
                parameters=[],
                response_schema={"type": "object"}
            ),
            APISpec(
                endpoint=f"/api/v1/{table_name}/{{id}}",
                method="PUT",
                description=f"Update {table_name} record",
                parameters=[{"name": "id", "in": "path", "type": "string", "required": True}],
                response_schema={"type": "object"}
            ),
            APISpec(
                endpoint=f"/api/v1/{table_name}/{{id}}",
                method="DELETE",
                description=f"Delete {table_name} record",
                parameters=[{"name": "id", "in": "path", "type": "string", "required": True}],
                response_schema={"type": "object"}
            )
        ]
        
        dockerfile = """FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]"""
        
        return Microservice(
            name=f"{table_name}-data-service",
            description=f"Data service for {table_name} operations",
            endpoints=endpoints,
            dependencies=["database"],
            dockerfile=dockerfile
        )
    
    def _generate_business_service(self, table_name: str, fields: List[Dict]) -> Microservice:
        """Generate Business Logic Service"""
        endpoints = [
            APISpec(
                endpoint=f"/api/v1/{table_name}/validate",
                method="POST",
                description=f"Validate {table_name} business rules",
                parameters=[],
                response_schema={"type": "object", "properties": {"valid": {"type": "boolean"}}}
            ),
            APISpec(
                endpoint=f"/api/v1/{table_name}/process",
                method="POST",
                description=f"Process {table_name} business logic",
                parameters=[],
                response_schema={"type": "object"}
            )
        ]
        
        dockerfile = """FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]"""
        
        return Microservice(
            name=f"{table_name}-business-service",
            description=f"Business logic service for {table_name}",
            endpoints=endpoints,
            dependencies=[f"{table_name}-data-service"],
            dockerfile=dockerfile
        )
    
    def _generate_customer_service(self) -> Microservice:
        """Generate Customer-specific service"""
        endpoints = [
            APISpec(
                endpoint="/api/v1/customers/search",
                method="GET",
                description="Search customers by criteria",
                parameters=[
                    {"name": "name", "in": "query", "type": "string", "required": False},
                    {"name": "city", "in": "query", "type": "string", "required": False},
                    {"name": "state", "in": "query", "type": "string", "required": False}
                ],
                response_schema={"type": "array", "items": {"type": "object"}}
            ),
            APISpec(
                endpoint="/api/v1/customers/{{id}}/orders",
                method="GET",
                description="Get customer orders",
                parameters=[{"name": "id", "in": "path", "type": "string", "required": True}],
                response_schema={"type": "array", "items": {"type": "object"}}
            )
        ]
        
        return Microservice(
            name="customer-service",
            description="Customer management service with search and order history",
            endpoints=endpoints,
            dependencies=["customer-data-service", "order-data-service"],
            dockerfile=None
        )
    
    def _generate_order_service(self) -> Microservice:
        """Generate Order-specific service"""
        endpoints = [
            APISpec(
                endpoint="/api/v1/orders/{{id}}/status",
                method="PUT",
                description="Update order status",
                parameters=[{"name": "id", "in": "path", "type": "string", "required": True}],
                response_schema={"type": "object"}
            ),
            APISpec(
                endpoint="/api/v1/orders/{{id}}/items",
                method="GET",
                description="Get order items",
                parameters=[{"name": "id", "in": "path", "type": "string", "required": True}],
                response_schema={"type": "array", "items": {"type": "object"}}
            )
        ]
        
        return Microservice(
            name="order-service",
            description="Order management service with status tracking",
            endpoints=endpoints,
            dependencies=["order-data-service", "product-data-service"],
            dockerfile=None
        )
    
    def _generate_product_service(self) -> Microservice:
        """Generate Product-specific service"""
        endpoints = [
            APISpec(
                endpoint="/api/v1/products/search",
                method="GET",
                description="Search products by criteria",
                parameters=[
                    {"name": "category", "in": "query", "type": "string", "required": False},
                    {"name": "price_min", "in": "query", "type": "number", "required": False},
                    {"name": "price_max", "in": "query", "type": "number", "required": False}
                ],
                response_schema={"type": "array", "items": {"type": "object"}}
            ),
            APISpec(
                endpoint="/api/v1/products/{{id}}/inventory",
                method="GET",
                description="Get product inventory",
                parameters=[{"name": "id", "in": "path", "type": "string", "required": True}],
                response_schema={"type": "object"}
            )
        ]
        
        return Microservice(
            name="product-service",
            description="Product catalog service with search and inventory",
            endpoints=endpoints,
            dependencies=["product-data-service", "inventory-data-service"],
            dockerfile=None
        )
    
    def _generate_employee_service(self) -> Microservice:
        """Generate Employee-specific service"""
        endpoints = [
            APISpec(
                endpoint="/api/v1/employees/{{id}}/profile",
                method="GET",
                description="Get employee profile",
                parameters=[{"name": "id", "in": "path", "type": "string", "required": True}],
                response_schema={"type": "object"}
            ),
            APISpec(
                endpoint="/api/v1/employees/department/{{dept}}",
                method="GET",
                description="Get employees by department",
                parameters=[{"name": "dept", "in": "path", "type": "string", "required": True}],
                response_schema={"type": "array", "items": {"type": "object"}}
            )
        ]
        
        return Microservice(
            name="employee-service",
            description="Employee management service with department organization",
            endpoints=endpoints,
            dependencies=["employee-data-service"],
            dockerfile=None
        )
    
    def _generate_financial_service(self) -> Microservice:
        """Generate Financial-specific service"""
        endpoints = [
            APISpec(
                endpoint="/api/v1/accounts/{{id}}/balance",
                method="GET",
                description="Get account balance",
                parameters=[{"name": "id", "in": "path", "type": "string", "required": True}],
                response_schema={"type": "object"}
            ),
            APISpec(
                endpoint="/api/v1/accounts/{{id}}/transactions",
                method="GET",
                description="Get account transactions",
                parameters=[{"name": "id", "in": "path", "type": "string", "required": True}],
                response_schema={"type": "array", "items": {"type": "object"}}
            )
        ]
        
        return Microservice(
            name="financial-service",
            description="Financial account management service",
            endpoints=endpoints,
            dependencies=["account-data-service", "transaction-data-service"],
            dockerfile=None
        )
    
    def _generate_generic_entity_service(self, table_name: str, fields: List[Dict]) -> Microservice:
        """Generate generic entity service"""
        endpoints = [
            APISpec(
                endpoint=f"/api/v1/{table_name}/search",
                method="GET",
                description=f"Search {table_name} records",
                parameters=[],
                response_schema={"type": "array", "items": {"type": "object"}}
            )
        ]
        
        return Microservice(
            name=f"{table_name}-service",
            description=f"Generic service for {table_name} entity",
            endpoints=endpoints,
            dependencies=[f"{table_name}-data-service"],
            dockerfile=None
        )
    
    def _generate_notification_service(self) -> Microservice:
        """Generate Notification Service"""
        endpoints = [
            APISpec(
                endpoint="/api/v1/notifications",
                method="POST",
                description="Send notification",
                parameters=[],
                response_schema={"type": "object"}
            ),
            APISpec(
                endpoint="/api/v1/notifications/{{id}}/status",
                method="GET",
                description="Get notification status",
                parameters=[{"name": "id", "in": "path", "type": "string", "required": True}],
                response_schema={"type": "object"}
            )
        ]
        
        return Microservice(
            name="notification-service",
            description="Notification service for alerts and communications",
            endpoints=endpoints,
            dependencies=[],
            dockerfile=None
        )
    
    def _generate_audit_service(self) -> Microservice:
        """Generate Audit Service"""
        endpoints = [
            APISpec(
                endpoint="/api/v1/audit/logs",
                method="GET",
                description="Get audit logs",
                parameters=[
                    {"name": "entity", "in": "query", "type": "string", "required": False},
                    {"name": "action", "in": "query", "type": "string", "required": False},
                    {"name": "date_from", "in": "query", "type": "string", "required": False},
                    {"name": "date_to", "in": "query", "type": "string", "required": False}
                ],
                response_schema={"type": "array", "items": {"type": "object"}}
            ),
            APISpec(
                endpoint="/api/v1/audit/log",
                method="POST",
                description="Create audit log entry",
                parameters=[],
                response_schema={"type": "object"}
            )
        ]
        
        return Microservice(
            name="audit-service",
            description="Audit logging service for compliance and tracking",
            endpoints=endpoints,
            dependencies=[],
            dockerfile=None
        )
    
    def _generate_integration_service(self) -> Microservice:
        """Generate Integration Service"""
        endpoints = [
            APISpec(
                endpoint="/api/v1/integrations/legacy",
                method="POST",
                description="Sync with legacy system",
                parameters=[],
                response_schema={"type": "object"}
            ),
            APISpec(
                endpoint="/api/v1/integrations/status",
                method="GET",
                description="Get integration status",
                parameters=[],
                response_schema={"type": "object"}
            )
        ]
        
        return Microservice(
            name="integration-service",
            description="Integration service for legacy system connectivity",
            endpoints=endpoints,
            dependencies=[],
            dockerfile=None
        )
    
    def generate_docker_compose(self, microservices: List[Microservice]) -> str:
        """Generate Docker Compose configuration"""
        compose = {
            "version": "3.8",
            "services": {},
            "networks": {
                "modernization-network": {
                    "driver": "bridge"
                }
            }
        }
        
        for service in microservices:
            service_name = service.name.replace("-", "_")
            compose["services"][service_name] = {
                "build": {
                    "context": f"./{service.name}",
                    "dockerfile": "Dockerfile"
                },
                "ports": [f"{8000 + len(compose['services'])}:8000"],
                "networks": ["modernization-network"],
                "environment": [
                    "NODE_ENV=production",
                    "DATABASE_URL=postgresql://user:password@database:5432/modernization"
                ],
                "depends_on": service.dependencies
            }
        
        # Add database service
        compose["services"]["database"] = {
            "image": "postgres:13",
            "environment": [
                "POSTGRES_DB=modernization",
                "POSTGRES_USER=user",
                "POSTGRES_PASSWORD=password"
            ],
            "ports": ["5432:5432"],
            "networks": ["modernization-network"],
            "volumes": ["./data:/var/lib/postgresql/data"]
        }
        
        return json.dumps(compose, indent=2)
    
    def generate_kubernetes_manifests(self, microservices: List[Microservice]) -> Dict[str, str]:
        """Generate Kubernetes manifests"""
        manifests = {}
        
        for service in microservices:
            service_name = service.name.replace("-", "_")
            
            # Deployment manifest
            deployment = {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {
                    "name": service_name,
                    "labels": {"app": service_name}
                },
                "spec": {
                    "replicas": 2,
                    "selector": {"matchLabels": {"app": service_name}},
                    "template": {
                        "metadata": {"labels": {"app": service_name}},
                        "spec": {
                            "containers": [{
                                "name": service_name,
                                "image": f"{service_name}:latest",
                                "ports": [{"containerPort": 8000}],
                                "env": [
                                    {"name": "NODE_ENV", "value": "production"},
                                    {"name": "DATABASE_URL", "value": "postgresql://user:password@database:5432/modernization"}
                                ]
                            }]
                        }
                    }
                }
            }
            
            # Service manifest
            service_manifest = {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {"name": service_name},
                "spec": {
                    "selector": {"app": service_name},
                    "ports": [{"port": 8000, "targetPort": 8000}],
                    "type": "ClusterIP"
                }
            }
            
            manifests[f"{service_name}-deployment.yaml"] = json.dumps(deployment, indent=2)
            manifests[f"{service_name}-service.yaml"] = json.dumps(service_manifest, indent=2)
        
        return manifests
