import os
import pandas as pd
from datetime import datetime
from pathlib import Path

# Define storage location
DATA_FOLDER = "./data"
CSV_FILE = os.path.join(DATA_FOLDER, "job_data.csv")

# Ensure the ./data folder exists
Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)


def save_jobs(job_list):
    """Save or update jobs in the CSV file, preventing duplicates."""
    today_date = datetime.today().strftime('%Y-%m-%d')

    # Load existing data if file exists
    if os.path.exists(CSV_FILE):
        df_existing = pd.read_csv(CSV_FILE)

    # Convert job list to DataFrame
    df_new = pd.DataFrame([job.model_dump() for job in job_list])

    # Save updated data
    df_new.to_csv(CSV_FILE, index=False)
    print(f"✅ Jobs updated in {CSV_FILE}!")

def load_jobs():
    """Load job listings from the CSV file."""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        return df
    else:
        raise Exception("⚠️ No job data found. Returning an empty DataFrame.")
