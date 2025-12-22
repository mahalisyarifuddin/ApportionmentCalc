from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Load the local HTML file
        page.goto(f"file://{os.path.abspath('ApportionmentCalc.html')}")

        # Check if the live total element exists (it should not)
        live_total = page.locator("#liveTotal")
        print(f"Live total visible: {live_total.is_visible()}")

        # Take a screenshot of the party list area
        page.locator(".container").screenshot(path="verification/before.png")
        browser.close()

if __name__ == "__main__":
    run()
