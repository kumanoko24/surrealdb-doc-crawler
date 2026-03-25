() => {
  // ── helpers ────────────────────────────────────────────────────────────────

  function md(node, depth) {
    if (!node) return '';
    depth = depth || 0;

    if (node.nodeType === 3) return node.textContent;
    if (node.nodeType !== 1) return '';

    const tag = node.tagName.toLowerCase();

    // skip non-content elements
    if (['script','style','noscript','svg','iframe'].includes(tag)) return '';

    const role = (node.getAttribute('role') || '').toLowerCase();
    const cls  = (node.className && typeof node.className === 'string')
                 ? node.className.toLowerCase() : '';
    const id   = (node.id || '').toLowerCase();

    if (['nav','header','footer'].includes(tag)) return '';
    if (role === 'navigation' || role === 'banner' || role === 'contentinfo') return '';
    if (/sidebar|breadcrumb|pagination|toc\b|table-of-content/.test(cls)) return '';
    if (/sidebar|breadcrumb|pagination/.test(id)) return '';

    const kids = () => Array.from(node.childNodes).map(c => md(c, depth)).join('');

    // ── block elements ───────────────────────────────────────────────────────
    if (/^h[1-6]$/.test(tag)) {
      const level = tag[1];
      return '\n' + '#'.repeat(level) + ' ' + node.textContent.trim() + '\n\n';
    }

    if (tag === 'pre') {
      const codeEl = node.querySelector('code');
      const langCls = codeEl ? codeEl.className : '';
      const langM   = langCls.match(/language-([\w-]+)/);
      const lang    = langM ? langM[1] : '';
      return '\n```' + lang + '\n' + node.innerText + '\n```\n';
    }

    if (tag === 'code') {
      if (!node.closest('pre')) return '`' + node.textContent + '`';
      return node.textContent;
    }

    if (tag === 'p')  return '\n' + kids().trim() + '\n';
    if (tag === 'br') return '\n';
    if (tag === 'hr') return '\n---\n';

    if (tag === 'strong' || tag === 'b') return '**' + node.textContent.trim() + '**';
    if (tag === 'em'     || tag === 'i') return '*'  + node.textContent.trim() + '*';

    if (tag === 'blockquote') {
      return '\n' + node.textContent.trim().split('\n').map(l => '> '+l).join('\n') + '\n';
    }

    if (tag === 'ul') {
      return '\n' + Array.from(node.querySelectorAll(':scope > li'))
        .map(li => '- ' + li.innerText.trim().replace(/\n+/g,' '))
        .join('\n') + '\n';
    }
    if (tag === 'ol') {
      return '\n' + Array.from(node.querySelectorAll(':scope > li'))
        .map((li,i) => (i+1)+'. ' + li.innerText.trim().replace(/\n+/g,' '))
        .join('\n') + '\n';
    }

    if (tag === 'table') {
      const rows = Array.from(node.querySelectorAll('tr'));
      if (!rows.length) return '';
      const hdrs = Array.from(rows[0].querySelectorAll('th,td'))
                       .map(c => c.innerText.trim().replace(/\n/g,' '));
      let t = '\n| ' + hdrs.join(' | ') + ' |\n';
      t    += '| ' + hdrs.map(()=>'---').join(' | ') + ' |\n';
      for (let i = 1; i < rows.length; i++) {
        const cells = Array.from(rows[i].querySelectorAll('td'))
                          .map(c => c.innerText.trim().replace(/\n/g,' '));
        if (cells.length) t += '| ' + cells.join(' | ') + ' |\n';
      }
      return t + '\n';
    }

    if (tag === 'a') {
      const href = node.getAttribute('href') || '';
      const text = node.textContent.trim();
      if (!text) return '';
      if (href && !href.startsWith('#') && text !== href) return '['+text+']('+href+')';
      return text;
    }

    return kids();
  }

  // ── find main content ──────────────────────────────────────────────────────
  const root = document.querySelector('article')
            || document.querySelector('main')
            || document.body;

  const raw     = md(root);
  const content = raw.replace(/\n{4,}/g, '\n\n\n').trim();

  // ── collect all in-scope links ─────────────────────────────────────────────
  const links = Array.from(document.querySelectorAll('a[href]'))
    .map(a => {
      let h = a.getAttribute('href') || '';
      h = h.split('#')[0];
      if (!h) return null;
      if (h.startsWith('https://surrealdb.com')) h = h.slice('https://surrealdb.com'.length);
      if (!h.startsWith('/docs/surrealql')) return null;
      return h.replace(/\/+$/, '') || '/docs/surrealql';
    })
    .filter(Boolean);

  const title = (document.querySelector('h1') || {textContent:''}).textContent.trim()
             || document.title;

  return { title, content, links: [...new Set(links)] };
}
