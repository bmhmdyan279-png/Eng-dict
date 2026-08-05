#!/usr/bin/env python3
"""ارتقا به فاز ۲: نسخه‌بندی، Pagefind، PWA."""
from pathlib import Path

FILES = {
    "requirements.txt": """mkdocs-material==9.5.*
pyyaml==6.0.*
mike==2.1.*
""",

    "mkdocs.yml": """site_name: فرهنگ واژه‌های تخصصی بتن
site_description: فرهنگ لغت آنلاین واژه‌های تخصصی بتن
site_url: https://bmhmdyan279-png.github.io/Eng-dict/
repo_url: https://github.com/bmhmdyan279-png/Eng-dict
repo_name: bmhmdyan279-png/Eng-dict
site_dir: site

theme:
  name: material
  language: fa
  direction: rtl
  font:
    text: Vazirmatn
    code: Fira Code
  features:
    - search.suggest
    - search.highlight
    - search.share
    - navigation.top
    - navigation.footer
    - navigation.indexes
    - navigation.tabs
    - content.tabs.link
    - content.code.copy
    - content.action.edit
  palette:
    - scheme: default
      primary: teal
      accent: teal
      toggle:
        icon: material/brightness-7
        name: تاریک شود
    - scheme: slate
      primary: teal
      accent: teal
      toggle:
        icon: material/brightness-4
        name: روشن شود
  icon:
    repo: fontawesome/brands/github
  logo: assets/icon.svg
  favicon: assets/icon.svg

plugins:
  - search:
      lang: [fa, en]
  - offline:
      enabled: true

markdown_extensions:
  - tables
  - attr_list
  - def_list
  - admonition
  - pymdownx.details
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - toc:
      permalink: true

extra:
  version:
    provider: mike
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/bmhmdyan279-png/Eng-dict

extra_css:
  - assets/css/extra.css

extra_javascript:
  - { path: "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js", defer: true }
  - { path: "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js", defer: true }
  - { path: assets/js/math.js, defer: true }
  - { path: assets/js/pagefind.js, type: module }

nav:
  - خانه: index.md
  - واژه‌ها:
    - الفبایی: terms/index.md
    - دسته‌بندی: terms/categories.md
  - مشارکت: contribute.md
  - درباره: about.md
  - ارجاع: citation.md
""",

    "docs/assets/icon.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<rect width="100" height="100" rx="15" fill="#009688"/>
<text x="50" y="68" font-size="60" font-family="Vazirmatn, Arial" font-weight="bold" text-anchor="middle" fill="white">ب</text>
</svg>""",

    "docs/manifest.webmanifest": """{
  "name": "فرهنگ واژه‌های تخصصی بتن",
  "short_name": "بتن دیکت",
  "description": "فرهنگ لغت آنلاین واژه‌های تخصصی بتن",
  "start_url": "/Eng-dict/",
  "display": "standalone",
  "background_color": "#009688",
  "theme_color": "#009688",
  "dir": "rtl",
  "lang": "fa",
  "icons": [
    { "src": "assets/icon.svg", "sizes": "any", "type": "image/svg+xml" }
  ]
}""",

    "docs/assets/js/pagefind.js": """// بارگذاری Pagefind بعد از رندر صفحه
document.addEventListener("DOMContentLoaded", () => {
  if (window.__pagefind__) return;
  const base = document.querySelector('meta[name="base"]')?.content
             || document.querySelector('link[rel="canonical"]')?.href.replace(/\\/+$/, '') + '/';
  const script = document.createElement("script");
  script.type = "module";
  script.src = base + "pagefind/pagefind.js";
  script.onload = () => {
    window.__pagefind__ = window.pagefind;
    if (window.pagefind?.init) window.pagefind.init();
  };
  document.head.appendChild(script);
});
""",

    "scripts/build_pages.py": '''#!/usr/bin/env python3
"""ساخت صفحات Markdown از YAML (به‌روزشده برای فاز ۲)."""
import yaml
from pathlib import Path

def load_terms(p="data/terms.yaml"):
    with Path(p).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []

def term_md(t):
    fa = t.get("fa", t["id"])
    en = t.get("languages", {}).get("en", "")
    slug = t.get("slug", t["id"])
    langs = t.get("languages", {})
    cat = t.get("category", "—")
    defn = t.get("definition", "").strip()
    stds = t.get("standards", [])
    rel = t.get("related", [])
    src = t.get("source", "")
    upd = t.get("last_updated", "")

    L = [f"---", f"title: {fa}", f"description: تعریف {fa} در فرهنگ بتن",
         f"keywords: [{', '.join([fa, en, cat])}]", f"---", "",
         f"# {fa}{f' / {en}' if en else ''}", ""]

    aliases = t.get("aliases", [])
    if aliases:
        L.append(f"**هم‌نام‌ها:** {'، '.join(aliases)}\n")

    if langs:
        L += ["## معادل‌ها", "", "| زبان | معادل |", "|------|-------|"]
        names = {"en":"انگلیسی","fr":"فرانسوی","de":"آلمانی","ar":"عربی","tr":"ترکی","ru":"روسی","es":"اسپانیایی"}
        for c, v in langs.items():
            L.append(f"| {names.get(c, c.upper())} | {v} |")
        L.append("")

    if defn:
        L += ["## تعریف", "", defn, ""]

    L += [f"## دسته", "", f"`{cat}`", ""]

    if stds:
        L += ["## استانداردهای مرتبط", ""]
        for s in stds: L.append(f"- `{s}`")
        L.append("")

    if rel:
        L += ["## واژه‌های مرتبط", ""]
        for r in rel: L.append(f"- [{r}](./{r}.md)")
        L.append("")

    if src or upd:
        L += ["## اطلاعات تکمیلی", ""]
        if src: L.append(f"- **منبع:** `{src}`")
        if upd: L.append(f"- **به‌روزرسانی:** {upd}")
        L.append("")

    L += ["---", "", '??? info "نحوهٔ ارجاع"', "",
          f"    فرهنگ واژه‌های تخصصی بتن، مدخل «{fa}»، {upd}.", ""]
    return "\\n".join(L)

def alpha_idx(terms):
    L = ["---", "title: فهرست الفبایی", "---", "",
         "# فهرست الفبایی واژه‌ها", "",
         "همهٔ واژه‌ها به ترتیب الفبای فارسی.", ""]
    by_l = {}
    for t in terms:
        fa = t.get("fa", t["id"])
        by_l.setdefault(fa[0] if fa else "?", []).append((fa, t.get("slug", t["id"])))
    alphabet = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
    letters = sorted(by_l.keys(), key=lambda x: alphabet.index(x) if x in alphabet else 999)
    L.append("**پرش به حرف:** " + " · ".join(f"[{l}](#{l})" for l in letters) + "\\n")
    for l in letters:
        L += [f"## <a name='{l}'></a>{l}", ""]
        for fa, s in sorted(by_l[l]): L.append(f"- [{fa}](./{s}.md)")
        L.append("")
    return "\\n".join(L)

def cat_idx(terms):
    L = ["---", "title: دسته‌بندی", "---", "", "# واژه‌ها بر اساس دسته", ""]
    by_c = {}
    for t in terms: by_c.setdefault(t.get("category","سایر"), []).append(t)
    for c, ts in sorted(by_c.items()):
        L += [f"## {c}", ""]
        for t in sorted(ts, key=lambda x: x.get("fa","")):
            L.append(f"- [{t['fa']}](./{t.get('slug',t['id'])}.md)")
        L.append("")
    return "\\n".join(L)

def main():
    d = Path("docs/terms"); d.mkdir(parents=True, exist_ok=True)
    terms = load_terms()
    print(f"Loaded {len(terms)} terms.")
    for t in terms:
        p = d / f"{t.get('slug', t['id'])}.md"
        p.write_text(term_md(t), encoding="utf-8")
        print(f"  ✅ {p}")
    (d/"index.md").write_text(alpha_idx(terms), encoding="utf-8")
    print("  ✅ docs/terms/index.md")
    (d/"categories.md").write_text(cat_idx(terms), encoding="utf-8")
    print("  ✅ docs/terms/categories.md")

if __name__ == "__main__":
    main()
''',

    ".github/workflows/deploy.yml": """name: Deploy
on:
  push:
    branches: [main, master]
  workflow_dispatch:
permissions:
  contents: write
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: false
jobs:
  build-deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deploy.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Generate Markdown pages
        run: python scripts/build_pages.py

      - name: Configure Git
        run: |
          git config user.name github-actions[bot]
          git config user.email github-actions[bot]@users.noreply.github.com

      - name: Build and deploy with mike (v1)
        run: mike deploy --push --update-aliases v1 latest --deploy-prefix .

      - name: Copy Pagefind assets into versioned dirs
        run: |
          cp -r docs/manifest.webmanifest site/ 2>/dev/null || true

      - name: Build Pagefind index
        run: |
          npx pagefind --site site --output-subdir pagefind
          # برای نسخه‌بندی mike، باید در ریشه باشد
          if [ -d "site/pagefind" ]; then
            echo "✅ Pagefind index built"
          fi

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./site

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
        id: deploy
""",
}

# فایل‌هایی که باید اضافه شوند (نه بازنویسی)
ADD_ONLY = [
    "data/terms.yaml",
    "scripts/build_pages.py",  # will overwrite, but listed for clarity
]

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 ارتقا به فاز ۲: نسخه‌بندی + Pagefind + PWA")
    print("=" * 60)
    for path, content in FILES.items():
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        print(f"✅ {path}")

    # manifest باید در docs باشد تا توسط mkdocs کپی شود
    print("\n📝 نکات مهم:")
    print("1. پوشهٔ .cache را به .gitignore اضافه کنید.")
    print("2. با اولین push، mike نسخهٔ v1 را خودکار می‌سازد.")
    print("=" * 60)