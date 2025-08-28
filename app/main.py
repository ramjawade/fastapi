from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import logging
from .api.routes_tasks import router
from .db.session import get_db_connection, close_pool, close_db_connection
from .core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Task API application...")
    try:
        # Test database connection and create tables
        conn = await get_db_connection()
        
        # Create the tasks table with all required columns
        await conn.execute("""
          CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                status_id INTEGER DEFAULT 1 CHECK (status_id IN (1, 2, 3)),
                flag_id INTEGER DEFAULT 1 CHECK (flag_id IN (1, 2)),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check if columns exist before creating indexes
        try:
            # Create indexes for better performance (only if columns exist)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_tasks_status_id ON tasks(status_id);
                CREATE INDEX IF NOT EXISTS idx_tasks_flag_id ON tasks(flag_id);
                CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);
            """)
            logger.info("Database indexes created successfully")
        except Exception as index_error:
            logger.warning(f"Some indexes could not be created: {index_error}")
        
        await close_db_connection(conn)
        logger.info("Database connection established and tables created")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Task API application...")
    await close_pool()
    logger.info("Application shutdown complete")

# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A high-performance FastAPI-based REST API for task management with full CRUD operations",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.DEBUG else ["localhost", "127.0.0.1"]
)

# Include routes
app.include_router(router, prefix=settings.API_V1_STR)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": "internal_error"
        }
    )

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to responses"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "timestamp": time.time()
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production",
        "health": "/health"
    }

# API info endpoint
@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": "High-performance task management API",
        "features": [
            "Full CRUD operations",
            "Batch operations",
            "Search and filtering",
            "Pagination",
            "Statistics",
            "Connection pooling",
            "Performance optimized"
        ],
        "endpoints": {
            "tasks": f"{settings.API_V1_STR}/tasks/",
            "batch_operations": f"{settings.API_V1_STR}/tasks/batch",
            "statistics": f"{settings.API_V1_STR}/tasks/stats/summary",
            "health": "/health"
        }
    }
