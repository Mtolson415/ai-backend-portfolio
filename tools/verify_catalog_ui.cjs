// Verify the actual offline catalog's filtering logic in a minimal DOM harness.
// This checks JavaScript behavior; it is not visual browser or accessibility QA.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'docs/research/2026-11-11/catalog.html'), 'utf8');
const data = /<script id="catalog-data" type="application\/json">([\s\S]*?)<\/script>/.exec(html)[1];
const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)];
const elements = new Map();
function element() { return {value:'', textContent:'', innerHTML:'', options:[], events:{}, append(x){this.options.push(x)}, addEventListener(n,fn){this.events[n]=fn}}; }
const document = {getElementById(id){if(!elements.has(id))elements.set(id,element());return elements.get(id)}, createElement(){return element()}};
document.getElementById('catalog-data').textContent=data;
const context=vm.createContext({document});
vm.runInContext(scripts.at(-1)[1], context);
const get=id=>document.getElementById(id);
assert.equal(Number(get('count').textContent),181);
get('search').value='gvisor';get('search').events.input();
assert.equal(Number(get('count').textContent),1);
get('category').value='Document ingestion';get('category').events.change();
assert.equal(Number(get('count').textContent),0);
get('reset').events.click();
assert.equal(Number(get('count').textContent),181);
get('priority').value='Avoid-new';get('priority').events.change();
assert.equal(Number(get('count').textContent),2);
assert.equal(vm.runInContext('escapeText("<img>")',context),'&lt;img&gt;');
console.log('PASS: initial count, text search, combined filters, empty state, reset, archived filter and HTML escaping');
