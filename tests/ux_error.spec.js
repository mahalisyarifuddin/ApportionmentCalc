
const { test, expect, _electron: electron } = require('@playwright/test');
const path = require('path');

test.describe('ApportionmentCalc UX', () => {
    test.beforeEach(async ({ page }) => {
        const filePath = path.resolve(__dirname, '../ApportionmentCalc.html');
        await page.goto(`file://${filePath}`);
    });

    test('should show inline error and dim button on invalid seats input', async ({ page }) => {
        // Set seats to 0
        await page.fill('#seats', '0');
        await page.click('#calculate');

        // Expect error to be visible
        const error = page.locator('#error');
        await expect(error).toBeVisible();
        await expect(error).toContainText('Total seats must be at least 1');

        // Expect button to be dimmed
        const button = page.locator('#calculate');
        await expect(button).toHaveClass(/dimmed/);
        await expect(button).toHaveCSS('opacity', '0.5');
        await expect(button).toHaveCSS('pointer-events', 'none');
    });

    test('should clear error and undim button on input change', async ({ page }) => {
        // Trigger error
        await page.fill('#seats', '0');
        await page.click('#calculate');

        const error = page.locator('#error');
        const button = page.locator('#calculate');

        await expect(error).toBeVisible();
        await expect(button).toHaveClass(/dimmed/);

        // Change input
        await page.fill('#seats', '10');

        // Expect error to be hidden and button active
        await expect(error).toHaveClass(/hidden/);
        await expect(button).not.toHaveClass(/dimmed/);
    });
});
