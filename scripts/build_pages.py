#!/usr/bin/env python3
"""ساخت صفحات Markdown از داده‌های YAML."""
import sys
from pathlib import Path
import yaml

def load_terms(path: str = "data/terms.yaml") -> list:
    p = Path(path)
    if not p.exists():
        print(f"❌ فایل {path} پیدا نشد. ابتدا setup.py را اجرا کنید.", file=sys.stderr)
        sys.exit(1)
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or []
    print(f"📂 {len(data)} واژه از YAML بارگذاری شد.")
    return data

def term_markdown(t: dict) -> str:
    fa = t.get("fa", t["id"])
    en = t.get("languages", {}).get("en", "")
    slug = t.get("slug", t["id"])
    langs = t.get("languages", {})
    cat = t.get("category", "—")
    defn = t.get("definition", "").strip()
    stds = t.get("standards", [])
    rel = t.get("related", [])
    src = t.get("source", "")
    upd = t.get("last_updated", "")

    lines = [
        "---",
        f"title: {fa}",
        f"description: تعریف {fa} در فرهنگ بتن",
        "---",
        "",
        f"# {fa}{f' / {en}' if en else ''}",
        "",
    ]

    if langs:
        lines += ["## معادل‌ها", "", "| زبان | معادل |", "|------|-------|"]
        lang_names = {"en":"انگلیسی","fr":"فرانسوی","de":"آلمانی","ar":"عربی","tr":"ترکی","ru":"روسی"}
        for code, word in langs.items():
            lines.append(f"| {lang_names.get(code, code.upper())} | {word} |")
        lines.append("")

    if defn:
        lines += ["## تعریف", "", defn, ""]

    lines += ["## دسته", "", f"`{cat}`", ""]

    if stds:
        lines += ["## استانداردهای مرتبط", ""]
        for s in stds:
            lines.append(f"- `{s}`")
        lines.append("")

    if rel:
        lines += ["## واژه‌های مرتبط", ""]
        for r in rel:
            lines.append(f"- [{r}](./{r}.md)")
        lines.append("")

    if src or upd:
        lines += ["## اطلاعات تکمیلی", ""]
        if src:
            lines.append(f"- **منبع:** `{src}`")
        if upd:
            lines.append(f"- **به‌روزرسانی:** {upd}")
        lines.append("")

    # جعبهٔ ارجاع
    lines += [
        "---",
        "",
        '??? info "نحوهٔ ارجاع"',
        "",
        f"    فرهنگ واژه‌های تخصصی بتن، مدخل «{fa}»، {upd or 'بی‌تاریخ'}.",
        "",
    ]
    return "\n".join(lines)

def alphabetical_index(terms: list) -> str:
    lines = [
        "---",
        "title: فهرست الفبایی",
        "---",
        "",
        "# فهرست الفبایی واژه‌ها",
        "",
        "همهٔ واژه‌ها به ترتیب الفبای فارسی.",
        "",
    ]
    grouped = {}
    for t in terms:
        fa = t.get("fa", t["id"])
        initial = fa[0] if fa else "?"
        grouped.setdefault(initial, []).append((fa, t.get("slug", t["id"])))

    # الفبای فارسی (با احتساب حروف ویژه)
    persian_alphabet = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
    sorted_initials = sorted(
        grouped.keys(),
        key=lambda x: persian_alphabet.index(x) if x in persian_alphabet else 999
    )
    jump_line = "**پرش به حرف:** " + " · ".join(f"[{l}](#{l})" for l in sorted_initials) + "\n"
    lines.append(jump_line)

    for initial in sorted_initials:
        lines.append(f"## <a name='{initial}'></a>{initial}")
        lines.append("")
        for fa, slug in sorted(grouped[initial]):
            lines.append(f"- [{fa}](./{slug}.md)")
        lines.append("")
    return "\n".join(lines)

def category_index(terms: list) -> str:
    lines = [
        "---",
        "title: دسته‌بندی",
        "---",
        "",
        "# واژه‌ها بر اساس دسته",
        "",
    ]
    grouped = {}
    for t in terms:
        cat = t.get("category", "سایر")
        grouped.setdefault(cat, []).append(t)

    for cat, items in sorted(grouped.items()):
        lines.append(f"## {cat}")
        lines.append("")
        # مرتب‌سازی بر اساس نام فارسی
        for item in sorted(items, key=lambda x: x.get("fa", "")):
            lines.append(f"- [{item['fa']}](./{item.get('slug', item['id'])}.md)")
        lines.append("")
    return "\n".join(lines)

def main():
    terms_dir = Path("docs/terms")
    terms_dir.mkdir(parents=True, exist_ok=True)

    terms = load_terms()
    for t in terms:
        slug = t.get("slug", t["id"])
        file_path = terms_dir / f"{slug}.md"
        file_path.write_text(term_markdown(t), encoding="utf-8")
        print(f"  ✅ {file_path}")

    # صفحات شاخص
    idx_path = terms_dir / "index.md"
    idx_path.write_text(alphabetical_index(terms), encoding="utf-8")
    print(f"  ✅ {idx_path}")

    cat_path = terms_dir / "categories.md"
    cat_path.write_text(category_index(terms), encoding="utf-8")
    print(f"  ✅ {cat_path}")

if __name__ == "__main__":
    main()
