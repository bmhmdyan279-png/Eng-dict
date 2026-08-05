#!/usr/bin/env python3
"""
ارتقا به فاز ۲ + تبدیل به فرهنگ عمومی مهندسی (بدون محدودیت بتن)
نسخه‌بندی mike، جست‌وجوی Pagefind، PWA
"""

from pathlib import Path
import sys

# ------------------------- تنظیمات -------------------------
# این مقادیر را می‌توانید بعداً هم تغییر دهید
SITE_NAME = "فرهنگ واژه‌های تخصصی مهندسی"
SITE_DESC = "فرهنگ لغت آنلاین و چندزبانهٔ واژه‌های فنی و مهندسی"
SHORT_NAME = "EngDict"
REPO_USER = "bmhmdyan279-png"
REPO_NAME = "Eng-dict"
SITE_URL = f"https://{REPO_USER}.github.io/{REPO_NAME}/"
REPO_URL = f"https://github.com/{REPO_USER}/{REPO_NAME}"

# ------------------------- محتوای فایل‌ها -------------------------
FILES = {
    "requirements.txt": """mkdocs-material==9.5.*
pyyaml==6.0.*
mike==2.1.*
""",

    "mkdocs.yml": f'''site_name: {SITE_NAME}
site_description: {SITE_DESC}
site_url: {SITE_URL}
repo_url: {REPO_URL}
repo_name: {REPO_USER}/{REPO_NAME}
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
      link: {REPO_URL}

extra_css:
  - assets/css/extra.css

extra_javascript:
  - {{ path: "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js", defer: true }}
  - {{ path: "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js", defer: true }}
  - {{ path: assets/js/math.js, defer: true }}
  - {{ path: assets/js/pagefind.js, type: module }}

nav:
  - خانه: index.md
  - واژه‌ها:
    - الفبایی: terms/index.md
    - دسته‌بندی: terms/categories.md
  - مشارکت: contribute.md
  - درباره: about.md
  - ارجاع: citation.md
''',

    "docs/assets/icon.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<rect width="100" height="100" rx="15" fill="#009688"/>
<text x="50" y="68" font-size="60" font-family="Vazirmatn, Arial" font-weight="bold" text-anchor="middle" fill="white">م</text>
</svg>''',

    "docs/manifest.webmanifest": f'''{{
  "name": "{SITE_NAME}",
  "short_name": "{SHORT_NAME}",
  "description": "{SITE_DESC}",
  "start_url": "/{REPO_NAME}/",
  "display": "standalone",
  "background_color": "#009688",
  "theme_color": "#009688",
  "dir": "rtl",
  "lang": "fa",
  "icons": [
    {{ "src": "assets/icon.svg", "sizes": "any", "type": "image/svg+xml" }}
  ]
}}''',

    "docs/assets/js/pagefind.js": """// بارگذاری Pagefind بعد از رندر صفحه
document.addEventListener("DOMContentLoaded", () => {
  if (window.__pagefind__) return;
  const base = document.querySelector('link[rel="canonical"]')?.href.replace(/\\/+$/, '') + '/'
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
""",

    "data/terms.yaml": """\
# فرهنگ واژه‌های تخصصی مهندسی — داده‌های اولیه
# می‌توانید هر رشته‌ای را اضافه کنید: عمران، مکانیک، برق، شیمی و...

- id: concrete
  fa: بتن
  slug: beton
  aliases: [Concrete, Béton]
  languages:
    en: Concrete
    fr: Béton
    de: Beton
    ar: خرسانة
  category: مهندسی عمران
  definition: >
    بتن مخلوطی از سیمان، سنگ‌دانه، آب و افزودنی‌هاست که پس از گیرش سخت می‌شود.
  standards: [ASTM C94, EN 206, ISIRI 3892]
  related: [cement, rebar]
  status: approved
  source: book-v1
  last_updated: "2026-08-05"
  contributors: [بنیان‌گذار]

- id: cement
  fa: سیمان
  slug: siman
  aliases: [Cement, Ciment]
  languages:
    en: Cement
    fr: Ciment
    de: Zement
    ar: الأسمنت
  category: مهندسی عمران
  definition: >
    سیمان مادهٔ چسباننده‌ای است که در مجاورت آب سخت می‌شود و اجزای بتن را به هم می‌چسباند.
  standards: [ASTM C150, EN 197-1]
  related: [concrete]
  status: approved

- id: rebar
  fa: آرماتور
  slug: armator
  aliases: [Rebar, Armature, میلگرد]
  languages:
    en: Rebar
    fr: Armature
    de: Bewehrung
    ar: حديد التسليح
  category: مهندسی عمران
  definition: >
    میلگرد فولادی که برای افزایش مقاومت کششی بتن به کار می‌رود.
  standards: [ASTM A615, ISIRI 3132]
  related: [concrete]
  status: approved

# نمونه واژه از رشته‌های دیگر (می‌توانید اضافه کنید)
- id: torque
  fa: گشتاور
  slug: gashtavar
  aliases: [Torque, Moment]
  languages:
    en: Torque
    fr: Couple
    de: Drehmoment
    ar: عزم الدوران
  category: مهندسی مکانیک
  definition: >
    گشتاور یا ممان، عاملی است که باعث چرخش یک جسم حول محور می‌شود.
  standards: [ISO 80000-4]
  related: [force]
  status: approved
""",

    "scripts/build_pages.py": '''#!/usr/bin/env python3
"""ساخت صفحات Markdown از YAML (به‌روز شده برای فاز ۲)."""
import yaml
from pathlib import Path

def load_terms(path="data/terms.yaml"):
    with Path(path).open("r", encoding="utf-8") as f:
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

    L = [f"---", f"title: {fa}", f"description: تعریف {fa} در فرهنگ مهندسی",
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
          f"    {SITE_NAME}، مدخل «{fa}»، {upd}.", ""]
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

SITE_NAME = "{SITE_NAME}"  # injected

def main():
    d = Path("docs/terms"); d.mkdir(parents=True, exist_ok=True)
    terms = load_terms()
    print(f"Loaded {{len(terms)}} terms.")
    for t in terms:
        p = d / f"{{t.get('slug', t['id'])}}.md"
        p.write_text(term_md(t), encoding="utf-8")
        print(f"  ✅ {{p}}")
    (d/"index.md").write_text(alpha_idx(terms), encoding="utf-8")
    print("  ✅ docs/terms/index.md")
    (d/"categories.md").write_text(cat_idx(terms), encoding="utf-8")
    print("  ✅ docs/terms/categories.md")

if __name__ == "__main__":
    main()
''',

    "docs/index.md": f"""---
hide: [navigation, toc]
---

# {SITE_NAME}

به فرهنگ آنلاین واژه‌های تخصصی مهندسی خوش آمدید.  
این پروژه با هدف گردآوری و ارائهٔ واژگان فنی تمام رشته‌های مهندسی ساخته شده و رایگان در دسترس همگان است.

<div class="grid cards" markdown>

- :material-book-alphabet: __فهرست واژه‌ها__
    : بر اساس الفبای فارسی یا دسته‌بندی موضوعی
    [:octicons-arrow-right-24: فهرست](terms/index.md)

- :material-magnify: __جست‌وجو__
    : از کادر جست‌وجوی بالای صفحه (فارسی و انگلیسی)

- :material-pencil-plus: __مشارکت__
    : واژهٔ جدید پیشنهاد دهید یا تعریف‌ها را بهبود بخشید
    [:octicons-arrow-right-24: مشارکت](contribute.md)

- :material-information: __دربارهٔ پروژه__
    : اهداف، مجوز و نحوهٔ ارجاع
    [:octicons-arrow-right-24: درباره](about.md)

</div>
""",

    "docs/about.md": f"""\
# دربارهٔ پروژه

فرهنگ واژه‌های تخصصی مهندسی یک پروژهٔ آزاد و مشارکتی است که به مرور همهٔ رشته‌های مهندسی را پوشش خواهد داد.  
در حال حاضر شامل واژگان پایه از مهندسی عمران، مکانیک و ... است.

## اصول
- **رایگان و آزاد** — کد MIT، محتوا CC BY-SA 4.0
- **پایدار** — نسخه‌بندی برای ارجاع در کتاب‌ها و مقالات
- **مشارکتی** — هر متخصصی می‌تواند دانش خود را اضافه کند
- **داده‌محور** — ساختار YAML برای استفاده در اپلیکیشن‌های آینده

## تماس
از طریق [Issues]({REPO_URL}/issues) در GitHub با ما در میان بگذارید.
""",

    "docs/contribute.md": f"""\
# مشارکت در توسعهٔ فرهنگ مهندسی

شما هم می‌توانید واژه‌های رشتهٔ خود را به این مجموعه اضافه کنید.

## روش‌ها
1. **ساده‌ترین:** فرم Issue از پیش آماده  
   [:octicons-arrow-right-24: پیشنهاد واژهٔ جدید]({REPO_URL}/issues/new?template=new-term.yml)
2. **مستقیم:** Pull Request روی فایل `data/terms.yaml`

## راهنمای افزودن واژه
- تعریف کوتاه، دقیق و فنی باشد.
- معادل‌ها به زبان‌های دیگر (حداقل انگلیسی) ذکر شود.
- در صورت امکان استاندارد یا منبع معتبر قید گردد.
- دسته‌بندی مرتبط (مثلاً «مهندسی برق») انتخاب شود.
""",

    "docs/citation.md": f"""\
# نحوهٔ ارجاع

## کل فرهنگ
> {SITE_NAME}، نسخهٔ v1، ۲۰۲۶، <{SITE_URL}>.

## یک مدخل خاص
> {SITE_NAME}، مدخل «**نام واژه**»، بازیابی‌شده در [تاریخ].

## BibTeX
```bibtex
@online{{engdict,
  title = {{{SITE_NAME}}},
  year  = {{2026}},
  url   = {{{SITE_URL}}}
}}""",

".github/workflows/deploy.yml": f"""
name: Deploy
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
url: ${{{{ steps.deploy.outputs.page_url }}}}
steps:

uses: actions/checkout@v4
with:
fetch-depth: 0
token: ${{{{ secrets.GITHUB_TOKEN }}}}

uses: actions/setup-python@v5
with:
python-version: '3.11'

uses: actions/setup-node@v4
with:
node-version: '20'

name: Install dependencies
run: pip install -r requirements.txt

name: Generate Markdown pages
run: python scripts/build_pages.py

name: Configure Git
run: |
git config user.name github-actions[bot]
git config user.email github-actions[bot]@users.noreply.github.com

name: Build and deploy with mike (v1)
run: mike deploy --push --update-aliases v1 latest --deploy-prefix .

name: Copy PWA manifest
run: cp -r docs/manifest.webmanifest site/ 2>/dev/null || true

name: Build Pagefind index
run: |
npx pagefind --site site --output-subdir pagefind

name: Upload Pages artifact
uses: actions/upload-pages-artifact@v3
with:
path: ./site

name: Deploy to GitHub Pages
uses: actions/deploy-pages@v4
id: deploy
""",
}