#!/usr/bin/env python3
"""
حذف hide: navigation از تمام فایل‌های docs
تا صفحات در ناوبری (nav) قابل ارجاع باشند.
"""

from pathlib import Path
import re

DOCS_DIR = Path(__file__).resolve().parent / "docs"

def fix_hide_navigation(md_file: Path):
    try:
        text = md_file.read_text(encoding="utf-8")
    except Exception:
        return False

    original = text
    # الگوهای مختلف hide را اصلاح می‌کنیم
    # ۱. hide: [navigation, toc] → hide: [toc]   (فقط toc بماند)
    # ۲. hide: [toc, navigation] → hide: [toc]
    # ۳. hide: [navigation] → خط hide کاملاً حذف شود
    # ۴. hide: navigation → حذف خط

    # حالت اول: hide: [navigation, toc] یا [toc, navigation]
    text = re.sub(r'^hide:\s*\[navigation,\s*toc\]', 'hide: [toc]', text, flags=re.MULTILINE)
    text = re.sub(r'^hide:\s*\[toc,\s*navigation\]', 'hide: [toc]', text, flags=re.MULTILINE)

    # حالت دوم: hide: [navigation] (بدون چیز دیگر)
    text = re.sub(r'^hide:\s*\[navigation\]\s*$', '', text, flags=re.MULTILINE)

    # حالت سوم: hide: navigation (بدون براکت)
    text = re.sub(r'^hide:\s*navigation\s*$', '', text, flags=re.MULTILINE)

    if text != original:
        md_file.write_text(text, encoding="utf-8", newline='\n')
        return True
    return False

def main():
    count = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        if fix_hide_navigation(md_file):
            print(f"✅ اصلاح شد: {md_file.relative_to(DOCS_DIR)}")
            count += 1
    print(f"\n✨ {count} فایل اصلاح شدند. حالا mkdocs serve را اجرا کنید.")

if __name__ == "__main__":
    main()