const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

async function run() {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  try {
    const page = await browser.newPage({ hasTouch: true });
    await page.emulateMedia({ reducedMotion: 'reduce' });
    const session = await page.context().newCDPSession(page);
    const staticRoot = path.resolve(__dirname, '../_static');
    const css = fs.readFileSync(path.join(staticRoot, 'custom.css'), 'utf8');
    const script = fs.readFileSync(path.join(staticRoot, 'image_viewer.js'), 'utf8');
    const image = 'data:image/svg+xml,' + encodeURIComponent(
      '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800"><rect width="1200" height="800" fill="#2980b9"/></svg>'
    );
    const icon = 'data:image/svg+xml,' + encodeURIComponent(
      '<svg xmlns="http://www.w3.org/2000/svg" width="38" height="29"><rect width="38" height="29" fill="#2980b9"/></svg>'
    );
    for (const width of [375, 1280, 1920]) {
      await page.setViewportSize({ width, height: 900 });
      await page.setContent(`<html lang="zh-CN"><style>${css}</style><div class="sdk-reading-main" style="width:100%;max-width:800px;margin:auto"><div class="rst-content"><p><img src='${image}' alt="Diagram"></p><p><a href='${image}'><img src='${image}' alt="Linked diagram"></a></p><p><a href="https://example.com"><img src='${image}' alt="External link"></a></p></div></div></html>`);
      await page.addScriptTag({ content: script });
      await page.waitForFunction(() => Array.from(document.images).slice(0, 3).every(image => image.complete));
      assert.equal(await page.locator('.sdk-image-trigger').count(), 2);
      assert.equal(await page.locator('a[href="https://example.com"]').getAttribute('aria-haspopup'), null);
      const alignment = await page.evaluate(() => {
        const main = document.querySelector('.sdk-reading-main').getBoundingClientRect();
        const image = document.querySelector('.sdk-image-trigger img').getBoundingClientRect();
        return Math.abs((main.left + main.right) / 2 - (image.left + image.right) / 2);
      });
      assert.ok(alignment < 1);
      await page.locator('.sdk-image-trigger').first().focus();
      await page.keyboard.press('Enter');
      await page.waitForFunction(() => document.querySelector('.sdk-image-viewer__canvas img').naturalWidth > 0);
      assert.equal(await page.locator('dialog').getAttribute('open'), '');
      const originalWidth = await page.locator('.sdk-image-viewer__canvas img').evaluate(image => image.getBoundingClientRect().width);
      await page.getByRole('button', { name: '\u653e\u5927', exact: true }).click();
      const enlargedWidth = await page.locator('.sdk-image-viewer__canvas img').evaluate(image => image.getBoundingClientRect().width);
      assert.ok(enlargedWidth > originalWidth);
      assert.equal(await page.locator('output').textContent(), '140%');
      await page.getByRole('button', { name: '\u7f29\u5c0f', exact: true }).click();
      assert.equal(await page.locator('output').textContent(), '100%');
      await page.locator('.sdk-image-viewer__stage').hover();
      await page.mouse.wheel(0, -100);
      await page.waitForFunction(() => document.querySelector('output').textContent === '110%');
      await page.keyboard.press('+');
      assert.equal(await page.locator('output').textContent(), '150%');
      await page.getByRole('button', { name: '\u9002\u5e94\u7a97\u53e3' }).click();
      assert.equal(await page.locator('output').textContent(), '100%');
      const layout = await page.evaluate(() => {
        const dialog = document.querySelector('dialog').getBoundingClientRect();
        const toolbar = document.querySelector('.sdk-image-viewer__toolbar').getBoundingClientRect();
        const close = document.querySelector('.sdk-image-viewer__close').getBoundingClientRect();
        return { width: dialog.width, height: dialog.height, toolbarX: toolbar.x + toolbar.width / 2, toolbarBottom: toolbar.bottom, closeRight: close.right, closeTop: close.top };
      });
      assert.equal(layout.width, width);
      assert.equal(layout.height, 900);
      assert.ok(Math.abs(layout.toolbarX - width / 2) < 1);
      assert.ok(layout.toolbarBottom > 800 && layout.toolbarBottom <= 900);
      assert.ok(layout.closeRight <= width && layout.closeRight > width - 80);
      assert.ok(layout.closeTop <= 30);
      const imageBox = await page.locator('.sdk-image-viewer__canvas img').boundingBox();
      const centerX = imageBox.x + imageBox.width / 2;
      const centerY = imageBox.y + imageBox.height / 2;
      await session.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [
        { x: centerX - 30, y: centerY, id: 1 }, { x: centerX + 30, y: centerY, id: 2 }
      ] });
      await session.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [
        { x: centerX - 60, y: centerY, id: 1 }, { x: centerX + 60, y: centerY, id: 2 }
      ] });
      await page.waitForFunction(() => document.querySelector('output').textContent === '200%');
      await session.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      for (let iteration = 0; iteration < 7; iteration += 1) {
        if (await page.getByRole('button', { name: '\u653e\u5927', exact: true }).isDisabled()) {
          break;
        }
        await page.getByRole('button', { name: '\u653e\u5927', exact: true }).click();
      }
      assert.equal(await page.locator('output').textContent(), '400%');
      assert.ok(await page.getByRole('button', { name: '\u653e\u5927', exact: true }).isDisabled());
      await page.mouse.move(centerX, centerY);
      await page.mouse.down();
      await page.mouse.move(centerX + 60, centerY + 40, { steps: 4 });
      await page.mouse.up();
      assert.ok(await page.locator('.sdk-image-viewer__canvas img').evaluate(image => {
        const matrix = new DOMMatrix(getComputedStyle(image).transform);
        return matrix.e !== 0 || matrix.f !== 0;
      }));
      await page.getByRole('button', { name: '\u9002\u5e94\u7a97\u53e3' }).click();
      for (let iteration = 0; iteration < 8; iteration += 1) {
        await page.keyboard.press('Tab');
        assert.ok(await page.evaluate(() => document.querySelector('dialog').contains(document.activeElement)));
      }
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.keyboard.press('Escape');
      await page.waitForFunction(() => document.documentElement.style.overflow === '');
      assert.equal(await page.locator('dialog').getAttribute('open'), null);
      assert.ok(await page.locator('.sdk-image-trigger').first().evaluate(button => button === document.activeElement));
      assert.equal(await page.evaluate(() => document.documentElement.style.overflow), '');
      await page.locator('.sdk-image-trigger').nth(1).click();
      assert.equal(await page.locator('dialog').getAttribute('open'), '');
      await page.getByRole('button', { name: '\u5173\u95ed', exact: true }).click();
      await page.waitForFunction(() => document.documentElement.style.overflow === '');
      await page.locator('.sdk-image-trigger').first().click();
      await page.locator('dialog').click({ position: { x: 5, y: 5 } });
      await page.waitForFunction(() => !document.querySelector('dialog').open);
      await page.waitForFunction(() => document.documentElement.style.overflow === '');
      console.log(`Image viewer passed at ${width}px`);
    }
    for (const width of [375, 1440]) {
      await page.setViewportSize({ width, height: 900 });
      await page.setContent(`<html lang="zh-CN"><style>${css}</style><div class="sdk-reading-main" style="width:100%;max-width:800px;margin:auto"><div class="rst-content"><ol><li><p>Observe the current waypoint and status;\n<img src='${image}' alt="List screenshot"></p></li></ol><p>Click the navigation <img src='${icon}' alt="Inline icon"> icon to continue.</p><figure><img src='${image}' alt="Figure screenshot"><figcaption>Caption text</figcaption></figure><p>Responsive picture: <picture><source srcset='${image}'><img src='${image}' alt="Responsive screenshot"></picture></p></div></div></html>`);
      await page.addScriptTag({ content: script });
      await page.waitForFunction(() => Array.from(document.querySelectorAll('.rst-content img')).every(image => image.complete && image.naturalWidth > 0));
      assert.equal(await page.locator('.sdk-image-trigger').count(), 4);
      assert.equal(await page.locator('.sdk-image-trigger--inline').count(), 1);
      assert.equal(await page.locator('picture source').count(), 1);
      assert.equal(await page.locator('.sdk-image-trigger--inline').evaluate(button => getComputedStyle(button).display), 'inline-flex');
      for (const description of ['List screenshot', 'Inline icon', 'Figure screenshot', 'Responsive screenshot']) {
        const trigger = page.locator('.sdk-image-trigger').filter({ has: page.getByAltText(description, { exact: true }) });
        await trigger.click();
        await page.waitForFunction(() => document.querySelector('.sdk-image-viewer__canvas img').naturalWidth > 0);
        assert.equal(await page.locator('dialog').getAttribute('open'), '');
        assert.equal(await page.locator('.sdk-image-viewer__canvas img').getAttribute('alt'), description);
        await page.getByRole('button', { name: '\u653e\u5927', exact: true }).click();
        assert.equal(await page.locator('output').textContent(), '140%');
        await page.keyboard.press('Escape');
        await page.waitForFunction(() => document.documentElement.style.overflow === '');
      }
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      console.log(`Mixed-content images passed at ${width}px`);
    }
  } finally {
    await browser.close();
  }
}

run().catch(error => { console.error(error); process.exitCode = 1; });
