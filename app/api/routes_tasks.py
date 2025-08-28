from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from ..schemas.task import Task, TaskCreate, TaskUpdate
from ..db.crud import TaskCRUD
from ..core.config import settings

router = APIRouter()

@router.post("/tasks/", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task"""
    try:
        return await TaskCRUD.create(task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")

@router.post("/tasks/batch", response_model=List[Task], status_code=201)
async def create_tasks_batch(tasks: List[TaskCreate]):
    """Create multiple tasks in a single request"""
    if not tasks:
        raise HTTPException(status_code=400, detail="No tasks provided")
    if len(tasks) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 tasks per batch")
    
    try:
        return await TaskCRUD.create_batch(tasks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create tasks: {str(e)}")

@router.get("/tasks/", response_model=List[Task])
async def get_tasks(
    limit: int = Query(100, ge=1, le=1000, description="Number of tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip"),
    status_id: Optional[int] = Query(None, description="Filter by status ID"),
    search: Optional[str] = Query(None, description="Search in name and description")
):
    """Get tasks with pagination, filtering, and search"""
    try:
        if search:
            return await TaskCRUD.search_tasks(search, limit)
        elif status_id is not None:
            return await TaskCRUD.get_by_status(status_id, limit)
        else:
            return await TaskCRUD.get_all(limit, offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tasks: {str(e)}")

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Get a specific task by ID"""
    try:
        task = await TaskCRUD.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch task: {str(e)}")

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update a task by ID"""
    try:
        task = await TaskCRUD.update(task_id, task_update)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")

@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """Delete a task by ID"""
    try:
        deleted = await TaskCRUD.delete(task_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Task not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")

@router.delete("/tasks/batch", status_code=204)
async def delete_tasks_batch(task_ids: List[int]):
    """Delete multiple tasks by IDs"""
    if not task_ids:
        raise HTTPException(status_code=400, detail="No task IDs provided")
    if len(task_ids) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 tasks per batch deletion")
    
    try:
        deleted_count = await TaskCRUD.delete_batch(task_ids)
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="No tasks found to delete")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete tasks: {str(e)}")

@router.get("/tasks/stats/summary")
async def get_task_stats():
    """Get task statistics summary"""
    try:
        stats = await TaskCRUD.get_stats()
        return {
            "total_tasks": stats["total_tasks"],
            "pending_tasks": stats["pending_tasks"],
            "in_progress_tasks": stats["in_progress_tasks"],
            "completed_tasks": stats["completed_tasks"],
            "tasks_with_description": stats["tasks_with_description"],
            "completion_rate": round(
                (stats["completed_tasks"] / stats["total_tasks"] * 100) if stats["total_tasks"] > 0 else 0, 
                2
            )
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch statistics: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Task API"}
