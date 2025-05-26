import hashlib
from unittest.mock import AsyncMock, Mock, patch

import pytest

from data_job_parser import JobPosting, JobPostingParser
from data_job_parser.scraper import JobPostingScraper


@pytest.fixture
def mock_openai_response():
    return JobPosting(
        title="Senior Software Engineer",
        company="Tech Corp",
        location={
            "city": "San Francisco",
            "state": "CA",
            "country": "USA",
            "is_remote": False,
        },
        description="We are looking for a senior software engineer...",
        required_skills=["Python", "AWS", "Docker"],
        salary={
            "min_amount": 120000,
            "max_amount": 180000,
            "currency": "USD",
            "period": "yearly",
        },
    )


@patch("data_job_parser.parser.OpenAI")
@patch("data_job_parser.scraper.async_playwright")
@patch("pathlib.Path.mkdir")
def test_parse_job_posting(
    mock_mkdir, mock_playwright, mock_openai, mock_openai_response
):
    # Setup playwright mock
    mock_page = AsyncMock()
    mock_page.title = AsyncMock(return_value="Job Title")
    mock_page.content = AsyncMock(
        return_value="<html><body>Job posting content</body></html>"
    )
    mock_page.set_viewport_size = AsyncMock()
    mock_page.goto = AsyncMock()
    mock_page.add_script_tag = AsyncMock()
    mock_page.evaluate = AsyncMock(return_value=None)  # Readability.js returns None
    mock_page.query_selector = AsyncMock(return_value=None)  # No main/article/section

    mock_browser = AsyncMock()
    mock_browser.new_page = AsyncMock(return_value=mock_page)
    mock_browser.close = AsyncMock()

    mock_playwright_instance = AsyncMock()
    mock_playwright_instance.chromium.launch = AsyncMock(return_value=mock_browser)
    mock_playwright.return_value.__aenter__ = AsyncMock(
        return_value=mock_playwright_instance
    )

    # Setup OpenAI mock for Structured Outputs
    mock_message = Mock()
    mock_message.parsed = mock_openai_response
    mock_message.refusal = None

    mock_choice = Mock()
    mock_choice.message = mock_message

    mock_completion = Mock()
    mock_completion.choices = [mock_choice]

    mock_openai.return_value.beta.chat.completions.parse.return_value = mock_completion

    # Test parsing
    parser = JobPostingParser(api_key="test-key")
    result, markdown_path, json_path = parser.parse("https://example.com/job")

    assert result.title == "Senior Software Engineer"
    assert result.company == "Tech Corp"
    assert result.location.city == "San Francisco"
    assert "Python" in result.required_skills
    assert markdown_path is None
    assert json_path is None


@patch("data_job_parser.parser.OpenAI")
@patch("data_job_parser.scraper.async_playwright")
@patch("builtins.open", create=True)
@patch("os.path.join")
@patch("pathlib.Path.mkdir")
def test_parse_with_markdown_save(
    mock_mkdir, mock_join, mock_open, mock_playwright, mock_openai, mock_openai_response
):
    # Setup playwright mock
    mock_page = AsyncMock()
    mock_page.title = AsyncMock(return_value="Job Title")
    mock_page.content = AsyncMock(
        return_value="<html><body>Job posting content</body></html>"
    )
    mock_page.set_viewport_size = AsyncMock()
    mock_page.goto = AsyncMock()
    mock_page.add_script_tag = AsyncMock()
    mock_page.evaluate = AsyncMock(return_value=None)
    mock_page.query_selector = AsyncMock(return_value=None)

    mock_browser = AsyncMock()
    mock_browser.new_page = AsyncMock(return_value=mock_page)
    mock_browser.close = AsyncMock()

    mock_playwright_instance = AsyncMock()
    mock_playwright_instance.chromium.launch = AsyncMock(return_value=mock_browser)
    mock_playwright.return_value.__aenter__ = AsyncMock(
        return_value=mock_playwright_instance
    )

    # Setup OpenAI mock for Structured Outputs
    mock_message = Mock()
    mock_message.parsed = mock_openai_response
    mock_message.refusal = None

    mock_choice = Mock()
    mock_choice.message = mock_message

    mock_completion = Mock()
    mock_completion.choices = [mock_choice]

    mock_openai.return_value.beta.chat.completions.parse.return_value = mock_completion

    # Setup path mocks
    def mock_join_side_effect(*args):
        if args[-1].endswith(".md"):
            return "data/markdown/hash.md"
        return "data/json/hash.json"

    mock_join.side_effect = mock_join_side_effect

    # Test parsing with save
    parser = JobPostingParser(api_key="test-key")
    result, markdown_path, json_path = parser.parse(
        "https://example.com/job", save_markdown=True, save_json=False
    )

    assert result.title == "Senior Software Engineer"
    assert markdown_path == "data/markdown/hash.md"
    assert json_path is None


def test_generate_filename():
    parser = JobPostingParser(api_key="test-key")
    url = "https://example.com/job"
    expected = hashlib.sha1(url.encode()).hexdigest() + ".json"
    assert parser._generate_filename(url) == expected


def test_scraper_initialization():
    scraper = JobPostingScraper()
    assert scraper.headless is True
    assert scraper.timeout == 60000
