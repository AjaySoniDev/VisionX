import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { pages, layout } from './pages.mjs';

export const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const config = JSON.parse(fs.readFileSync(path.join(root, 'site.config.json'), 'utf8'));
const release = JSON.parse(fs.readFileSync(path.join(root, 'evidence/release.json'), 'utf8'));
const status = JSON.parse(fs.readFileSync(path.join(root, 'docs/visionx-status.json'), 'utf8'));
const reports = Object.fromEntries(['notebook04', 'synthetic'].map(name => [name, JSON.parse(fs.readFileSync(path.join(root, `evidence/${name}/report.json`), 'utf8'))]));
if (Object.values(reports).some(r => r.environment.source.sha256 !== release.sourceSha256)) throw new Error('Evidence reports have inconsistent source identities');
const destination = path.resolve(root, 'public');
if (path.dirname(destination) !== root || path.basename(destination) !== 'public') throw new Error('Unsafe build destination');
if (fs.existsSync(destination)) {
  if (!fs.existsSync(path.join(destination, '.visionx-build'))) throw new Error('Refusing to replace an unmarked public directory');
  fs.rmSync(destination, { recursive: true });
}
fs.mkdirSync(destination);
fs.writeFileSync(path.join(destination, '.visionx-build'), 'Generated VisionX static website\n');
for (const directory of ['assets', 'docs', 'evidence']) fs.cpSync(path.join(root, directory), path.join(destination, directory), { recursive: true });
for (const name of ['styles.css', 'script.js', 'robots.txt']) fs.copyFileSync(path.join(root, name), path.join(destination, name));
const context = { config, release, status, reports, root };
const generatedPages = pages(context);
for (const page of generatedPages) {
  const html = layout(page, context);
  fs.writeFileSync(path.join(destination, page.file), html);
}
fs.writeFileSync(path.join(destination, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${generatedPages.filter(p => p.file !== '404.html').map(p => `<url><loc>${config.canonicalUrl}/${p.file === 'index.html' ? '' : p.file}</loc><lastmod>${config.date}</lastmod></url>`).join('')}</urlset>\n`);
console.log(`Built ${generatedPages.length} pages with matching source ${release.sourceSha256.slice(0, 12)}.`);
