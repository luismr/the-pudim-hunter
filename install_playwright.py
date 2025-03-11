import subprocess

def install_playwright():
    """Ensure Playwright and its browsers are installed."""
    try:
        from playwright.sync_api import sync_playwright
        print("✅ Playwright is already installed.")
    except ImportError:
        print("⚠️ Playwright not found. Installing now...")
        subprocess.run(["pip", "install", "playwright"], check=True)

    # Ensure Playwright browsers are installed
    print("🔄 Installing Playwright browsers...")
    subprocess.run(["playwright", "install"], check=True)
    print("✅ Playwright installation complete!")

# If running this script directly, install Playwright
if __name__ == "__main__":
    install_playwright()
