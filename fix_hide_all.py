#!/usr/bin/env python3
"""
حذف قاطعانهٔ هرگونه hide: navigation از تمام فایل‌های Markdown در docs/
"""

from pathlib import Path
import re

DOCS_DIR = Path(__file__).resolve().parent / "docs"

def remove_hide_navigation(text: str) -> str:
    """تمام حالات hide: navigation را حذف می‌کند."""
    # hide: [navigation, toc] -> hide: [toc]
    text = re.sub(r'^hide:\s*\[navigation,\s*toc\]', 'hide: [toc]', text, flags=re.MULTILINE)
    # hide: [toc, navigation] -> hide: [toc]
    text = re.sub(r'^hide:\s*\[toc,\s*navigation\]', 'hide: [toc]', text, flags=re.MULTILINE)
    # hide: [navigation] -> (حذف کامل خط)
    text = re.sub(r'^hide:\s*\[navigation\]\s*$', '', text, flags=re.MULTILINE)
    # hide: navigation -> (حذف خط)
    text = re.sub(r'^hide:\s*navigation\s*$', '', text, flags=re.MULTILINE)
    # hide: [navigation, ... چیزهای دیگر] -> navigation حذف شود
    text = re.sub(r'^hide:\s*\[([^\]]*),\s*navigation\s*\]', r'hide: [\1]', text, flags=re.MULTILINE)
    text = re.sub(r'^hide:\s*\[navigation,\s*([^\]]*)\]', r'hide: [\1]', text, flags=re.MULTILINE)
    return text

def main():
    count = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        try:
            original = md_file.read_text(encoding="utf-8")
        except Exception:
            continue
        cleaned = remove_hide_navigation(original)
        # حذف خطوط خالی اضافی که ممکن است از حذف hide باقی مانده باشد
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)
        if cleaned != original:
            md_file.write_text(cleaned, encoding="utf-8", newline='\n')
            print(f"✅ اصلاح شد: {md_file.relative_to(DOCS_DIR)}")
            count += 1
    if count == 0:
        print("ℹ️  هیچ فایلی نیاز به اصلاح نداشت.")
    else:
        print(f"\n✨ {count} فایل اصلاح شدند.")

if __name__ == "__main__":
    main()