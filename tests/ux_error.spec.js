
const { test, expect, _electron: electron } = require('@playwright/test');
const path = require('path');

test.describe('ApportionmentCalc UX', () => {
    test.beforeEach(async ({ page }) => {
        const filePath = path.resolve(__dirname, '../ApportionmentCalc.html');
        await page.goto(`file://${filePath}`);
    });

    test('should show inline error and dim button on invalid seats input', async ({ page }) => {
        await page.fill('#seats', '0');
        await page.click('#calculate');

        const error = page.locator('#error');
        await expect(error).toBeVisible();
        await expect(error).toContainText('Total seats must be at least 1');

        const button = page.locator('#calculate');
        await expect(button).toBeDisabled();
        await expect(button).toHaveCSS('opacity', '0.6');
    });

    test('should clear error and undim button on input change', async ({ page }) => {
        await page.fill('#seats', '0');
        await page.click('#calculate');

        const error = page.locator('#error');
        const button = page.locator('#calculate');

        await expect(error).toBeVisible();
        await expect(button).toBeDisabled();

        await page.fill('#seats', '10');

        await expect(error).toHaveClass(/hidden/);
        await expect(button).toBeEnabled();
    });
});
