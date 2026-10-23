import { test, expect } from '@playwright/test';

test('landing page exposes the main authentication actions', async ({ page }) => {
  await page.goto('/');

  const navigation = page.getByRole('navigation', { name: 'Site navigation' });

  await expect(
    navigation.getByRole('link', { name: 'Get Started', exact: true })
  ).toBeVisible();

  await expect(
    navigation.getByRole('link', { name: 'Log in', exact: true })
  ).toBeVisible();
});
