from typing import Any, Dict, List

from pydantic import BaseModel


class ArtifactChart(BaseModel):
    name: str
    url: str


class ArtifactsResponse(BaseModel):
    latest_run: str
    metrics: Dict[str, Any]
    charts: List[ArtifactChart]
