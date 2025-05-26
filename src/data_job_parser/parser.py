import hashlib
import os
from pathlib import Path
from typing import Optional, Tuple

import logfire
from openai import OpenAI

from .config import config
from .models import JobPosting
from .scraper import JobPostingScraper


class JobPostingParser:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        headless: Optional[bool] = None,
    ) -> None:
        self.api_key = api_key or config.openai_api_key
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Provide it as parameter or set "
                "OPENAI_API_KEY environment variable."
            )

        self.client = OpenAI(api_key=self.api_key)
        self.model = model or config.openai_model or "gpt-4o-2024-08-06"
        self.scraper = JobPostingScraper(
            headless=headless if headless is not None else config.playwright_headless,
            timeout=config.playwright_timeout,
        )

        # Ensure data directories exist
        Path(config.data_dir).mkdir(parents=True, exist_ok=True)
        Path(config.markdown_output_dir).mkdir(parents=True, exist_ok=True)
        Path(config.json_output_dir).mkdir(parents=True, exist_ok=True)

    def _generate_filename(self, url: str) -> str:
        return hashlib.sha1(url.encode()).hexdigest() + ".json"

    def _save_json(
        self, url: str, job_posting: JobPosting, output_dir: Optional[str] = None
    ) -> str:
        output_dir = output_dir or config.json_output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        filename = self._generate_filename(url)
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(job_posting.model_dump_json(indent=2))

        logfire.info("Saved JSON", filepath=filepath, url=url)
        return filepath

    def _extract_structured_data(self, content: str) -> JobPosting:
        with logfire.span("extract_structured_data", model=self.model):
            try:
                completion = self.client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an expert at structured data extraction. "
                                "Extract all relevant information from the job posting and fill in as many fields as possible. "
                                "For fields you cannot determine, leave them as null or empty lists as appropriate. "
                                "Pay special attention to extracting tech stack, salary information, experience level, and work mode details."
                            ),
                        },
                        {"role": "user", "content": content},
                    ],
                    response_format=JobPosting,
                )

                if completion.choices[0].message.refusal:
                    raise ValueError(
                        f"Model refused to parse: {completion.choices[0].message.refusal}"
                    )

                job_posting = completion.choices[0].message.parsed
                if job_posting is None:
                    raise ValueError("Failed to parse job posting data")

                logfire.info(
                    "Successfully extracted job data",
                    title=job_posting.title,
                    company=job_posting.company,
                )
                return job_posting

            except Exception as e:
                logfire.error("Error extracting structured data", error=str(e))
                raise

    def parse(
        self,
        url: str,
        save_markdown: bool = False,
        save_json: bool = False,
        markdown_dir: Optional[str] = None,
        json_dir: Optional[str] = None,
    ) -> Tuple[JobPosting, Optional[str], Optional[str]]:
        """
        Parse job posting from URL.

        Args:
            url: The job posting URL
            save_markdown: Whether to save the markdown content
            save_json: Whether to save the extracted data as JSON
            markdown_dir: Directory to save markdown files (default: "data/markdown")
            json_dir: Directory to save JSON files (default: "data/json")

        Returns:
            Tuple of (JobPosting object, markdown filepath if saved, json filepath if saved)
        """
        with logfire.span("parse_job_posting", url=url):
            content, markdown_path = self.scraper.fetch_content(
                url, save_markdown, markdown_dir or config.markdown_output_dir
            )
            job_posting = self._extract_structured_data(content)

            json_path = None
            if save_json:
                json_path = self._save_json(
                    url, job_posting, json_dir or config.json_output_dir
                )

            return job_posting, markdown_path, json_path

    async def parse_async(
        self,
        url: str,
        save_markdown: bool = False,
        save_json: bool = False,
        markdown_dir: Optional[str] = None,
        json_dir: Optional[str] = None,
    ) -> Tuple[JobPosting, Optional[str], Optional[str]]:
        """
        Asynchronous version of parse method for use in environments with running event loops
        (like Jupyter notebooks).

        Args:
            url: The job posting URL
            save_markdown: Whether to save the markdown content
            save_json: Whether to save the extracted data as JSON
            markdown_dir: Directory to save markdown files (default: "data/markdown")
            json_dir: Directory to save JSON files (default: "data/json")

        Returns:
            Tuple of (JobPosting object, markdown filepath if saved, json filepath if saved)
        """
        with logfire.span("parse_job_posting_async", url=url):
            content, markdown_path = await self.scraper._fetch_content_async(
                url, save_markdown, markdown_dir or config.markdown_output_dir
            )
            job_posting = self._extract_structured_data(content)

            json_path = None
            if save_json:
                json_path = self._save_json(
                    url, job_posting, json_dir or config.json_output_dir
                )

            return job_posting, markdown_path, json_path
