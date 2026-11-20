// Render the one-pager as an image (site/onepager.png) and the link-preview card (site/og.png).
// Run after site/build.py.  Needs Playwright and network access for the web fonts:  node site/snap.js
// Then  python3 site/build.py --shrink  to palette-compress the one-pager image.
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const root = path.resolve(__dirname, '..');
  const browser = await chromium.launch();

  let context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2, colorScheme: 'light' });
  let page = await context.newPage();
  await page.goto('file://' + path.join(root, 'onepager.html'), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  await page.locator('.op').screenshot({ path: path.join(root, 'site', 'onepager.png') });
  await context.close();

  context = await browser.newContext({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1, colorScheme: 'light' });
  page = await context.newPage();
  await page.goto('file://' + path.join(root, 'index.html'), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(root, 'site', 'og.png') });
  await browser.close();
  console.log('wrote site/onepager.png and site/og.png');
})();
