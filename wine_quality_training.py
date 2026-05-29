# wine_quality_training.py
import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import mlflow
import joblib

mlflow.set_tracking_uri(os.getenv("https://dagshub.com/jekster22/ais-devil2-wine-quality.mlflow"))
mlflow.autolog()

def main():
    df = pd.read_parquet("data/winequality.parquet")
    
    df["wine_color"] = df["wine_color"].apply(lambda x: 1 if x == "red" else 0)
    
    X = df.drop(columns=["quality"])
    y = df["quality"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        model.fit(X_train, y_train)
        
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        print(f"Accuracy: {acc}")
        
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/wine_quality_model.pkl")
        
        metadata = {"accuracy": acc, "report": classification_report(y_test, preds, output_dict=True)}
        with open("models/wine_quality_model.metadata.json", "w") as f:
            json.dump(metadata, f)

if __name__ == "__main__":
    main()
