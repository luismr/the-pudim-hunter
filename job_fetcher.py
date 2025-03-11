import os
from datetime import datetime
from job_storage import save_jobs  # Import storage functions
from install_playwright import install_playwright  # Import the Playwright installer

# Ensure Playwright is installed
install_playwright()

from playwright.sync_api import sync_playwright  # Now import Playwright safely

# Function to fetch jobs
def fetch_jobs():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)  # Change to True for faster execution
        page = browser.new_page()

        # Define job search parameters
        job_title = os.getenv("JOB_TITLE", "Software Engineer")  # Set JOB_TITLE key in environment variables
        job_location = os.getenv("JOB_LOCATION", "Remote")  # Set JOB_LOCATION key in environment variables

        # Open SimplyHired search page
        base_url = f"https://www.simplyhired.com/search?q={job_title.replace(' ', '+')}&l={job_location.replace(' ', '+')}"
        page.goto(base_url, timeout=60000)  # Wait up to 60 seconds

        job_list = []
        today_date = datetime.today().strftime('%Y-%m-%d')

        page_number = 1  # Start from page 1

        while True:
            print(f"🔍 Scraping page {page_number}...")

            # Wait for job list to appear
            try:
                page.wait_for_selector("#job-list li", timeout=10000)
            except:
                print("⚠️ No more job listings found. Exiting...")
                break  # Stop if no job list is found

            # Select all job postings
            job_elements = page.query_selector_all("#job-list li")

            for job in job_elements:
                title_element = job.query_selector("h2 a")
                company_element = job.query_selector("[data-testid='companyName']")
                location_element = job.query_selector("[data-testid='searchSerpJobLocation']")
                salary_element = job.query_selector("[data-testid='searchSerpJobSalaryConfirmed']")

                title = title_element.inner_text() if title_element else "N/A"
                link = title_element.get_attribute("href") if title_element else None
                company = company_element.inner_text() if company_element else "N/A"
                job_location = location_element.inner_text() if location_element else "N/A"
                salary = salary_element.inner_text() if salary_element else "N/A"

                if link:
                    full_link = f"https://www.simplyhired.com{link}"
                    job_list.append({
                        "job_id": full_link.split("/")[-1],  # Unique ID from job link
                        "title": title,
                        "company": company,
                        "location": job_location,
                        "salary": salary,
                        "link": full_link,
                        "first_seen": today_date,  # First time fetched
                        "last_fetched": today_date,  # Last time updated
                        "applied": False,  # Default as not applied
                        "date_applied": None
                    })

            # Find the next page link using the correct page number
            next_page_number = page_number + 1
            next_page_button = page.query_selector(f"a[data-testid='paginationBlock{next_page_number}']")

            if next_page_button:
                next_page_url = next_page_button.get_attribute("href")
                if next_page_url:
                    print(f"➡️ Moving to page {next_page_number}: {next_page_url}")
                    page.goto(next_page_url, timeout=60000)
                    page_number += 1
                else:
                    print("❌ No more pages available.")
                    break
            else:
                print("❌ No more pages available.")
                break

        browser.close()

        # Save or update jobs
        save_jobs(job_list)

# Run job fetcher
fetch_jobs()
