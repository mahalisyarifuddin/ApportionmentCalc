from playwright.sync_api import sync_playwright
import os

def handle_dialog(dialog):
    dialog.accept()

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("dialog", handle_dialog)

        page.goto("file:///app/ApportionmentCalc.html")

        # Set Seats to 10
        page.fill("#seats", "10")

        # Set Threshold to 2.5
        page.fill("#threshold", "2.5")

        # Clear existing parties
        page.click("#clear")

        # Add Party A: 90
        page.fill(".party-row:nth-child(1) input[type=text]", "Party A")
        page.fill(".party-row:nth-child(1) input[type=number]", "90")

        # Add Party B: 2
        page.click("#add")
        page.fill(".party-row:nth-child(2) input[type=text]", "Party B")
        page.fill(".party-row:nth-child(2) input[type=number]", "2")

        # Calculate
        page.click("#calculate")

        # Screenshot
        page.screenshot(path="verification/after_fix.png", full_page=True)

        browser.close()
