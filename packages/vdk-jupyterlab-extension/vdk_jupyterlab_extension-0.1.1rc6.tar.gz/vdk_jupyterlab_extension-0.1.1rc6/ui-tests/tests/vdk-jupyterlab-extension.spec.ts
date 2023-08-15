/*
 * Copyright 2021-2023 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

import { expect, test } from '@jupyterlab/galata';

/**
 * Don't load JupyterLab webpage before running the tests.
 * This is required to ensure we capture all log messages.
 */
test.use({ autoGoto: false });

test('should open run job pop up and then cancel the operation', async ({
  page
}) => {
  await page.goto('');
  await page.menu.open('VDK');
  await page.locator('#jp-vdk-menu').getByText('Run').click();
  await page.locator('div').filter({ hasText: 'Run Job' });
  await page.getByRole('button', { name: 'Cancel' }).click();
});

test('should try to run a job with empty input and get error', async ({
  page
}) => {
  await page.goto('');
  await page.menu.open('VDK');
  await page.locator('#jp-vdk-menu').getByText('Run').click();
  await page.locator('div').filter({ hasText: 'Run Job' });
  await page.getByRole('button', { name: 'OK' }).click();
  await page
    .locator('div')
    .filter({ hasText: 'Encountered an error when trying to run the job.' });
  await page.getByRole('button', { name: 'OK' }).click();
});

test('should try to run a job with incorrect data and get a dialog error message', async ({
  page
}) => {
  await page.goto('');
  await page.menu.open('VDK');
  await page.locator('#jp-vdk-menu').getByText('Run').click();
  await page.getByLabel('Path to job directory:').click();
  await page.getByLabel('Path to job directory:').fill('/my-folder');
  await page.getByRole('button', { name: 'OK' }).click();
  page.once('dialog', async dialog => {
    console.log(`Dialog message: ${dialog.message()}`);
    dialog.dismiss().catch(() => {});
  });
});

test('should open create job pop up and then cancel the operation', async ({
  page
}) => {
  await page.goto('');
  await page.menu.open('VDK');
  await page.locator('#jp-vdk-menu').getByText('Create').click();
  await page.locator('div').filter({ hasText: 'Create Job' });
  await page.getByRole('button', { name: 'Cancel' }).click();
});

test('should try to create a job with empty input and get error', async ({
  page
}) => {
  await page.goto('');
  await page.menu.open('VDK');
  await page.locator('#jp-vdk-menu').getByText('Create').click();
  await page.locator('div').filter({ hasText: 'Run Job' });
  await page.getByRole('button', { name: 'OK' }).click();
  await page
    .locator('div')
    .filter({ hasText: 'Encountered an error when creating the job.' });
  await page.getByRole('button', { name: 'OK' }).click();
});

test('should try to create a job with incorrect input and get error', async ({
  page
}) => {
  await page.goto('');
  await page.menu.open('VDK');
  await page.locator('#jp-vdk-menu').getByText('Create').click();
  await page.getByLabel('Job name:').click();
  await page.getByLabel('Job name:').fill('first-job');
  await page.getByLabel('Job team:').click();
  await page.getByLabel('Job team:').fill('example-team');
  await page.getByLabel('Path to job directory:').click();
  await page.getByLabel('Path to job directory:').fill('sdfgsdfsdfsd');
  await page.getByRole('button', { name: 'OK' }).click();
  await page
    .locator('div')
    .filter({ hasText: 'Encountered an error when creating the job.' });
  await page.getByRole('button', { name: 'OK' }).click();
});

test('should try to create a job successfully', async ({ page }) => {
  await page.goto('');
  await page.menu.open('VDK');
  await page.locator('#jp-vdk-menu').getByText('Create').click();
  await page.getByLabel('Job name:').click();
  await page.getByLabel('Job name:').fill('first-job');
  await page.getByLabel('Job team:').click();
  await page.getByLabel('Job team:').fill('my-team');
  await page.getByRole('button', { name: 'OK' }).click();
  page.on('dialog', async dialog => {
    expect(dialog.type()).toContain('alert');
    expect(dialog.message()).toContain(
      'Job with name first-job was created successfully!'
    );
    await dialog.accept();
  });
  await page.getByRole('button', { name: 'OK' }).click();
});

test('should open download job pop up and then cancel the operation', async ({
  page
}) => {
  await page.goto('');
  await page.menu.open('VDK');
  await page.locator('#jp-vdk-menu').getByText('Download').click();
  await page.locator('div').filter({ hasText: 'Download Job' });
  await page.getByRole('button', { name: 'Cancel' }).click();
});

test('should try download operation with empty input and get error', async ({
  page
}) => {
  await page.goto('');
  await page.menu.open('VDK');
  await page.locator('#jp-vdk-menu').getByText('Download').click();
  await page.locator('div').filter({ hasText: 'Download Job' });
  await page.getByRole('button', { name: 'OK' }).click();
  await page.locator('div').filter({
    hasText: 'Encountered an error when trying to download the job. '
  });
  await page.getByRole('button', { name: 'OK' }).click();
});

test('should create an init cell when opening a new notebook', async ({
  page
}) => {
  await page.goto('');
  await page.locator('.jp-LauncherCard-icon').first().click();
  await expect(
    page.getByText(`job_input = VDK.get_initialized_job_input()`)
  ).toBeVisible();
});


test('should save the token from local storage to a server', async ({ page }) => {
  // Step 1: Create an item in the browser's local storage
  await page.evaluate(() => {
    localStorage.setItem('test-token', JSON.stringify({ "token": "value" }));
  });

  // Step 2: Mock the server endpoint to return the desired value
  // Note: The actual mechanism to mock the server might be different based on your setup.
  // The following is a generic approach and might need adjustments.
  await page.route('**/vdkLocation', route => {
    route.fulfill({
      contentType: 'application/json',
      body: JSON.stringify({ "tokenLocation": "/path/to/token/on/server" })
    });
  });

  // Step 3: Advance 30 seconds in the future
  // Note: Playwright doesn't have a direct method to advance time.
  // Instead, you'd either have to wait for 30 seconds or find a way to fast-forward your application's logic.
  await page.waitForTimeout(30000); // Waits for 30 seconds

  // Step 4: Verify the token is saved on the server
  // Note: The exact mechanism to verify this might differ based on your setup.
  // The following is a general approach and might need adjustments.
  const tokenFileContent = await page.evaluate(async () => {
    // This assumes you have some client-side way to fetch the content of the server file.
    // Replace this with your actual method to verify the token on the server.
    const response = await fetch("/path/to/token/on/server");
    return response.text();
  });

  expect(tokenFileContent).toContain('value'); // Adjust this assertion based on the expected content.
});

