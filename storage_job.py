import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

class JobStorage:
    """Storage for job data."""

    def __init__(self, data_folder: str = "./data", file_name: str = "job_data.csv"):
        """Initialize the JobStorage with data folder and CSV file path."""
        self.data_folder = data_folder
        self.csv_file = os.path.join(data_folder, file_name)
        
        # Ensure the data folder exists
        Path(self.data_folder).mkdir(parents=True, exist_ok=True)
        
        # Initialize or load the DataFrame
        self._load_data()

    def _load_data(self) -> None:
        """Load data from CSV file or create empty DataFrame if file doesn't exist."""
        if os.path.exists(self.csv_file):
            self.df = pd.read_csv(self.csv_file)
        else:
            self.df = pd.DataFrame()

    def _save_data(self) -> None:
        """Save the current DataFrame to CSV file."""
        self.df.to_csv(self.csv_file, index=False)
        print(f"✅ Jobs saved to {self.csv_file}!")

    def create(self, jobs: List[Dict[str, Any]]) -> None:
        """Create new job entries."""
        if not jobs:
            return

        # Convert jobs to DataFrame
        new_jobs_df = pd.DataFrame(jobs)
        
        # Add timestamp if not present
        if 'timestamp' not in new_jobs_df.columns:
            new_jobs_df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Append new jobs to existing data
        self.df = pd.concat([self.df, new_jobs_df], ignore_index=True)
        self._save_data()

    def read(self, filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Read jobs with optional filtering."""
        if filters is None:
            return self.df.copy()
        
        # Apply filters
        mask = pd.Series(True, index=self.df.index)
        for key, value in filters.items():
            if key in self.df.columns:
                mask &= (self.df[key] == value)
        
        return self.df[mask].copy()

    def update(self, job_id: str, updates: Dict[str, Any]) -> bool:
        """Update a specific job by ID."""
        if 'id' not in self.df.columns:
            return False
        
        mask = self.df['id'] == job_id
        if not mask.any():
            return False
        
        # Update the job
        for key, value in updates.items():
            if key in self.df.columns:
                self.df.loc[mask, key] = value
        
        self._save_data()
        return True

    def delete(self, job_id: str) -> bool:
        """Delete a specific job by ID."""
        if 'id' not in self.df.columns:
            return False
        
        mask = self.df['id'] == job_id
        if not mask.any():
            return False
        
        # Remove the job
        self.df = self.df[~mask]
        self._save_data()
        return True

    def get_all(self) -> pd.DataFrame:
        """Get all jobs."""
        return self.df.copy()

    def get_by_id(self, job_id: str) -> Optional[pd.Series]:
        """Get a specific job by ID."""
        if 'id' not in self.df.columns:
            return None
        
        job = self.df[self.df['id'] == job_id]
        return job.iloc[0] if not job.empty else None

    def clear(self) -> None:
        """Clear all job data."""
        self.df = pd.DataFrame()
        self._save_data()
