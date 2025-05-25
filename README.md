# Data Job Parser

[![PyPI Downloads](https://static.pepy.tech/badge/data-job-parser)](https://pepy.tech/projects/data-job-parser)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/data-job-parser)](https://pypi.org/project/data-job-parser/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/mazzasaverio/data-job-parser/workflows/CI/badge.svg)](https://github.com/mazzasaverio/data-job-parser/actions)

Extract structured data from job postings using OpenAI's structured output capabilities.

## Features

- 🎯 **Smart Extraction**: Extract structured information from any job posting URL
- 🧠 **AI-Powered**: Uses OpenAI's GPT models with structured output for accurate parsing
- 📊 **Comprehensive Data**: Covers all job posting aspects including salary, skills, requirements
- 🌐 **Advanced Scraping**: Playwright-based scraping handles JavaScript-heavy sites
- 💾 **File Storage**: Save as markdown and JSON with SHA-1 hash filenames for deduplication
- 🔄 **Reliability**: Automatic retries with exponential backoff for robust operation
- 📝 **Observability**: Detailed logging with Logfire integration
- 🐍 **Modern Python**: Full type hints and Python 3.8+ support

## Installation

```bash
pip install data-job-parser
```

After installation, install Playwright browsers:

```bash
playwright install chromium
```

## Quick Start

### Basic Usage

```python
from data_job_parser import JobPostingParser

# Initialize with OpenAI API key
parser = JobPostingParser(api_key="your-openai-api-key")

# Parse a job posting
job_data = parser.parse("https://example.com/job-posting")

# Access structured data
print(f"Title: {job_data.title}")
print(f"Company: {job_data.company}")
print(f"Location: {job_data.location.city}, {job_data.location.country}")
print(f"Salary: {job_data.salary.min_amount}-{job_data.salary.max_amount} {job_data.salary.currency}")
print(f"Skills: {', '.join(job_data.required_skills)}")
```

### Save Files

```python
# Parse and save both markdown and JSON
job_data, markdown_path, json_path = await parser.parse_async(
    "https://jobs.pradagroup.com/job/Milan-Data-Engineer/1199629101/",
    save_markdown=True,
    save_json=True
)

print(f"Markdown: {markdown_path}")
print(f"JSON: {json_path}")
```

### Batch Processing

```python
from data_job_parser import JobPostingParser

parser = JobPostingParser(api_key="your-api-key")
urls = ["https://job1.com", "https://job2.com", "https://job3.com"]

for url in urls:
    try:
        job_data, md_path, json_path = parser.parse(
            url, 
            save_markdown=True, 
            save_json=True
        )
        print(f"✅ {job_data.title} at {job_data.company}")
    except Exception as e:
        print(f"❌ Failed to parse {url}: {e}")
```

## Configuration

### Environment Variables

Create a `.env` file in your project root:

```bash
# Required
OPENAI_API_KEY=your-openai-api-key

# Optional - Logging
LOGFIRE_TOKEN=your-logfire-token

# Optional - Model Configuration
OPENAI_MODEL=gpt-4-turbo-preview

# Optional - Playwright Settings
PLAYWRIGHT_HEADLESS=true
PLAYWRIGHT_TIMEOUT=60000
```

### API Key Setup

**Option 1: Parameter**
```python
parser = JobPostingParser(api_key="your-api-key")
```

**Option 2: Environment Variable**
```bash
export OPENAI_API_KEY="your-api-key"
```
```python
parser = JobPostingParser()  # Auto-loads from env
```

### Model Selection

```python
# Use different OpenAI model
parser = JobPostingParser(
    api_key="your-api-key", 
    model="gpt-4o"  # or gpt-3.5-turbo, etc.
)
```

### File Storage

Files are saved with SHA-1 hash filenames to prevent duplicates:

```
data/
├── markdown/
│   └── a1b2c3d4e5f6789.md
└── json/
    └── a1b2c3d4e5f6789.json
```

## Data Model

The parser extracts comprehensive job information:

**Core Information**
- Title, company, location, description
- Work type (full-time, part-time, contract)
- Work mode (remote, hybrid, on-site)
- Experience level required

**Compensation & Benefits**
- Salary range with currency
- Benefits and perks
- Stock options, bonuses

**Skills & Requirements**
- Required technical skills
- Preferred/nice-to-have skills
- Education requirements
- Years of experience needed

**Additional Details**
- Team size and department
- Application process
- Company culture information

## Error Handling

The parser includes robust error handling:

```python
from data_job_parser import JobPostingParser
from data_job_parser.exceptions import ParsingError, ScrapingError

parser = JobPostingParser(api_key="your-api-key")

try:
    job_data = parser.parse("https://example.com/job")
except ScrapingError as e:
    print(f"Failed to scrape URL: {e}")
except ParsingError as e:
    print(f"Failed to parse content: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/mazzasaverio/data-job-parser.git
cd data-job-parser

# Install with uv (recommended)
uv sync --dev

# Or with pip
pip install -e ".[dev]"
```

### Run Tests

```bash
# Run all tests
uv run pytest

# With coverage report
uv run pytest --cov=src/data_job_parser --cov-report=html

# Run specific test file
uv run pytest tests/test_parser.py -v
```

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy src/
```

### Release Process

1. **Update version** in both files:
   - `src/data_job_parser/__init__.py`
   - `pyproject.toml`

2. **Run quality checks**:
   ```bash
   uv run pytest
   uv run ruff check .
   uv run mypy src/
   ```

3. **Commit and tag**:
   ```bash
   git add .
   git commit -m "chore: bump version to X.Y.Z"
   git push origin main
   
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

4. **Automated deployment**: GitHub Actions will automatically:
   - Run tests
   - Build package  
   - Publish to PyPI
   - Create GitHub release

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes with tests
4. **Run** quality checks: `uv run pytest && uv run ruff check .`
5. **Commit** changes: `git commit -m 'feat: add amazing feature'`
6. **Push** branch: `git push origin feature/amazing-feature`
7. **Open** a Pull Request

### Development Guidelines

- Write tests for new features
- Follow existing code style
- Update documentation as needed
- Use conventional commit messages

## Requirements

- **Python**: 3.8+
- **OpenAI API Key**: Required for parsing
- **Internet Connection**: For web scraping and API calls

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenAI** for structured output capabilities
- **Playwright** for robust web scraping
- **Pydantic** for data validation
- **Logfire** for observability

---

**Made with ❤️ by [Saverio Mazza](https://github.com/mazzasaverio)**