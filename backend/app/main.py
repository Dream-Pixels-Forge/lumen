from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import perception, reasoning

app = FastAPI(
    title="Lumen UI Navigator",
    description="A Large Action Model (LAM) framework for visual automation.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(perception.router, prefix="/api/v1", tags=["Perception"])
app.include_router(reasoning.router, prefix="/api/v1", tags=["Reasoning"])

@app.get("/")
async def root():
    return {"message": "Lumen UI Navigator is active", "status": "online"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
