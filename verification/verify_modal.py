import os
from playwright.sync_api import sync_playwright

def test_modal():
    cwd = os.getcwd()
    file_path = f"file://{cwd}/ApportionmentCalc.html"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(file_path)

        # 1. Calculate to enable steps button
        page.click('#calculate')

        # Check that results are shown
        assert page.is_visible('#results')

        # Check modal is hidden initially
        assert 'hidden' in page.locator('#modal').get_attribute('class').split()

        # 2. Open modal via click
        # We focus first to test the focus return functionality
        page.focus('#steps')
        page.click('#steps')

        # 3. Verify modal is visible
        assert page.is_visible('#modal')
        assert 'hidden' not in page.locator('#modal').get_attribute('class').split()

        # 4. Verify focus is on close button
        is_close_focused = page.evaluate("document.activeElement === document.getElementById('close')")
        assert is_close_focused, "Focus should be on close button"

        # 5. Close modal
        page.click('#close')

        # 6. Verify modal is hidden
        assert not page.is_visible('#modal')
        assert 'hidden' in page.locator('#modal').get_attribute('class').split()

        # 7. Verify focus returns to steps button
        is_steps_focused = page.evaluate("document.activeElement === document.getElementById('steps')")
        assert is_steps_focused, "Focus should return to steps button"

        print("Modal test passed!")
        browser.close()

if __name__ == "__main__":
    test_modal()
