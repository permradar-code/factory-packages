// Paste into the Gemini tab with javascript_tool (once per page load; the SPA keeps it across "new chat").
// Patch: keeps <input type=file> in the page instead of opening the native dialog; helpers for the image queue.
// NOTE: javascript_tool times out after 45 s per call -> START() is non-blocking, WAIT(ms<=40000) polls.
(() => {
  const o = HTMLInputElement.prototype.click;
  HTMLInputElement.prototype.click = function () {
    if (this.type === 'file') { this.id = 'cc_file_input'; this.style.cssText = 'position:fixed;top:0;left:0;width:20px;height:20px;opacity:0.01;z-index:99999'; document.body.appendChild(this); return; }
    return o.apply(this, arguments);
  };
  window.showOpenFilePicker = async () => { throw new DOMException('blocked', 'AbortError'); };
  window.sleep = ms => new Promise(r => setTimeout(r, ms));
  // generated images have alt "..., создано искусственным интеллектом"
  window.gimgs = () => [...document.querySelectorAll('img')].filter(i => /создано искусственным/.test(i.alt || ''));
  window.READY = () => { const g = gimgs(); if (!g.length) return false; return g[g.length - 1].getBoundingClientRect().width > 200; };
  // scroll the newest image to the top; returns click coordinates: download icon (x,y) and image centre (cx,cy) for the hover
  window.POS = async () => { const g = gimgs(); if (!g.length) return { err: 'no images' }; const im = g[g.length - 1]; im.scrollIntoView({ block: 'start' }); await sleep(900); const r = im.getBoundingClientRect(); return { x: Math.round(r.right - 30), y: Math.round(r.top + 30), cx: Math.round(r.left + r.width / 2), cy: Math.round(r.top + r.height / 2), n: g.length }; };
  // Q = queue loaded from _variants/queue_images.json (built by tools/build_queue.py) through the PQ file input
  window.START = (id) => { const it = Q.find(x => x.id === id); if (!it) return 'no item'; window.__res = null; window.__t0 = Date.now();
    (async () => { await sleep(4000); const before = gimgs().length; const ed = document.querySelector('.ql-editor'); ed.focus(); document.execCommand('selectAll'); document.execCommand('insertText', false, it.prompt); await sleep(900);
      const send = [...document.querySelectorAll('button')].find(b => /Отправ/i.test(b.getAttribute('aria-label') || '')); if (!send) { window.__res = { err: 'no send button' }; return; } send.click();
      const t0 = Date.now(); while (!(gimgs().length > before && READY())) { if (Date.now() - t0 > 420000) { window.__res = { err: 'timeout' }; return; } await sleep(2000); }
      await sleep(2500); window.__res = await POS(); window.__res.id = id; })();
    return 'started ' + id; };
  window.WAIT = async (ms = 38000) => { const t0 = Date.now(); while (!window.__res && Date.now() - t0 < ms) await sleep(1500); return JSON.stringify(window.__res || { pending: true, s: Math.round((Date.now() - window.__t0) / 1000) }); };
  // smallest visible element whose label/text matches re -> centre coordinates (to click with the computer tool)
  window.FIND = (re) => { const els = [...document.querySelectorAll('button,[role=menuitem],[role=option],[role=menuitemcheckbox],div,span')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.width < 500 && re.test(((e.getAttribute('aria-label') || '') + ' ' + (e.innerText || '')).trim()) && (e.innerText || '').length < 60; }); els.sort((a, b) => a.getBoundingClientRect().width * a.getBoundingClientRect().height - b.getBoundingClientRect().width * b.getBoundingClientRect().height); const e = els[0]; if (!e) return null; const r = e.getBoundingClientRect(); return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2) }; };
  // file input for the prompt queue (upload _variants/queue_images.json into it, then await LOADQ())
  const i = document.createElement('input'); i.type = 'file'; i.id = 'PQ'; i.setAttribute('aria-label', 'PROMPT_QUEUE_INPUT'); i.style.cssText = 'position:fixed;top:30px;left:0;width:20px;height:20px;opacity:0.01;z-index:99999'; document.body.appendChild(i);
  window.LOADQ = async () => { const f = i.files[0]; if (!f) return 'no file'; window.Q = JSON.parse(await f.text()); return 'loaded ' + window.Q.length; };
})();
