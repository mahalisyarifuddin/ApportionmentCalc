
const { test, expect, _electron: electron } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

test.describe('ApportionmentCalc UX', () => {
    test('should show inline error on invalid seats input', async ({ page }) => {
        const filePath = path.resolve(__dirname, '../ApportionmentCalc.html');
        await page.goto(`file://${filePath}`);

        // Set seats to 0
        await page.fill('#seats', '0');

        await page.click('#calculate');

        // Expect error to be visible and contain message
        const error = page.locator('#error');
        await expect(error).toBeVisible();
        await expect(error).not.toHaveClass(/hidden/);
        await expect(error).toContainText('Total seats must be at least 1');
    });
});
