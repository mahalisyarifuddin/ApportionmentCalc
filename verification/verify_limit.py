from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the local HTML file
        page.goto(f"file://{os.path.abspath('ApportionmentCalc.html')}")

        # Set a large number of seats
        page.fill('#seats', '3000')

        # Calculate
        page.click('#calculate')

        # Open steps modal
        page.click('#steps')

        # Wait for modal to appear
        page.wait_for_selector('#modalSteps')

        # Take screenshot of the modal to verify warning message and truncation
        page.screenshot(path="verification/steps_modal.png")

        # Verify that summary warning is present
        content = page.content()
        if "Showing first 1000 rounds only." in content:
            print("Verified: Summary limited warning found.")
        else:
            print("FAILED: Summary limited warning NOT found.")

        browser.close()

if __name__ == '__main__':
    run()
