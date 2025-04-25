# The Pudim Hunter 🍮

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![OpenAI API 0.28](https://img.shields.io/badge/openai--api-0.28-green.svg)](https://pypi.org/project/openai/)
[![Pandas 2.2.x](https://img.shields.io/badge/pandas-2.2.x-orange.svg)](https://pypi.org/project/pandas/)
[![Beautifulsoup4 4.13.x](https://img.shields.io/badge/beautifulsoup4-4.13.x-lightgrey.svg)](https://pypi.org/project/beautifulsoup4/)
[![pudim-hunter-driver 1.0.0](https://img.shields.io/badge/pudim--hunter--driver-1.0.0-blue.svg)](https://github.com/luismr/pudim-hunter-driver)
[![pudim-hunter-driver-scraper 1.0.1](https://img.shields.io/badge/pudim--hunter--driver--scraper-1.0.1-blue.svg)](https://github.com/luismr/pudim-hunter-driver-scraper)
[![pudim-hunter-simply-hired 1.0.1](https://img.shields.io/badge/pudim--hunter--simply--hired-1.0.1-blue.svg)](https://github.com/luismr/pudim-hunter-driver-simply-hired)

A job hunting assistant that helps you find and analyze job opportunities. It fetches job listings from various sources, analyzes them against your resume, and provides match scores and detailed analyses.

## Features

- **Job Fetcher**: Automatically fetches job listings from multiple sources
- **Resume Analysis**: Analyzes job descriptions against your resume
- **Match Scoring**: Provides a score (0-100) for each job based on your resume match
- **Detailed Analysis**: Gives detailed explanations for the match scores
- **Storage Management**: Efficiently manages job data, analysis results, and resume content
- **Modular Design**: Clean separation of concerns with dedicated modules for each functionality
- **Environment Configuration**: Flexible configuration through environment variables and command-line arguments

## Project Structure

```
the-pudim-hunter/
├── data/                    # Data storage directory
│   ├── job_data.csv        # Fetched job listings
│   ├── job_analysis.csv    # Analysis results
│   └── resume.txt          # Your resume content
├── analysis_helper.py      # OpenAI analysis utilities
├── job_fetcher.py         # Main job fetching script
├── job_analyze_scores.py  # Job analysis script
├── storage_job.py         # Job data storage
├── storage_analysis.py    # Analysis results storage
├── storage_resume.py      # Resume content storage
├── requirements.txt       # Python dependencies
└── README.md
```

## Dependencies

This project relies on several key packages:

- [pudim-hunter-driver](https://github.com/luismr/pudim-hunter-driver): Core driver interface for job search
- [pudim-hunter-driver-scraper](https://github.com/luismr/pudim-hunter-driver-scraper): Web scraping utilities
- [pudim-hunter-driver-simply-hired](https://github.com/luismr/pudim-hunter-driver-simply-hired): SimplyHired job board implementation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/the-pudim-hunter.git
cd the-pudim-hunter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
# OpenAI API configuration
export OPENAI_API_KEY="your-api-key"
export OPENAI_API_MODEL="gpt-4o"  # Optional, defaults to gpt-4o

# Job search configuration
export JOB_TITLE="Software Engineer"
export JOB_LOCATION="Remote"
```

## Usage

### 1. Add Your Resume

Create a file at `data/resume.txt` with your resume content. You can also specify a custom path using the `--resume-path` argument.

### 2. Fetch Jobs

Run the job fetcher with your desired parameters:

```bash
# Using environment variables
python job_fetcher.py

# Using command-line arguments
python job_fetcher.py \
    --title "Software Engineer" \
    --location "Remote" \
    --output "data/job_data.csv" \
    --disable-headless
```

Command-line arguments for `job_fetcher.py`:
- `--title`: Job title to search for (default: "Software Engineer")
- `--location`: Job location to search in (default: "Remote")
- `--output`: Path to save job data CSV file (default: "data/job_data.csv")
- `--disable-headless`: Disable headless mode (show browser window)

### 3. Analyze Jobs

Analyze the fetched jobs against your resume:

```bash
# Using environment variables
python job_analyze_scores.py

# Using command-line arguments
python job_analyze_scores.py \
    --openai-api-key "your-api-key" \
    --openai-model "gpt-4o" \
    --analysis-path "data/job_analysis.csv" \
    --resume-path "data/resume.txt" \
    --jobs-path "data/job_data.csv"
```

Command-line arguments for `job_analyze_scores.py`:
- `--openai-api-key`: OpenAI API key (overrides OPENAI_API_KEY environment variable)
- `--openai-model`: OpenAI model to use (default: "gpt-4o")
- `--analysis-path`: Path to job analysis file (default: "data/job_analysis.csv")
- `--resume-path`: Path to resume file (default: "data/resume.txt")
- `--jobs-path`: Path to jobs file (default: "data/job_data.csv")

## Storage Management

The project uses dedicated storage classes for managing different types of data:

1. **JobStorage** (`storage_job.py`): Manages job listings
   - Handles CRUD operations for job data
   - Supports custom data folder and file name
   - Ensures data integrity and file existence

2. **AnalysisStorage** (`storage_analysis.py`): Manages analysis results
   - Stores match scores and analyses
   - Maintains job metadata
   - Supports custom storage paths

3. **ResumeStorage** (`storage_resume.py`): Manages resume content
   - Handles resume file operations
   - Validates resume content
   - Supports custom file paths

## Analysis Process

The job analysis process uses OpenAI's GPT models to:

1. Compare job descriptions with your resume
2. Generate match scores (0-100)
3. Provide detailed analyses explaining the scores
4. Store results for future reference

The analysis considers:
- Job requirements and qualifications
- Your skills and experience
- Job responsibilities
- Location and salary information

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Implement your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT models
- [Playwright](https://playwright.dev/) for web automation
- [Pandas](https://pandas.pydata.org/) for data management
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [pudim-hunter-driver](https://github.com/luismr/pudim-hunter-driver) for the core driver interface
- [pudim-hunter-driver-scraper](https://github.com/luismr/pudim-hunter-driver-scraper) for web scraping utilities
- [pudim-hunter-driver-simply-hired](https://github.com/luismr/pudim-hunter-driver-simply-hired) for SimplyHired job board implementation

*Automate your job search smarter with The Pudim Hunter 🍮!*