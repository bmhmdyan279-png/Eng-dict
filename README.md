# 🏗️ دیکشنری تخصصی مهندسی 

[![Deploy](https://github.com/bmhmdyan279-png/Eng-dict/actions/workflows/deploy.yml/badge.svg)](https://github.com/bmhmdyan279-png/Eng-dict/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE-CODE.md)
[![Content License: CC BY-SA 4.0](https://img.shields.io/badge/Content%20License-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE-CONTENT.md)

## 📖 دربارهٔ پروژه

این پروژه یک **دیکشنری تخصصی مهندسی  است. 

### ویژگی‌ها
- 🌐 **نسخهٔ وب PWA** – قابل نصب روی گوشی، کارکرد آفلاین
- 📱 **واکنش‌گرا (Responsive)** – بهینه برای موبایل و تبلت
- 🔍 **جستجوی پیشرفتهٔ فارسی** – با پشتیبانی از Pagefind
- 🌍 **معادل‌های چندزبانه**: انگلیسی، فرانسوی، آلمانی، عربی
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
