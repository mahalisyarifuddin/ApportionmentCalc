from playwright.sync_api import sync_playwright

def verify_feature(page):
    page.goto("file:///app/ApportionmentCalc.html")
    page.wait_for_timeout(500)

    # Click Calculate
    page.locator("#calculate").click()
    page.wait_for_timeout(500)

    page.screenshot(path="/home/jules/verification/verification.png", full_page=True)
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="/home/jules/verification/video")
        page = context.new_page()
        try:
            verify_feature(page)
        finally:
            context.close()
            browser.close()
