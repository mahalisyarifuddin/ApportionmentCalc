
from playwright.sync_api import sync_playwright

def verify(page):
    # Load the local HTML file
    import os
    file_path = os.path.abspath("ApportionmentCalc.html")
    page.goto(f"file://{file_path}")

    # Check if title exists
    assert page.title() == "ApportionmentCalc"

    # Check if we can add a party
    page.click("#add")

    # Take a screenshot
    page.screenshot(path="verification/screenshot.png")
    print("Screenshot saved to verification/screenshot.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        verify(page)
        browser.close()
