from pydantic import BaseModel, Field

class ProtocolRequest(BaseModel):
    protocol: str = Field(
        ..., 
        min_length=50, 
        title="Protocol Text",
        description="The full text of the scientific protocol to be visualized."
    )

class TaskResponse(BaseModel):
    task_id: str = Field(..., description="The unique identifier for the generation task.")

class StatusResponse(BaseModel):
    task_id: str = Field(..., description="The unique identifier for the generation task.")
    status: str = Field(..., description="The current status of the task (e.g., PENDING, PROCESSING, COMPLETED, FAILED).")
