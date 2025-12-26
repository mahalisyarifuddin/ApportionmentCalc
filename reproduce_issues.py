import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Load local file
        page.goto(f"file://{os.getcwd()}/ApportionmentCalc.html")

        # Test 1: Negative Votes
        print("Test 1: Negative Votes")

        # Handle clear confirm
        page.once("dialog", lambda dialog: dialog.accept())
        page.click("#clear")

        # Add Party
        # clearAll adds one party automatically

        # Fill name and negative votes
        page.fill(".party-row:first-child input[type='text']", "Party A")
        page.fill(".party-row:first-child input[type='number']", "-10")

        # Calculate
        page.click("#calculate")

        # Check error
        error = page.locator("#error")
        if error.is_visible():
            print(f"Error shown: {error.text_content()}")
        else:
            print("No error shown")

        results = page.locator("#results")
        print(f"Results visible: {results.is_visible()}")

        # Test 2: CSV Import with Newlines
        print("\nTest 2: CSV Import with Newlines")

        # Reload to reset state
        page.reload()

        csv_content = 'Party,Votes\n"Party\nA",100\nParty B,200'
        with open("test_newline.csv", "w") as f:
            f.write(csv_content)

        # Upload
        with page.expect_file_chooser() as fc_info:
            page.click("#import")
        file_chooser = fc_info.value
        file_chooser.set_files("test_newline.csv")

        # Check for error or parties
        time.sleep(0.5) # Wait for file reading

        party_inputs = page.locator(".party-row input[type='text']")
        count = party_inputs.count()
        print(f"Parties found: {count}")
        for i in range(count):
            print(f"Party {i+1}: {party_inputs.nth(i).input_value()}")

        browser.close()

if __name__ == "__main__":
    run()
