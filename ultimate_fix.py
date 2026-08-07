import os
import yaml
import subprocess

print("⏳ در حال اعمال استراتژی جایگزینی هوشمند برای دور زدن محدودیت ویندوز...")

yaml_file = "data/terms.yaml"

# ۱. خواندن YAML اصلی و ایجاد نگاشت برای کلمات دارای اسلش
with open(yaml_file, "r", encoding="utf-8") as f:
    original_content = f.read()
    terms_data = yaml.safe_load(original_content)

safe_to_original_fa = {}
safe_to_original_en = {}

for term in terms_data:
    fa = term.get("term_fa", "")
    en = term.get("term_en", "")

    fa_safe = fa.replace("/", "-").replace("\\", "-")
    en_safe = en.replace("/", "-").replace("\\", "-")

    if fa != fa_safe:
        safe_to_original_fa[fa_safe] = fa
    if en != en_safe:
        safe_to_original_en[en_safe] = en

# ۲. اصلاح موقت فایل YAML برای اجرای بدون خطا
temp_content = original_content.replace("/", "-").replace("\\", "-")
with open(yaml_file, "w", encoding="utf-8") as f:
    f.write(temp_content)

# ۳. اجرای build_pages.py با نام‌های ایمن
print("🔄 در حال اجرای build_pages.py...")
subprocess.run(["python", "scripts/build_pages.py"], check=True)

# ۴. بازگرداندن YAML به حالت اصلی (تا دیتابیس شما دست‌نخورده بماند)
with open(yaml_file, "w", encoding="utf-8") as f:
    f.write(original_content)

# ۵. بازیابی کاراکترهای اصلی در فایل‌های Markdown ساخته شده
print("📝 در حال بازیابی کاراکترهای اصلی در فایل‌های Markdown...")
terms_dir = "docs/terms"
if os.path.exists(terms_dir):
    for filename in os.listdir(terms_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(terms_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            for safe_fa, orig_fa in safe_to_original_fa.items():
                content = content.replace(safe_fa, orig_fa)
            for safe_en, orig_en in safe_to_original_en.items():
                content = content.replace(safe_en, orig_en)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

# ۶. افزودن باکس ویژه و ساخت صفحه فرود نهایی
admonition = """!!! info "واژه ویژه کتاب آزمایشات فناوری بتن"
    این واژه مستقیماً از کتاب آزمایشات فناوری بتن استخراج شده است.

"""

book_md = """# 📖 واژگان اختصاصی کتاب آزمایشات فناوری بتن

!!! success "به دیکشنری تخصصی خوش آمدید"
    این واژگان، برابرهای مصوب **فرهنگستان زبان و ادب فارسی** هستند که در کتاب آزمایشات فناوری بتن به کار رفته‌اند.

<div class="grid cards" markdown>
"""

for term in terms_data:
    if term.get("featured_book"):
        fa = term.get("term_fa")
        en = term.get("term_en")

        fa_safe = fa.replace("/", "-").replace("\\", "-")
        en_safe = en.lower().replace("/", "-").replace("\\", "-")

        actual_file = None
        link = ""

        if os.path.exists(f"docs/terms/{fa_safe}.md"):
            actual_file = f"docs/terms/{fa_safe}.md"
            link = f"terms/{fa_safe}.md"
        elif os.path.exists(f"docs/terms/{en_safe}.md"):
            actual_file = f"docs/terms/{en_safe}.md"
            link = f"terms/{en_safe}.md"

        if actual_file:
            with open(actual_file, "r", encoding="utf-8") as f:
                md_content = f.read()

            if "ویژه کتاب" not in md_content:
                with open(actual_file, "w", encoding="utf-8") as f:
                    f.write(admonition + md_content)

            book_md += f"""
-   :material-book:{{ .lg .middle }} **{fa}** ({en})
    ---
    {term.get("definition", "برابر مصوب فرهنگستان زبان و ادب فارسی.")}
    [:octicons-arrow-right-24: مشاهده جزئیات]({link})
"""

book_md += "\n</div>\n"
with open("docs/book-vocab.md", "w", encoding="utf-8") as f:
    f.write(book_md)

print("✅ شاهکار انجام شد! حالا تغییرات را کامیت و پوش کنید.")
