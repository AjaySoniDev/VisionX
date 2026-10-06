import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export function validatedDemoUrl(value) {
  const url = new URL(value);
  if (url.protocol !== 'https:' || !['youtube.com','www.youtube.com','youtu.be'].includes(url.hostname) || url.username || url.password) throw new Error('Use an HTTPS YouTube URL');
  const id = url.hostname === 'youtu.be' ? url.pathname.slice(1) : url.searchParams.get('v') || url.pathname.match(/^\/(?:shorts|live)\/([^/]+)$/)?.[1];
  if (!id || !/^[A-Za-z0-9_-]{11}$/.test(id)) throw new Error('Use a specific video with an 11-character YouTube ID');
  return `https://www.youtube.com/watch?v=${id}`;
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const [value,title,credit] = process.argv.slice(2);
  if (!value || !title || !credit) throw new Error('Usage: npm run set:demo -- URL "Recording title" "Recording owner"');
  const file = path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../site.config.json');
  const config = JSON.parse(fs.readFileSync(file,'utf8'));
  config.demo = {url:validatedDemoUrl(value),title,credit,isPlaceholder:false,note:'Project recording supplied by the owner. Review its device, input and source provenance with the accompanying evidence.'};
  fs.writeFileSync(file,JSON.stringify(config,null,2)+'\n');
  console.log('Demo configuration updated. Run npm run build to refresh demo.html.');
}
