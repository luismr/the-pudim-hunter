import os
import pandas as pd
from datetime import datetime
from pathlib import Path

# Define storage location
DATA_FOLDER = "./data"
CSV_FILE = os.path.join(DATA_FOLDER, "job_data.csv")

# Ensure the ./data folder exists
Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)

# Define required columns
COLUMNS = [
    "job_id", "title", "company", "location", "salary", "link",
    "first_seen", "last_fetched", "applied", "date_applied",
    "score", "date_score_updated","score_analysis"
]

def ensure_columns(df):
    """Ensure the CSV file has all required columns."""
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = None  # Add missing columns with default None values
    return df

def save_jobs(job_list):
    """Save or update jobs in the CSV file, preventing duplicates."""
    today_date = datetime.today().strftime('%Y-%m-%d')

    # Load existing data if file exists
    if os.path.exists(CSV_FILE):
        df_existing = pd.read_csv(CSV_FILE)
        df_existing = ensure_columns(df_existing)
    else:
        df_existing = pd.DataFrame(columns=COLUMNS)

    # Convert applied column to boolean
    df_existing["applied"] = df_existing["applied"].astype(bool)

    # Convert job list to DataFrame
    df_new = pd.DataFrame(job_list)
    df_new = ensure_columns(df_new)

    # Merge data to avoid duplicates
    df_merged = pd.concat([df_existing, df_new]).drop_duplicates(subset=["job_id"], keep="first")

    # Update last_fetched date for existing jobs
    df_merged.loc[df_merged["job_id"].isin(df_new["job_id"]), "last_fetched"] = today_date

    # Save updated data
    df_merged.to_csv(CSV_FILE, index=False)
    print(f"✅ Jobs updated in {CSV_FILE}!")

def load_jobs():
    """Load job listings from the CSV file."""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        return ensure_columns(df)  # Ensure all columns exist
    else:
        print("⚠️ No job data found. Returning an empty DataFrame.")
        return pd.DataFrame(columns=COLUMNS)

def truncate_jobs(confirm=False):
    """Clear all job listings from the CSV file."""
    if not confirm and __name__ == "__main__":
        confirmation = input("⚠️ Are you sure you want to delete ALL job data? (y/yes): ").strip().lower()
        if confirmation not in ["y", "yes"]:
            print("❌ Truncate operation canceled.")
            return

    df_empty = pd.DataFrame(columns=COLUMNS)
    df_empty.to_csv(CSV_FILE, index=False)
    print(f"🗑️ All job data cleared from {CSV_FILE}!")

def mark_as_applied(job_id):
    """Mark a job as applied by updating the 'applied' status and saving the change."""
    df = load_jobs()

    if job_id in df["job_id"].values:
        today_date = datetime.today().strftime('%Y-%m-%d')
        df.loc[df["job_id"] == job_id, "applied"] = True
        df.loc[df["job_id"] == job_id, "date_applied"] = today_date
        df.to_csv(CSV_FILE, index=False)
        print(f"✅ Job {job_id} marked as applied on {today_date}")
    else:
        print(f"❌ Job ID {job_id} not found!")

def update_job_score(job_id, score, analysis):
    """Update the score of a job and set the last score update date."""
    df = load_jobs()

    if job_id in df["job_id"].values:
        today_date = datetime.today().strftime('%Y-%m-%d')
        df.loc[df["job_id"] == job_id, "score"] = score
        df.loc[df["job_id"] == job_id, "date_score_updated"] = today_date
        df.loc[df["job_id"] == job_id, "score_analysis"] = analysis
        df.to_csv(CSV_FILE, index=False)
        print(f"✅ Job {job_id} updated with score {score} on {today_date}")
    else:
        print(f"❌ Job ID {job_id} not found!")

# If run directly, ask the user before truncating job data
if __name__ == "__main__":
    truncate_jobs()
