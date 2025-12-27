import os
from playwright.sync_api import sync_playwright

def verify():
    file_path = os.path.abspath("ApportionmentCalc.html")
    url = f"file://{file_path}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Click calculate
        page.click("#calculate")

        # Check if chart exists
        chart_count = page.locator("#chart").count()
        print(f"Chart container count: {chart_count}")

        # Check if chart rows exist (should be at least 1 since we have default parties)
        rows_count = page.locator(".chart-row").count()
        print(f"Chart row count: {rows_count}")

        browser.close()

if __name__ == "__main__":
    verify()
