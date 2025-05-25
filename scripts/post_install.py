#!/usr/bin/env python
"""Post-installation script to install Playwright browsers"""

import subprocess
import sys


def install_playwright_browsers():
    """Install Playwright Chromium browser"""
    print("Installing Playwright browsers...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "playwright", "install", "chromium"]
        )
        print("✅ Playwright browsers installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Playwright browsers: {e}")
        print("\nPlease run manually: playwright install chromium")
        sys.exit(1)


if __name__ == "__main__":
    install_playwright_browsers()
