(function () {
    let lexiconData = null;
    let popup = null;

    function getSiteRoot() {
        const script = document.querySelector('script[src*="stepbible.js"]');
        if (script) {
            return script.src.replace(/assets\/stepbible\.js.*$/, '');
        }
        return '/szentiras-forditas/';
    }

    const SITE_ROOT = getSiteRoot();

    async function loadLexicon() {
        if (lexiconData) return lexiconData;
        try {
            const res = await fetch(SITE_ROOT + 'assets/lexicon.json');
            lexiconData = await res.json();
        } catch (e) {
            console.error('Lexicon betöltési hiba:', e);
            lexiconData = {};
        }
        return lexiconData;
    }

    function createPopup() {
        if (popup) return;
        popup = document.createElement('div');
        popup.id = 'step-popup';
        popup.innerHTML = `
            <div id="step-popup-header">
                <span id="step-popup-title"></span>
                <span id="step-popup-close" title="Bezárás">✕</span>
            </div>
            <div id="step-popup-body"></div>
        `;
        document.body.appendChild(popup);

        document.getElementById('step-popup-close').addEventListener('click', () => {
            popup.style.display = 'none';
        });

        document.addEventListener('click', (e) => {
            if (popup.style.display === 'block' && !popup.contains(e.target) && !e.target.classList.contains('heb-term')) {
                popup.style.display = 'none';
            }
        });
    }

    function formatRefLink(ref) {
        // ref format: "01-bereshit/01:5" -> url: SITE_ROOT + "tanakh/01-bereshit/01/"
        const [pathPart, verse] = ref.split(':');
        const label = pathPart.replace(/^\d+-/, '').replace('/', ' ') + ':' + verse;
        const url = `${SITE_ROOT}tanakh/${pathPart}/`;
        return `<a class="step-ref-link" href="${url}">${label}</a>`;
    }

    async function showPopup(term, targetEl) {
        createPopup();
        const data = await loadLexicon();
        const entry = data[term];

        const titleEl = document.getElementById('step-popup-title');
        const bodyEl = document.getElementById('step-popup-body');
        titleEl.textContent = term;

        if (!entry) {
            bodyEl.innerHTML = `<div>Részletes szótári bejegyzés előkészítés alatt.</div>`;
        } else {
            const translations = Object.entries(entry.t || {})
                .map(([hu, cnt]) => `<li><strong>${hu}</strong> (${cnt}x)</li>`)
                .join('');

            const refs = (entry.r || []).map(formatRefLink).join('');

            bodyEl.innerHTML = `
                <div class="step-badge">Előfordulás a Tanakhban: ${entry.c}x</div>
                <div class="step-section-title">Leggyakoribb fordítási alakok</div>
                <ul style="margin: 4px 0 8px 18px; padding: 0;">${translations || '<li>—</li>'}</ul>
                <div class="step-section-title">Konkordancia (igehelyek)</div>
                <div class="step-refs">${refs}</div>
            `;
        }

        popup.style.display = 'block';
        const rect = targetEl.getBoundingClientRect();
        let top = rect.bottom + 8;
        let left = rect.left;

        if (left + 350 > window.innerWidth) {
            left = Math.max(10, window.innerWidth - 355);
        }
        if (top + 260 > window.innerHeight) {
            top = Math.max(10, rect.top - 260);
        }

        popup.style.top = top + 'px';
        popup.style.left = left + 'px';
    }

    function enhanceHebrewTerms() {
        const article = document.querySelector('.md-content__inner');
        if (!article) return;

        // Megkeressük a <em> tag-eket, amelyek zárójelben vannak: (<em>hokhmáh</em>)
        const ems = article.querySelectorAll('p em, li em');
        ems.forEach(em => {
            const prev = em.previousSibling;
            const next = em.nextSibling;
            if (prev && next && prev.nodeType === 3 && next.nodeType === 3) {
                if (prev.textContent.endsWith('(') && next.textContent.startsWith(')')) {
                    const term = em.textContent.trim();
                    if (term.length > 1 && term.length <= 35 && !term.includes(':')) {
                        em.classList.add('heb-term');
                        em.title = 'Kattints a héber szóelemzéshez';
                        em.addEventListener('click', (e) => {
                            e.stopPropagation();
                            showPopup(term, em);
                        });
                    }
                }
            }
        });
    }

    document.addEventListener('DOMContentLoaded', enhanceHebrewTerms);
    // MkDocs Material instant navigation támogatás
    if (typeof document$ !== 'undefined') {
        document$.subscribe(enhanceHebrewTerms);
    }
})();
