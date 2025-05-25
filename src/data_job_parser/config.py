import os
from dataclasses import dataclass
from pathlib import Path


def load_env():
    """Load environment variables from .env file if it exists"""
    env_path = Path(".env")
    if env_path.exists():
        try:
            from dotenv import load_dotenv

            load_dotenv()
        except ImportError:
            pass


@dataclass
class Config:
    """Configuration from environment variables"""

    def __init__(self):
        load_env()

        # OpenAI
        self.openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

        # Logfire
        self.logfire_token: str | None = os.getenv("LOGFIRE_TOKEN")

        # Directories
        self.data_dir: str = os.getenv("DATA_DIR", "data")
        self.markdown_output_dir: str = os.getenv(
            "MARKDOWN_OUTPUT_DIR", "data/markdown"
        )
        self.json_output_dir: str = os.getenv("JSON_OUTPUT_DIR", "data/json")

        # Playwright
        self.playwright_headless: bool = (
            os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() == "true"
        )
        self.playwright_timeout: int = int(os.getenv("PLAYWRIGHT_TIMEOUT", "60000"))


config = Config()
