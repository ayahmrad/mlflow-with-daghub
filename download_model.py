import os
import shutil
import mlflow
from mlflow.tracking import MlflowClient

uri = "https://dagshub.com/ayahmrad/mlflow-with-daghub.mlflow"

mlflow.set_tracking_uri(uri)
mlflow.set_registry_uri(uri)

name = os.getenv("MODEL_NAME", "digits-random-forest")

versions = list(
    MlflowClient().search_model_versions(f"name='{name}'")
)
if not versions:
    raise RuntimeError(f"No registered versions found for {name}")

latest = max(versions, key=lambda v: int(v.version))

path = mlflow.artifacts.download_artifacts(
    artifact_uri=f"models:/{name}/{latest.version}"
)

shutil.copytree(path, "model", dirs_exist_ok=True)

print(f"Downloaded {name} version {latest.version}")