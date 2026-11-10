import { test, expect, Locator, Page } from '@playwright/test';

const email = process.env.STUDYHUB_EMAIL;
const password = process.env.STUDYHUB_PASSWORD;

async function signIn(page: Page) {
  test.skip(!email || !password, 'STUDYHUB_EMAIL and STUDYHUB_PASSWORD are required');

  await page.goto('/users/login/');
  await page.getByLabel('Email address').fill(email!);
  await page.getByLabel('Password').fill(password!);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page).not.toHaveURL(/\/users\/login\//);
}

async function itemWithQuickComplete(
  page: Page,
  view: 'cards' | 'list',
  status: 'New' | 'In Progress',
): Promise<{ item: Locator; title: string }> {
  const container = page.locator(
    view === 'cards' ? '#view-cards-container > div' : '#view-list-container article',
  );
  const item = container
    .filter({ hasText: status })
    .filter({ has: page.getByRole('button', { name: 'Quick Complete' }) })
    .first();

  if (await item.count() === 0) {
    test.skip(true, `No ${status} content is available in ${view} view`);
  }

  const titleLink = view === 'cards' ? item.locator('h3 a') : item.locator('h2 a');
  return { item, title: await titleLink.innerText() };
}

test.describe('SH-208: Quick Complete from content listing', () => {
  test('quick completes New content in Card View, persists status, hides it by default, and preserves context', async ({ page }) => {
    await signIn(page);
    const context = '/contents/?sort=title&show_completed=0';
    await page.goto(context);

    const { item, title } = await itemWithQuickComplete(page, 'cards', 'New');
    const form = item.locator('form').filter({ has: page.getByRole('button', { name: 'Quick Complete' }) });
    await expect(form).toHaveAttribute('method', /post/i);
    await expect(form.locator('input[name="csrfmiddlewaretoken"]')).toHaveCount(1);

    await form.getByRole('button', { name: 'Quick Complete' }).click();
    await expect(page).toHaveURL(context);
    await expect(page.getByText('Status updated to Completed.')).toBeVisible();

    await page.reload();
    await expect(page.getByText(title, { exact: true })).toHaveCount(0);

    await page.goto('/contents/?sort=title&show_completed=1');
    const completed = page.locator('#view-cards-container > div').filter({ hasText: title });
    await expect(completed).toContainText('Completed');
    await expect(completed.getByRole('button', { name: 'Quick Complete' })).toHaveCount(0);
  });

  test('quick completes In Progress content in List View and keeps it visible when Show Completed is active', async ({ page }) => {
    await signIn(page);
    await page.goto('/contents/?sort=title&show_completed=1');
    await page.getByRole('button', { name: 'List view' }).click();

    const { item, title } = await itemWithQuickComplete(page, 'list', 'In Progress');
    const form = item.locator('form').filter({ has: page.getByRole('button', { name: 'Quick Complete' }) });
    await form.getByRole('button', { name: 'Quick Complete' }).click();

    await expect(page).toHaveURL(/\/contents\/\?sort=title&show_completed=1/);
    await page.reload();
    const completed = page.locator('#view-list-container article').filter({ hasText: title });
    await expect(completed).toContainText('Completed');
    await expect(completed.getByRole('button', { name: 'Quick Complete' })).toHaveCount(0);
  });

  test('preserves pagination context when completing an item on the last listing page', async ({ page }) => {
    await signIn(page);
    await page.goto('/contents/?show_completed=1');
    const lastPage = page.locator('a[href*="page="]').last();
    test.skip(await lastPage.count() === 0, 'The account has no paginated listing');
    const lastPageUrl = await lastPage.getAttribute('href');
    await lastPage.click();

    const eligibleItems = page.locator('#view-cards-container > div').filter({
      has: page.getByRole('button', { name: 'Quick Complete' }),
    });
    test.skip(await eligibleItems.count() === 0, 'No New or In Progress content is available on the last page');

    const item = eligibleItems.first();
    const title = await item.locator('h3 a').innerText();
    await item.getByRole('button', { name: 'Quick Complete' }).click();
    await expect(page).toHaveURL(new RegExp(`${lastPageUrl!.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`));
    await page.reload();

    const completed = page.locator('#view-cards-container > div').filter({ hasText: title });
    await expect(completed).toContainText('Completed');
    await expect(completed.getByRole('button', { name: 'Quick Complete' })).toHaveCount(0);
  });
});
