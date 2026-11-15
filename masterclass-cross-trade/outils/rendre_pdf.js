// Rend une page HTML en PDF (et éventuellement en PNG) avec Chromium/Playwright.
// Usage : node outils/rendre_pdf.js <entrée.html> <sortie.pdf> [carrousel|a4] [dossier_png]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const [input, output, mode = 'a4', pngDir] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
  await page.goto('file://' + path.resolve(input), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  // Rendu des diagrammes Mermaid s'ils existent
  await page.evaluate(async () => {
    if (window.renderMermaid) await window.renderMermaid();
  });
  const errs = await page.evaluate(() => window.__mermaidErrors || []);
  if (errs.length) { console.error('Erreurs Mermaid :', errs); process.exitCode = 1; }
  if (mode === 'carrousel') {
    await page.pdf({ path: output, width: '1080px', height: '1350px', printBackground: true });
    if (pngDir) {
      fs.mkdirSync(pngDir, { recursive: true });
      const slides = await page.$$('section.slide');
      for (let i = 0; i < slides.length; i++) {
        await slides[i].screenshot({ path: path.join(pngDir, `slide-${String(i + 1).padStart(2, '0')}.png`) });
      }
    }
  } else if (mode === 'image') {
    const el = await page.$('#visuel');
    await el.screenshot({ path: output });
  } else {
    await page.pdf({
      path: output, format: 'A4', printBackground: true,
      margin: { top: '18mm', bottom: '18mm', left: '16mm', right: '16mm' },
      displayHeaderFooter: true,
      headerTemplate: '<div></div>',
      footerTemplate: '<div style="width:100%;font-size:8px;color:#5B6B7B;padding:0 16mm;display:flex;justify-content:space-between;font-family:sans-serif"><span>Masterclass Cross-Trade International · données fictives et pédagogiques</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    });
  }
  await browser.close();
  console.log('OK →', output);
})();
