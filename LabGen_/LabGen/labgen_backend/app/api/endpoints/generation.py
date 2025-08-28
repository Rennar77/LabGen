import uuid
import os
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import FileResponse
from app.models import schemas
from app.services import placeholder_services

router = APIRouter()

# In-memory dictionary to act as a database for task status
# In a real application, this would be Redis, Celery results backend, or a database.
tasks = {}

@router.post("/generate", response_model=schemas.TaskResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_generation_task(
    request: schemas.ProtocolRequest, background_tasks: BackgroundTasks
):
    """
    Initiates a new video generation job.

    - Accepts a protocol text.
    - Generates a unique task ID.
    - Starts a background task to process the video.
    - Returns the task ID immediately.
    """
    task_id = str(uuid.uuid4())
    # Store protocol text and initialize task status.
    # The 'file_path' will be populated by the background worker upon completion.
    tasks[task_id] = {
        "status": "PENDING",
        "file_path": None,
        "protocol_text": request.protocol,
    }

    background_tasks.add_task(
        placeholder_services.process_video_generation, task_id, tasks
    )

    return {"task_id": task_id}

@router.get("/status/{task_id}", response_model=schemas.StatusResponse)
async def get_task_status(task_id: str):
    """
    Checks the status of a generation job.
    
    - Returns the current status of the task (e.g., PENDING, PROCESSING, COMPLETED, FAILED).
    """
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"task_id": task_id, "status": task["status"]}

@router.get("/video/{task_id}", response_class=FileResponse)
async def get_video_file(task_id: str):
    """
    Retrieves the generated video file.
    
    - This endpoint returns the video file directly if the task status is 'COMPLETED'.
    - It uses FileResponse to stream the video content.
    """
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] != "COMPLETED":
        raise HTTPException(
            status_code=400,
            detail=f"Video not ready. Current status: {task['status']}",
        )
    
    file_path = task.get("file_path")
    if not file_path:
        raise HTTPException(status_code=500, detail="Task completed, but file path is missing.")

    if not os.path.exists(file_path):
         raise HTTPException(status_code=404, detail="Video file not found on the server. It may have been deleted.")

    return FileResponse(path=file_path, media_type='video/mp4', filename=f"{task_id}.mp4")
