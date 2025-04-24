import os

from job_storage import save_jobs  
from pudim_hunter_driver.models import JobQuery
from pudim_hunter_driver_simply_hired.driver import SimplyHiredScraperJobDriver

# Function to fetch jobs
def fetch_jobs():
    # Define job search parameters
    job_title = os.getenv("JOB_TITLE", "Software Engineer")  # Set JOB_TITLE key in environment variables
    job_location = os.getenv("JOB_LOCATION", "Remote")  # Set JOB_LOCATION key in environment variables

    query = JobQuery(keywords=job_title, location=job_location)
    driver = SimplyHiredScraperJobDriver(headless=False)
    job_list = driver.fetch_jobs(query)

    # Save or update jobs
    save_jobs(job_list.jobs)

# Run job fetcher
if __name__ == "__main__":
    fetch_jobs()
