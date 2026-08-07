import os
import builtins

print("⏳ در حال رفع مشکل اسلش ویندوز و ساخت کامل واژگان...")

# ۱. هوک کردن open برای جلوگیری از خطای نام فایل در ویندوز
original_open = builtins.open


def custom_open(file, mode="r", *args, **kwargs):
    if "w" in mode and isinstance(file, str) and "terms" in file:
        dir_name = os.path.dirname(file)
        base_name = os.path.basename(file)
        for char in ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]:
            base_name = base_name.replace(char, "-")
        file = os.path.join(dir_name, base_name)
    return original_open(file, mode, *args, **kwargs)


builtins.open = custom_open

# ۲. اجرای build_pages.py با هوک فعال
print("🔄 در حال اجرای build_pages.py...")
try:
    with original_open("scripts/build_pages.py", "r", encoding="utf-8") as f:
        code = f.read()
    namespace = {
        "__name__": "__main__",
        "__file__": "scripts/build_pages.py",
        "__builtins__": builtins,
    }
    exec(code, namespace)
except Exception as e:
    print(f"❌ خطا در اجرای اسکریپت اصلی: {e}")
    exit(1)

# برگرداندن open به حالت عادی
builtins.open = original_open

# ۳. افزودن باکس ویژه به فایل‌های ساخته شده و ساخت صفحه فرود
admonition = """!!! info "واژه ویژه کتاب آزمایشات فناوری بتن"
    این واژه مستقیماً از کتاب آزمایشات فناوری بتن استخراج شده است.

"""

book_md = """# 📖 واژگان اختصاصی کتاب آزمایشات فناوری بتن

!!! success "به دیکشنری تخصصی خوش آمدید"
    این واژگان، برابرهای مصوب **فرهنگستان زبان و ادب فارسی** هستند که در کتاب آزمایشات فناوری بتن به کار رفته‌اند.

<div class="grid cards" markdown>
"""

terms_data = [
    ("رقمی", "Digital"),
    ("تاوَن", "Oven"),
    ("اندازه غربالی", "Mesh"),
    ("واسنجیدن", "Calibration"),
    ("آمادگاه", "Depot"),
    ("جیک", "Jig / Jigging"),
    ("آژند", "Cement"),
    ("واپایش", "Control"),
    ("تشریفات", "Protocol"),
    ("دسته", "Batch"),
    ("مخلوط ساز", "Batching"),
    ("رواداری / تحمل", "Tolerance"),
    ("بسامد", "Frequency"),
    ("لرزاننده", "Vibrator"),
    ("تالار", "Gallery"),
    ("بطری چگالی", "Pycnometer"),
]

for fa, en in terms_data:
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
        with original_open(actual_file, "r", encoding="utf-8") as f:
            content = f.read()
        if "ویژه کتاب" not in content:
            with original_open(actual_file, "w", encoding="utf-8") as f:
                f.write(admonition + content)

        book_md += f"""
-   :material-book:{{ .lg .middle }} **{fa}** ({en})
    ---
    برابر مصوب فرهنگستان زبان و ادب فارسی.
    [:octicons-arrow-right-24: مشاهده جزئیات]({link})
"""

book_md += "\n</div>\n"
with original_open("docs/book-vocab.md", "w", encoding="utf-8") as f:
    f.write(book_md)

print("✅ تمام! حالا تغییرات را کامیت و پوش کنید.")
