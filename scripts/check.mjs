import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const hashFile = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');

function parseAttributes(source) {
  const attrs = [];
  const pattern = /([^\s=/>]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;
  for (const match of source.matchAll(pattern)) attrs.push({ name: match[1].toLowerCase(), value: match[2] ?? match[3] ?? match[4] ?? '' });
  return attrs;
}

function parseTags(html) {
  const tags = [];
  const pattern = /<([a-zA-Z][\w:-]*)\b([^>]*)>/g;
  for (const match of html.matchAll(pattern)) tags.push({ tagName: match[1].toLowerCase(), attrs: parseAttributes(match[2]) });
  return tags;
}

export const attr = (node, name) => node.attrs?.find(a => a.name === name)?.value;

export function inspectDirectory(directory, config) {
  const errors = [], externalLinks = new Set();
  let localReferences = 0;
  const files = fs.readdirSync(directory).filter(name => name.endsWith('.html'));
  const documents = new Map(files.map(file => {
    const html = fs.readFileSync(path.join(directory, file), 'utf8');
    return [file, { html, tags: parseTags(html) }];
  }));

  for (const [file, document] of documents) {
    const { html, tags } = document;
    if (tags.filter(n => n.tagName === 'h1').length !== 1) errors.push(`${file}: expected one h1`);
    if (tags.filter(n => n.tagName === 'main').length !== 1) errors.push(`${file}: expected one main landmark`);
    if (!tags.some(n => n.tagName === 'meta' && attr(n, 'name') === 'viewport')) errors.push(`${file}: missing viewport`);
    if (!tags.some(n => n.tagName === 'title')) errors.push(`${file}: missing title`);
    const ids = tags.map(n => attr(n, 'id')).filter(Boolean);
    if (new Set(ids).size !== ids.length) errors.push(`${file}: duplicate IDs`);
    if (/AjaySoni-Dev|visionx-sih-core-evidence\.ajaysoni-dev/.test(html)) errors.push(`${file}: obsolete team URL`);

    for (const node of tags) {
      if (node.tagName === 'img' && !attr(node, 'alt')) errors.push(`${file}: image lacks alternative text`);
      if (node.tagName === 'script' && !attr(node, 'src')) errors.push(`${file}: inline script violates deployment CSP`);
      for (const { name, value } of node.attrs || []) {
        if (name.startsWith('on') || name === 'style') errors.push(`${file}: inline behavior/style violates deployment policy`);
        if (!['href', 'src'].includes(name) || !value || value.startsWith('data:')) continue;
        if (/^(javascript|vbscript):/i.test(value)) { errors.push(`${file}: unsafe URL scheme`); continue; }
        if (/^(https?:|mailto:)/.test(value)) {
          if (name === 'href') externalLinks.add(value);
          if (attr(node, 'target') === '_blank' && !attr(node, 'rel')?.includes('noopener')) errors.push(`${file}: external new-tab link lacks noopener`);
          continue;
        }
        let url;
        try { url = new URL(value, `https://local.invalid/${file}`); }
        catch { errors.push(`${file}: invalid local URL ${value}`); continue; }
        let local;
        try { local = decodeURIComponent(url.pathname).replace(/^\//, '') || 'index.html'; }
        catch { errors.push(`${file}: invalid URL encoding ${value}`); continue; }
        const target = path.resolve(directory, local);
        if (!target.startsWith(directory + path.sep) || !fs.existsSync(target) || !fs.statSync(target).isFile()) { errors.push(`${file}: missing or unsafe ${value}`); continue; }
        localReferences++;
        if (url.hash && local.endsWith('.html')) {
          const targetTags = documents.get(local)?.tags || parseTags(fs.readFileSync(target, 'utf8'));
          let fragment;
          try { fragment = decodeURIComponent(url.hash.slice(1)); }
          catch { errors.push(`${file}: invalid fragment encoding ${value}`); continue; }
          if (!targetTags.some(n => attr(n, 'id') === fragment)) errors.push(`${file}: missing fragment ${value}`);
        }
      }
    }
  }

  for (const name of fs.readdirSync(path.join(directory, 'assets')).filter(n => n.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(directory, 'assets', name), 'utf8');
    if (/<script\b|\bon[a-z]+\s*=|<foreignObject\b/i.test(svg)) errors.push(`assets/${name}: active SVG content`);
  }
  return { errors, pages: files.length, localReferences, externalLinks: [...externalLinks].sort() };
}

export function inspectMarkdownLinks(rootDirectory) {
  const errors = [];
  let localReferences = 0;
  const docsDirectory = path.join(rootDirectory, 'docs');
  if (!fs.existsSync(docsDirectory)) return { errors: ['docs directory is missing'], localReferences };
  const markdownFiles = [];
  const collect = directory => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const candidate = path.join(directory, entry.name);
      if (entry.isDirectory()) collect(candidate);
      else if (entry.isFile() && entry.name.endsWith('.md')) markdownFiles.push(candidate);
    }
  };
  collect(docsDirectory);
  const linkPattern = /!?\[[^\]]*\]\(([^)]+)\)/g;
  for (const file of markdownFiles) {
    const text = fs.readFileSync(file, 'utf8');
    for (const match of text.matchAll(linkPattern)) {
      let href = match[1].trim();
      if (!href || /^(https?:|mailto:|#)/.test(href)) continue;
      if (href.startsWith('<') && href.endsWith('>')) href = href.slice(1, -1);
      href = href.replace(/\s+["'][^"']*["']\s*$/, '');
      const [pathname] = href.split('#');
      if (!pathname) continue;
      let decoded;
      try { decoded = decodeURIComponent(pathname); }
      catch { errors.push(`${path.relative(rootDirectory, file)}: invalid URL encoding ${href}`); continue; }
      const candidate = decoded.startsWith('/') ? path.resolve(rootDirectory, '.' + decoded) : path.resolve(path.dirname(file), decoded);
      if (candidate !== rootDirectory && !candidate.startsWith(rootDirectory + path.sep)) { errors.push(`${path.relative(rootDirectory, file)}: unsafe local link ${href}`); continue; }
      if (!fs.existsSync(candidate) || !fs.statSync(candidate).isFile()) { errors.push(`${path.relative(rootDirectory, file)}: missing local link ${href}`); continue; }
      localReferences++;
    }
  }
  return { errors, files: markdownFiles.length, localReferences };
}

function sourceFileCount(sourceRoot) {
  const ignored = new Set(['.git', 'node_modules', 'public', 'validation', 'test-results', 'playwright-report', '.vercel']);
  let count = 0;
  const visit = directory => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      if (entry.isDirectory() && ignored.has(entry.name)) continue;
      const candidate = path.join(directory, entry.name);
      if (entry.isDirectory()) visit(candidate);
      else if (entry.isFile()) count++;
    }
  };
  visit(sourceRoot);
  return count;
}

export function verifySourceHygiene(sourceRoot) {
  const errors = [];
  const forbidden = [
    'RELEASE_MANIFEST.json', 'content/status.json',
    '404.html', 'architecture.html', 'business.html', 'demo.html', 'evidence.html', 'index.html', 'references.html', 'reproduce.html', 'research.html', 'source.html',
    'docs/ARCHITECTURE.md', 'docs/AUDIT.md', 'docs/BUSINESS.md', 'docs/CLAIMS.md', 'docs/EVALUATION.md', 'docs/REFERENCES.md', 'docs/REPRODUCE.md', 'docs/STATUS.md',
    'docs/VisionX_Business_Revenue_Model.md', 'docs/VisionX_Canonical_Master_Deep_Report_2026-09-29.md', 'docs/VisionX_Jury_Evidence_Link_Strategy.md', 'docs/VisionX_Research_References.md',
    'assets/VisionX_01_Proposed_Solution.svg', 'assets/VisionX_02_System_Architecture.svg', 'assets/VisionX_03_Technology_Stack.svg', 'assets/VisionX_04_Impact_Benefits.svg',
    'assets/logo_text_part.webp', 'test-results/.last-run.json',
    'evidence/notebook04/memory', 'evidence/notebook04/window-evidence', 'evidence/synthetic/memory', 'evidence/synthetic/window-evidence',
  ];
  for (const relative of forbidden) if (fs.existsSync(path.join(sourceRoot, relative))) errors.push(`source hygiene: generated/duplicate/bulk path present: ${relative}`);
  const count = sourceFileCount(sourceRoot);
  if (count > 300) errors.push(`source hygiene: ${count} files exceeds the 300-file repository budget`);
  return errors;
}

export function verifyEvidence(directory) {
  const errors = [];
  const evidence = path.join(directory, 'evidence');
  const release = JSON.parse(fs.readFileSync(path.join(evidence, 'release.json'), 'utf8'));
  const judgePack = JSON.parse(fs.readFileSync(path.join(evidence, 'judge-pack.json'), 'utf8'));
  const deployed = judgePack.deployedEvidence?.files || {};
  if (Object.keys(deployed).length !== judgePack.deployedEvidence?.fileCount) errors.push('judge-pack: deployed file count mismatch');
  for (const [relative, digest] of Object.entries(deployed)) {
    const candidate = path.resolve(evidence, relative);
    if (!candidate.startsWith(evidence + path.sep) || !fs.existsSync(candidate) || !fs.statSync(candidate).isFile()) errors.push(`judge-pack: missing ${relative}`);
    else if (hashFile(candidate) !== digest) errors.push(`judge-pack: checksum mismatch ${relative}`);
  }
  for (const name of ['notebook04', 'synthetic']) {
    const base = path.join(evidence, name);
    const report = JSON.parse(fs.readFileSync(path.join(base, 'report.json'), 'utf8'));
    if (report.environment.source.sha256 !== release.sourceSha256) errors.push(`${name}: source hash mismatch`);
    if (Object.values(report.methods).some(m => m.metrics.error_count > 0)) errors.push(`${name}: classifier failures in evidence`);
    for (const [relative, digest] of Object.entries(JSON.parse(fs.readFileSync(path.join(base, 'checksums.json'), 'utf8')))) {
      const candidate = path.resolve(base, relative);
      if (!candidate.startsWith(base + path.sep) || !fs.existsSync(candidate) || hashFile(candidate) !== digest) errors.push(`${name}: checksum mismatch ${relative}`);
    }
  }
  for (const [relative, digest] of Object.entries(release.sourceFiles)) {
    const candidate = path.join(evidence, 'source/vxn_ramnet', relative);
    if (!fs.existsSync(candidate) || hashFile(candidate) !== digest) errors.push(`source excerpt mismatch: ${relative}`);
  }
  if (release.verification.pytest.failures || release.verification.pytest.errors) errors.push('Published verification contains test failures');
  return errors;
}

export function verifyLocalArchive(sourceRoot) {
  const errors = [];
  const manifestPath = path.join(sourceRoot, 'evidence/judge-pack.json');
  if (!fs.existsSync(manifestPath)) return ['archive verification: judge-pack.json missing'];
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const info = manifest.fullEvidenceArchive;
  if (!info?.path || !info?.sha256) return ['archive verification: metadata missing'];
  const archive = path.resolve(sourceRoot, info.path);
  // Optimized judge/deployment packages may omit the bulky archive. If present, it must match the recorded immutable identity.
  if (fs.existsSync(archive) && hashFile(archive) !== info.sha256) errors.push('archive verification: full evidence archive checksum mismatch');
  return errors;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const directory = path.resolve(root, 'public');
  const config = JSON.parse(fs.readFileSync(path.join(root, 'site.config.json'), 'utf8'));
  const results = inspectDirectory(directory, config);
  const markdown = inspectMarkdownLinks(directory);
  results.markdownFiles = markdown.files;
  results.markdownLocalReferences = markdown.localReferences;
  results.errors.push(...markdown.errors, ...verifyEvidence(directory), ...verifySourceHygiene(root), ...verifyLocalArchive(root));
  if (results.errors.length) { console.error(results.errors.join('\n')); process.exitCode = 1; }
  else console.log(`Verified ${results.pages} pages, ${results.localReferences} HTML references/fragments, ${results.markdownLocalReferences} documentation links, compact evidence checksums, and the <=300 source-file budget. ${results.externalLinks.length} external destinations inventoried.`);
  fs.mkdirSync(path.join(root, 'validation'), { recursive: true });
  fs.writeFileSync(path.join(root, 'validation/static-check.json'), JSON.stringify(results, null, 2) + '\n');
}
