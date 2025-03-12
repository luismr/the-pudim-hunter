# The Pudim Hunter 🍮

**The Pudim Hunte 🍮r** is a Proof of Concept (PoC) tool designed to automate your job search by scraping job listings from SimplyHired, analyzing them against your resume, and assigning a relevance score. This provides insights into how well each job matches your skills, helping you focus on the most promising opportunities.

## Features

- **Job Scraping**: Fetches open positions from SimplyHired.
- **Resume Analysis**: Compares job descriptions with your resume to assess compatibility.
- **Scoring System**: Assigns a relevance score to each job based on the analysis.
- **Insightful Reporting**: Offers detailed feedback on how well each job aligns with your skills.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/luismr/the-pudim-hunter.git
   cd the-pudim-hunter
   ```

2. **Set up a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Prepare Your Resume  
Ensure your resume is available at `data/resume.txt`. The analysis script relies on this file.

### 2. Fetch Job Listings  

By default, the script searches for "Software Engineer" roles in "Remote" locations.  
You can modify the job title and location using environment variables:

#### Default Run:
```bash
python job_fetcher.py
```

#### Custom Job Title and Location:
```bash
export JOB_TITLE="Data Scientist"
export JOB_LOCATION="New York"
python job_fetcher.py
```

On Windows (PowerShell):
```powershell
$env:JOB_TITLE="Data Scientist"
$env:JOB_LOCATION="New York"
python job_fetcher.py
```

This will fetch jobs for "Data Scientist" in "New York".

### 3. Analyze Job Listings Against Your Resume  

To analyze job listings, you **must** set an OpenAI API key in the `OPENAI_API_KEY` environment variable. You can generate a key from your OpenAI account dashboard.

#### Set the OpenAI API Key:

On Linux/macOS:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

On Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

Then, run the analysis script:

```bash
python job_analyze_scores.py
```

This script will compare each job listing with `data/resume.txt` and assign a relevance score.

### 4. Review the Results  

The analyzed job listings will be saved in `data/job_data.csv`. You can open this file using a spreadsheet application such as **Excel** or **Google Spreadsheets** to explore the results.

#### Suggested Analysis:
- **Filter positions with a score ≥ 80** to focus on the most relevant job opportunities.
- **Check the `score_analysis` column** for highlights that explain why each job was rated as a strong match for your resume.
- **Sort jobs by score** to prioritize applications for the highest-ranked positions.

By reviewing the `score_analysis` details, you can refine your job applications and target roles that best match your profile.

## Expected Improvements

The project is under continuous improvement. Below are some planned enhancements:

✅ **Better OpenAI Prompting**: Improve the AI prompt to refine the filtering of **remote-only positions**, specifically those that:

   👀 Allow candidates to work **fully remote**.
   👀 Are **open to applicants from Brazil** or **worldwide**.

✅ **Playwright Headless Mode**: Tune Playwright to **work in headless mode** for faster and more efficient job scraping.

✅ **Automatic Sorting of job_data.csv**: Ensure job listings are **automatically sorted by score** before saving, making it easier to identify top matches.

✅ **Auto Apply to Quick Apply Jobs**: Implement an automation feature to **auto-apply** to positions that have the **"Quick Apply"** option available.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `(LICENSE)[./LICENSE.md]` file for more details.

## Acknowledgments

- [Playwright](https://playwright.dev/python/docs/intro) for web scraping capabilities.
- [OpenAI](https://openai.com/) for natural language processing tools.

*Automate your job search smarter with The Pudim Hunter 🍮!*