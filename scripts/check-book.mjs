import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile, readdir, mkdir, writeFile, access } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import markdownToHtml from 'zenn-markdown-html';
import { load } from 'cheerio';

// Check the manuscript with the same official renderer version as Zenn CLI.
// Image meaning and browser interactions still need human inspection.
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const book = path.join(root, 'books/lean4-formalization');
const output = path.join(root, 'lean/.generated/book-display');
const read = p => readFile(p, 'utf8');
const digest = s => createHash('sha256').update(s).digest('hex');
await mkdir(output, { recursive: true });
const config = await read(path.join(book, 'config.yaml'));
const chapters = [...config.split('\nchapters:\n')[1].matchAll(/^  - (\w+)$/gm)].map(m => m[1]);
assert.equal(new Set(chapters).size, chapters.length, 'duplicate chapter');
assert.deepEqual((await readdir(book)).filter(f => f.endsWith('.md')).sort(), chapters.map(c => c + '.md').sort());
const index = JSON.parse(await read(path.join(root, 'lean/catalog/index.json')));
const rows = (await Promise.all(index.block_files.map(f => read(path.join(root, 'lean/catalog', f)).then(JSON.parse)))).flat();
const labels = { complete: '完成例・確認コマンド', fragment: '断片', expected_error: '意図的なエラー例', unfinished: '未完成の骨格・練習問題', excerpt: '説明用の抜粋' };
const results = [];
const errors = [];
for (const chapter of chapters) {
  const source = `books/lean4-formalization/${chapter}.md`;
  const text = await read(path.join(root, source));
  const check = (condition, message) => { if (!condition) errors.push(`${chapter}: ${message}`); };
  const chapterRows = rows.filter(r => r.source === source);
  const body = text.replace(/^---\n[\s\S]*?\n---\n/, '');
  let fence = null;
  let number = 0;
  let details = 0;
  let messages = 0;
  const containers = [];
  for (const line of body.split('\n')) {
    const f = line.match(/^(`{3,}|~{3,})(.*)$/);
    if (f) {
      if (fence) { if (f[1][0] === fence[0] && f[1].length >= fence.length && !f[2].trim()) fence = null; }
      else {
        fence = f[1];
        if (f[2].startsWith('lean')) {
          const row = chapterRows[number++];
          check(row && f[2] === `lean:${labels[row.category]}`, `code label ${number} differs from catalog`);
        }
      }
      continue;
    }
    if (fence) continue;
    const c = line.match(/^(:{3,})(.*)$/);
    if (c) {
      const tail = c[2].trim();
      if (/^(details|message)( |$)/.test(tail)) {
        const kind = tail.split(' ')[0];
        containers.push({ kind, size: c[1].length });
        if (kind === 'details') details++; else messages++;
      } else {
        const current = containers.pop();
        check(!tail && current && current.size === c[1].length, 'unbalanced Zenn container');
      }
    }
    check(!/<\/?(?:details|summary)>/.test(line), 'raw HTML details remain');
    check(!/^#+ \d+\.X\b/.test(line), 'temporary section number remains');
  }
  check(!fence && !containers.length, 'unclosed fence or container');
  check(number === chapterRows.length, 'Lean block count differs');
  const html = await markdownToHtml(body);
  await writeFile(path.join(output, chapter + '.html'), html);
  const $ = load(html);
  check($('details').length === details, 'rendered details count differs');
  check($('details > summary').length === details, 'missing summary');
  check($('.msg').length === messages, 'rendered message count differs');
  check(!html.includes('&lt;details'), 'escaped details in output');
  const images = [];
  for (const img of $('img').toArray()) {
    const src = $(img).attr('src');
    check(!!$(img).attr('alt')?.trim(), 'image alt is empty');
    const caption = $(img).parent().find('em').text();
    check(/^図\d+-\d+：/.test(caption), `missing numbered caption for ${src}`);
    if (src.startsWith('/images/')) {
      try { await access(path.join(root, src)); } catch { check(false, `missing image ${src}`); }
    } else check(/^https:\/\//.test(src), `unsupported image path ${src}`);
    images.push({ src, alt: $(img).attr('alt'), caption });
  }
  const links = [];
  for (const link of $('a[href]').toArray()) {
    const href = $(link).attr('href');
    if (/^(https?:|mailto:)/.test(href)) continue;
    if (href.startsWith('#')) {
      check($('[id]').toArray().some(n => decodeURIComponent($(n).attr('id')) === decodeURIComponent(href.slice(1))), `missing anchor ${href}`);
    } else {
      check(chapters.includes(href), `unknown chapter link ${href}`);
      links.push(href);
    }
  }
  const prose = $.root().clone();
  prose.find('pre, code, embed-katex').remove();
  check(!prose.text().includes('**'), 'unrendered bold markup');
  results.push({ source, sha256: digest(text), lean_blocks: number, details, messages, math_expressions: $('embed-katex').length, images, chapter_links: links });
}
const report = {
  status: errors.length ? 'failed' : 'passed',
  renderer: JSON.parse(await read(path.join(root, 'node_modules/zenn-markdown-html/package.json'))).version,
  cli: JSON.parse(await read(path.join(root, 'node_modules/zenn-cli/package.json'))).version,
  node: process.version,
  config_sha256: digest(config),
  scope: 'Source structure and official HTML rendering. Browser display, remote image loading and deployed chapter navigation require separate checks.',
  chapters: results, errors,
};
await writeFile(path.join(output, 'report.json'), JSON.stringify(report, null, 2) + '\n');
const total = key => results.reduce((sum, r) => sum + r[key], 0);
console.log(JSON.stringify({ status: report.status, chapters: results.length, lean_blocks: total('lean_blocks'), details: total('details'), messages: total('messages'), images: results.reduce((s,r)=>s+r.images.length,0), chapter_links: results.reduce((s,r)=>s+r.chapter_links.length,0), errors }, null, 2));
if (errors.length) process.exitCode = 1;
