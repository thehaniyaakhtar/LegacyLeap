# LegacyLeap

A comprehensive AI-powered solution for modernizing IBM AS/400 (iSeries) systems into modern APIs and microservices architectures.

## 🚀 Features

### Core Capabilities
- **Legacy Data Ingestion**: Support for flat files, DB2 tables, green-screen interfaces, and RPG programs
- **AI-Powered Transformation**: Intelligent analysis and conversion to modern data structures
- **REST API Generation**: Automatic creation of modern REST APIs with OpenAPI specifications
- **Microservices Architecture**: Smart suggestions for microservices decomposition
- **Modern Dashboard**: Beautiful React-based UI for visualization and management
- **Real-time Processing**: Live data transformation and monitoring

### Supported Legacy Formats
- **Flat Files**: Fixed-width and delimited formats
- **DB2 Tables**: DDS and SQL table definitions
- **Green Screen Interfaces**: AS/400 display file formats
- **RPG Programs**: RPG and RPGLE source code analysis

### Modern Outputs
- **REST APIs**: Full CRUD operations with filtering and pagination
- **JSON Schemas**: Modern data structure definitions
- **Microservices**: Domain-driven service architecture
- **Docker Containers**: Containerized deployment configurations
- **Kubernetes Manifests**: Production-ready orchestration

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React UI      │    │   FastAPI       │    │   AI Engine     │
│   Dashboard     │◄──►│   Backend       │◄──►│   (OpenAI)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         │              │  Legacy Data    │              │
         │              │  Ingestion      │              │
         │              └─────────────────┘              │
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         └─────────────►│  Modernized     │◄─────────────┘
                        │  Data Store     │
                        └─────────────────┘
```

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- Docker (optional)
- OpenAI API key (optional, for AI features)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional):
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

5. **Run the backend**:
   ```bash
   python main.py
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd my-legacy-modernizer
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the frontend**:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## 📖 Usage

### 1. Upload Legacy Data

**Via Web Interface**:
- Drag and drop AS/400 files onto the upload area
- Supported formats: `.txt`, `.dat`, `.sql`, `.rpg`, `.rpgle`

**Via API**:
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@your-legacy-file.txt"
```

**Direct Ingestion**:
```bash
curl -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "CUST001JOHN DOE    123 MAIN ST    NEW YORK    NY10001 555-0123",
    "source_type": "flat_file",
    "name": "customer_data.txt"
  }'
```

### 2. Transform Data

```bash
curl -X POST "http://localhost:8000/transform/{legacy_id}"
```

### 3. Query Modernized Data

```bash
curl -X POST "http://localhost:8000/query/{modernized_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "table_name": "customers",
    "filters": {"city": "NEW YORK"},
    "limit": 10
  }'
```

### 4. Get Microservices Architecture

```bash
curl "http://localhost:8000/microservices/{modernized_id}"
```

## 🔧 API Endpoints

### Core Endpoints
- `POST /upload` - Upload legacy files
- `POST /ingest` - Ingest legacy data directly
- `POST /transform/{legacy_id}` - Transform legacy data
- `GET /legacy/{legacy_id}` - Get legacy data details
- `GET /modernized/{modernized_id}` - Get modernized data
- `POST /query/{modernized_id}` - Query modernized data
- `GET /microservices/{modernized_id}` - Get microservices architecture
- `GET /api-specs/{modernized_id}` - Get OpenAPI specification
- `GET /dashboard` - Get dashboard overview

### Sample Data
The system includes sample AS/400 data files for testing:
- Customer data (fixed-width and delimited)
- Order data
- Product/inventory data
- Employee data
- Financial data
- DB2 table definitions
- RPG programs
- Green screen interfaces

## 🏢 Microservices Architecture

The system generates intelligent microservices recommendations:

### Core Services
- **API Gateway**: Routing and load balancing
- **Data Service**: CRUD operations for each entity
- **Business Service**: Domain-specific business logic

### Domain Services
- **Customer Service**: Customer management and search
- **Order Service**: Order processing and status tracking
- **Product Service**: Product catalog and inventory
- **Employee Service**: HR and organizational management
- **Financial Service**: Account and transaction management

### Supporting Services
- **Notification Service**: Alerts and communications
- **Audit Service**: Compliance and tracking
- **Integration Service**: Legacy system connectivity

## 🐳 Docker Deployment

### Docker Compose
```bash
# Generate docker-compose.yml
curl "http://localhost:8000/microservices/{modernized_id}" | jq '.docker_compose' > docker-compose.yml

# Deploy
docker-compose up -d
```

### Kubernetes
```bash
# Generate Kubernetes manifests
curl "http://localhost:8000/microservices/{modernized_id}" | jq '.kubernetes_manifests' > manifests/

# Deploy
kubectl apply -f manifests/
```

## 📊 Dashboard Features

- **Real-time Metrics**: Processing status and success rates
- **Data Visualization**: Charts and graphs for insights
- **File Management**: Upload and track legacy files
- **Transformation Monitoring**: Live progress tracking
- **API Documentation**: Interactive API explorer
- **Microservices Overview**: Architecture visualization

## 🔍 Sample Data Formats

### Fixed-Width Flat File
```
CUST001JOHN DOE    123 MAIN ST    NEW YORK    NY10001 555-0123
CUST002JANE SMITH  456 OAK AVE   CHICAGO     IL60601 555-0456
```

### Delimited Flat File
```
CUST_ID|CUST_NAME|ADDRESS|CITY|STATE|ZIP|PHONE
CUST001|JOHN DOE|123 MAIN ST|NEW YORK|NY|10001|555-0123
```

### DB2 DDS
```
A          R CUSTOMER
A            CUSTID         10A        TEXT('Customer ID')
A            CUSTNAME       30A        TEXT('Customer Name')
A            ADDRESS        50A        TEXT('Street Address')
```

### RPG Program
```
     FCUSTOMER  IF   E           K DISK
     D CustomerDS       DS
     D  CustID                10A
     D  CustName              30A
```

## 🚀 Getting Started

1. **Start the backend**:
   ```bash
   cd backend
   python main.py
   ```

2. **Start the frontend**:
   ```bash
   cd my-legacy-modernizer
   npm run dev
   ```

3. **Open your browser** to `http://localhost:3000`

4. **Upload a sample file** or use the provided sample data

5. **Watch the magic happen** as your legacy data transforms into modern APIs!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏆 Hackathon Features

This solution addresses the hackathon requirements:

✅ **Legacy Input Ingestion**: Supports AS/400 flat files, DB2 tables, green-screen commands
✅ **AI-Powered Analysis**: Intelligent parsing and structure detection
✅ **Modern Data Structures**: JSON schemas and REST APIs
✅ **User Interface**: Beautiful React dashboard
✅ **Microservices Architecture**: Smart service decomposition
✅ **Scalability**: Docker and Kubernetes support
✅ **Real-world Impact**: Addresses enterprise modernization challenges

## 🎯 Business Impact

- **Reduced Migration Costs**: Automated transformation reduces manual effort
- **Faster Time-to-Market**: Quick API generation from legacy data
- **Modern Integration**: REST APIs enable cloud and mobile integration
- **Scalable Architecture**: Microservices support future growth
- **Risk Mitigation**: Gradual modernization approach
- **Developer Productivity**: Modern tools and interfaces

---


