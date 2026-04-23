const { chromium } = require('/tmp/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const pdfPath = '/home/gerion/.openclaw/workspace/decks/elan-cero-energetico/cero-energetico.pdf';
const dir = '/home/gerion/.openclaw/workspace/decks/elan-cero-energetico';

const http = require('http');
const server = http.createServer((req, res) => {
  let urlPath = req.url === '/' ? '/index.html' : req.url;
  let filePath = dir + urlPath;
  try {
    const content = fs.readFileSync(filePath);
    const ext = path.extname(filePath);
    let ct = 'text/html';
    if (ext === '.png') ct = 'image/png';
    else if (ext === '.jpg' || ext === '.jpeg') ct = 'image/jpeg';
    res.writeHead(200, {'Content-Type': ct});
    res.end(content);
  } catch(e) {
    res.writeHead(404); res.end('Not found');
  }
});

server.listen(8765, async () => {
  const { PDFDocument } = require('/tmp/node_modules/pdf-lib');

  const browser = await chromium.launch({ args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
  const page = await context.newPage();

  await page.goto('http://localhost:8765/index.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);

  // Hide nav controls and progress dots before PDF generation
  await page.addStyleTag({ content: '.nav, .progress-dots { display: none !important; } .slide-counter { display: none !important; }' });

  const totalSlides = 11;
  const mergedPdf = await PDFDocument.create();

  for (let i = 0; i < totalSlides; i++) {
    if (i > 0) {
      await page.evaluate((idx) => goTo(idx), i);
      await page.waitForTimeout(600);
    }
    const buf = await page.pdf({
      width: '1280px',
      height: '720px',
      printBackground: true,
      margin: { top: '0', right: '0', bottom: '0', left: '0' }
    });
    const slidePdf = await PDFDocument.load(buf);
    const pages = await mergedPdf.copyPages(slidePdf, slidePdf.getPageIndices());
    pages.forEach(p => mergedPdf.addPage(p));
    process.stdout.write('Slide ' + (i+1) + '/' + totalSlides + ' done\n');
  }

  const pdfBytes = await mergedPdf.save();
  fs.writeFileSync(pdfPath, pdfBytes);

  await browser.close();
  server.close();

  console.log('PDF saved:', pdfBytes.length, 'bytes,', totalSlides, 'pages');
});
