// Usage: node shoot_reports.js <reports.html> <outdir>
// Screenshots every section.page to <outdir>/<data-file>, and fails if a page's
// .body content runs into the footer zone.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const SAFE_BOTTOM = 1340; // px from page top; footer disclaimer sits below this

(async () => {
  const [html, outDir] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

  const overflow = await page.$$eval('section.page', (els, safe) => els.flatMap(sec => {
    const top = sec.getBoundingClientRect().top;
    return [...sec.querySelectorAll('.body')]
      .map(b => ({ file: sec.dataset.file, bottom: Math.round(b.getBoundingClientRect().bottom - top) }))
      .filter(r => r.bottom > safe);
  }), SAFE_BOTTOM);
  if (overflow.length) {
    console.error('overflow:', JSON.stringify(overflow));
    process.exitCode = 1;
  }

  const files = await page.$$eval('section.page', els => els.map(e => e.dataset.file));
  for (const [i, file] of files.entries()) {
    const target = path.join(outDir, file);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    await page.locator('section.page').nth(i).screenshot({ path: target });
  }
  console.log(`shot ${files.length} images`);
  await browser.close();
})();
