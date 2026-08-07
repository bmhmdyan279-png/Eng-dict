#!/usr/bin/env python3
"""
اصلاح لینک‌های فارسی قدیمی در book-vocab.md و construction-terms.md
"""

import re
import yaml
from pathlib import Path


def normalize_persian(text: str) -> str:
    if not text:
        return text
    text = text.replace('ي', 'ی').replace('ك', 'ک')
    return text


def build_mapping():
    """ساخت نگاشت از واژه فارسی به slug انگلیسی"""
    data_file = Path("data/terms.yaml")
    with open(data_file, "r", encoding="utf-8") as f:
        terms = yaml.safe_load(f)
    
    mapping = {}
    seen_slugs = set()
    
    for term in terms:
        if not isinstance(term, dict):
            continue
        
        term_fa = term.get('term_fa', '').strip()
        if not term_fa:
            continue
        
        term_fa = normalize_persian(term_fa)
        
        # تولید slug
        slug = term.get('slug', '').strip()
        if not slug:
            term_en = term.get('term_en', '').strip()
            if term_en:
                slug = re.sub(r'[^a-z0-9\s-]', '', term_en.lower())
                slug = re.sub(r'[\s]+', '-', slug.strip())
            else:
                # slugify فارسی ساده
                fa_to_en = {
                    'آ': 'a', 'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's',
                    'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'z',
                    'ر': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's',
                    'ض': 'z', 'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f',
                    'ق': 'gh', 'ک': 'k', 'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n',
                    'و': 'v', 'ه': 'h', 'ی': 'y',
                }
                slug = ''.join(fa_to_en.get(c, '') for c in term_fa)
                slug = re.sub(r'[^a-z0-9\-]', '', slug.lower())
        
        # یکتا کردن
        base_slug = slug
        counter = 1
        while slug in seen_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        mapping[term_fa] = slug
        seen_slugs.add(slug)
    
    return mapping


def fix_file(filepath: Path, mapping: dict):
    """اصلاح لینک‌ها در یک فایل"""
    if not filepath.exists():
        print(f"⚠️ فایل {filepath} یافت نشد")
        return
    
    content = filepath.read_text(encoding='utf-8')
    original = content
    
    # پیدا کردن تمام لینک‌های فارسی
    # الگو: [متن](terms/واژه-فارسی.md)
    pattern = r'\[([^\]]+)\]\(terms/([^)]+\.md)\)'
    
    def replace_link(match):
        link_text = match.group(1)
        filename = match.group(2)
        
        # حذف .md و تبدیل به واژه فارسی
        term_fa = filename.replace('.md', '')
        term_fa_normalized = normalize_persian(term_fa)
        
        # پیدا کردن slug جدید
        if term_fa_normalized in mapping:
            new_slug = mapping[term_fa_normalized]
            return f'[{link_text}](terms/{new_slug}.md)'
        else:
            # اگر پیدا نشد، لینک را حذف کن
            return f'~~{link_text}~~'
    
    content = re.sub(pattern, replace_link, content)
    
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        print(f"✅ {filepath} اصلاح شد")
    else:
        print(f"ℹ️ {filepath} تغییری نکرد")


def main():
    print("🔍 ساخت نگاشت واژه‌ها...")
    mapping = build_mapping()
    print(f"📚 {len(mapping)} واژه نگاشت شد")
    
    # اصلاح فایل‌های مشکل‌دار
    files_to_fix = [
        Path("docs/book-vocab.md"),
        Path("docs/construction-terms.md"),
    ]
    
    for filepath in files_to_fix:
        fix_file(filepath, mapping)
    
    print("🎉 اصلاح لینک‌ها کامل شد")


if __name__ == "__main__":
    main()
