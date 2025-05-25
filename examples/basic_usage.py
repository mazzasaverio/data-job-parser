import os

import logfire

from data_job_parser import JobPostingParser


def main():
    # Configure Logfire for detailed logging
    logfire.configure()

    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment var")
        return

    # Example job posting URL
    job_url = "https://www.helloprima.com/it/carriere/offerte-lavoro/senior-data-engineer-1211d8cc-cda2-4a65-9743-cab60f83a8b1"

    # Initialize parser (headless=False to see browser in action)
    parser = JobPostingParser(api_key=api_key, headless=True)

    try:
        # Parse the job posting and save both markdown and JSON
        job, markdown_path, json_path = parser.parse(
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


def parse_multiple_jobs():
    """Example of parsing multiple job postings"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        return

    job_urls = [
        "https://example.com/job1",
        "https://example.com/job2",
        "https://example.com/job3",
    ]

    parser = JobPostingParser(api_key=api_key)

    for url in job_urls:
        try:
            job, filepath = parser.parse(url, save_markdown=True)
            print(f"✅ Parsed: {job.title} at {job.company}")
            print(f"   Saved to: {filepath}")
        except Exception as e:
            print(f"❌ Failed to parse {url}: {e}")


def demonstrate_filename_generation():
    """Show how URLs are converted to SHA-1 filenames"""
    from job_posting_parser.scraper import JobPostingScraper

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
    main()

    # Demonstrate filename generation
    demonstrate_filename_generation()

    # Uncomment to parse multiple jobs
    # parse_multiple_jobs()
