import os
import time
import openai

from job_storage import load_jobs
from analysis_storage import AnalysisStorage

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

# Initialize the storage
storage = AnalysisStorage()

def analyze_match_score(job_description, job_qualifications, resume):
    """Uses OpenAI GPT-4o (default) to analyze the job description and compute a match score with justification."""

    qualifications_list = "\n- ".join(job_qualifications) if job_qualifications else "No qualifications provided."

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

                Job Qualifications:
                {qualifications_list}

                Résumé:
                {resume}

                *** ASSUMPTIONS ***
                - be realistic with the score
                - keep your scope to the provided job description and qualifications
                - do not make assumptions about the job description or qualifications
                - do not make assumptions about the résumé
                - be assertive and objective with your justification analysis

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
    jobs_to_score = load_jobs()

    if jobs_to_score.empty:
        print("✅ All jobs already have scores. No updates needed.")
        return

    print(f"🔍 Found {len(jobs_to_score)} jobs to analyze.")

    for index, row in jobs_to_score.iterrows():
        job_id = row["id"]
        job_title = row["title"]
        job_summary = row["summary"]
        job_description = row["description"]
        job_source = row["source"]
        job_url = row["url"]
        job_location = row["location"]
        job_salary_range = row["salary_range"]
        job_qualifications = row["qualifications"]
        job_posted_at = row["posted_at"]

        print(f"🔹 Processing job: {job_title} ({job_id})")

        # Compute match score and analysis
        job_score, job_analysis = analyze_match_score(job_description, job_qualifications, resume_content)

        if job_score is None:
            print(f"⚠️ Skipping {job_title} (Failed to compute score).")
            continue

        # Save the analysis to CSV
        storage.save_job_analysis(
            job_id=job_id,
            job_title=job_title,
            job_summary=job_summary,
            job_source=job_source,
            job_url=job_url,
            job_location=job_location,
            job_salary_range=job_salary_range,
            job_qualifications=job_qualifications,
            job_posted_at=job_posted_at,
            match_score=job_score,
            analysis=job_analysis
        )

        print(f"✅ Updated {job_title} with 🍮 score: {job_score} and 👀 Analysis {job_analysis}")

        # Rate limit to avoid API abuse
        time.sleep(2)

    print("🎯 Job analysis completed!")

# Run the job analysis
if __name__ == "__main__":
    process_jobs()
