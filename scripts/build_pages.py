#!/usr/bin/env python3
import sys
import yaml
from pathlib import Path
from slugify import slugify
import unicodedata

def normalize_persian(text: str) -> str:
    if not text: return ""
    text = text.replace("ي", "ی").replace("ك", "ک")
    return unicodedata.normalize("NFKC", text)

def main():
    data_file = Path("data/terms.yaml")
    if not data_file.exists():
        sys.exit("data/terms.yaml not found")

    with open(data_file, "r", encoding="utf-8") as f:
        raw_terms = yaml.safe_load(f)

    valid_terms, seen_slugs, seen_terms = [], set(), set()

    for term in raw_terms:
        if not isinstance(term, dict): continue

        term_fa = normalize_persian(str(term.get("term_fa") or "").strip())
        if not term_fa or term_fa in seen_terms: continue

        seen_terms.add(term_fa)
        term["term_fa"] = term_fa

        slug = term.get("slug") or ""
        if not slug:
            term_en = str(term.get("term_en") or "").strip()
            slug = slugify(term_en if term_en else term_fa, separator='-', lowercase=True)

        base_slug, counter = slug, 1
        while slug in seen_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1

        term["slug"] = slug
        seen_slugs.add(slug)
        valid_terms.append(term)

    if not valid_terms: sys.exit("No valid terms found")

    terms_dir = Path("docs/terms")
    terms_dir.mkdir(parents=True, exist_ok=True)
    for old_file in terms_dir.glob("*.md"): old_file.unlink()

    slug_to_file = {t["slug"]: f"{t['slug']}.md" for t in valid_terms}
    slug_to_term_fa = {t["slug"]: t["term_fa"] for t in valid_terms}

    for term in valid_terms:
        slug, term_fa = term["slug"], term["term_fa"]
        term_en = str(term.get("term_en") or "—").strip() or "—"
        term_fr = str(term.get("term_fr") or "—").strip() or "—"
        term_de = str(term.get("term_de") or "—").strip() or "—"
        term_ar = str(term.get("term_ar") or "—").strip() or "—"
        category = str(term.get("category") or "عمومی").strip()
        definition = str(term.get("definition") or "تعریفی ثبت نشده است.").strip()
        references = term.get("references") or []
        if isinstance(references, str): references = [references]
        related_terms = term.get("related_terms") or []
        if isinstance(related_terms, str): related_terms = [related_terms]
        standards, source = term.get("standards") or "", term.get("source") or ""
        featured_book = term.get("featured_book", False)

        page = f"---\ntitle: {term_fa}\ndescription: تعریف و معادل‌های واژه {term_fa}\nslug: {slug}\n---\n\n# {term_fa}\n"
        if featured_book: page += '\n!!! note "از کتاب آزمایشات فناوری بتن"\n    این واژه در کتاب آزمایشات فناوری بتن آورده شده است.\n'

        page += f"""
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
"""
        if standards: page += f"\n## استانداردهای مرتبط\n{standards}\n"

        page += "\n## منابع\n"
        if references:
            for ref in references: page += f"- {ref}\n"
        elif source: page += f"- {source}\n"
        else: page += "منبعی ثبت نشده است.\n"

        page += '\n## واژه‌های مرتبط\n<div class="related-terms">\n'
        valid_related = [f'<a href="./{slug_to_file[r]}">{slug_to_term_fa[r]}</a>' for r in related_terms if r in slug_to_file]
        page += ("\n".join(valid_related) + "\n" if valid_related else "واژه مرتبطی ثبت نشده است.\n")
        page += "\n</div>\n\n---\n\nبازگشت به فهرست\n"

        (terms_dir / f"{slug}.md").write_text(page, encoding="utf-8")

    terms_by_letter = {}
    for term in valid_terms:
        letter = normalize_persian(term["term_fa"])[0]
        terms_by_letter.setdefault(letter, []).append((term["term_fa"], term["slug"]))

    index_content = "---\ntitle: فهرست واژگان\n---\n\n# فهرست واژگان\n\n## فهرست الفبایی\n\n"
    persian_alphabet = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
    for letter in sorted(terms_by_letter.keys(), key=lambda l: persian_alphabet.find(l) if l in persian_alphabet else 999):
        index_content += f"\n### حرف {letter}\n\n"
        for term_fa, slug in sorted(terms_by_letter[letter]):
            index_content += f"- [{term_fa}](./{slug}.md)\n"

    (terms_dir / "index.md").write_text(index_content, encoding="utf-8")
    print(f"✅ {len(valid_terms)} صفحه تولید شد")

if __name__ == "__main__":
    main()
