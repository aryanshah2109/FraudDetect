from fastapi import APIRouter, HTTPException, Request

from app.schemas.artifacts_schema import ArtifactsResponse
from app.services.artifacts_service import artifacts_service

router = APIRouter(
    prefix="/artifacts",
    tags=["artifacts"]
)


@router.get("/", response_model=ArtifactsResponse)
async def get_latest_artifacts(request: Request):
    try:
        return artifacts_service.get_latest_artifacts(request)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
