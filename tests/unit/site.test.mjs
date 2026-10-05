import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { validatedDemoUrl } from '../../scripts/set-demo.mjs';
import { escape } from '../../scripts/pages.mjs';
import { inspectDirectory,inspectMarkdownLinks,verifyEvidence,verifySourceHygiene } from '../../scripts/check.mjs';

test('HTML/source text is escaped instead of executable', () => {
  assert.equal(escape('<script>"x" & \'y\'</script>'),'&lt;script&gt;&quot;x&quot; &amp; &#39;y&#39;&lt;/script&gt;');
});
test('YouTube video URLs normalize without arbitrary redirects', () => {
  assert.equal(validatedDemoUrl('https://youtu.be/V2frBYX62LU'),'https://www.youtube.com/watch?v=V2frBYX62LU');
  assert.equal(validatedDemoUrl('https://www.youtube.com/shorts/V2frBYX62LU'),'https://www.youtube.com/watch?v=V2frBYX62LU');
  for (const url of ['https://youtube.com.evil.test/watch?v=V2frBYX62LU','javascript:alert(1)','http://www.youtube.com/watch?v=V2frBYX62LU','https://www.youtube.com/','https://user:secret@www.youtube.com/watch?v=V2frBYX62LU']) assert.throws(() => validatedDemoUrl(url));
});
test('The built release has complete local links and matching evidence', () => {
  const root = path.resolve('public');
  const config = JSON.parse(fs.readFileSync('site.config.json','utf8'));
  assert.deepEqual(inspectDirectory(root,config).errors,[]);
  assert.deepEqual(inspectMarkdownLinks(root).errors,[]);
  assert.deepEqual(verifyEvidence(root),[]);
  assert.deepEqual(verifySourceHygiene(path.resolve('.')),[]);
});
test('Integrity checker detects missing files and fragments', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(),'visionx-link-test-'));
  // Only this exact freshly created temporary directory is removed below.
  assert.ok(directory.startsWith(path.join(os.tmpdir(),'visionx-link-test-')));
  fs.mkdirSync(path.join(directory,'assets'));
  const html = '<!doctype html><html lang="en"><head><title>Test</title><meta name="viewport" content="width=device-width"></head><body><main><h1>Test</h1><a href="/missing.html">Missing</a><a href="#absent">Absent</a></main></body></html>';
  fs.writeFileSync(path.join(directory,'index.html'),html);
  fs.writeFileSync(path.join(directory,'demo.html'),html);
  const errors = inspectDirectory(directory,{demo:{isPlaceholder:false}}).errors;
  assert.ok(errors.some(e => e.includes('missing or unsafe')));
  assert.ok(errors.some(e => e.includes('missing fragment')));
  fs.rmSync(directory,{recursive:true});
});

test('Documentation checker detects a missing local file', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(),'visionx-doc-test-'));
  fs.mkdirSync(path.join(directory,'docs'));
  fs.writeFileSync(path.join(directory,'docs','README.md'),'[Missing](/docs/not-here.md)\n');
  const errors = inspectMarkdownLinks(directory).errors;
  assert.ok(errors.some(e => e.includes('missing local link')));
  fs.rmSync(directory,{recursive:true});
});

