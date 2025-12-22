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

    // Focus the last input
    const lastVoteInput = page.locator('.party-row').last().locator('input[type="number"]');
    await lastVoteInput.click();
    await lastVoteInput.press('Enter');

    // Wait for the new row to appear (wait for count to increase)
    await page.waitForFunction((initial) => {
        return document.querySelectorAll('.party-row').length > initial;
    }, initialCount);

    const newCount = await page.locator('.party-row').count();
    console.log(`New rows: ${newCount}`);

    // Focus the new row's name input to show focus state in screenshot
    const newNameInput = page.locator('.party-row').last().locator('input[type="text"]');
    await newNameInput.focus();

    // Take screenshot
    await page.screenshot({ path: 'verification/verification.png', fullPage: true });

    await browser.close();
})();
