# 🏗️ دیکشنری تخصصی مهندسی

## 📖 دربارهٔ پروژه

این پروژه یک **دیکشنری تخصصی مهندسی** است.

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
git clone https://github.com/bmhmdyan279-png/eng-terms-fa.git
cd eng-terms-fa

# نصب وابستگی‌ها
pip install -r requirements.txt
npm install pagefind  # نصب محلی

# تولید صفحات از داده‌ها
python scripts/build_pages.py

# اجرای محلی
mkdocs serve
```

حالا مرورگر را روی `http://localhost:8000` باز کنید.

## 📂 ساختار پروژه

```
eng-terms-fa/
├── .github/workflows/    # CI/CD (خودکار)
├── data/
│   └── terms.yaml        # تمام واژگان در این فایل (YAML)
├── docs/                 # سایت MkDocs
│   ├── assets/           # CSS, JS, QR Code
│   ├── terms/            # صفحات واژگان (خودکار ساخته می‌شود)
│   └── manifest.webmanifest  # تنظیمات PWA
├── scripts/
│   ├── build_pages.py    # تبدیل terms.yaml به Markdown
│   └── cleanup_terms.py  # پاکسازی داده‌ها
├── tests/                # تست‌های واحد
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
  references:
    - منبع اول
    - منبع دوم
  slug: slug-unique
```

۳. صفحات را بازسازی کنید:

```bash
python scripts/build_pages.py
```

۴. تغییرات را کامیت و پوش کنید.

۵. GitHub Actions به‌صورت خودکار سایت را به‌روز می‌کند.

## 🤝 مشارکت

ما از مشارکت شما استقبال می‌کنیم!

- [فرم پیشنهاد واژه](https://bmhmdyan279-png.github.io/eng-terms-fa/contribute-form/)
- [راهنمای مشارکت](CONTRIBUTING.md)
- [کد رفتار](CODE_OF_CONDUCT.md)

## 📜 مجوز

- **کد:** MIT License (LICENSE-CODE.md)
- **محتوا (واژگان):** Creative Commons BY-SA 4.0 (LICENSE-CONTENT.md)

---

**توسعه‌دهنده:** [bmhmdyan279-png](https://github.com/bmhmdyan279-png)
