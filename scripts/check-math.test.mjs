import assert from 'node:assert/strict';
import test from 'node:test';
import markdownToHtml from 'zenn-markdown-html';
import { load } from 'cheerio';
import { renderMath } from './check-math.mjs';

test('Zenn macro and Japanese text with a mathematical sigma render', () => {
  assert.match(renderMath(String.raw`\RR\text{ 上の }\sigma\text{-代数}`, true), /class="katex"/);
});

test('unknown commands and unsupported text glyphs fail', () => {
  for (const tex of [String.raw`\notARealMathCommand`, String.raw`\text{σ}`]) {
    assert.throws(() => renderMath(tex, false));
  }
});

test('a formula inside a closed answer is still checked', async () => {
  const $ = load(await markdownToHtml(':::details 解答\n$$\n\\notARealMathCommand\n$$\n:::'));
  assert.equal($('details:not([open]) embed-katex').length, 1);
  const formula = $('embed-katex');
  assert.throws(() => renderMath(formula.text(), formula.attr('display-mode') === '1'));
});
