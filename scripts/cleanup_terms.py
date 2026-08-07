#!/usr/bin/env python3
"""
پاکسازی و یکسان‌سازی data/terms.yaml
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ PyYAML نصب نیست: pip install pyyaml")
    sys.exit(1)


def cleanup_terms():
    data_file = Path("data/terms.yaml")
    if not data_file.exists():
        print("❌ data/terms.yaml یافت نشد")
        return

    # پشتیبان‌گیری
    backup_file = Path("data/terms_backup.yaml")
    backup_file.write_text(data_file.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"✅ پشتیبان در {backup_file} ذخیره شد")

    with open(data_file, "r", encoding="utf-8") as f:
        terms = yaml.safe_load(f)

    if not isinstance(terms, list):
        print("❌ فایل معتبر نیست")
        return

    cleaned = []
    seen_terms = set()

    for term in terms:
        if not isinstance(term, dict):
            continue

        term_fa = term.get("term_fa", "").strip()
        if not term_fa:
            continue

        # نرمال‌سازی
        term["term_fa"] = term_fa.replace("ي", "ی").replace("ك", "ک")

        # یکسان‌سازی فیلدهای منبع
        references = term.get("references", [])
        standards = term.get("standards", "")
        source = term.get("source", "")

        # تبدیل همه به یک لیست references
        if isinstance(references, str):
            references = [references] if references else []

        if standards and standards not in references:
            references.append(standards)

        if source and source not in references:
            references.append(source)

        term["references"] = references
        term.pop("standards", None)
        term.pop("source", None)

        # حذف فیلدهای اضافی
        if "featured_book" in term:
            term["featured_book"] = bool(term["featured_book"])

        # بررسی تکراری
        key = term_fa.lower()
        if key in seen_terms:
            print(f"⚠️  تکراری حذف شد: {term_fa}")
            continue

        seen_terms.add(key)
        cleaned.append(term)

    # ذخیره فایل تمیز
    with open(data_file, "w", encoding="utf-8") as f:
        yaml.dump(
            cleaned, f, allow_unicode=True, sort_keys=False, default_flow_style=False
        )

    print(f"✅ {len(cleaned)} واژه تمیز ذخیره شد (از {len(terms)} واژه اولیه)")


if __name__ == "__main__":
    cleanup_terms()
