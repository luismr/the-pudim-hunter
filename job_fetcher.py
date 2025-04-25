import os
import argparse
from pathlib import Path

from storage_job import JobStorage
from pudim_hunter_driver.models import JobQuery
from pudim_hunter_driver_simply_hired.driver import SimplyHiredScraperJobDriver

# Function to fetch jobs
def fetch_jobs(job_title: str, job_location: str, output_path: str, headless: bool = True) -> None:
    # Initialize job storage
    data_folder = str(Path(output_path).parent)
    csv_file = Path(output_path).name
    storage = JobStorage(data_folder=data_folder, file_name=csv_file)

    # Fetch jobs
    query = JobQuery(keywords=job_title, location=job_location)
    driver = SimplyHiredScraperJobDriver(headless=headless)
    job_list = driver.fetch_jobs(query)

    # Save jobs
    storage.create([job.model_dump() for job in job_list.jobs])

# Run job fetcher
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch jobs based on title and location')
    parser.add_argument('--title', type=str, default="Software Engineer",
                      help='Job title to search for (default: Software Engineer)')
    parser.add_argument('--location', type=str, default="Remote",
                      help='Job location to search in (default: Remote)')
    parser.add_argument('--output', type=str, default="data/job_data.csv",
                      help='Path to save job data CSV file (default: data/job_data.csv)')
    parser.add_argument('--disable-headless', action='store_true',
                      help='Disable headless mode (show browser window)')
    
    args = parser.parse_args()
    fetch_jobs(args.title, args.location, args.output, not args.disable_headless)
