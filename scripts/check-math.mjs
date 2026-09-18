import katex from 'katex';

// Zenn's embed-katex options, with invalid or unsupported notation rejected.
export function renderMath(tex, displayMode) {
  return katex.renderToString(tex, {
    displayMode,
    macros: { '\\RR': '\\mathbb{R}' },
    throwOnError: true,
    strict: 'error',
  });
}
