import { chromium } from 'playwright';
import { PDFDocument } from 'pdf-lib';
import { createServer } from 'http';
import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = 8765;
const DECK_DIR = __dirname;

// Simple HTTP server for the deck
const server = createServer((req, res) => {
  let filePath = DECK_DIR + req.url;
  try {
    const content = readFileSync(filePath);
    const ext = path.extname(filePath);
    const mime = { '.html': 'text/html', '.png': 'image/png', '.js': 'application/javascript', '.css': 'text/css' }[ext] || 'text/plain';
    res.writeHead(200, { 'Content-Type': mime });
    res.end(content);
  } catch {
    res.writeHead(404);
    res.end('Not found');
  }
});

await new Promise(r => server.listen(PORT, r));
console.log(`Server on port ${PORT}`);

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.setViewportSize({ width: 1280, height: 720 });

const pdfDoc = await PDFDocument.create();
const TOTAL_SLIDES = 11;

for (let i = 1; i <= TOTAL_SLIDES; i++) {
  await page.goto(`http://localhost:${PORT}/index.html#s${i}`);
  await page.waitForTimeout(600);
  const screenshot = await page.screenshot({ type: 'png' });
  const img = await pdfDoc.embedPng(screenshot);
  const slidePage = pdfDoc.addPage([1280, 720]);
  slidePage.drawImage(img, { x: 0, y: 0, width: 1280, height: 720 });
  console.log(`  Slide ${i}/${TOTAL_SLIDES}`);
}

await browser.close();
server.close();

const pdfBytes = await pdfDoc.save();
writeFileSync(path.join(DECK_DIR, 'cero-energetico-v2.pdf'), pdfBytes);
console.log(`PDF generated: ${(pdfBytes.length / 1024).toFixed(0)} KB`);
