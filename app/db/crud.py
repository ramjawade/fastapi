from typing import List, Optional, Dict, Any
import asyncpg
from .session import get_db_connection, close_db_connection
from ..schemas.task import TaskCreate, TaskUpdate, Task

class TaskCRUD:
    @staticmethod
    async def create(task: TaskCreate) -> Task:
        """Create a new task with optimized query"""
        conn = await get_db_connection()
        try:
            query = """
                INSERT INTO tasks (name, description, status_id, flag_id)
                VALUES ($1, $2, $3, $4)
                RETURNING id, name, description, status_id, flag_id
            """
            row = await conn.fetchrow(
                query, 
                task.name, 
                task.description, 
                task.status_id, 
                task.flag_id
            )
            return Task(**dict(row))
        except asyncpg.UniqueViolationError:
            raise ValueError("Task with this name already exists")
        except asyncpg.ForeignKeyViolationError:
            raise ValueError("Invalid status_id or flag_id")
        finally:
            await close_db_connection(conn)

    @staticmethod
    async def create_batch(tasks: List[TaskCreate]) -> List[Task]:
        """Create multiple tasks in a single transaction"""
        if not tasks:
            return []
            
        conn = await get_db_connection()
        try:
            async with conn.transaction():
                query = """
                    INSERT INTO tasks (name, description, status_id, flag_id)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id, name, description, status_id, flag_id
                """
                rows = await conn.executemany(query, [
                    (task.name, task.description, task.status_id, task.flag_id)
                    for task in tasks
                ])
                return [Task(**dict(row)) for row in rows]
        finally:
            await close_db_connection(conn)

    @staticmethod
    async def get_all(limit: int = 100, offset: int = 0) -> List[Task]:
        """Get all tasks with pagination"""
        conn = await get_db_connection()
        try:
            query = """
                SELECT id, name, description, status_id, flag_id
                FROM tasks 
                ORDER BY id
                LIMIT $1 OFFSET $2
            """
            rows = await conn.fetch(query, limit, offset)
            return [Task(**dict(row)) for row in rows]
        finally:
            await close_db_connection(conn)

    @staticmethod
    async def get_by_id(task_id: int) -> Optional[Task]:
        """Get task by ID with optimized query"""
        conn = await get_db_connection()
        try:
            query = """
                SELECT id, name, description, status_id, flag_id
                FROM tasks 
                WHERE id = $1
            """
            row = await conn.fetchrow(query, task_id)
            return Task(**dict(row)) if row else None
        finally:
            await close_db_connection(conn)

    @staticmethod
    async def get_by_status(status_id: int, limit: int = 50) -> List[Task]:
        """Get tasks by status with pagination"""
        conn = await get_db_connection()
        try:
            query = """
                SELECT id, name, description, status_id, flag_id
                FROM tasks 
                WHERE status_id = $1
                ORDER BY id
                LIMIT $2
            """
            rows = await conn.fetch(query, status_id, limit)
            return [Task(**dict(row)) for row in rows]
        finally:
            await close_db_connection(conn)

    @staticmethod
    async def search_tasks(search_term: str, limit: int = 50) -> List[Task]:
        """Search tasks by name or description"""
        conn = await get_db_connection()
        try:
            query = """
                SELECT id, name, description, status_id, flag_id
                FROM tasks 
                WHERE name ILIKE $1 OR description ILIKE $1
                ORDER BY 
                    CASE 
                        WHEN name ILIKE $1 THEN 1
                        WHEN description ILIKE $1 THEN 2
                        ELSE 3
                    END,
                    id
                LIMIT $2
            """
            search_pattern = f"%{search_term}%"
            rows = await conn.fetch(query, search_pattern, limit)
            return [Task(**dict(row)) for row in rows]
        finally:
            await close_db_connection(conn)

    @staticmethod
    async def update(task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """Update task by ID with optimized query building"""
        conn = await get_db_connection()
        try:
            # Check if task exists first
            existing = await conn.fetchrow(
                "SELECT id FROM tasks WHERE id = $1", 
                task_id
            )
            if not existing:
                return None
            
            # Build dynamic update query efficiently
            update_data = {}
            if task_update.name is not None:
                update_data['name'] = task_update.name
            if task_update.description is not None:
                update_data['description'] = task_update.description
            if task_update.status_id is not None:
                update_data['status_id'] = task_update.status_id
            if task_update.flag_id is not None:
                update_data['flag_id'] = task_update.flag_id
            
            if not update_data:
                # Return existing task if no updates
                existing_task = await conn.fetchrow(
                    "SELECT * FROM tasks WHERE id = $1", 
                    task_id
                )
                return Task(**dict(existing_task))
            
            # Build query dynamically
            set_clause = ", ".join(f"{k} = ${i+2}" for i, k in enumerate(update_data.keys()))
            values = list(update_data.values()) + [task_id]
            
            query = f"""
                UPDATE tasks 
                SET {set_clause}
                WHERE id = ${len(values)}
                RETURNING id, name, description, status_id, flag_id
            """
            
            row = await conn.fetchrow(query, *values)
            return Task(**dict(row))
        except asyncpg.ForeignKeyViolationError:
            raise ValueError("Invalid status_id or flag_id")
        finally:
            await close_db_connection(conn)

    @staticmethod
    async def delete(task_id: int) -> bool:
        """Delete task by ID"""
        conn = await get_db_connection()
        try:
            result = await conn.execute(
                "DELETE FROM tasks WHERE id = $1", 
                task_id
            )
            return result == "DELETE 1"
        finally:
            await close_db_connection(conn)

    @staticmethod
    async def delete_batch(task_ids: List[int]) -> int:
        """Delete multiple tasks by IDs"""
        if not task_ids:
            return 0
            
        conn = await get_db_connection()
        try:
            # Use ANY operator for efficient batch deletion
            query = "DELETE FROM tasks WHERE id = ANY($1)"
            result = await conn.execute(query, task_ids)
            # Extract the number of deleted rows
            deleted_count = int(result.split()[-1])
            return deleted_count
        finally:
            await close_db_connection(conn)

    @staticmethod
    async def get_stats() -> Dict[str, Any]:
        """Get task statistics"""
        conn = await get_db_connection()
        try:
            query = """
                SELECT 
                    COUNT(*) as total_tasks,
                    COUNT(CASE WHEN status_id = 1 THEN 1 END) as pending_tasks,
                    COUNT(CASE WHEN status_id = 2 THEN 1 END) as in_progress_tasks,
                    COUNT(CASE WHEN status_id = 3 THEN 1 END) as completed_tasks,
                    COUNT(CASE WHEN description IS NOT NULL THEN 1 END) as tasks_with_description
                FROM tasks
            """
            row = await conn.fetchrow(query)
            return dict(row)
        finally:
            await close_db_connection(conn)
