#!/usr/bin/env python3
"""ساخت صفحات Markdown از YAML (فاز ۲)."""
import yaml
from pathlib import Path

SITE_NAME = 'فرهنگ واژه\u200cهای تخصصی مهندسی'  # مقدار از پیش تنظیم‌شده

def load_terms(path="data/terms.yaml"):
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []

def term_md(t):
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

    L = ["---", f"title: {fa}", f"description: تعریف {fa} در فرهنگ مهندسی",
         f"keywords: [{', '.join([fa, en, cat])}]", "---", "",
         f"# {fa}{f' / {en}' if en else ''}", ""]

    aliases = t.get("aliases", [])
    if aliases:
        L.append(f"**هم‌نام‌ها:** {'، '.join(aliases)}\n")

    if langs:
        L += ["## معادل‌ها", "", "| زبان | معادل |", "|------|-------|"]
        names = {"en":"انگلیسی","fr":"فرانسوی","de":"آلمانی","ar":"عربی","tr":"ترکی","ru":"روسی","es":"اسپانیایی"}
        for c, v in langs.items():
            L.append(f"| {names.get(c, c.upper())} | {v} |")
        L.append("")

    if defn:
        L += ["## تعریف", "", defn, ""]

    L += [f"## دسته", "", f"`{cat}`", ""]

    if stds:
        L += ["## استانداردهای مرتبط", ""]
        for s in stds: L.append(f"- `{s}`")
        L.append("")

    if rel:
        L += ["## واژه‌های مرتبط", ""]
        for r in rel: L.append(f"- [{r}](./{r}.md)")
        L.append("")

    if src or upd:
        L += ["## اطلاعات تکمیلی", ""]
        if src: L.append(f"- **منبع:** `{src}`")
        if upd: L.append(f"- **به‌روزرسانی:** {upd}")
        L.append("")

    L += ["---", "", '??? info "نحوهٔ ارجاع"', "",
          f"    {SITE_NAME}، مدخل «{fa}»، {upd}.", ""]
    return "\n".join(L)

def alpha_idx(terms):
    L = ["---", "title: فهرست الفبایی", "---", "",
         "# فهرست الفبایی واژه‌ها", "",
         "همهٔ واژه‌ها به ترتیب الفبای فارسی.", ""]
    by_l = {}
    for t in terms:
        fa = t.get("fa", t["id"])
        by_l.setdefault(fa[0] if fa else "?", []).append((fa, t.get("slug", t["id"])))
    alphabet = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
    letters = sorted(by_l.keys(), key=lambda x: alphabet.index(x) if x in alphabet else 999)
    L.append("**پرش به حرف:** " + " · ".join(f"[{l}](#{l})" for l in letters) + "\n")
    for l in letters:
        L += [f"## <a name='{l}'></a>{l}", ""]
        for fa, s in sorted(by_l[l]): L.append(f"- [{fa}](./{s}.md)")
        L.append("")
    return "\n".join(L)

def cat_idx(terms):
    L = ["---", "title: دسته‌بندی", "---", "", "# واژه‌ها بر اساس دسته", ""]
    by_c = {}
    for t in terms: by_c.setdefault(t.get("category","سایر"), []).append(t)
    for c, ts in sorted(by_c.items()):
        L += [f"## {c}", ""]
        for t in sorted(ts, key=lambda x: x.get("fa","")):
            L.append(f"- [{t['fa']}](./{t.get('slug',t['id'])}.md)")
        L.append("")
    return "\n".join(L)

def main():
    d = Path("docs/terms"); d.mkdir(parents=True, exist_ok=True)
    terms = load_terms()
    print(f"Loaded {len(terms)} terms.")
    for t in terms:
        p = d / f"{t.get('slug', t['id'])}.md"
        p.write_text(term_md(t), encoding="utf-8")
        print(f"  ✅ {p}")
    (d/"index.md").write_text(alpha_idx(terms), encoding="utf-8")
    print("  ✅ docs/terms/index.md")
    (d/"categories.md").write_text(cat_idx(terms), encoding="utf-8")
    print("  ✅ docs/terms/categories.md")

if __name__ == "__main__":
    main()
