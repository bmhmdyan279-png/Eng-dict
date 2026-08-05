// بارگذاری Pagefind بعد از رندر صفحه
document.addEventListener("DOMContentLoaded", () => {
  if (window.__pagefind__) return;
  const base = document.querySelector('link[rel="canonical"]')?.href.replace(/\/+$/, '') + '/'
             || document.querySelector('meta[name="base"]')?.content
             || window.location.origin + '/';
  const script = document.createElement("script");
  script.type = "module";
  script.src = base + "pagefind/pagefind.js";
  script.onload = () => {
    window.__pagefind__ = window.pagefind;
    if (window.pagefind?.init) window.pagefind.init();
  };
  document.head.appendChild(script);
});
