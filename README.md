# Data Job Parser

[![PyPI Downloads](https://static.pepy.tech/badge/data-job-parser)](https://pepy.tech/projects/data-job-parser)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/data-job-parser)](https://pypi.org/project/data-job-parser/)

Extract structured data from job postings using OpenAI's structured output capabilities

## Features

- 🎯 Extract structured information from any job posting URL
- 🧠 Powered by OpenAI's GPT models with structured output
- 📊 Comprehensive data model covering all job posting aspects
- 🌐 Advanced web scraping with Playwright (handles JavaScript-heavy sites)
- 💾 Save job postings as markdown and JSON files with SHA-1 hash filenames
- 🔄 Automatic retries with exponential backoff
- 📝 Detailed logging with Logfire
- 🐍 Full type hints and Python 3.12+ support

## Installation

```bash
pip install data-job-parser
```

After installation, you need to install Playwright browsers:

```bash
playwright install chromium
```

## Quick Start

```python
from data_job_parser import JobPostingParser

# Initialize parser with your OpenAI API key
parser = JobPostingParser(api_key="your-openai-api-key")

# Parse a job posting
job, markdown_file, json_file = parser.parse("https://example.com/job-posting")

# Access structured data
print(f"Title: {job.title}")
print(f"Company: {job.company}")
print(f"Location: {job.location.city}, {job.location.country}")
print(f"Salary: {job.salary.min_amount}-{job.salary.max_amount} {job.salary.currency}")
print(f"Required Skills: {', '.join(job.required_skills)}")

# Parse and save both markdown and JSON
job, markdown_path, json_path = parser.parse(
    "https://example.com/job-posting",
    save_markdown=True,
    save_json=True
)
print(f"Markdown saved to: {markdown_path}")
print(f"JSON saved to: {json_path}")
```

### Batch Processing

```python
from data_job_parser import JobPostingParser

parser = JobPostingParser(api_key="your-api-key")

urls = ["url1", "url2", "url3"]

for url in urls:
    try:
        job, markdown_path, json_path = parser.parse(url, save_markdown=True, save_json=True)
        print(f"Parsed: {job.title} at {job.company}")
        print(f"Files saved: {markdown_path}, {json_path}")
    except Exception as e:
        print(f"Failed to parse {url}: {e}")
```

## Configuration

### Environment Variables

Create a `.env` file in your project root (see `.env.example` for reference):

```bash
# Required
OPENAI_API_KEY=your-openai-api-key

# Optional
LOGFIRE_TOKEN=your-logfire-token
OPENAI_MODEL=gpt-4-turbo-preview
PLAYWRIGHT_HEADLESS=true
PLAYWRIGHT_TIMEOUT=60000
```

### API Key

You can provide your OpenAI API key in two ways:

1. **As a parameter:**
   ```python
   parser = JobPostingParser(api_key="your-api-key")
   ```

2. **As an environment variable:**
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```

### Model Selection

By default, the parser uses `gpt-4-turbo-preview`. You can specify a different model:

```python
parser = JobPostingParser(api_key="your-api-key", model="gpt-4")
```

### File Storage

By default, files are saved in a `data` directory with the following structure:

```
data/
├── markdown/
│   └── <sha1-hash>.md
└── json/
    └── <sha1-hash>.json
```

Example:
```python
# URL: https://example.com/job-123
# Saved as: 
# - data/markdown/a1b2c3d4e5f6.md
# - data/json/a1b2c3d4e5f6.json
```

## Data Model

The parser extracts the following information:

- **Basic Information**: title, company, location, description
- **Job Details**: experience level, work type, work mode
- **Compensation**: salary range with currency
- **Skills**: required and preferred skills
- **Requirements**: responsibilities, requirements, education
- **Benefits**: benefits and perks
- **Additional Info**: team size, department, application details

## Logging

The package uses Logfire for structured logging. Logs include:
- URL fetching status
- Content extraction progress
- OpenAI API calls
- Errors and warnings

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/mazzasaverio/data-job-parser.git
cd data-job-parser

# Install with dev dependencies
uv sync
```

### Testing

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov
```

### Code Quality

```bash
# Format code
uv run black src tests
uv run isort src tests

# Lint
uv run ruff check src tests

# Type check
uv run mypy src
```

### Publishing a New Version

To publish a new version of the package, follow these steps:

1. **Run Tests and Quality Checks**
   ```bash
   # Run all tests
   uv run pytest
   
   # Run code quality checks
   uv run black src tests
   uv run isort src tests
   uv run ruff check src tests
   uv run mypy src
   ```

2. **Update Version Numbers**
   - Update version in `src/data_job_parser/__init__.py`:
     ```python
     __version__ = "X.Y.Z"  # Replace with new version
     ```
   - Update version in `pyproject.toml`:
     ```toml
     [project]
     version = "X.Y.Z"  # Replace with new version
     ```

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "chore: update version to X.Y.Z"
   ```

4. **Create and Push Tag**
   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

5. **Push Changes to Master**
   ```bash
   git push origin master
   ```

The GitHub workflow will automatically:
- Run tests
- Build the package
- Publish to PyPI
- Create a GitHub release

### Adding Dependencies

```bash
# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name
```

### Updating Dependencies

```bash
# Update all dependencies
uv sync --upgrade

# Update specific package
uv add package-name --upgrade
```

## Versioning

This project follows [Semantic Versioning](https://semver.org/). For the versions available, see the [tags on this repository](https://github.com/mazzasaverio/data-job-parser/tags).

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
MIT License - see LICENSE file for details.
