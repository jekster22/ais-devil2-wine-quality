import mlflow
import os

def download():
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])

    with open(".model-version", "r") as f:
        version = f.read().strip()

    # Note the exact name "wine-quality" is used here
    model_uri = f"models:/wine-quality/{version}"
    print(f"Downloading {model_uri}...")

    mlflow.artifacts.download_artifacts(artifact_uri=model_uri, dst_path="models/")

if __name__ == "__main__":
    download()