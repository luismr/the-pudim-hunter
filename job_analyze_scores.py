import os
import time
from job_storage import load_jobs, update_job_score
from install_playwright import install_playwright
from playwright.sync_api import sync_playwright
import openai

# Ensure Playwright is installed
install_playwright()

# Load API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Set API key in environment variables
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL", "gpt-4o")  # Set Model in environment variables


if not OPENAI_API_KEY:
    print("❌ ERROR: OpenAI API key is missing. Set OPENAI_API_KEY environment variable.")
    exit(1)

openai.api_key = OPENAI_API_KEY

# Ensure resume.txt exists
RESUME_PATH = "./data/resume.txt"

if not os.path.exists(RESUME_PATH):
    print("❌ ERROR: Resume file not found! Ensure 'data/resume.txt' exists.")
    exit(1)

# Load resume content
with open(RESUME_PATH, "r", encoding="utf-8") as file:
    resume_content = file.read().strip()

def fetch_job_description(job_url):
    """Fetches job description from the main <aside> section of the job page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(job_url, timeout=60000)

        try:
            # page.wait_for_selector("aside", timeout=10000)  # Wait for any aside element
            job_description_element = page.query_selector("aside")  # Select the only aside
            job_description = job_description_element.inner_text() if job_description_element else ""
        except:
            print(f"⚠️ Could not retrieve job details for: {job_url}")
            job_description = ""

        browser.close()
        return job_description.strip()


def analyze_match_score(job_description, resume):
    """Uses OpenAI GPT-4o (default) to analyze the job description and compute a match score with justification."""
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_API_MODEL,
            messages=[
                {"role": "system", "content": "You are an AI that rates job suitability based on a résumé."},
                {"role": "user", "content": f"""
                Compare the following job description with the provided résumé.
                - Provide a match score from 0 to 100, where 100 is a perfect match.
                - Then, give a short analysis explaining why the score was given.

                Job Description:
                {job_description}

                Résumé:
                {resume}

                Respond in the following format:
                SCORE: <numeric_score>
                ANALYSIS: <justification>
                """}
            ]
        )

        response_text = response["choices"][0]["message"]["content"].strip()

        # Splitting response by 'SCORE:' and 'ANALYSIS:'
        parts = response_text.split("ANALYSIS:")

        if len(parts) == 2:
            score_part = parts[0].replace("SCORE:", "").strip()
            analysis_part = parts[1].strip()

            score = int(score_part) if score_part.isdigit() else None
            analysis = analysis_part if analysis_part else "No analysis provided."
        else:
            score, analysis = None, "Failed to extract analysis."

        return max(0, min(score, 100)) if score is not None else None, analysis

    except Exception as e:
        print(f"⚠️ OpenAI API Error: {e}")
        return None, "Error occurred during analysis."


def process_jobs():
    """Reads jobs without scores, fetches descriptions, computes scores, and updates CSV."""
    df = load_jobs()
    jobs_to_score = df[df["score"].isna() | df["score"].isnull()]

    if jobs_to_score.empty:
        print("✅ All jobs already have scores. No updates needed.")
        return

    print(f"🔍 Found {len(jobs_to_score)} jobs to analyze.")

    for index, row in jobs_to_score.iterrows():
        job_id = row["job_id"]
        job_title = row["title"]
        job_link = row["link"]

        print(f"🔹 Processing job: {job_title} ({job_id})")

        # Fetch job description
        job_description = fetch_job_description(job_link)

        if not job_description:
            print(f"⚠️ Skipping {job_title} (No job description found).")
            continue

        # Compute match score and analysis
        score, analysis = analyze_match_score(job_description, resume_content)

        if score is None:
            print(f"⚠️ Skipping {job_title} (Failed to compute score).")
            continue

        # Update the job score in job_data.csv
        update_job_score(job_id, score, analysis)
        print(f"✅ Updated {job_title} with 🍮 score: {score} and 👀 Analysis {analysis}")

        # Rate limit to avoid API abuse
        time.sleep(2)

    print("🎯 Job analysis completed!")

# Run the job analysis
process_jobs()
