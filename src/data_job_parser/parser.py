import hashlib
import os
from pathlib import Path

import logfire
from openai import OpenAI

from .config import config
from .models import JobPosting
from .scraper import JobPostingScraper


class JobPostingParser:
    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        headless: bool | None = None,
    ):
        self.api_key = api_key or config.openai_api_key
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Provide it as parameter or set "
                "OPENAI_API_KEY environment variable."
            )

        self.client = OpenAI(api_key=self.api_key)
        self.model = model or config.openai_model
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
        self, url: str, job_posting: JobPosting, output_dir: str | None = None
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
                                "You are an expert at extracting structured information from job "
                                "postings. Extract all relevant information and organize it "
                                "according to the provided schema. Be thorough and accurate in "
                                "your extraction. The content is in markdown format."
                            ),
                        },
                        {
                            "role": "user",
                            "content": (
                                "Extract structured information from this job posting:\n\n"
                                f"{content}"
                            ),
                        },
                    ],
                    response_format=JobPosting,
                )

                result = completion.choices[0].message.parsed
                logfire.info(
                    "Successfully extracted job data",
                    title=result.title,
                    company=result.company,
                )
                return result

            except Exception as e:
                logfire.error("Error extracting structured data", error=str(e))
                raise

    def parse(
        self,
        url: str,
        save_markdown: bool = False,
        save_json: bool = False,
        markdown_dir: str | None = None,
        json_dir: str | None = None,
    ) -> tuple[JobPosting, str | None, str | None]:
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
