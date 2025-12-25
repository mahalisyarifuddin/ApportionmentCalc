from playwright.sync_api import sync_playwright, expect
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/ApportionmentCalc.html")

        # Initial screenshot
        page.screenshot(path="verification/initial.png")

        # Wait for rows
        expect(page.locator('.party-row')).to_have_count(5)

        # Get last row input
        last_row = page.locator('.party-row').last
        input_name = last_row.locator('input').first
        input_name.fill('New Party')
        input_name.press('Enter')

        # Should add a new row
        expect(page.locator('.party-row')).to_have_count(6)

        # New row should be focused
        focused = page.evaluate('document.activeElement === document.querySelector(".party-row:last-child input")')
        if not focused:
            print("FAILURE: Focus is not on the last row input!")
        else:
            print("SUCCESS: Focus IS on the last row input.")

        # Test middle row navigation
        first_row = page.locator('.party-row').first
        first_input = first_row.locator('input').first
        first_input.focus()
        first_input.press('Enter')

        # Should focus second row input
        focused_second = page.evaluate('document.activeElement === document.querySelector(".party-row:nth-child(2) input")')
        if not focused_second:
             print("FAILURE: Focus did not move to second row!")
        else:
             print("SUCCESS: Focus moved to second row.")

        page.screenshot(path="verification/final.png")
        browser.close()

if __name__ == '__main__':
    run()
