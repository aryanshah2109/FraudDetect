import json
from pathlib import Path
from typing import Any, Dict, List

from fastapi import Request
from src.config import config_loader
from src.path_constants import ROOT_DIR


class ArtifactsService:
    def __init__(self):
        config = config_loader.load_config()
        self.model_name = config["model"]["name"]
        self.artifacts_root = ROOT_DIR / "artifacts" / self.model_name

    def get_latest_artifacts(self, request: Request) -> Dict[str, Any]:
        latest_run_path = self._get_latest_run_path()
        metrics = self._load_metrics(latest_run_path)
        charts = self._build_chart_urls(latest_run_path, request)

        return {
            "latest_run": latest_run_path.name,
            "metrics": metrics,
            "charts": charts,
        }

    def _get_latest_run_path(self) -> Path:
        if not self.artifacts_root.exists():
            raise FileNotFoundError("Artifacts directory does not exist.")

        run_dirs = [entry for entry in self.artifacts_root.iterdir() if entry.is_dir()]
        if not run_dirs:
            raise FileNotFoundError("No artifact runs found.")

        latest_run = max(run_dirs, key=lambda entry: entry.name)
        return latest_run

    def _load_metrics(self, run_path: Path) -> Dict[str, Any]:
        metrics_path = run_path / "metrics.json"
        if not metrics_path.is_file():
            raise FileNotFoundError(f"metrics.json not found for run {run_path.name}.")

        with open(metrics_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _build_chart_urls(self, run_path: Path, request: Request) -> List[Dict[str, str]]:
        plots_dir = run_path / "plots"
        if not plots_dir.exists() or not plots_dir.is_dir():
            raise FileNotFoundError(f"Plots directory not found for run {run_path.name}.")

        chart_files = sorted(
            [item for item in plots_dir.iterdir() if item.is_file() and item.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg"}],
            key=lambda path: path.name,
        )
        if not chart_files:
            raise FileNotFoundError(f"No chart image files found for run {run_path.name}.")

        base_url = str(request.base_url).rstrip("/")
        return [
            {
                "name": chart.name,
                "url": f"{base_url}/artifacts/files/{self.model_name}/{run_path.name}/plots/{chart.name}",
            }
            for chart in chart_files
        ]


artifacts_service = ArtifactsService()
