import os
import time
import argparse
from pathlib import Path
from typing import Optional

from storage_job import JobStorage
from storage_analysis import AnalysisStorage
from storage_resume import ResumeStorage
from analysis_helper import OpenAIAnalyzer, PromptTemplate

def split_path(path: str) -> tuple[str, str]:
    """Split a path into data folder and file name."""
    path_obj = Path(path)
    return str(path_obj.parent), path_obj.name

def analyze_match_score(analyzer: OpenAIAnalyzer, template: PromptTemplate, 
                      job_description: str, job_qualifications: list, resume: str) -> tuple[Optional[int], str]:
    """Uses OpenAI to analyze the job description and compute a match score with justification."""
    prompt_job_qualifications = "\n- ".join(job_qualifications) if job_qualifications else "No qualifications provided."

    result = analyzer.ask_with_template(
        template,
        {
            "job_description": job_description,
            "job_qualifications": prompt_job_qualifications,
            "resume": resume
        }
    )

    if "ERROR" in result:
        return None, result["ERROR"]

    score = int(result.get("SCORE", 0)) if result.get("SCORE", "").isdigit() else None
    analysis = result.get("ANALYSIS", "No analysis provided.")

    return max(0, min(score, 100)) if score is not None else None, analysis

# Job analysis logic
def analyze_jobs(api_key: str, model: str, analysis_path: str, resume_path: str, jobs_path: str) -> None:
    # Split paths into data_folder and file_name
    analysis_data_folder, analysis_file_name = split_path(analysis_path)
    resume_data_folder, resume_file_name = split_path(resume_path)
    jobs_data_folder, jobs_file_name = split_path(jobs_path)
    
    # Initialize storages
    analysis_storage = AnalysisStorage(data_folder=analysis_data_folder, file_name=analysis_file_name)
    job_storage = JobStorage(data_folder=jobs_data_folder, file_name=jobs_file_name)
    resume_storage = ResumeStorage(data_folder=resume_data_folder, file_name=resume_file_name)
    analyzer = OpenAIAnalyzer(api_key=api_key, model=model)

    # Check if resume is empty
    if resume_storage.is_empty():
        raise EmptyResumeError("❌ ERROR: Resume file is empty. Please add your resume content to the file.")

    # Define the prompt template
    job_analysis_template = PromptTemplate(
        system="""
            You are an AI that rates job suitability based on a résumé.
            You will be given a job description and qualifications, and a résumé.
            You will then provide a match score and a justification for the score.
        """,
        user="""
            Compare the following job description with the provided résumé.
            - Provide a match score from 0 to 100, where 100 is a perfect match.
            - Then, give a short analysis explaining why the score was given.

            Job Description:
            {job_description}

            Job Qualifications:
            {job_qualifications}

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
        """
    )

    # Get all jobs from storage
    jobs_df = job_storage.get_all()
    
    if jobs_df.empty:
        print("✅ No jobs to analyze. No updates needed.")
        return

    print(f"🔍 Found {len(jobs_df)} jobs to analyze.")

    for index, row in jobs_df.iterrows():
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
        job_score, job_analysis = analyze_match_score(
            analyzer,
            job_analysis_template,
            job_description, 
            job_qualifications, 
            resume_storage.get_content()
        )

        if job_score is None:
            print(f"⚠️ Skipping {job_title} (Failed to compute score).")
            continue

        # Save the analysis to CSV
        analysis_storage.save_job_analysis(
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze job matches using OpenAI')
    parser.add_argument('--openai-api-key', type=str,
                      help='OpenAI API key (overrides OPENAI_API_KEY environment variable)')
    parser.add_argument('--openai-model', type=str, default="gpt-4o",
                      help='OpenAI model to use (default: gpt-4o)')
    parser.add_argument('--analysis-path', type=str, default="data/job_analysis.csv",
                      help='Path to job analysis file (default: data/job_analysis.csv)')
    parser.add_argument('--resume-path', type=str, default="data/resume.txt",
                      help='Path to resume file (default: data/resume.txt)')
    parser.add_argument('--jobs-path', type=str, default="data/job_data.csv",
                      help='Path to jobs file (default: data/job_data.csv)')
    
    args = parser.parse_args()
    
    # Get API key from command line or environment
    api_key = args.openai_api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERROR: OpenAI API key is missing. Set OPENAI_API_KEY environment variable or use --openai-api-key argument.")
        exit(1)
    
    # Get model from command line or environment
    model = args.openai_model or os.getenv("OPENAI_API_MODEL", "gpt-4o")

    # Run the job analysis
    analyze_jobs(api_key, model, args.analysis_path, args.resume_path, args.jobs_path)