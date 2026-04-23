import { test, expect } from '@playwright/test';

test.describe('Print Design — Auth + landing (P0) @smoke', () => {
  test('authenticated session reaches /desk', async ({ page }) => {
    await page.goto('/desk');
    await expect(page).toHaveURL(/\/desk/);
    await expect(page).not.toHaveURL(/\/login/);
  });

  test('Print Design workspace loads', async ({ page }) => {
    await page.goto('/desk/print-design');
    await expect(page).toHaveURL(/\/desk\/print-design/);
  });

  test('Print Template JP list loads', async ({ page }) => {
    await page.goto('/desk/print-template-jp');
    await expect(page).toHaveURL(/\/desk\/print-template-jp/);
  });
});
