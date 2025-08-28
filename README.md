# Task API - High-Performance CRUD Operations

A **high-performance** FastAPI-based REST API that provides complete CRUD (Create, Read, Update, Delete) operations for managing tasks with advanced features and optimizations.

## 🚀 **Performance Features**

- **Connection Pooling**: Efficient database connection management
- **Batch Operations**: Create/delete multiple tasks in single requests
- **Pagination**: Optimized data retrieval with configurable limits
- **Search & Filtering**: Full-text search with relevance scoring
- **Database Indexes**: Optimized queries with proper indexing
- **Async Operations**: Non-blocking I/O for high concurrency
- **Request Timing**: Performance monitoring with response headers

## ✨ **Enhanced Features**

- **Create** - Add new tasks with validation
- **Read** - Retrieve tasks with pagination, filtering, and search
- **Update** - Modify existing tasks (partial updates supported)
- **Delete** - Remove tasks individually or in batches
- **Statistics** - Get comprehensive task analytics
- **Health Monitoring** - System health and pool status
- **Batch Operations** - Efficient bulk operations
- **Advanced Search** - Full-text search with relevance ranking

## 🔗 **API Endpoints**

### **Core CRUD Operations**

#### 1. Create Task
- **POST** `/api/v1/tasks/`
- **Description**: Create a new task
- **Request Body**:
```json
{
    "name": "Task Name",
    "description": "Task Description",
    "status_id": 1,
    "flag_id": 1
}
```

#### 2. Create Multiple Tasks (Batch)
- **POST** `/api/v1/tasks/batch`
- **Description**: Create multiple tasks in a single request
- **Request Body**: Array of task objects (max 100)

#### 3. Get Tasks with Advanced Options
- **GET** `/api/v1/tasks/`
- **Query Parameters**:
  - `limit`: Number of tasks (1-1000, default: 100)
  - `offset`: Skip tasks (default: 0)
  - `status_id`: Filter by status
  - `search`: Search in name and description

#### 4. Get Task by ID
- **GET** `/api/v1/tasks/{task_id}`

#### 5. Update Task
- **PUT** `/api/v1/tasks/{task_id}`
- **Description**: Update task with partial data support

#### 6. Delete Task
- **DELETE** `/api/v1/tasks/{task_id}`

#### 7. Delete Multiple Tasks (Batch)
- **DELETE** `/api/v1/tasks/batch`
- **Request Body**: Array of task IDs (max 100)

### **Advanced Features**

#### 8. Task Statistics
- **GET** `/api/v1/tasks/stats/summary`
- **Response**: Complete task analytics with completion rates

#### 9. Health Check
- **GET** `/health`
- **Response**: System health status

#### 10. API Information
- **GET** `/api/info`
- **Response**: API features and endpoint information

## 🗄️ **Enhanced Database Schema**

The `tasks` table includes:
- `id`: Primary key (auto-increment)
- `name`: Task name (required, unique)
- `description`: Task description (optional)
- `status_id`: Status identifier (1=pending, 2=in_progress, 3=completed)
- `flag_id`: Flag identifier (1=normal, 2=priority)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

**Performance Indexes**:
- `idx_tasks_status_id`: Status filtering optimization
- `idx_tasks_flag_id`: Flag filtering optimization
- `idx_tasks_created_at`: Time-based queries optimization

## ⚙️ **Configuration & Environment**

### **Environment Variables**
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# API Settings
ENVIRONMENT=development  # development/production
DEBUG=true
API_V1_STR=/api/v1

# Database Pool
DB_POOL_MIN_SIZE=5
DB_POOL_MAX_SIZE=20
DB_COMMAND_TIMEOUT=60

# Security
SECRET_KEY=your-secret-key
```

### **Performance Tuning**
- **Connection Pool**: Configurable min/max pool sizes
- **Query Timeouts**: Configurable command and statement timeouts
- **Batch Limits**: Configurable batch operation sizes
- **Pagination**: Configurable page size limits

## 🐍 **Virtual Environment Setup**

### **Automatic Setup (Recommended)**

#### **Windows (Batch)**
```bash
# Run the activation script
activate_venv.bat
```

### **Manual Setup**

#### **1. Create Virtual Environment**
```bash
# Windows (using py launcher)
py -m venv venv

# Unix/Linux/macOS
python3 -m venv venv
```

#### **2. Activate Virtual Environment**
```bash
# Windows
venv\Scripts\activate.bat

# PowerShell
venv\Scripts\Activate.ps1

# Unix/Linux/macOS
source venv/bin/activate
```

#### **3. Install Dependencies**
```bash
pip install -r app/requirements.txt
```

#### **4. Deactivate (when done)**
```bash
deactivate
```

## 🚀 **Setup and Installation**

### **Prerequisites**
- Python 3.8+ installed
- PostgreSQL database running
- pip package manager

### **1. Install Dependencies**
```bash
# Install required packages
pip install -r app/requirements.txt

# Or install individually:
pip install fastapi uvicorn asyncpg pydantic
```

### **2. Database Configuration**
- Ensure PostgreSQL is running
- Update the `DATABASE_URL` in `app/core/config.py` with your database credentials

### **3. Run the Application**
```bash
# Method 1: Using launcher
python run.py

# Method 2: Direct uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **4. Access the API**
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## 📊 **Performance Monitoring**

### **Response Headers**
- `X-Process-Time`: Request processing time in seconds

### **Health Endpoints**
- `/health`: Basic health status
- `/api/info`: Detailed API information

### **Database Pool Status**
- Connection pool utilization
- Pool size and free connections

## 🔍 **Search and Filtering**

### **Text Search**
- Full-text search in task names and descriptions
- Relevance-based ranking
- Configurable result limits

### **Status Filtering**
- Filter by task status (pending, in-progress, completed)
- Pagination support for filtered results

### **Advanced Queries**
- Combined search and filtering
- Optimized SQL with proper indexing

## 📈 **Batch Operations**

### **Batch Creation**
- Create up to 100 tasks in single request
- Transaction-based for data consistency
- Efficient bulk insertion

### **Batch Deletion**
- Delete multiple tasks by IDs
- Optimized with PostgreSQL ANY operator
- Returns deletion count

## 🛡️ **Security & Privacy**

- **Input Validation**: Comprehensive Pydantic validation
- **SQL Injection Protection**: Parameterized queries
- **Error Handling**: Secure error messages
- **CORS Configuration**: Configurable cross-origin settings
- **Trusted Hosts**: Host validation middleware
- **Rate Limiting**: Configurable request limits

## 📝 **Example Usage**

### **Create a task**:
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Learn FastAPI", "description": "Study FastAPI framework"}'
```

### **Search tasks**:
```bash
curl "http://localhost:8000/api/v1/tasks/?search=FastAPI&limit=10"
```

### **Batch create tasks**:
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/batch" \
     -H "Content-Type: application/json" \
     -d '[
       {"name": "Task 1", "description": "First task"},
       {"name": "Task 2", "description": "Second task"}
     ]'
```

### **Get statistics**:
```bash
curl "http://localhost:8000/api/v1/tasks/stats/summary"
```

## 🏗️ **Project Structure**

```
app/
│── __init__.py
│── main.py
│
├── api/
│   └── routes_tasks.py
│
├── core/
│   └── config.py
│
├── db/
│   ├── session.py
│   ├── models.py
│   └── crud.py
│
├── schemas/
│   └── task.py
│
├── requirements.txt
     └── setup scripts/
     └── activate_venv.bat
```

## 🔧 **Development & Testing**

### **Test Imports**:
```bash
python test_imports.py
```

### **Performance Testing**:
- Use batch endpoints for bulk operations
- Monitor response headers for timing
- Check database pool utilization

## 🚨 **Troubleshooting**

### **Common Issues**:

#### 1. **Import Errors**
```bash
# Error: ModuleNotFoundError: No module named 'pydantic_settings'
# Solution: The app now uses standard pydantic BaseSettings
```

#### 2. **Missing Dependencies**
```bash
# Install dependencies:
pip install -r app/requirements.txt

# Or install individually:
pip install fastapi uvicorn asyncpg pydantic
```

#### 3. **Database Connection Issues**
- Check if PostgreSQL is running
- Verify connection string in `app/core/config.py`
- Ensure database exists and is accessible

#### 4. **Python Path Issues**
- Run from project root directory
- Ensure all `__init__.py` files are present
- Check Python version (3.8+ required)

#### 5. **Virtual Environment Issues**
```bash
# If using py launcher on Windows:
py -m venv venv
venv\Scripts\activate.bat

# If using python directly:
python -m venv venv
venv\Scripts\activate.bat
```

### **Debug Mode**:
Set `DEBUG=true` in environment for detailed logging and error messages.

## 📚 **Best Practices Implemented**

- **Connection Pooling**: Efficient database resource management
- **Async/Await**: Non-blocking I/O operations
- **Input Validation**: Comprehensive data validation
- **Error Handling**: Graceful error management
- **Performance Monitoring**: Request timing and pool status
- **Security**: Input sanitization and validation
- **Scalability**: Configurable limits and timeouts
- **Virtual Environment**: Isolated dependency management

## 🔄 **Recent Updates**

- **Fixed**: Replaced `pydantic_settings` with standard `pydantic.BaseSettings`
- **Simplified**: Reduced external dependencies
- **Enhanced**: Improved error handling and configuration validation
- **Optimized**: Better performance and connection management
- **Added**: Virtual environment activation script
- **Updated**: Support for Windows `py` launcher
