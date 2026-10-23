import { test, expect } from '@playwright/test';

const email = process.env.STUDYHUB_EMAIL;
const password = process.env.STUDYHUB_PASSWORD;

test('FR-22: content view can toggle and persists after reload', async ({ page }) => {
  test.skip(!email || !password, 'STUDYHUB_EMAIL and STUDYHUB_PASSWORD are required');

  await page.goto('/users/login/');
  await page.getByLabel('Email address').fill(email!);
  await page.getByLabel('Password').fill(password!);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page).not.toHaveURL(/\/users\/login\//);

  await page.evaluate(() => localStorage.removeItem('studyhub_content_view'));
  await page.goto('/contents/');

  const listViewButton = page.getByRole('button', { name: 'List view' });
  const cardsContainer = page.locator('#view-cards-container');
  const listContainer = page.locator('#view-list-container');

  await expect(cardsContainer).toBeVisible();
  await expect(listContainer).toBeHidden();

  await listViewButton.click();
  await expect(cardsContainer).toBeHidden();
  await expect(listContainer).toBeVisible();
  await expect.poll(() => page.evaluate(() => localStorage.getItem('studyhub_content_view'))).toBe('list');

  await page.reload();
  await expect(cardsContainer).toBeHidden();
  await expect(listContainer).toBeVisible();
});
