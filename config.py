from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()

# Get the GitHub token from the environment
GITHUB_TOKEN = os.getenv("MY_GITHUB_PAT")

# Optional: Raise error if token not found
if not GITHUB_TOKEN:
    raise ValueError("MY_GITHUB_PAT not found in environment variables")
