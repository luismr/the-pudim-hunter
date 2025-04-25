import os
from pathlib import Path
from typing import Optional

class ResumeStorage:
    """Storage for the resume file."""

    def __init__(self, data_folder: str = "./data", file_name: str = "resume.txt"):
        """Initialize the ResumeStorage with a path to the resume file."""
        self.resume_path = os.path.join(data_folder, file_name)
        self._ensure_resume_exists()
        self._load_resume()

    def _ensure_resume_exists(self) -> None:
        """Ensure the resume file exists, create directory if needed."""
        path = Path(self.resume_path)
        if not path.exists():
            # Create parent directory if it doesn't exist
            path.parent.mkdir(parents=True, exist_ok=True)
            # Create empty file
            path.touch()
            print(f"⚠️ Created empty resume file at {self.resume_path}")

    def _load_resume(self) -> None:
        """Load the resume content from file."""
        try:
            with open(self.resume_path, "r", encoding="utf-8") as file:
                self.content = file.read().strip()
        except Exception as e:
            print(f"❌ Error loading resume: {e}")
            self.content = ""

    def get_content(self) -> str:
        """Get the current resume content."""
        return self.content

    def update_content(self, new_content: str) -> None:
        """Update the resume content and save to file."""
        self.content = new_content.strip()
        try:
            with open(self.resume_path, "w", encoding="utf-8") as file:
                file.write(self.content)
            print(f"✅ Resume updated at {self.resume_path}")
        except Exception as e:
            print(f"❌ Error saving resume: {e}")

    def is_empty(self) -> bool:
        """Check if the resume content is empty."""
        return not bool(self.content) 