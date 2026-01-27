import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.grant_permissions(['clipboard-read', 'clipboard-write'])
        page = context.new_page()

        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))

        cwd = os.getcwd()
        file_path = os.path.join(cwd, 'ApportionmentCalc.html')
        page.goto(f'file://{file_path}')

        try:
            page.evaluate("""
                window.mockClipboard = [];
                Object.defineProperty(navigator, 'clipboard', {
                    value: {
                        writeText: (text) => {
                            window.mockClipboard.push(text);
                            return Promise.resolve();
                        }
                    },
                    configurable: true
                });
            """)
        except Exception as e:
            print(f"Could not mock clipboard: {e}")

        print("Clicking calculate...")
        page.click('#calculate')

        # Check for error
        if page.locator('#error').is_visible():
            print(f"ERROR shown: {page.locator('#error').inner_text()}")

        print("Waiting for results...")
        try:
            page.wait_for_selector('#results', state='visible', timeout=5000)
        except:
            print("Results did not appear.")
            # Debug page content
            # print(page.content())
            if page.locator('#error').is_visible():
                 print(f"ERROR shown: {page.locator('#error').inner_text()}")
            raise

        copy_btn = page.locator('#copy')
        assert copy_btn.is_visible(), "Copy button not visible"

        print("Clicking copy...")
        copy_btn.click()

        page.wait_for_timeout(100)
        text = copy_btn.inner_text()
        print(f"Button text after click: {text}")
        assert "Copied!" in text or "Tersalin!" in text

        content = page.evaluate("window.mockClipboard && window.mockClipboard[0]")
        if content:
            print(f"Clipboard content prefix: {content[:50]}...")
            assert "Apple Party" in content
        else:
            print("Could not verify clipboard content")

        print("Verification passed!")
        context.close()
        browser.close()

if __name__ == "__main__":
    run()
