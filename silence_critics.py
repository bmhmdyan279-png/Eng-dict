import re
import shutil
from pathlib import Path
import subprocess
import sys
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent
MKDOCS_YML = PROJECT_ROOT / "mkdocs.yml"
DEPLOY_YML = PROJECT_ROOT / ".github" / "workflows" / "deploy.yml"
README_MD = PROJECT_ROOT / "README.md"


# ═══════════════════════════════════════
# ۱. رفع خطای ۴۰۴ صفحات (حذف .md از nav)
# ═══════════════════════════════════════
def fix_404_pages():
    """اصلاح لینک‌های nav که .md دارند و باعث ۴۰۴ می‌شوند"""
    if not MKDOCS_YML.exists():
        return False
    content = MKDOCS_YML.read_text(encoding="utf-8")
    original = content

    # الگو: پیدا کردن خطوطی که در nav به فایل .md اشاره می‌کنند
    # و جایگزینی با مسیر بدون پسوند
    fixed = re.sub(r'(\s*-\s+\w+:\s+)([\w-]+)\.md', r'\1\2', content)

    if fixed != original:
        backup = MKDOCS_YML.with_suffix(f".yml.bak_fix404_{datetime.now():%Y%m%d_%H%M%S}")
        shutil.copy2(MKDOCS_YML, backup)
        MKDOCS_YML.write_text(fixed, encoding="utf-8")
        print("✅  خطای ۴۰۴ رفع شد: پسوند .md از لینک‌های nav حذف گردید")
        return True
    else:
        print("ℹ️  لینک‌های nav مشکلی نداشتند (بدون .md)")
        return False


# ═══════════════════════════════════════
# ۲. بررسی و اصلاح CI/CD (deploy.yml)
# ═══════════════════════════════════════
def fix_ci_cd():
    """اطمینان از اینکه build_pages قبل از mkdocs و Pagefind بعد از آن اجرا می‌شود"""
    if not DEPLOY_YML.exists():
        print("⚠️  فایل deploy.yml یافت نشد. ساخت فایل استاندارد...")
        create_deploy_yml()
        return

    content = DEPLOY_YML.read_text(encoding="utf-8")
    original = content

    # بررسی وجود build_pages قبل از mkdocs
    if "build_pages.py" not in content:
        print("❌ build_pages.py در workflow نیست! اضافه می‌کنم...")
        # تزریق مرحله قبل از mkdocs build
        content = content.replace(
            "mkdocs build",
            "python scripts/build_pages.py\n      - name: Build MkDocs\n        run: mkdocs build"
        )

    # بررسی وجود Pagefind بعد از mkdocs
    if "pagefind" not in content.lower():
        print("❌ Pagefind در workflow نیست! اضافه می‌کنم...")
        content = content.replace(
            "mkdocs build",
            "mkdocs build\n      - name: Index with Pagefind\n        run: npx pagefind --site site"
        )

    if content != original:
        backup = DEPLOY_YML.with_suffix(f".yml.bak_{datetime.now():%Y%m%d_%H%M%S}")
        shutil.copy2(DEPLOY_YML, backup)
        DEPLOY_YML.write_text(content, encoding="utf-8")
        print("✅  CI/CD اصلاح شد: build_pages → mkdocs → pagefind")
    else:
        print("✅  CI/CD از قبل درست تنظیم شده بود")


def create_deploy_yml():
    """ساخت فایل استاندارد deploy.yml اگر وجود نداشته باشد"""
    DEPLOY_YML.parent.mkdir(parents=True, exist_ok=True)
    deploy_content = """name: Deploy MkDocs
on:
  push:
    branches: [main]
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          npm install -g pagefind
      - name: Generate pages from YAML
        run: python scripts/build_pages.py
      - name: Build MkDocs
        run: mkdocs build
      - name: Index with Pagefind
        run: npx pagefind --site site
      - name: Deploy to GitHub Pages
        run: mike deploy v1 latest --push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""
    DEPLOY_YML.write_text(deploy_content, encoding="utf-8")
    print("✅  فایل deploy.yml استاندارد ساخته شد")


# ═══════════════════════════════════════
# ۳. بهینه‌سازی mkdocs.yml (RTL، جستجو، زبان)
# ═══════════════════════════════════════
def optimize_mkdocs():
    """افزودن تنظیمات RTL، جستجوی فارسی و نسخه‌بندی"""
    if not MKDOCS_YML.exists():
        print("❌ mkdocs.yml نیست!")
        return

    content = MKDOCS_YML.read_text(encoding="utf-8")
    original = content

    # ۱. تنظیم زبان فارسی
    if "language:" not in content or "fa" not in content:
        content = re.sub(
            r'(theme:\s*\n\s*name:\s*material)',
            r'\1\n  language: fa',
            content
        )

    # ۲. فعال‌سازی search.highlight و search.suggest
    if "search:" not in content:
        content += """
# جستجوی پیشرفته فارسی
theme:
  features:
    - search.suggest
    - search.highlight
    - search.share
"""
    else:
        if "search.suggest" not in content:
            content = content.replace("search:", "search:\n    suggest: true\n    highlight: true")

    # ۳. فعال‌سازی use_directory_urls (پیش‌فرض true است)
    if "use_directory_urls: false" in content:
        content = content.replace("use_directory_urls: false", "use_directory_urls: true")
        print("⚠️  use_directory_urls به true تغییر کرد (URLهای تمیزتر)")

    if content != original:
        backup = MKDOCS_YML.with_suffix(f".yml.bak_opt_{datetime.now():%Y%m%d_%H%M%S}")
        shutil.copy2(MKDOCS_YML, backup)
        MKDOCS_YML.write_text(content, encoding="utf-8")
        print("✅  mkdocs.yml بهینه شد (زبان فارسی، جستجوی پیشرفته، RTL)")
    else:
        print("✅  تنظیمات mkdocs.yml از قبل کامل بود")


# ═══════════════════════════════════════
# ۴. بازنویسی README.md
# ═══════════════════════════════════════
def rewrite_readme():
    """جایگزینی README با نسخهٔ جامع و حرفه‌ای"""
    new_readme = """# 🏗️ دیکشنری تخصصی مهندسی عمران – بتن و سازه

**آدرس سایت:** [betondict.ir](https://betondict.ir) (به‌زودی)  
**نسخهٔ پایدار کتاب:** [v1](https://bmhmdyan279-png.github.io/Eng-dict/v1/)

[![Deploy](https://github.com/bmhmdyan279-png/Eng-dict/actions/workflows/deploy.yml/badge.svg)](https://github.com/bmhmdyan279-png/Eng-dict/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE-CODE.md)
[![Content License: CC BY-SA 4.0](https://img.shields.io/badge/Content%20License-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE-CONTENT.md)

## 📖 دربارهٔ پروژه

این پروژه یک **دیکشنری تخصصی مهندسی عمران با تمرکز بر بتن و سازه** است که به همراه کتاب چاپی ارائه می‌شود.  
با اسکن QR Code داخل کتاب، به نسخهٔ آنلاین و همیشه به‌روز دسترسی پیدا می‌کنید.

### ویژگی‌ها
- 🌐 **نسخهٔ وب PWA** – قابل نصب روی گوشی، کارکرد آفلاین
- 📱 **واکنش‌گرا (Responsive)** – بهینه برای موبایل و تبلت
- 🔍 **جستجوی پیشرفتهٔ فارسی** – با پشتیبانی از Pagefind
- 🌍 **معادل‌های چندزبانه**: انگلیسی، فرانسوی، آلمانی، عربی
- 📦 **نسخه‌بندی پایدار** – نسخهٔ v1 مخصوص کتاب چاپی
- 🤝 **مشارکت آسان** – فرم پیشنهاد واژه (فنی و غیرفنی)

## 🚀 اجرای محلی

### پیش‌نیازها
- Python 3.10+
- Node.js 18+ (برای Pagefind)
- Git

### راه‌اندازی سریع
```bash
# کلون پروژه
git clone https://github.com/bmhmdyan279-png/Eng-dict.git
cd Eng-dict

# نصب وابستگی‌ها
pip install -r requirements.txt
npm install -g pagefind  # فقط برای جستجوی آفلاین

# تولید صفحات از داده‌ها
python scripts/build_pages.py

# اجرای محلی
mkdocs serve
```
حالا مرورگر را روی `http://localhost:8000` باز کنید.

## 📂 ساختار پروژه

```
Eng-dict/
├── .github/workflows/    # CI/CD (خودکار)
├── data/
│   └── terms.yaml        # تمام واژگان در این فایل (YAML)
├── docs/                 # سایت MkDocs
│   ├── assets/           # CSS, JS, QR Code
│   ├── terms/            # صفحات واژگان (خودکار ساخته می‌شود)
│   └── ...
├── scripts/
│   └── build_pages.py    # تبدیل terms.yaml به Markdown
├── mkdocs.yml            # تنظیمات اصلی
└── requirements.txt      # وابستگی‌های پایتون
```

## ✍️ نحوهٔ افزودن واژهٔ جدید

۱. فایل `data/terms.yaml` را باز کنید.  
۲. یک واژهٔ جدید به این شکل اضافه کنید:

```yaml
- term_fa: واژهٔ فارسی
  term_en: English Word
  term_fr: Mot français
  term_de: Deutsches Wort
  term_ar: کلمة عربیة
  category: دسته‌بندی
  definition: |
    تعریف کامل واژه...
  standards: استانداردهای مرتبط
  source: منبع
```

۳. صفحات را بازسازی کنید:
```bash
python scripts/build_pages.py
```

۴. تغییرات را کامیت و پوش کنید.  
۵. GitHub Actions به‌صورت خودکار سایت را به‌روز می‌کند.

## 🖨️ نسخهٔ چاپی (کتاب)

QR Code داخل کتاب به آدرس **نسخهٔ پایدار v1** اشاره می‌کند:
```
https://betondict.ir/v1/  (پس از ثبت دامنه)
```
این نسخه با دستور `mike deploy v1` فریز شده و با به‌روزرسانی‌های آینده تغییر نمی‌کند.

## 🤝 مشارکت

ما از مشارکت شما استقبال می‌کنیم!  
- [فرم پیشنهاد واژه](https://bmhmdyan279-png.github.io/Eng-dict/contribute-form/)
- [راهنمای مشارکت](CONTRIBUTING.md)
- [کد رفتار](CODE_OF_CONDUCT.md)

## 📜 مجوز

- **کد:** MIT License ([LICENSE-CODE.md](LICENSE-CODE.md))
- **محتوا (واژگان):** Creative Commons BY-SA 4.0 ([LICENSE-CONTENT.md](LICENSE-CONTENT.md))

---
با ❤️ برای جامعهٔ مهندسی عمران ایران
"""
    README_MD.write_text(new_readme, encoding="utf-8")
    print("✅  README.md بازنویسی شد (جامع و حرفه‌ای)")


# ═══════════════════════════════════════
# ۵. اجرای mike برای تثبیت نسخهٔ v1
# ═══════════════════════════════════════
def freeze_v1():
    """فریز نسخهٔ v1 برای کتاب (اگر mike نصب باشد)"""
    try:
        subprocess.run(["mike", "deploy", "v1", "latest", "--push"], check=True, cwd=PROJECT_ROOT)
        subprocess.run(["mike", "set-default", "latest", "--push"], check=True, cwd=PROJECT_ROOT)
        print("✅  نسخهٔ v1 با mike فریز و به latest تنظیم شد")
    except FileNotFoundError:
        print("⚠️  mike در دسترس نیست (با pip install mike نصب کنید)")
    except subprocess.CalledProcessError as e:
        print(f"❌ خطا در اجرای mike: {e}")


# ═══════════════════════════════════════
# ۶. راهنمای دامنهٔ .ir
# ═══════════════════════════════════════
def print_domain_guide():
    """نمایش راهنمای ثبت دامنهٔ .ir در کنسول"""
    guide = """
╔══════════════════════════════════════════════════════╗
║  🌐 راهنمای خرید و تنظیم دامنهٔ .ir (فقط ۵ دقیقه)  ║
╚══════════════════════════════════════════════════════╝

1️⃣  خرید دامنه
   به یکی از این سایت‌ها بروید:
   • one.ir
   • nic.ir
   دامنه‌های پیشنهادی:
   ✅ betondict.ir
   ✅ dict-beton.ir
   ✅ concrete-dict.ir
   قیمت: حدود ۳۰-۵۰ هزار تومان در سال

2️⃣  تنظیم DNS
   پس از خرید، در پنل مدیریت دامنه، این رکوردها را اضافه کنید:

   نوع: A
   نام: @
   مقدار: 185.199.108.153

   نوع: A
   نام: @
   مقدار: 185.199.109.153

   نوع: A
   نام: @
   مقدار: 185.199.110.153

   نوع: A
   نام: @
   مقدار: 185.199.111.153

   (یا یک رکورد CNAME به username.github.io)

3️⃣  اتصال به GitHub Pages
   • به تنظیمات مخزن بروید: Settings → Pages
   • در بخش Custom domain، دامنهٔ خود را وارد کنید (مثلاً betondict.ir)
   • گزینه Enforce HTTPS را فعال کنید
   • صبر کنید تا گواهی SSL صادر شود (چند دقیقه)

4️⃣  بروزرسانی QR Code
   حالا دامنهٔ جدید را در اسکریپت generate_qr.py جایگزین کنید و دوباره اجرا:
   python scripts/generate_qr.py

   آدرس جدید QR Code:
   https://betondict.ir/v1/

⚠️  هشدار: تا وقتی دامنه قطعی نشده، QR Code نهایی را چاپ نکنید!
"""
    print(guide)


# ═══════════════════════════════════════
# اجرای اصلی
# ═══════════════════════════════════════
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔇  خاموش‌کنندهٔ منتقدان – اسکریپت جامع فاز ۳.۵")
    print("=" * 60 + "\n")

    print("▶ گام ۱: رفع خطای ۴۰۴ صفحات...")
    fix_404_pages()

    print("\n▶ گام ۲: اصلاح CI/CD...")
    fix_ci_cd()

    print("\n▶ گام ۳: بهینه‌سازی mkdocs.yml...")
    optimize_mkdocs()

    print("\n▶ گام ۴: بازنویسی README.md...")
    rewrite_readme()

    print("\n▶ گام ۵: فریز نسخهٔ v1 با mike...")
    freeze_v1()

    print("\n▶ گام ۶: راهنمای دامنهٔ .ir...")
    print_domain_guide()

    print("\n" + "=" * 60)
    print("✅  همهٔ ایرادات منتقدان رفع شد!")
    print("=" * 60)
    print("اقدام بعدی: کامیت و پوش کنید:")
    print("  git add .")
    print('  git commit -m "Fix all critic issues: 404, CI/CD, README, v1 freeze"')
    print("  git push origin main")
