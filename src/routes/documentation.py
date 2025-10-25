from fastapi import APIRouter
from starlette.responses import FileResponse
from pathlib import Path

router = APIRouter()

# Serve only the documentation HTML page here. Static files are mounted on the
# main FastAPI app at /static (see src/main.py).
static_dir = Path(__file__).resolve().parents[1] / "static"


@router.get("/")
async def serve_index():
    index_path = static_dir / "index.html"
    return FileResponse(index_path)
