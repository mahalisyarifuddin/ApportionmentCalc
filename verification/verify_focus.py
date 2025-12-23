from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the local HTML file
        # We need absolute path
        cwd = os.getcwd()
        path = f"file://{cwd}/ApportionmentCalc.html"
        page.goto(path)

        # Test 1: Add Party and check focus
        # Initial parties count = 5
        expect_count = 5
        page.wait_for_selector(".party-row")
        rows = page.locator(".party-row")
        print(f"Initial rows: {rows.count()}")

        # Click Add Party
        page.click("#add")

        # Verify new row
        expect_count += 1
        print(f"Rows after add: {rows.count()}")
        if rows.count() != expect_count:
            print("FAIL: Row count mismatch after add")

        # Verify focus is on the new input
        # The last row is the new one
        last_row = rows.nth(expect_count - 1)
        focused = page.evaluate("document.activeElement === document.querySelector(\".party-row:last-child input[type=text]\")")
        print(f"Focus on new input: {focused}")

        # Type something to ensure we are focused
        if focused:
            page.keyboard.type("New Party")
            # Verify value
            val = last_row.locator("input[type=text]").input_value()
            print(f"Typed value: {val}")

        # Test 2: Remove Party and check focus
        # Let us remove the second to last party (index 4 out of 6)
        # 0: Apple, 1: Banana, 2: Cherry, 3: Date, 4: Elderberry, 5: New Party

        # Remove Elderberry (id 5, index 4)
        # Focus should go to index 4 (New Party)?
        # Wait, if I remove index 4. The item at index 5 moves to index 4.
        # So I should focus item at index 4 (New Party).

        # Let us remove "New Party" (last one, index 5)
        # Focus should go to index 4 (Elderberry).

        # First, click delete on last row
        last_row_btn = last_row.locator(".danger")
        last_row_btn.click()

        # Verify count
        expect_count -= 1
        print(f"Rows after remove: {rows.count()}")

        # Verify focus is on the new last row (Elderberry) delete button
        # Elderberry is now at index 4 (last)
        # Focus should be on its delete button
        focused_del = page.evaluate("document.activeElement === document.querySelector(\".party-row:last-child .danger\")")
        print(f"Focus on last row delete button: {focused_del}")

        # Test 3: Remove first party and check focus
        # Remove Apple (index 0)
        # Banana moves to index 0.
        # Focus should be on Banana delete button.

        first_row_btn = rows.nth(0).locator(".danger")
        first_row_btn.click()

        expect_count -= 1

        # Verify focus on new first row (Banana)
        focused_del_first = page.evaluate("document.activeElement === document.querySelector(\".party-row:first-child .danger\")")
        print(f"Focus on first row delete button: {focused_del_first}")

        page.screenshot(path="verification/focus_test.png")
        browser.close()

if __name__ == "__main__":
    run()
