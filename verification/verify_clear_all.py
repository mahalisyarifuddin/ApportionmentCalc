import os
from playwright.sync_api import sync_playwright

def verify():
    file_path = os.path.abspath("ApportionmentCalc.html")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{file_path}")

        # Check title
        assert "ApportionmentCalc" in page.title()

        # Check initial parties exist
        parties = page.locator(".party-row")
        print(f"Initial parties: {parties.count()}")
        assert parties.count() > 0

        # Take screenshot of initial state
        page.screenshot(path="verification/before_clear.png")

        # Click Clear All and accept dialog
        page.on("dialog", lambda dialog: dialog.accept())
        page.click("#clear")

        # Should have 1 party (empty)
        assert parties.count() == 1

        # Take screenshot of cleared state
        page.screenshot(path="verification/after_clear.png")

        print("Verification with Clear All passed")
        browser.close()

if __name__ == "__main__":
    verify()
