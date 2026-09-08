/* Yayın paketindeki HTML JavaScript'lerini ve yerel varlık bağlantılarını
   tarayıcı açmadan doğrular. */
const fs = require('fs');
const path = require('path');

const roots = ['app/src/main/assets', 'web'];
const files = [];

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (entry.name.endsWith('.html')) files.push(full);
  }
}

for (const root of roots) walk(root);

let scripts = 0;
for (const file of files) {
  const html = fs.readFileSync(file, 'utf8');
  const tags = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
  let match;
  while ((match = tags.exec(html))) {
    if (!match[1].trim()) continue;
    try {
      new Function(match[1]);
      scripts++;
    } catch (error) {
      throw new Error(`${file} JavaScript: ${error.message}`);
    }
  }
}

for (const file of ['web/api-client.js', 'app/src/main/assets/api-client.js']) {
  if (!fs.existsSync(file)) throw new Error(`Eksik API istemcisi: ${file}`);
  try {
    new Function(fs.readFileSync(file, 'utf8'));
    scripts++;
  } catch (error) {
    throw new Error(`${file} JavaScript: ${error.message}`);
  }
}

const assetRoot = 'app/src/main/assets';
const missing = [];
for (const file of files.filter(item => item.startsWith(assetRoot))) {
  const html = fs.readFileSync(file, 'utf8');
  const links = /(?:src|href)=["']([^"']+)["']/gi;
  let match;
  while ((match = links.exec(html))) {
    const url = match[1];
    if (/^(?:https?:|data:|#|javascript:|mailto:|tel:)/.test(url) || url.includes('${')) continue;
    const clean = url.split(/[?#]/)[0];
    if (!clean) continue;
    const target = path.resolve(path.dirname(file), clean);
    if (!fs.existsSync(target)) missing.push(`${file} -> ${url}`);
  }
}

if (missing.length) throw new Error(`Eksik yerel varlıklar:\n${missing.join('\n')}`);

console.log(`HTML_JS_OK files=${files.length} scripts=${scripts}`);
console.log('LOCAL_ASSETS_OK');
