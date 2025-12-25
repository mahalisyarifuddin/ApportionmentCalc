from playwright.sync_api import sync_playwright

def verify_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{os.getcwd()}/ApportionmentCalc.html")

        # 1. Calculate to show results
        page.click('#calculate')

        # 2. Open modal
        page.click('#steps')

        # 3. Take screenshot of the open modal
        page.screenshot(path="/home/jules/verification/modal_visible.png")

        browser.close()

import os
if __name__ == "__main__":
    verify_frontend()
