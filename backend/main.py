import logging
import os
import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import config as app_config
import storage
from models import ApiConfig, SolveRequest, SolveResponse, SolutionStep
from solver import solve_problem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Ensure data directory exists
os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)

app = FastAPI(title="Photo Solver API", version="1.0.0")

# CORS - allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "name": "Photo Solver API"}


@app.post("/api/solve", response_model=SolveResponse)
async def solve(request: SolveRequest):
    """Solve a problem from an uploaded image.

    Accepts a base64-encoded image, calls the AI Vision API to recognize
    and solve the problem, then returns step-by-step solution.
    """
    if not request.image or not request.image.strip():
        raise HTTPException(status_code=400, detail="图片内容不能为空")

    logger.info(
        f"Received solve request, filename={request.filename}, "
        f"image_length={len(request.image)}"
    )

    try:
        result = await solve_problem(request.image, request.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error during solving")
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

    # Build the response
    record_id = str(uuid.uuid4())
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    solution_steps = [
        SolutionStep(step=s["step"], title=s["title"], content=s["content"])
        for s in result["solution"]
    ]

    response = SolveResponse(
        id=record_id,
        problem=result["problem"],
        subject=result["subject"],
        solution=solution_steps,
        tips=result.get("tips", ""),
        created_at=created_at,
    )

    # Save to storage
    storage.save(response.model_dump())

    logger.info(f"Solved problem, id={record_id}, subject={result['subject']}")
    return response


@app.get("/api/history")
async def get_history():
    """Get all history records (summary only, no full solution)."""
    return storage.get_all()


@app.get("/api/history/{record_id}")
async def get_history_detail(record_id: str):
    """Get a single history record with full solution details."""
    record = storage.get_by_id(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    return record


@app.delete("/api/history/{record_id}")
async def delete_history(record_id: str):
    """Delete a history record."""
    deleted = storage.delete(record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="记录不存在")
    return {"status": "ok"}


@app.post("/api/config")
async def save_config(config: ApiConfig):
    """Save API configuration (key, endpoint, model)."""
    app_config.save_config(config)
    logger.info("API configuration saved")
    return {"status": "ok"}


@app.get("/api/config")
async def get_config():
    """Get current API configuration (API key is masked)."""
    return app_config.get_config()


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Photo Solver API on port 8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
