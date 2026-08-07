#!/usr/bin/env python3
"""
تبدیل data/terms.yaml به صفحات Markdown - نسخه نهایی
"""

import sys
import re
import unicodedata
import hashlib
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ PyYAML نصب نیست: pip install pyyaml")
    sys.exit(1)


def normalize_persian(text: str) -> str:
    """نرمال‌سازی حروف فارسی"""
    if not text:
        return text
    text = text.replace("ي", "ی").replace("ك", "ک")
    return unicodedata.normalize("NFKC", text)


def slugify_english(text: str) -> str:
    """تولید slug انگلیسی قابل اطمینان"""
    if not text:
        return ""
    text = normalize_persian(text)

    # نگاشت فارسی به لاتین
    fa_to_en = {
        "آ": "a",
        "ا": "a",
        "ب": "b",
        "پ": "p",
        "ت": "t",
        "ث": "s",
        "ج": "j",
        "چ": "ch",
        "ح": "h",
        "خ": "kh",
        "د": "d",
        "ذ": "z",
        "ر": "r",
        "ز": "z",
        "ژ": "zh",
        "س": "s",
        "ش": "sh",
        "ص": "s",
        "ض": "z",
        "ط": "t",
        "ظ": "z",
        "ع": "a",
        "غ": "gh",
        "ف": "f",
        "ق": "gh",
        "ک": "k",
        "گ": "g",
        "ل": "l",
        "م": "m",
        "ن": "n",
        "و": "v",
        "ه": "h",
        "ی": "y",
        "ئ": "y",
        "ة": "h",
        "۰": "0",
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
    }

    result = "".join(fa_to_en.get(c, "") for c in text)
    result = re.sub(r"[^a-z0-9\-]", "", result.lower())
    result = re.sub(r"-+", "-", result).strip("-")

    # اگر خالی بود، از hash استفاده کن
    if not result:
        return "term-" + hashlib.md5(text.encode()).hexdigest()[:8]

    return result


def main():
    data_file = Path("data/terms.yaml")
    if not data_file.exists():
        print("❌ data/terms.yaml یافت نشد")
        sys.exit(1)

    with open(data_file, "r", encoding="utf-8") as f:
        raw_terms = yaml.safe_load(f)

    if not isinstance(raw_terms, list):
        print("❌ data/terms.yaml باید لیست باشد")
        sys.exit(1)

    valid_terms = []
    seen_slugs = set()

    for i, term in enumerate(raw_terms):
        if not isinstance(term, dict):
            continue

        term_fa = term.get("term_fa", "").strip()
        if not term_fa:
            continue

        term["term_fa"] = normalize_persian(term_fa)

        # تولید slug یکتا
        slug = term.get("slug", "").strip()
        if not slug:
            term_en = term.get("term_en", "").strip()
            if term_en:
                slug = re.sub(r"[^a-z0-9\s-]", "", term_en.lower())
                slug = re.sub(r"[\s]+", "-", slug.strip())
            else:
                slug = slugify_english(term_fa)

            # یکتا کردن
            base_slug = slug
            counter = 1
            while slug in seen_slugs:
                slug = f"{base_slug}-{counter}"
                counter += 1

            term["slug"] = slug

        seen_slugs.add(term["slug"])
        valid_terms.append(term)

    if not valid_terms:
        print("❌ هیچ واژه معتبری یافت نشد")
        sys.exit(1)

    print(f"📚 {len(valid_terms)} واژه بارگذاری شد")

    terms_dir = Path("docs/terms")
    terms_dir.mkdir(parents=True, exist_ok=True)

    # پاک کردن فایل‌های قدیمی
    for old_file in terms_dir.glob("*.md"):
        old_file.unlink()

    slug_to_file = {term["slug"]: f"{term['slug']}.md" for term in valid_terms}
    slug_to_term_fa = {term["slug"]: term["term_fa"] for term in valid_terms}

    for term in valid_terms:
        slug = term["slug"]
        term_fa = term["term_fa"]
        term_en = term.get("term_en", "")
        term_fr = term.get("term_fr", "")
        term_de = term.get("term_de", "")
        term_ar = term.get("term_ar", "")
        category = term.get("category", "عمومی")
        definition = term.get("definition", "تعریفی ثبت نشده است.").strip()
        references = term.get("references", []) or []
        related_terms = term.get("related_terms", []) or []
        standards = term.get("standards", "")
        source = term.get("source", "")
        featured_book = term.get("featured_book", False)

        page = f"""---
title: {term_fa}
description: تعریف و معادل‌های واژه {term_fa}
slug: {slug}
---

# {term_fa}
"""
        if featured_book:
            page += '\n!!! note "از کتاب آزمایشات فناوری بتن"\n    این واژه در کتاب آزمایشات فناوری بتن آورده شده است.\n'

        page += f"""
<div class="term-card">

## معادل‌های واژه

| زبان | معادل |
|------|-------|
| **انگلیسی** | {term_en or "—"} |
| **فرانسوی** | {term_fr or "—"} |
| **آلمانی** | {term_de or "—"} |
| **عربی** | {term_ar or "—"} |

</div>

## تعریف

{definition}

## دسته‌بندی
**{category}**
"""
        if standards:
            page += f"\n## استانداردهای مرتبط\n{standards}\n"

        page += "\n## منابع\n"
        if references:
            for ref in references:
                page += f"- {ref}\n"
        elif source:
            page += f"- {source}\n"
        else:
            page += "منبعی ثبت نشده است.\n"

        page += '\n## واژه‌های مرتبط\n<div class="related-terms">\n'
        if related_terms:
            valid_related = []
            for rel_slug in related_terms:
                if rel_slug in slug_to_file:
                    rel_term_fa = slug_to_term_fa[rel_slug]
                    rel_filename = slug_to_file[rel_slug]
                    valid_related.append(
                        f'<a href="./{rel_filename}">{rel_term_fa}</a>'
                    )

            page += (
                "\n".join(valid_related) + "\n"
                if valid_related
                else "واژه مرتبطی ثبت نشده است.\n"
            )
        else:
            page += "واژه مرتبطی ثبت نشده است.\n"

        page += """
</div>

---

بازگشت به [فهرست](index.md)
"""
        output_file = terms_dir / f"{slug}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(page)

    print(f"✅ {len(valid_terms)} صفحه تولید شد")

    # فهرست الفبایی
    terms_by_letter = {}
    for term in valid_terms:
        letter = normalize_persian(term["term_fa"])[0]
        terms_by_letter.setdefault(letter, []).append((term["term_fa"], term["slug"]))

    index_content = """---
title: فهرست واژگان
description: فهرست الفبایی تمام واژگان تخصصی مهندسی
---

# فهرست واژگان

!!! note "راهنما"
    برای جستجوی واژه خاص، از نوار جستجوی بالا استفاده کنید.

## فهرست الفبایی

"""
    persian_alphabet = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
    for letter in sorted(
        terms_by_letter.keys(),
        key=lambda l: persian_alphabet.find(l) if l in persian_alphabet else 999,
    ):
        index_content += f"\n### حرف {letter}\n\n"
        for term_fa, slug in sorted(terms_by_letter[letter]):
            index_content += f"- [{term_fa}]({slug}.md)\n"

    with open(terms_dir / "index.md", "w", encoding="utf-8") as f:
        f.write(index_content)

    print("✅ فهرست الفبایی ساخته شد")


if __name__ == "__main__":
    main()
