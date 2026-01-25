import os
import sys
from playwright.sync_api import sync_playwright

def verify_live_stats():
    # Get absolute path to the HTML file
    repo_root = os.getcwd()
    file_path = os.path.join(repo_root, 'ApportionmentCalc.html')
    url = f'file://{file_path}'

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Wait for the app to load
        page.wait_for_selector('h1')
        print("Page loaded.")

        # Interact with inputs to set known values.
        inputs = page.locator('.party-row input[type="number"]')
        count = inputs.count()
        print(f"Found {count} party inputs.")

        # Set all to 0 to start clean
        for i in range(count):
            inputs.nth(i).fill('0')

        # Set first to 100
        inputs.nth(0).fill('100')

        # Set second to 300
        inputs.nth(1).fill('300')

        # Total = 400.
        # Party 1: 100/400 = 25%.
        # Party 2: 300/400 = 75%.

        # Check spans
        spans = page.locator('.party-share')

        share1 = spans.nth(0).text_content()
        share2 = spans.nth(1).text_content()

        print(f"Share 1: {share1}")
        print(f"Share 2: {share2}")

        # Check for expected values
        # We check simply for the number and %, allowing for potential formatting differences
        assert "25" in share1 and "%" in share1
        assert "75" in share2 and "%" in share2

        # Test updating live
        inputs.nth(0).fill('200')
        # Total = 500.
        # Party 1: 200/500 = 40%.
        # Party 2: 300/500 = 60%.

        share1 = spans.nth(0).text_content()
        share2 = spans.nth(1).text_content()

        print(f"Updated Share 1: {share1}")
        print(f"Updated Share 2: {share2}")

        assert "40" in share1 and "%" in share1
        assert "60" in share2 and "%" in share2

        # Test Total = 0
        inputs.nth(0).fill('0')
        inputs.nth(1).fill('0')

        share1 = spans.nth(0).text_content()

        print(f"Zero Total Share 1: {share1}")
        assert "0%" in share1

        print("Verification passed!")
        page.screenshot(path="verification/live_stats.png", full_page=True)
        print("Screenshot saved to verification/live_stats.png")
        browser.close()

if __name__ == "__main__":
    verify_live_stats()
