import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware  
from app.api.endpoints import generation

# Create directory for generated videos 
os.makedirs("generated_videos", exist_ok=True)

app = FastAPI(
    title="LabGen AI Video Generator",
    description="API for generating lab experiment videos from text protocols.",
    version="1.0.0",
)

#  Add CORS middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #replace * with serever later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the 'generated_videos' directory to serve the generated video files.

# This makes files in 'generated_videos' accessible at '/generated_videos/<filename>'.
app.mount("/generated_videos", StaticFiles(directory="generated_videos"), name="generated_videos")

app.include_router(generation.router, prefix="/api/v1", tags=["Video Generation"])

@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Welcome to the LabGen API. Visit /docs for API documentation."
    }


"""from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.api.endpoints import generation
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="LabGen AI Video Generator",
    description="API for generating lab experiment videos from text protocols.",
    version="1.0.0",
)

app.include_router(generation.router, prefix="/api/v1", tags=["Video Generation"])

@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def read_root():
    index_path = Path(__file__).parent / "index.html"
    return index_path.read_text(encoding="utf-8")


# Mount the media directory to be served as static files
app.mount("/media", StaticFiles(directory="media"), name="media")
# Mount the /media URL to serve files from the media/ directory
app.mount("/media", StaticFiles(directory="media"), name="media")

_from fastapi import FastAPI
from app.api.endpoints import generation

app = FastAPI(
    title="LabGen AI Video Generator",
    description="API for generating lab experiment videos from text protocols.",
    version="1.0.0",
)

app.include_router(generation.router, prefix="/api/v1", tags=["Video Generation"])

@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Welcome to the LabGen API. Visit /docs for API documentation."
    }"""

