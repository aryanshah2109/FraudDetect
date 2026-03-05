import logging
import os
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Reduce logging noise
logging.getLogger("mlflow").setLevel(logging.ERROR)
logging.getLogger("alembic").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("xgboost").setLevel(logging.ERROR)
logging.getLogger("git").setLevel(logging.ERROR)
logging.getLogger("matplotlib").setLevel(logging.ERROR)
logging.getLogger("PIL").setLevel(logging.ERROR)

# Disable MLflow telemetry
os.environ["MLFLOW_DISABLE_TELEMETRY"] = "true"

from src.pipelines.training_pipeline import TrainingPipeline

TrainingPipeline().run_pipeline()
