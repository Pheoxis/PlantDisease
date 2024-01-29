"""Project pipelines."""
from kedro.pipeline import Pipeline
from backend.pipelines.backend import create_pipeline as create_backend_pipeline

def register_pipelines() -> dict[str, Pipeline]:
    return {
        "backend": create_backend_pipeline()
    }
