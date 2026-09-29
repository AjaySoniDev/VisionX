import fs from 'node:fs';import path from 'node:path';
const root=path.resolve(process.cwd());const pages=['index.html','business.html','references.html','404.html'];let bad=[];
for(const p of pages){const s=fs.readFileSync(path.join(root,p),'utf8');for(const m of s.matchAll(/(?:href|src)="([^"#]+)"/g)){const u=m[1];if(/^https?:|^mailto:|^data:/.test(u))continue;const local=u.startsWith('/')?u.slice(1):path.join(path.dirname(p),u);if(local && !fs.existsSync(path.join(root,local)))bad.push(`${p}: ${u}`)}}
if(bad.length){console.error('Broken local references:\n'+bad.join('\n'));process.exit(1)}console.log('Static integrity check passed.');
