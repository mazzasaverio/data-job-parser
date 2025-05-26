import os
import asyncio
import argparse
import logfire
from pathlib import Path

from data_job_parser import JobPostingParser, config


def get_job_url() -> str:
    """Get job URL from command line input."""
    parser = argparse.ArgumentParser(description="Parse a job posting URL")
    parser.add_argument("url", help="URL of the job posting to parse")
    args = parser.parse_args()
    return args.url


async def main():
    # Configure Logfire for detailed logging
    logfire.configure()

    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment var")
        return

    # Get job URL from command line
    job_url = get_job_url()

    # Initialize parser (headless=False to see browser in action)
    parser = JobPostingParser(api_key=api_key, headless=True)

    try:
        # Parse the job posting and save both markdown and JSON
        job, markdown_path, json_path = await parser.parse_async(
            job_url,
            save_markdown=True,
            save_json=True,
        )

        # Display results
        print(f"\n{'=' * 60}")
        print(f"Job Title: {job.title}")
        print(f"Company: {job.company}")
        print(f"{'=' * 60}\n")

        # Show where files were saved
        if markdown_path:
            print(f"📄 Markdown saved to: {markdown_path}")
            print(f"   (SHA-1 hash of URL: {os.path.basename(markdown_path)})\n")

        if json_path:
            print(f"📄 JSON saved to: {json_path}")
            print(f"   (SHA-1 hash of URL: {os.path.basename(json_path)})\n")

        # Location
        print("📍 Location:")
        print(f"  - City: {job.location.city}")
        print(f"  - Country: {job.location.country}")
        print(f"  - Remote: {'Yes' if job.location.is_remote else 'No'}")

        # Salary
        if job.salary:
            print("\n💰 Salary:")
            if job.salary.min_amount and job.salary.max_amount:
                print(
                    f"  - Range: {job.salary.min_amount:,.0f} - {job.salary.max_amount:,.0f} {job.salary.currency}"
                )
            print(f"  - Period: {job.salary.period}")

        # Skills
        if job.required_skills:
            print("\n🔧 Required Skills:")
            for skill in job.required_skills:
                print(f"  - {skill}")

        if job.preferred_skills:
            print("\n✨ Preferred Skills:")
            for skill in job.preferred_skills:
                print(f"  - {skill}")

        # Experience
        if job.experience_level:
            print(f"\n📊 Experience Level: {job.experience_level.value}")

        if job.years_of_experience:
            print(f"⏱️  Years of Experience: {job.years_of_experience}+")

        # Work details
        if job.work_type:
            print(f"\n💼 Work Type: {job.work_type.value}")

        if job.work_mode:
            print(f"🏢 Work Mode: {job.work_mode.value}")

    except Exception as e:
        print(f"❌ Error parsing job posting: {e}")
        logfire.error("Failed to parse job posting", error=str(e))


async def parse_multiple_jobs():
    """Example of parsing multiple job postings"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        return

    # Get job URLs from command line
    parser = argparse.ArgumentParser(description="Parse multiple job posting URLs")
    parser.add_argument("urls", nargs="+", help="List of job posting URLs to parse")
    args = parser.parse_args()
    job_urls = args.urls

    parser = JobPostingParser(api_key=api_key)

    for url in job_urls:
        try:
            job, markdown_path, json_path = await parser.parse_async(
                url, save_markdown=True, save_json=True
            )
            print(f"✅ Parsed: {job.title} at {job.company}")
            print(f"   Saved to: {markdown_path}")
        except Exception as e:
            print(f"❌ Failed to parse {url}: {e}")


def demonstrate_filename_generation():
    """Show how URLs are converted to SHA-1 filenames"""
    from data_job_parser.scraper import JobPostingScraper

    scraper = JobPostingScraper()

    test_urls = [
        "https://careers.google.com/jobs/results/12345",
        "https://www.linkedin.com/jobs/view/98765",
        "https://jobs.lever.co/company/position-id",
    ]

    print("\n📁 URL to Filename Mapping:")
    print("-" * 60)
    for url in test_urls:
        filename = scraper._generate_filename(url)
        print(f"URL: {url}")
        print(f"SHA-1 Filename: {filename}")
        print("-" * 60)


if __name__ == "__main__":
    # Run the main example
    asyncio.run(main())

    # Demonstrate filename generation
    demonstrate_filename_generation()

    # Uncomment to parse multiple jobs
    # asyncio.run(parse_multiple_jobs())
