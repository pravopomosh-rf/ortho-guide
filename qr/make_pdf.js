// Full QR sheet of all site topics: node qr/make_pdf.js [FONTS_DIR]
// FONTS_DIR = node_modules/@fontsource (needs rubik + noto-sans-arabic). Output: qr/QR_kody_operacii.pdf
// Order and titles come from nav-<lang>.js (rebuild them first with tools/mknav.py). QR images: qr/<page>.png (make_qr.py).
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..');
const FONTS = process.argv[2] || 'node_modules/@fontsource';
const L = ['he', 'ar', 'ru', 'en'];
const N = {};
for (const l of L) { global.window = {}; eval(fs.readFileSync(path.join(ROOT, `nav-${l}.js`), 'utf8')); N[l] = window.NAVD[l]; }
const id = h => h.replace('ops/', '').replace('.html', '');
const title = (l, h) => { for (const s of N[l].secs) for (const i of s.items) if (i.h === h) return i.t; return ''; };
const secT = (l, k) => (N[l].secs.find(s => s.k === k) || {}).t || '';
const SITEMAP = { he: 'כל הנושאים באתר', ar: 'كل مواضيع الموقع', ru: 'Все темы сайта', en: 'All topics on the site' };
const ROUTES = { he: 'מסלולים לפי ניתוח: הכול לפי הסדר', ar: 'مسارات حسب العملية: كل شيء بالترتيب', ru: 'Маршруты по операциям: всё по порядку', en: 'Surgery pathways: everything in order' };
const groups = [];
const seen = new Set();
// 1) pathways + sitemap
const paths = [];
for (const s of N.ru.secs) for (const i of s.items) if (i.p && !seen.has(i.h)) { seen.add(i.h); paths.push({ h: i.h }); }
paths.push({ h: 'ops/sitemap.html', sm: 1 }); seen.add('ops/sitemap.html');
groups.push({ t: ROUTES, items: paths });
// 2) every section, each page once
for (const s of N.ru.secs) {
  const items = [];
  for (const i of s.items) if (!seen.has(i.h)) { seen.add(i.h); items.push({ h: i.h }); }
  if (items.length) groups.push({ t: Object.fromEntries(L.map(l => [l, secT(l, s.k)])), items });
}
const missing = [];
const card = it => {
  const p = id(it.h), img = path.join(__dirname, p + '.png');
  if (!fs.existsSync(img)) missing.push(p);
  const t = l => it.sm ? SITEMAP[l] : title(l, it.h);
  return `<div class="c"><img src="data:image/png;base64,${fs.existsSync(img) ? fs.readFileSync(img).toString('base64') : ''}">` +
    `<div class="he" dir="rtl">${t('he')}</div><div class="ar" dir="rtl">${t('ar')}</div><div class="ru">${t('ru')}</div><div class="en">${t('en')}</div></div>`;
};
const f = (fam, file, w) => `@font-face{font-family:${fam};font-weight:${w};src:url(data:font/woff2;base64,${fs.readFileSync(path.join(FONTS, file)).toString('base64')})}`;
const css = [
  f('R', 'rubik/files/rubik-hebrew-400-normal.woff2', 400), f('R', 'rubik/files/rubik-hebrew-700-normal.woff2', 700),
  f('R', 'rubik/files/rubik-latin-400-normal.woff2', 400), f('R', 'rubik/files/rubik-latin-700-normal.woff2', 700),
  f('R', 'rubik/files/rubik-cyrillic-400-normal.woff2', 400), f('R', 'rubik/files/rubik-cyrillic-700-normal.woff2', 700),
  f('A', 'noto-sans-arabic/files/noto-sans-arabic-arabic-400-normal.woff2', 400), f('A', 'noto-sans-arabic/files/noto-sans-arabic-arabic-700-normal.woff2', 700),
].join('');
const day = new Date().toISOString().slice(0, 10).split('-').reverse().join('.');
const html = `<!doctype html><html><head><meta charset="utf-8"><style>${css}
@page{size:A4;margin:10mm 9mm 12mm}
body{font-family:R,A,sans-serif;color:#1d2b2a;margin:0}
h1{font-size:20px;margin:0 0 2px}.sub{color:#46595a;font-size:11.5px;margin:0 0 3px}h1+.sub{margin-top:4px}
h2{font-size:15px;margin:10px 0 6px;padding:4px 8px;background:#e8f3f1;border-radius:6px;break-after:avoid}
h2 span{font-weight:400;color:#46595a;font-size:12px}
.k{break-inside:avoid;page-break-inside:avoid;margin-bottom:7px}.g{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}
.c{border:1px solid #c9d4d2;border-radius:8px;padding:6px 6px 7px;text-align:center;break-inside:avoid}
.c img{width:100%;max-width:120px;display:block;margin:0 auto 3px}
.he{font-weight:700;font-size:12.5px;line-height:1.25}.ar{font-family:A,R;font-size:11px;line-height:1.3}
.ru{font-weight:700;font-size:10.5px;line-height:1.25;margin-top:2px}.en{font-size:9.5px;color:#46595a;line-height:1.25}
</style></head><body>
<h1 dir="rtl">קודי QR לכל הנושאים באתר</h1><h1>QR-коды всех тем сайта</h1>
<p class="sub" dir="rtl">סרקו את הקוד ובחרו שפה: עברית, العربية, Русский, English</p><p class="sub">Наведите камеру телефона на код и выберите язык. Полный список тем, ${day}</p>
${groups.map(g => { const rows = []; for (let k = 0; k < g.items.length; k += 4) rows.push(`<div class="g">${g.items.slice(k, k + 4).map(card).join('')}</div>`);
  const h = `<h2><div dir="rtl">${g.t.he} <span>· ${g.t.ar}</span></div><div>${g.t.ru} <span>· ${g.t.en}</span></div></h2>`;
  return `<div class="k">${h}${rows[0]}</div>` + rows.slice(1).map(r => `<div class="k">${r}</div>`).join(''); }).join('\n')}
</body></html>`;
(async () => {
  const { chromium } = require('playwright');
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.setContent(html, { waitUntil: 'load' }); await pg.evaluate(() => document.fonts.ready);
  await pg.pdf({ path: path.join(__dirname, 'QR_kody_operacii.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>', footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#777"><span class="pageNumber"></span> / <span class="totalPages"></span></div>' });
  await b.close();
  console.log('groups', groups.length, 'cards', groups.reduce((a, g) => a + g.items.length, 0), 'missing', missing);
})();
