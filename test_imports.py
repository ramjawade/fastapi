#!/usr/bin/env python3
"""Test script to verify all imports work correctly"""

def test_imports():
    try:
        print("Testing imports...")
        
        # Test core config
        from app.core.config import settings
        print("✅ Core config imported successfully")
        print(f"   Project: {settings.PROJECT_NAME}")
        print(f"   Version: {settings.VERSION}")
        
        # Test database session
        from app.db.session import get_db_connection, close_db_connection
        print("✅ Database session imported successfully")
        
        # Test schemas
        from app.schemas.task import Task, TaskCreate, TaskUpdate
        print("✅ Schemas imported successfully")
        
        # Test CRUD operations
        from app.db.crud import TaskCRUD
        print("✅ CRUD operations imported successfully")
        
        # Test API routes
        from app.api.routes_tasks import router
        print("✅ API routes imported successfully")
        
        # Test main app
        from app.main import app
        print("✅ Main app imported successfully")
        
        print("\n🎉 All imports successful! The application structure is correct.")
        print(f"📊 Configuration loaded: {settings.PROJECT_NAME} v{settings.VERSION}")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try installing dependencies: pip install -r app/requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
