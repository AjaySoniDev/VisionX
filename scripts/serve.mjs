import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../public');
const config = JSON.parse(fs.readFileSync(path.resolve(root,'../vercel.json'),'utf8'));
const port = Number(process.env.PORT || 4174);
const types = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.jpeg':'image/jpeg','.jpg':'image/jpeg','.webp':'image/webp','.webm':'video/webm','.json':'application/json; charset=utf-8','.csv':'text/csv; charset=utf-8','.xml':'application/xml; charset=utf-8','.md':'text/plain; charset=utf-8','.py':'text/plain; charset=utf-8','.txt':'text/plain; charset=utf-8'};
const server = http.createServer((request,response) => {
  for (const header of config.headers[0].headers) if (header.key !== 'Content-Security-Policy') response.setHeader(header.key,header.value);
  // frame-ancestors is an HTTP header directive; apply the same deployment CSP.
  response.setHeader('Content-Security-Policy',config.headers[0].headers.find(h => h.key === 'Content-Security-Policy').value);
  try {
    const pathname = decodeURIComponent(new URL(request.url,'http://localhost').pathname);
    const candidate = path.resolve(root,'.' + (pathname === '/' ? '/index.html' : pathname));
    if (!candidate.startsWith(root + path.sep) || path.basename(candidate).startsWith('.')) { response.writeHead(403); response.end('Forbidden'); return; }
    const exists = fs.existsSync(candidate) && fs.statSync(candidate).isFile();
    const target = exists ? candidate : path.join(root,'404.html');
    response.writeHead(exists ? 200 : 404, {'Content-Type':types[path.extname(target)] || 'application/octet-stream'});
    if (request.method === 'HEAD') response.end(); else fs.createReadStream(target).pipe(response);
  } catch { response.writeHead(400); response.end('Bad request'); }
});
server.listen(port,'127.0.0.1',() => console.log(`VisionX preview: http://127.0.0.1:${port}`));
