import yaml
import os
import re

TERMS_TO_FEATURE = [
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


def main():
    print("⏳ در حال اعمال تنظیمات...")

    # ۱. آپدیت فایل terms.yaml
    terms_file = "data/terms.yaml"
    if os.path.exists(terms_file):
        with open(terms_file, "r", encoding="utf-8") as f:
            terms = yaml.safe_load(f)

        for term in terms:
            if term.get("term_fa") in TERMS_TO_FEATURE:
                term["featured_book"] = True

        with open(terms_file, "w", encoding="utf-8") as f:
            yaml.dump(terms, f, allow_unicode=True, sort_keys=False)

    # ۲. ساخت خودکار صفحه book-vocab.md
    book_file = "docs/book-vocab.md"
    book_md = "# 📖 واژگان اختصاصی کتاب آزمایشات فناوری بتن\n\n"
    book_md += '!!! success "به دیکشنری تخصصی خوش آمدید"\n'
    book_md += "    این واژگان، برابرهای مصوب **فرهنگستان زبان و ادب فارسی** هستند که در کتاب آزمایشات فناوری بتن به کار رفته‌اند.\n\n"
    book_md += '<div class="grid cards" markdown>\n\n'

    for term in terms:
        if term.get("featured_book"):
            fa = term.get("term_fa")
            en = term.get("term_en")
            en_slug = en.lower().replace(" ", "-").replace("/", "-").strip("-")
            book_md += f"-   :material-book:{{ .lg .middle }} **{fa}** ({en})\n"
            book_md += f"    ---\n"
            book_md += f"    {term.get('definition', '')}\n"
            book_md += (
                f"    [:octicons-arrow-right-24: مشاهده جزئیات](terms/{en_slug}.md)\n\n"
            )

    book_md += "</div>\n"
    with open(book_file, "w", encoding="utf-8") as f:
        f.write(book_md)

    # ۳. تزریق خودکار کد به build_pages.py
    script_file = "scripts/build_pages.py"
    if os.path.exists(script_file):
        with open(script_file, "r", encoding="utf-8") as f:
            content = f.read()

        if "featured_book" not in content:
            match = re.search(r"([ \t]+)with open\([^\n]*?['\"]w['\"]\)", content)
            if match:
                indent = match.group(1)
                inject_code = f"""{indent}if term.get('featured_book'):
{indent}    md_content += \"\"\"

!!! info "واژه ویژه کتاب آزمایشات فناوری بتن"
    این واژه مستقیماً از کتاب آزمایشات فناوری بتن استخراج شده است.
\"\"\"
"""
                idx = match.start()
                new_content = content[:idx] + inject_code + "\n" + content[idx:]
                with open(script_file, "w", encoding="utf-8") as f:
                    f.write(new_content)

    print(
        "✅ تمام! حالا فقط اسکریپت اصلی را اجرا کرده و تغییرات را Commit و Push کنید."
    )


if __name__ == "__main__":
    main()
