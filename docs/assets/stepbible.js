(function () {
    let lexiconData = null;
    let popup = null;

    function getSiteRoot() {
        const script = document.querySelector('script[src*="stepbible.js"]');
        return script ? script.src.replace(/assets\/stepbible\.js.*$/, '') : '/szentiras-forditas/';
    }

    async function loadLexicon() {
        if (lexiconData) return lexiconData;
        try {
            const res = await fetch(getSiteRoot() + 'assets/lexicon.json');
            lexiconData = await res.json();
        } catch (e) {
            lexiconData = {};
        }
        return lexiconData;
    }

    function createPopup() {
        if (popup) return;
        popup = document.createElement('div');
        popup.id = 'step-popup';
        popup.innerHTML = `<div id="step-popup-header"><span id="step-popup-title"></span><span id="step-popup-close">✕</span></div><div id="step-popup-body"></div>`;
        document.body.appendChild(popup);
        document.getElementById('step-popup-close').onclick = () => popup.style.display = 'none';
        document.addEventListener('click', (e) => {
            if (popup.style.display === 'block' && !popup.contains(e.target) && !e.target.classList.contains('heb-term')) {
                popup.style.display = 'none';
            }
        });
    }

    async function showPopup(term, targetEl) {
        createPopup();
        const data = await loadLexicon();
        const entry = data[term];
        const titleEl = document.getElementById('step-popup-title');
        const bodyEl = document.getElementById('step-popup-body');

        if (!entry) {
            titleEl.textContent = term;
            bodyEl.innerHTML = `<div>Szótári adat előkészítés alatt.</div>`;
        } else {
            const heb = entry.h ? `<span style="font-size:1.25rem;font-style:normal;margin-right:6px;">${entry.h}</span>` : '';
            const code = entry.s ? `<span style="font-size:0.75rem;font-style:normal;background:var(--md-primary-fg-color,#4051b5);color:#fff;padding:1px 6px;border-radius:4px;margin-left:6px;">${entry.s}</span>` : '';
            titleEl.innerHTML = `${heb}${term}${code}`;

            const def = entry.d ? `<div style="font-size:0.8rem;margin-bottom:8px;padding:6px 8px;background:var(--md-code-bg-color,#f5f5f5);border-radius:4px;"><strong>Strong gyök:</strong> ${entry.d}</div>` : '';
            const tr = Object.entries(entry.t || {}).map(([hu, c]) => `<li><strong>${hu}</strong> (${c}x)</li>`).join('');
            const root = getSiteRoot();
            const refs = (entry.r || []).map(r => {
                const [p, v] = r.split(':');
                return `<a class="step-ref-link" href="${root}tanakh/${p}/">${p.replace(/^\d+-/, '').replace('/', ' ')}:${v}</a>`;
            }).join('');

            bodyEl.innerHTML = `<div class="step-badge">Előfordulás: ${entry.c}x</div>${def}<div class="step-section-title">Fordítási alakok</div><ul style="margin:4px 0 8px 18px;padding:0;">${tr || '<li>—</li>'}</ul><div class="step-section-title">Konkordancia</div><div class="step-refs">${refs}</div>`;
        }

        popup.style.display = 'block';
        const rect = targetEl.getBoundingClientRect();
        popup.style.top = Math.min(window.innerHeight - 280, Math.max(10, rect.bottom + 8)) + 'px';
        popup.style.left = Math.min(window.innerWidth - 355, Math.max(10, rect.left)) + 'px';
    }

    function enhance() {
        const article = document.querySelector('.md-content__inner');
        if (!article) return;
        article.querySelectorAll('p em, li em').forEach(em => {
            if (em.dataset.enhanced) return;
            const prev = em.previousSibling, next = em.nextSibling;
            if (prev && next && prev.nodeType === 3 && next.nodeType === 3 && prev.textContent.endsWith('(') && next.textContent.startsWith(')')) {
                const term = em.textContent.trim();
                if (term.length > 1 && term.length <= 35 && !term.includes(':')) {
                    em.dataset.enhanced = '1';
                    em.classList.add('heb-term');
                    em.onclick = (e) => { e.stopPropagation(); showPopup(term, em); };
                }
            }
        });
    }

    document.addEventListener('DOMContentLoaded', enhance);
    if (typeof document$ !== 'undefined') document$.subscribe(enhance);
})();
