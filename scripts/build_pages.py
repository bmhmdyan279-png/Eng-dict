#!/usr/bin/env python3
"""
اسکریپت ساخت صفحات واژگان از data/terms.yaml
مخصوص اجرا در GitHub Actions و محیط محلی
"""

import os
import re
from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    print("نصب PyYAML...")
    os.system("pip install pyyaml")
    import yaml

def slugify(text):
    if not text:
        return ""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def main():
    data_file = Path("data/terms.yaml")
    if not data_file.exists():
        print("❌ فایل data/terms.yaml یافت نشد.")
        sys.exit(1)

    with open(data_file, "r", encoding="utf-8") as f:
        raw_terms = yaml.safe_load(f)

    if not isinstance(raw_terms, list):
        print("❌ ساختار data/terms.yaml باید یک لیست باشد.")
        sys.exit(1)

    # فیلتر واژه‌های معتبر (حتماً term_fa داشته باشند)
    valid_terms = []
    for i, term in enumerate(raw_terms):
        if isinstance(term, dict) and 'term_fa' in term and term['term_fa']:
            valid_terms.append(term)
        else:
            print(f"⚠️ آیتم {i+1} نامعتبر یا فاقد term_fa - نادیده گرفته شد.")

    if not valid_terms:
        print("❌ هیچ واژه معتبری با فیلد term_fa یافت نشد.")
        sys.exit(1)

    print(f"📚 {len(valid_terms)} واژه معتبر بارگذاری شد.")

    terms_dir = Path("docs/terms")
    terms_dir.mkdir(parents=True, exist_ok=True)

    # نگاشت slug به نام فایل
    slug_to_file = {}
    for term in valid_terms:
        slug = term.get('slug', slugify(term.get('term_en', '')))
        slug_to_file[slug] = f"{term['term_fa']}.md"

    # تولید صفحات
    for term in valid_terms:
        term_fa = term['term_fa']
        term_en = term.get('term_en', '')
        term_fr = term.get('term_fr', '')
        term_de = term.get('term_de', '')
        term_ar = term.get('term_ar', '')
        category = term.get('category', 'عمومی')
        definition = term.get('definition', 'تعریفی ثبت نشده است.')
        references = term.get('references', [])
        related_terms = term.get('related_terms', [])

        page = f"""---
title: {term_fa}
description: تعریف و معادل‌های واژه {term_fa}
---

# {term_fa}

<div class="term-card">

## معادل‌های واژه

| زبان | معادل |
|------|-------|
| **انگلیسی** | {term_en} |
| **فرانسوی** | {term_fr} |
| **آلمانی** | {term_de} |
| **عربی** | {term_ar} |

</div>

## تعریف

{definition}

## دسته‌بندی
**{category}**

## منابع
"""
        if references:
            for ref in references:
                page += f"- {ref}\n"
        else:
            page += "منبعی ثبت نشده است.\n"

        page += """
## واژه‌های مرتبط
<div class="related-terms">
"""
        if related_terms:
            for slug in related_terms:
                related_file = slug_to_file.get(slug, f"{slug}.md")
                page += f'<a href="./{related_file}">{slug}</a>\n'
        else:
            page += "واژه مرتبطی ثبت نشده است.\n"

        page += """
</div>

---

[بازگشت به فهرست](index.md)
"""
        output_file = terms_dir / f"{term_fa}.md"
        output_file = output_file.with_name(output_file.name.replace(" / ", "-").replace("/", "-"))
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(page)
        print(f"   ✓ {term_fa}")

    # ساخت فهرست الفبایی
    terms_by_letter = {}
    for term in valid_terms:
        first_letter = term['term_fa'][0]
        if first_letter not in terms_by_letter:
            terms_by_letter[first_letter] = []
        terms_by_letter[first_letter].append(term['term_fa'])

    index_content = """---
title: فهرست واژگان
description: فهرست الفبایی تمام واژگان تخصصی مهندسی
---

# فهرست واژگان

<div class="admonition note">
<p class="admonition-title">راهنما</p>
<p>برای جستجوی واژه خاص، از نوار جستجوی بالا استفاده کنید.</p>
</div>

## فهرست الفبایی

"""
    for letter in sorted(terms_by_letter.keys()):
        index_content += f"\n### حرف {letter}\n\n"
        for term_fa in sorted(terms_by_letter[letter]):
            index_content += f"- [{term_fa}]({term_fa}.md)\n"

    with open(terms_dir / "index.md", "w", encoding="utf-8") as f:
        f.write(index_content)

    print("✅ فهرست الفبایی ساخته شد.")
    print("🎉 تمام صفحات واژگان با موفقیت تولید شدند.")

if __name__ == "__main__":
    main()