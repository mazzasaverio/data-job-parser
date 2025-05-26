import asyncio
import hashlib
import os
from pathlib import Path
from typing import Optional, Tuple

import html2text
import logfire
from playwright.async_api import async_playwright

from .config import config


class JobPostingScraper:
    def __init__(self, headless: bool = True, timeout: int = 60000) -> None:
        self.headless = headless
        self.timeout = timeout
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False
        self.converter.body_width = 0

        if config.logfire_token:
            logfire.configure(token=config.logfire_token)
        else:
            logfire.configure()

    def _generate_filename(self, url: str) -> str:
        return hashlib.sha1(url.encode()).hexdigest() + ".md"

    async def _fetch_content_async(
        self, url: str, save_markdown: bool = False, output_dir: Optional[str] = None
    ) -> Tuple[str, Optional[str]]:
        with logfire.span("fetch_job_posting", url=url):
            try:
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=self.headless)
                    page = await browser.new_page()

                    await page.set_viewport_size({"width": 1280, "height": 720})
                    await page.goto(
                        url, wait_until="domcontentloaded", timeout=self.timeout
                    )

                    await asyncio.sleep(2)

                    title = await page.title()

                    # Try to use Readability.js to extract main content
                    readability_js = """
                    // Readability.js from https://github.com/mozilla/readability
                    // (minified version or CDN link)
                    """
                    await page.add_script_tag(content=readability_js)
                    main_content = await page.evaluate(
                        """
                        () => {
                            if (window.Readability) {
                                let article = new Readability(document).parse();
                                return article ? article.content : null;
                            }
                            return null;
                        }
                    """
                    )
                    if main_content:
                        markdown = self.converter.handle(main_content)
                    else:
                        # Fallback: try to get the largest <main>, <article>, or <section>
                        element = await page.query_selector("main, article, section")
                        if element:
                            content = await element.inner_html()
                            markdown = self.converter.handle(content)
                        else:
                            # Fallback: whole page
                            content = await page.content()
                            markdown = self.converter.handle(content)

                    await browser.close()

                    logfire.info(
                        "Successfully fetched content",
                        url=url,
                        title=title,
                        length=len(markdown),
                    )

                    filepath = None
                    if save_markdown:
                        filepath = self._save_markdown(url, markdown, output_dir)

                    return markdown, filepath

            except Exception as e:
                logfire.error("Error fetching content", url=url, error=str(e))
                raise

    def _save_markdown(
        self, url: str, content: str, output_dir: Optional[str] = None
    ) -> str:
        output_dir = output_dir or config.markdown_output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        filename = self._generate_filename(url)
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"<!-- URL: {url} -->\n")
            f.write(f"<!-- Filename: {filename} -->\n\n")
            f.write(content)

        logfire.info("Saved markdown", filepath=filepath, url=url)
        return filepath

    def fetch_content(
        self, url: str, save_markdown: bool = False, output_dir: Optional[str] = None
    ) -> Tuple[str, Optional[str]]:
        return asyncio.run(self._fetch_content_async(url, save_markdown, output_dir))
