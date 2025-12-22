const { chromium } = require('playwright');
const path = require('path');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    const filePath = path.resolve(__dirname, '../ApportionmentCalc.html');
    await page.goto(`file://${filePath}`);

    // Wait for the app to load
    await page.waitForSelector('.party-row');

    // Get initial count
    const initialCount = await page.locator('.party-row').count();
    console.log(`Initial rows: ${initialCount}`);

    // Focus the last input (Votes)
    const lastVoteInput = page.locator('.party-row').last().locator('input[type="number"]');
    await lastVoteInput.click();
    await lastVoteInput.press('Enter');

    // Wait for the new row to appear (wait for count to increase)
    await page.waitForFunction((initial) => {
        return document.querySelectorAll('.party-row').length > initial;
    }, initialCount);

    const newCount = await page.locator('.party-row').count();
    console.log(`New rows: ${newCount}`);

    // Focus the new row's NAME input (first column) to show focus state in screenshot
    // Since we pressed Enter on Votes (index 1), logic now dictates it goes to Name (index 0).
    const newNameInput = page.locator('.party-row').last().locator('input[type="text"]');

    // Check if it's focused automatically (which it should be)
    const isFocused = await newNameInput.evaluate(el => document.activeElement === el);
    console.log(`Is new Name input focused? ${isFocused}`);

    // Take screenshot
    await page.screenshot({ path: 'verification/verification_return.png', fullPage: true });

    await browser.close();
})();
