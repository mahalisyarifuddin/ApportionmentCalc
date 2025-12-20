
const { test, expect, _electron: electron } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

test.describe('ApportionmentCalc UX', () => {
    test('should show toast on invalid seats input', async ({ page }) => {
        const filePath = path.resolve(__dirname, '../ApportionmentCalc.html');
        await page.goto(`file://${filePath}`);

        // Set seats to 0
        await page.fill('#seats', '0');

        // Note: We don't need dialog handler anymore as alert is replaced

        await page.click('#calculate');

        // Expect toast to be visible and contain message
        const toast = page.locator('#toast');
        await expect(toast).toBeVisible();
        await expect(toast).toHaveClass(/show/);
        await expect(toast).toContainText('Total seats must be at least 1');
    });
});
