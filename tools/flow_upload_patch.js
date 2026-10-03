// Run in the Flow tab with javascript_tool BEFORE clicking "Загрузить".
// Prevents the native Windows file dialog (which freezes the tab): the <input type=file> is kept on the page instead.
// Then: find "cc_file_input file input" -> ref, and call file_upload(paths, ref). Lost on page reload.
(() => {
  const o = HTMLInputElement.prototype.click;
  HTMLInputElement.prototype.click = function () {
    if (this.type === 'file') {
      this.id = 'cc_file_input';
      this.style.cssText = 'position:fixed;top:0;left:0;width:20px;height:20px;opacity:0.01;z-index:99999';
      document.body.appendChild(this);
      window.__cc_captured = true;
      return;
    }
    return o.apply(this, arguments);
  };
  if (window.showOpenFilePicker) {
    window.showOpenFilePicker = async () => { window.__cc_showpicker = true; throw new DOMException('blocked', 'AbortError'); };
  }
  return 'patched';
})()
