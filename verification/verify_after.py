from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Load the local HTML file
        page.goto(f"file://{os.path.abspath('ApportionmentCalc.html')}")

        # Check if the live total element exists
        live_total = page.locator("#liveTotal")
        print(f"Live total visible: {live_total.is_visible()}")

        # Check initial value (should match initial parties sum)
        # Initial parties: 25000 + 15000 + 9000 + 5000 + 1500 = 55500
        expect_text = "Votes: 55,500"
        print(f"Initial text: '{live_total.inner_text()}'")
        if expect_text not in live_total.inner_text():
             print(f"FAIL: Expected '{expect_text}' but got '{live_total.inner_text()}'")

        # Modify a vote
        first_vote_input = page.locator(".party-row input[type=number]").first
        first_vote_input.fill("30000")

        # Check updated value
        # 30000 + 15000 + 9000 + 5000 + 1500 = 60500
        expect_text_updated = "Votes: 60,500"
        print(f"Updated text: '{live_total.inner_text()}'")
        if expect_text_updated not in live_total.inner_text():
             print(f"FAIL: Expected '{expect_text_updated}' but got '{live_total.inner_text()}'")

        # Take a screenshot
        page.locator(".container").screenshot(path="verification/after.png")
        browser.close()

if __name__ == "__main__":
    run()
