from pydantic import BaseModel, Field
from typing import Optional

class ProtocolRequest(BaseModel):
    protocol: str = Field(
        ..., 
        min_length=50, 
        title="Protocol Text",
        description="The full text of the scientific protocol to be visualized."
    )

class TaskResponse(BaseModel):
    task_id: str = Field(..., description="The unique identifier for the generation task.")
    status: str = Field(..., description="The current status of the task (e.g., PENDING, PROCESSING, COMPLETED, FAILED).")
    video_url: Optional[str] = Field(
        None,
        description="The URL where the generated video can be accessed, available only if COMPLETED."
    )

class StatusResponse(BaseModel):
    task_id: str = Field(..., description="The unique identifier for the generation task.")
    status: str = Field(..., description="The current status of the task (e.g., PENDING, PROCESSING, COMPLETED, FAILED).")
    video_url: Optional[str] = Field(
        None,
        description="The URL where the generated video can be accessed, available only if COMPLETED."
    )
