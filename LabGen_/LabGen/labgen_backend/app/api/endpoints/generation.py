import uuid
import os
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import FileResponse
from app.models import schemas
from app.services import placeholder_services

router = APIRouter()

# In-memory dictionary to act as a database for task status
tasks = {}

@router.post("/generate", response_model=schemas.TaskResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_generation_task(
    request: schemas.ProtocolRequest, background_tasks: BackgroundTasks
):
    """
    Initiates a new video generation job.
    """
    task_id = str(uuid.uuid4())

    tasks[task_id] = {
        "status": "PENDING",
        "file_path": None,
        "protocol_text": request.protocol,
    }

    background_tasks.add_task(
        placeholder_services.process_video_generation, task_id, tasks
    )

    # Return immediately with task_id
    return {"task_id": task_id, "status": "PENDING", "video_url": None}


@router.get("/status/{task_id}", response_model=schemas.StatusResponse)
async def get_task_status(task_id: str):
    """
    Checks the status of a generation job.
    """
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Build video URL only if completed
    video_url = None
    if task["status"] == "COMPLETED" and task["file_path"]:
        video_url = f"/api/v1/video/{task_id}"

    return {"task_id": task_id, "status": task["status"], "video_url": video_url}


@router.get("/video/{task_id}", response_class=FileResponse)
async def get_video_file(task_id: str):
    """
    Retrieves the generated video file.
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
