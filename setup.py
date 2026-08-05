import subprocess
import sys
from pathlib import Path
from string import Template
from typing import Dict

# ------------------------- تنظیمات پایه -------------------------
try:
    # تلاش برای گرفتن آدرس origin از git
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
        check=True,
    )
    remote_url = result.stdout.strip()
    # الگوهای مختلف آدرس‌دهی گیت‌هاب
    if remote_url.startswith("https://github.com/"):
        _, _, repo_path = remote_url.partition("github.com/")
    elif remote_url.startswith("git@github.com:"):
        _, _, repo_path = remote_url.partition("git@github.com:")
    else:
        raise ValueError("آدرس ریموت قابل شناسایی نیست.")
    repo_path = repo_path.removesuffix(".git")
    username, repo_name = repo_path.split("/")
    print(f"✅ شناسایی شد: کاربر {username}، مخزن {repo_name}")
except Exception:
    username = input("🔹 نام کاربری GitHub خود را وارد کنید: ").strip()
    repo_name = input("🔹 نام مخزن را وارد کنید (مثلاً beton-dict): ").strip()

SITE_URL = f"https://{username}.github.io/{repo_name}/"
REPO_URL = f"https://github.com/{username}/{repo_name}"
FULL_REPO = f"{username}/{repo_name}"

# ------------------------- محتوای فایل‌ها -------------------------
FILES: Dict[str, str] = {
    # =============== فایل‌های اصلی ===============
    "requirements.txt": "mkdocs-material==9.5.*\npyyaml==6.0.*\n",
    "pyproject.toml": f'''[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "concrete-dict"
version = "1.0.0"
description = "فرهنگ آنلاین واژه‌های تخصصی بتن"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "mkdocs-material>=9.5,<10",
    "pyyaml>=6.0,<7",
]

[project.license]
text = "MIT"
''',

    "mkdocs.yml": f'''site_name: فرهنگ واژه‌های تخصصی بتن
site_description: فرهنگ لغت آنلاین واژه‌های تخصصی بتن
site_url: {SITE_URL}
repo_url: {REPO_URL}
repo_name: {FULL_REPO}

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
    - content.tabs.link
    - content.code.copy
    - navigation.indexes
  palette:
    - scheme: default
      primary: teal
      accent: teal
      toggle:
        icon: material/brightness-7
        name: حالت تاریک
    - scheme: slate
      primary: teal
      accent: teal
      toggle:
        icon: material/brightness-4
        name: حالت روشن

plugins:
  - search:
      lang: [fa, en]

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
  - toc:
      permalink: true

extra_css:
  - assets/css/extra.css

extra_javascript:
  - https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js
  - https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js
  - assets/js/math.js
''',

    "data/terms.yaml": """\
# فرهنگ واژه‌های تخصصی بتن — فایل داده‌ها
# این فایل به صورت YAML نگهداری می‌شود. برای افزودن واژه،
# یک شیء جدید با همان ساختار اضافه کنید.

- id: concrete
  fa: بتن
  slug: beton
  aliases: [Concrete, Béton]
  languages:
    en: Concrete
    fr: Béton
    de: Beton
    ar: خرسانة
  category: مصالح
  definition: >
    بتن مخلوطی از سیمان، سنگ‌دانه، آب و در صورت نیاز افزودنی است
    که پس از گیرش سخت می‌شود.
  standards: [ASTM C94, EN 206, ISIRI 3892]
  related: [cement, rebar, admixture]
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
  category: مصالح
  definition: >
    سیمان مادهٔ چسباننده‌ای است که با آب واکنش می‌دهد و سخت می‌شود.
  standards: [ASTM C150, EN 197-1]
  related: [concrete, clinker]
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
  category: تقویت
  definition: >
    آرماتور یا میلگرد فولادی است که در بتن قرار می‌گیرد تا مقاومت
    کششی آن را افزایش دهد.
  standards: [ASTM A615, ISIRI 3132]
  related: [concrete]
  status: approved
""",

    "scripts/build_pages.py": '''#!/usr/bin/env python3
"""ساخت صفحات Markdown از داده‌های YAML."""
import sys
from pathlib import Path
import yaml

def load_terms(path: str = "data/terms.yaml") -> list:
    p = Path(path)
    if not p.exists():
        print(f"❌ فایل {path} پیدا نشد. ابتدا setup.py را اجرا کنید.", file=sys.stderr)
        sys.exit(1)
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or []
    print(f"📂 {len(data)} واژه از YAML بارگذاری شد.")
    return data

def term_markdown(t: dict) -> str:
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

    lines = [
        "---",
        f"title: {fa}",
        f"description: تعریف {fa} در فرهنگ بتن",
        "---",
        "",
        f"# {fa}{f' / {en}' if en else ''}",
        "",
    ]

    if langs:
        lines += ["## معادل‌ها", "", "| زبان | معادل |", "|------|-------|"]
        lang_names = {"en":"انگلیسی","fr":"فرانسوی","de":"آلمانی","ar":"عربی","tr":"ترکی","ru":"روسی"}
        for code, word in langs.items():
            lines.append(f"| {lang_names.get(code, code.upper())} | {word} |")
        lines.append("")

    if defn:
        lines += ["## تعریف", "", defn, ""]

    lines += ["## دسته", "", f"`{cat}`", ""]

    if stds:
        lines += ["## استانداردهای مرتبط", ""]
        for s in stds:
            lines.append(f"- `{s}`")
        lines.append("")

    if rel:
        lines += ["## واژه‌های مرتبط", ""]
        for r in rel:
            lines.append(f"- [{r}](./{r}.md)")
        lines.append("")

    if src or upd:
        lines += ["## اطلاعات تکمیلی", ""]
        if src:
            lines.append(f"- **منبع:** `{src}`")
        if upd:
            lines.append(f"- **به‌روزرسانی:** {upd}")
        lines.append("")

    # جعبهٔ ارجاع
    lines += [
        "---",
        "",
        '??? info "نحوهٔ ارجاع"',
        "",
        f"    فرهنگ واژه‌های تخصصی بتن، مدخل «{fa}»، {upd or 'بی‌تاریخ'}.",
        "",
    ]
    return "\\n".join(lines)

def alphabetical_index(terms: list) -> str:
    lines = [
        "---",
        "title: فهرست الفبایی",
        "---",
        "",
        "# فهرست الفبایی واژه‌ها",
        "",
        "همهٔ واژه‌ها به ترتیب الفبای فارسی.",
        "",
    ]
    grouped = {}
    for t in terms:
        fa = t.get("fa", t["id"])
        initial = fa[0] if fa else "?"
        grouped.setdefault(initial, []).append((fa, t.get("slug", t["id"])))

    # الفبای فارسی (با احتساب حروف ویژه)
    persian_alphabet = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
    sorted_initials = sorted(
        grouped.keys(),
        key=lambda x: persian_alphabet.index(x) if x in persian_alphabet else 999
    )
    jump_line = "**پرش به حرف:** " + " · ".join(f"[{l}](#{l})" for l in sorted_initials) + "\\n"
    lines.append(jump_line)

    for initial in sorted_initials:
        lines.append(f"## <a name='{initial}'></a>{initial}")
        lines.append("")
        for fa, slug in sorted(grouped[initial]):
            lines.append(f"- [{fa}](./{slug}.md)")
        lines.append("")
    return "\\n".join(lines)

def category_index(terms: list) -> str:
    lines = [
        "---",
        "title: دسته‌بندی",
        "---",
        "",
        "# واژه‌ها بر اساس دسته",
        "",
    ]
    grouped = {}
    for t in terms:
        cat = t.get("category", "سایر")
        grouped.setdefault(cat, []).append(t)

    for cat, items in sorted(grouped.items()):
        lines.append(f"## {cat}")
        lines.append("")
        # مرتب‌سازی بر اساس نام فارسی
        for item in sorted(items, key=lambda x: x.get("fa", "")):
            lines.append(f"- [{item['fa']}](./{item.get('slug', item['id'])}.md)")
        lines.append("")
    return "\\n".join(lines)

def main():
    terms_dir = Path("docs/terms")
    terms_dir.mkdir(parents=True, exist_ok=True)

    terms = load_terms()
    for t in terms:
        slug = t.get("slug", t["id"])
        file_path = terms_dir / f"{slug}.md"
        file_path.write_text(term_markdown(t), encoding="utf-8")
        print(f"  ✅ {file_path}")

    # صفحات شاخص
    idx_path = terms_dir / "index.md"
    idx_path.write_text(alphabetical_index(terms), encoding="utf-8")
    print(f"  ✅ {idx_path}")

    cat_path = terms_dir / "categories.md"
    cat_path.write_text(category_index(terms), encoding="utf-8")
    print(f"  ✅ {cat_path}")

if __name__ == "__main__":
    main()
''',

    "docs/index.md": """\
---
hide: [navigation, toc]
---

# فرهنگ واژه‌های تخصصی بتن

به فرهنگ آنلاین واژه‌های تخصصی بتن خوش آمدید. این فرهنگ همراه کتاب طراحی شده و رایگان در دسترس همه است.

<div class="grid cards" markdown>

- :material-book-alphabet: __فهرست واژه‌ها__
    : با الفبای فارسی یا بر اساس دسته
    [:octicons-arrow-right-24: فهرست](terms/index.md)

- :material-magnify: __جست‌وجو__
    : از کادر جست‌وجو در بالای صفحه استفاده کنید

- :material-pencil-plus: __مشارکت__
    : واژه پیشنهاد دهید یا تعریف را اصلاح کنید
    [:octicons-arrow-right-24: مشارکت](contribute.md)

- :material-information: __درباره__
    : دربارهٔ پروژه، مجوز و ارجاع
    [:octicons-arrow-right-24: درباره](about.md)

</div>
""",

    "docs/about.md": """\
# دربارهٔ پروژه

این فرهنگ لغت ضمیمهٔ دیجیتال کتاب «[نام کتاب]» است.

## اصول

1. **رایگان و آزاد** — کد MIT، محتوا CC BY-SA 4.0
2. **پایدار** — بارکد چاپی به نسخهٔ ثابت اشاره می‌کند
3. **مشارکتی** — همه می‌توانند کمک کنند
4. **داده‌محور** — YAML برای API و اپ آینده

## تماس

از [GitHub Issues]({{ config.repo_url }}/issues) استفاده کنید.
""",

    "docs/contribute.md": """\
# مشارکت

## راه ۱: GitHub (فنی)

- [پیشنهاد واژهٔ جدید]({{ config.repo_url }}/issues/new?template=new-term.yml)
- [اصلاح واژهٔ موجود]({{ config.repo_url }}/issues/new?template=correction.yml)
- یا Pull Request مستقیم روی `data/terms.yaml`

## راه ۲: فرم (به‌زودی)

در فاز ۲ یک فرم ساده به Issue خودکار وصل می‌شود.

## راهنما

- تعریف کوتاه، دقیق و بدون ابهام
- ذکر منبع یا استاندارد در صورت وجود
- مشارکت تحت CC BY-SA 4.0 منتشر می‌شود
""",

    "docs/citation.md": """\
# نحوهٔ ارجاع

## کل فرهنگ
> فرهنگ واژه‌های تخصصی بتن، نسخهٔ v1، ۲۰۲۶، <{{ config.site_url }}>.

## یک واژه
> فرهنگ واژه‌های تخصصی بتن، مدخل «**نام واژه**»، بازیابی‌شده در [تاریخ].

## BibTeX
```bibtex
@online{betondict,
  title = {فرهنگ واژه‌های تخصصی بتن},
  year  = {2026},
  url   = {{{{ config.site_url }}}}
}
```
""",

    "docs/assets/css/extra.css": """\
:root { --md-text-font: "Vazirmatn"; }
body, .md-content, .md-sidebar, .md-header__title, .md-footer__inner { direction: rtl; }
.md-typeset table:not([class]),
.md-typeset table:not([class]) th,
.md-typeset table:not([class]) td { direction: rtl; text-align: right; }
.md-typeset { line-height: 1.8; font-size: 0.95rem; }
.md-typeset blockquote {
  border-right: 0.2rem solid var(--md-accent-fg-color);
  border-left: none;
  padding-right: 0.6rem;
  padding-left: 0;
}
.md-typeset .grid.cards > :is(ul, ol) {
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
}
""",

    "docs/assets/js/math.js": """\
document$.subscribe(({body}) => {
  renderMathInElement(body, {
    delimiters: [
      {left: "$$", right: "$$", display: true},
      {left: "$", right: "$", display: false}
    ]
  });
});
""",

    ".github/workflows/deploy.yml": f"""\
name: Deploy
on:
  push:
    branches: [main, master]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: "pages"
  cancel-in-progress: false
jobs:
  build-deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{{{ steps.deploy.outputs.page_url }}}}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python scripts/build_pages.py
      - run: mkdocs build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./site
      - uses: actions/deploy-pages@v4
        id: deploy
""",

    ".github/ISSUE_TEMPLATE/new-term.yml": """\
name: پیشنهاد واژهٔ جدید
description: افزودن واژه به فرهنگ
labels: ["new-term"]
body:
  - type: input
    id: fa
    attributes:
      label: واژهٔ فارسی
    validations:
      required: true
  - type: input
    id: en
    attributes:
      label: معادل انگلیسی
    validations:
      required: true
  - type: input
    id: fr
    attributes:
      label: معادل فرانسوی (اختیاری)
  - type: input
    id: de
    attributes:
      label: معادل آلمانی (اختیاری)
  - type: input
    id: ar
    attributes:
      label: معادل عربی (اختیاری)
  - type: input
    id: category
    attributes:
      label: دستهٔ تخصصی
    validations:
      required: true
  - type: textarea
    id: definition
    attributes:
      label: تعریف پیشنهادی
    validations:
      required: true
  - type: textarea
    id: standards
    attributes:
      label: استانداردها (هر کدام در یک خط)
  - type: input
    id: chapter
    attributes:
      label: فصل مرتبط در کتاب
  - type: checkboxes
    id: agree
    attributes:
      label: توافق
      options:
        - label: مشارکتم تحت CC BY-SA 4.0 منتشر شود.
          required: true
""",

    ".github/ISSUE_TEMPLATE/correction.yml": """\
name: اصلاح واژه
description: اصلاح یا بهبود یک واژهٔ موجود
labels: ["correction"]
body:
  - type: input
    id: term
    attributes:
      label: نام واژه
    validations:
      required: true
  - type: dropdown
    id: type
    attributes:
      label: نوع اصلاح
      options:
        - اشتباه در تعریف
        - اشتباه در ترجمه
        - اطلاعات ناقص
        - املایی
        - سایر
    validations:
      required: true
  - type: textarea
    id: current
    attributes:
      label: متن فعلی یا مشکل
    validations:
      required: true
  - type: textarea
    id: suggested
    attributes:
      label: پیشنهاد شما
    validations:
      required: true
  - type: textarea
    id: ref
    attributes:
      label: منبع
  - type: checkboxes
    id: agree
    attributes:
      label: توافق
      options:
        - label: مشارکتم تحت CC BY-SA 4.0 منتشر شود.
          required: true
""",

    "README.md": f"""\
# فرهنگ واژه‌های تخصصی بتن 📚

> فرهنگ لغت آنلاین، مشارکتی و رایگان برای واژه‌های تخصصی بتن.

🌐 **سایت:** {SITE_URL}

## ✨ ویژگی‌ها

- 🌐 چندزبانه (فارسی، انگلیسی، فرانسوی، آلمانی، عربی)
- 🔍 جست‌وجوی فارسی و انگلیسی
- 📱 RTL و سازگار با موبایل
- 📐 پشتیبانی از فرمول (KaTeX)
- 🔓 متن‌باز

## 🛠️ توسعهٔ محلی

```bash
pip install -r requirements.txt
python scripts/build_pages.py
mkdocs serve
```

## 📜 مجوز

- **کد:** [MIT](LICENSE-CODE.md)
- **محتوا:** [CC BY-SA 4.0](LICENSE-CONTENT.md)
""",

    "CONTRIBUTING.md": f"""\
# راهنمای مشارکت

## راه‌ها

1. **ساده‌ترین:** Issue بسازید با [این فرم]({REPO_URL}/issues/new?template=new-term.yml)
2. **فنی‌تر:** روی `data/terms.yaml` Pull Request بزنید

```bash
git checkout -b add-term-beton
# ویرایش data/terms.yaml
python scripts/build_pages.py
mkdocs serve
git add .
git commit -m "Add term: بتن"
git push
```

## معیارها

- دقت فنی
- ذکر منبع
- ارتباط با حوزهٔ بتن

## مجوز

- کد: MIT
- محتوا: CC BY-SA 4.0
""",

    "CODE_OF_CONDUCT.md": """\
# میثاق‌نامهٔ رفتار مشارکت‌کنندگان

ما متعهد می‌شویم محیطی بدون آزار برای همه بسازیم، فارغ از سن، قومیت، جنسیت، تجربه، ملیت یا مذهب.

## رفتار مورد انتظار

- همدلی و مهربانی
- احترام به نظرات متفاوت
- پذیرش مسئولیت

## رفتار غیرقابل‌قبول

- توهین، تحقیر، آزار
- محتوای جنسی نامرتبط
- انتشار اطلاعات خصوصی

## گزارش

موارد را از طریق GitHub Issues به راهبران گزارش دهید.

برگرفته از [Contributor Covenant 2.0](https://www.contributor-covenant.org/version/2/0/code_of_conduct.html).
""",

    "LICENSE-CODE.md": """\
MIT License

Copyright (c) 2026 [نام شما]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",

    "LICENSE-CONTENT.md": """\
# محتوای این پروژه تحت مجوز CC BY-SA 4.0 است

## شما آزاد هستید:

- **اشتراک‌گذاری** — کپی و توزیع مجدد
- **اقتباس** — ساخت اثر مشتق‌شده حتی برای کاربردهای تجاری

## با این شرایط:

- **انتساب** — ذکر منبع
- **اشتراک مشابه** — انتشار تحت همین مجوز

متن کامل: <https://creativecommons.org/licenses/by-sa/4.0/deed.fa>
""",

    ".gitignore": """\
__pycache__/
*.py[cod]
venv/
.venv/
site/
.idea/
.vscode/
*.swp
.DS_Store
""",

    ".gitattributes": """\
# Ensure line endings are LF for all text files
* text=auto eol=lf
*.md text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
*.py text eol=lf
*.css text eol=lf
*.js text eol=lf
*.toml text eol=lf
""",
}

# ------------------------- اجرای اصلی -------------------------
def create_files():
    print("🏗️  شروع راه‌اندازی...")
    for rel_path, content in FILES.items():
        p = Path(rel_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        print(f"✅ {rel_path}")

    # اعتبارسنجی YAML
    try:
        import yaml
        with Path("data/terms.yaml").open("r", encoding="utf-8") as f:
            yaml.safe_load(f)
        print("✔  فایل YAML معتبر است.")
    except Exception as e:
        print(f"⚠️  خطا در YAML: {e}", file=sys.stderr)

    print("\n🎉 همه فایل‌ها با موفقیت ساخته شدند.")
    print(f"📍 سایت نهایی: {SITE_URL}")
    print("\n📋 گام‌های بعدی:")
    print("  1. یک محیط مجازی بسازید: python -m venv venv")
    print("  2. فعال‌سازی: source venv/bin/activate  (یا venv\\Scripts\\activate)")
    print("  3. نصب پیش‌نیازها: pip install -r requirements.txt")
    print("  4. ساخت صفحات واژه‌ها: python scripts/build_pages.py")
    print("  5. اجرای محلی: mkdocs serve")
    print("  6. سپس git add . && git commit -m 'Initial setup' && git push")
    print("  7. در GitHub: Settings → Pages → Source: GitHub Actions")
    print("  8. چند دقیقه صبر کنید تا سایت بالا بیاید.")

if __name__ == "__main__":
    create_files()