import pandas as pd
from typing import Optional
from datetime import datetime
import os

class AnalysisStorage:
    def __init__(self, csv_path: str = "data/analysis.csv"):
        self.csv_path = csv_path
        self._ensure_csv_exists()

    def _ensure_csv_exists(self):
        """Create the CSV file with headers if it doesn't exist."""
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists(self.csv_path):
            # Create empty DataFrame with all necessary columns
            df = pd.DataFrame(columns=[
                "job_id",
                "job_title",
                "job_summary",
                "job_source",
                "job_url",
                "job_location",
                "job_salary_range",
                "job_qualifications",
                "job_posted_at",
                "match_score",
                "analysis",
                "analyzed_at"
            ])
            # Save empty DataFrame with headers
            df.to_csv(self.csv_path, index=False)

    def save_job_analysis(
        self,
        job_id: str,
        job_title: str,
        job_summary: Optional[str],
        job_source: str,
        job_url: str,
        job_location: str,
        job_salary_range: Optional[str],
        job_qualifications: str,
        job_posted_at: str,
        match_score: float,
        analysis: str
    ) -> None:
        """
        Save job analysis data to CSV file.
        If a record with the same job_id exists, it will be updated.
        """
        # Prepare the new data
        new_data = {
            "job_id": [job_id],
            "job_title": [job_title],
            "job_summary": [job_summary],
            "job_source": [job_source],
            "job_url": [job_url],
            "job_location": [job_location],
            "job_salary_range": [job_salary_range],
            "job_qualifications": [job_qualifications],
            "job_posted_at": [job_posted_at],
            "match_score": [match_score],
            "analysis": [analysis],
            "analyzed_at": [datetime.now().isoformat()]
        }

        # Create DataFrame from new data
        new_df = pd.DataFrame(new_data)

        try:
            # Read existing CSV if it exists
            if os.path.exists(self.csv_path):
                df = pd.read_csv(self.csv_path)
                
                # Remove existing entry with same job_id if exists
                df = df[df["job_id"] != job_id]
                
                # Append new data
                df = pd.concat([df, new_df], ignore_index=True)
            else:
                df = new_df

            # Save to CSV
            df.to_csv(self.csv_path, index=False)
            print(f"✅ Successfully saved analysis for job ID: {job_id}")
            
        except Exception as e:
            print(f"❌ Error saving analysis for job ID {job_id}: {str(e)}")
            raise

    def get_job_analysis(self, job_id: str) -> Optional[dict]:
        """
        Retrieve job analysis data for a specific job_id.
        Returns None if job_id is not found.
        """
        try:
            df = pd.read_csv(self.csv_path)
            job_data = df[df["job_id"] == job_id]
            
            if len(job_data) == 0:
                return None
                
            return job_data.iloc[0].to_dict()
            
        except Exception as e:
            print(f"❌ Error retrieving analysis for job ID {job_id}: {str(e)}")
            return None 