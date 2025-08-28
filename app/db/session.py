import asyncpg
from typing import Optional
from ..core.config import settings

# Global connection pool
_pool: Optional[asyncpg.Pool] = None

async def get_pool() -> asyncpg.Pool:
    """Get or create the database connection pool"""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            settings.DATABASE_URL,
            min_size=settings.DB_POOL_MIN_SIZE,
            max_size=settings.DB_POOL_MAX_SIZE,
            command_timeout=settings.DB_COMMAND_TIMEOUT
        )
    return _pool

async def get_db_connection():
    """Get database connection from pool"""
    pool = await get_pool()
    return await pool.acquire()

async def close_db_connection(conn):
    """Return connection to pool"""
    if conn:
        pool = await get_pool()
        await pool.release(conn)

async def close_pool():
    """Close the connection pool"""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None

async def get_pool_status():
    """Get connection pool status"""
    if _pool:
        return {
            "pool_size": _pool.get_size(),
            "min_size": settings.DB_POOL_MIN_SIZE,
            "max_size": settings.DB_POOL_MAX_SIZE,
            "status": "active"
        }
    return {"pool_size": 0, "min_size": 0, "max_size": 0, "status": "inactive"}
