# backend/data_loader.py

import os
import pandas as pd
import uuid

class DataLoader:
    def __init__(self, data_dir="backend/data"):
        self.data_dir = data_dir
        self.raw_dir = f"{data_dir}/raw"
        os.makedirs(self.raw_dir, exist_ok=True)

    # 📤 Save uploaded dataset (CSV)
    def save_dataset(self, file, dataset_name: str = None):
        if dataset_name is None:
            dataset_name = str(uuid.uuid4())
        dataset_path = f"{self.raw_dir}/{dataset_name}.csv"

        # Save file
        with open(dataset_path, "wb") as f:
            f.write(file)

        return {"dataset_id": dataset_name, "path": dataset_path}

    # 📥 Load dataset as DataFrame
    def load_dataset(self, dataset_id: str) -> pd.DataFrame:
        dataset_path = f"{self.raw_dir}/{dataset_id}.csv"
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset {dataset_id} not found.")
        return pd.read_csv(dataset_path)

    # ✅ Validate dataset (check columns, NaNs, etc.)
    def validate_dataset(self, dataset_id: str):
        df = self.load_dataset(dataset_id)

        summary = {
            "dataset_id": dataset_id,
            "n_rows": len(df),
            "n_columns": len(df.columns),
            "columns": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "dtypes": df.dtypes.astype(str).to_dict(),
        }

        return summary

    # 📂 List all datasets
    def list_datasets(self):
        datasets = []
        for file in os.listdir(self.raw_dir):
            if file.endswith(".csv"):
                dataset_id = file.replace(".csv", "")
                datasets.append(dataset_id)
        return datasets

    # ❌ Delete a dataset
    def delete_dataset(self, dataset_id: str):
        dataset_path = f"{self.raw_dir}/{dataset_id}.csv"
        if os.path.exists(dataset_path):
            os.remove(dataset_path)
            return {"message": f"Dataset {dataset_id} deleted."}
        return {"error": "Dataset not found."}
