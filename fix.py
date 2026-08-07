import os
import subprocess

print("⏳ در حال افزودن واژگان جدید و اصلاح فایل‌ها...")

yaml_addition = """
- term_fa: رقمی
  term_en: Digital
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: تاوَن
  term_en: Oven
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: اندازه غربالی
  term_en: Mesh
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: واسنجیدن
  term_en: Calibration
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: آمادگاه
  term_en: Depot
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: جیک
  term_en: Jig / Jigging
  category: واژگان مصوب فرهنگستان
  definition: متراکم سازی نمونه با بلند کردن و کوبیدن متناوب پیمانه.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: آژند
  term_en: Cement
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: واپایش
  term_en: Control
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: تشریفات
  term_en: Protocol
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: دسته
  term_en: Batch
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: مخلوط ساز
  term_en: Batching
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: رواداری / تحمل
  term_en: Tolerance
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: بسامد
  term_en: Frequency
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: لرزاننده
  term_en: Vibrator
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: تالار
  term_en: Gallery
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true

- term_fa: بطری چگالی
  term_en: Pycnometer
  category: واژگان مصوب فرهنگستان
  definition: برابر مصوب فرهنگستان زبان و ادب فارسی.
  standards: ""
  source: کتاب آزمایشات فناوری بتن
  featured_book: true
"""

# ۱. افزودن مستقیم به YAML
with open("data/terms.yaml", "a", encoding="utf-8") as f:
    f.write(yaml_addition)

# ۲. اجرای اسکریپت اصلی برای ساخت صفحات
print("🔄 در حال اجرای build_pages.py...")
subprocess.run(["python", "scripts/build_pages.py"], check=True)

# ۳. افزودن باکس ویژه به فایل‌های ساخته شده
admonition = """!!! info "واژه ویژه کتاب آزمایشات فناوری بتن"
    این واژه مستقیماً از کتاب آزمایشات فناوری بتن استخراج شده است.

"""

terms_fa = [
    "رقمی",
    "تاوَن",
    "اندازه غربالی",
    "واسنجیدن",
    "آمادگاه",
    "جیک",
    "آژند",
    "واپایش",
    "تشریفات",
    "دسته",
    "مخلوط ساز",
    "رواداری / تحمل",
    "بسامد",
    "لرزاننده",
    "تالار",
    "بطری چگالی",
]
terms_en = [
    "Digital",
    "Oven",
    "Mesh",
    "Calibration",
    "Depot",
    "Jig",
    "Cement",
    "Control",
    "Protocol",
    "Batch",
    "Batching",
    "Tolerance",
    "Frequency",
    "Vibrator",
    "Gallery",
    "Pycnometer",
]

for fa, en in zip(terms_fa, terms_en):
    fa_file_name = fa.replace(" / ", "-").replace("/", "-")
    en_file_name = en.lower().replace(" / ", "-").replace("/", "-")

    for file_name in [fa_file_name, en_file_name]:
        filepath = f"docs/terms/{file_name}.md"
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            if "ویژه کتاب" not in content and "featured_book" not in content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(admonition + content)

# ۴. ساخت خودکار صفحه فرود
print("📝 در حال ساخت صفحه فرود...")
book_md = """# 📖 واژگان اختصاصی کتاب آزمایشات فناوری بتن

!!! success "به دیکشنری تخصصی خوش آمدید"
    این واژگان، برابرهای مصوب **فرهنگستان زبان و ادب فارسی** هستند که در کتاب آزمایشات فناوری بتن به کار رفته‌اند.

<div class="grid cards" markdown>
"""

for fa, en in zip(terms_fa, terms_en):
    fa_file_name = fa.replace(" / ", "-").replace("/", "-")
    en_file_name = en.lower().replace(" / ", "-").replace("/", "-")

    link = ""
    if os.path.exists(f"docs/terms/{fa_file_name}.md"):
        link = f"terms/{fa_file_name}.md"
    elif os.path.exists(f"docs/terms/{en_file_name}.md"):
        link = f"terms/{en_file_name}.md"
    else:
        link = f"terms/{fa}.md"

    book_md += f"""
-   :material-book:{{ .lg .middle }} **{fa}** ({en})
    ---
    برابر مصوب فرهنگستان زبان و ادب فارسی.
    [:octicons-arrow-right-24: مشاهده جزئیات]({link})
"""

book_md += "\n</div>\n"
with open("docs/book-vocab.md", "w", encoding="utf-8") as f:
    f.write(book_md)

print("✅ تمام! حالا تغییرات را کامیت و پوش کنید.")
