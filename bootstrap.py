import os
import re
from pathlib import Path
import shutil

try:
    import yaml
except ImportError:
    print("نصب PyYAML...")
    os.system("pip install pyyaml")
    import yaml

# ۱. ساخت پوشه‌های ضروری
for folder in ["docs/terms", "data", "scripts", ".github/workflows"]:
    Path(folder).mkdir(parents=True, exist_ok=True)
print("✅ پوشه‌ها آماده شدند.")

# ۲. ایجاد contribute.md در صورت نبود
contribute_file = Path("docs/contribute.md")
if not contribute_file.exists():
    contribute_content = """# راهنمای مشارکت

## مقدمه
از اینکه می‌خواهید در توسعه این فرهنگ واژگان مشارکت کنید، سپاسگزاریم!

## روش‌های مشارکت

### ۱. افزودن واژه جدید
برای افزودن یک واژه جدید، فایل `data/terms.yaml` را ویرایش کنید.

فرمت مورد نیاز:
```yaml
- term_fa: "نام واژه به فارسی"
  term_en: "English term"
  term_fr: "Terme français"
  term_de: "Deutscher Begriff"
  term_ar: "المصطلح العربي"
  category: "دسته‌بندی واژه"
  definition: |
    تعریف کامل و دقیق واژه.
  references:
    - "منبع اول"
  related_terms:
    - "slug-واژه-مرتبط"
  slug: "slug-واژه"
```

### ۲. بهبود تعاریف موجود
اگر تعریف یک واژه ناقص است، آن را اصلاح کنید.

### ۳. افزودن منابع
منابع معتبر را به بخش references اضافه کنید.

## فرآیند ارسال تغییرات
1. Fork کردن مخزن
2. ایجاد Branch جدید
3. اعمال تغییرات
4. Commit و Push
5. ایجاد Pull Request

## معیارهای پذیرش
- واژه در حوزه مهندسی باشد
- تعریف کامل و مستند باشد
- حداقل یک منبع معتبر
- ساختار YAML رعایت شود
- slug منحصر به فرد باشد

## ارتباط
سوالی دارید؟ [Issue جدید](https://github.com/bmhmdyan279-png/Eng-dict/issues) ایجاد کنید.
"""
    with open(contribute_file, "w", encoding="utf-8") as f:
        f.write(contribute_content)
    print("✅ docs/contribute.md ساخته شد.")
else:
    print("⚠️ docs/contribute.md از قبل وجود داشت، حفظ شد.")

# ۳. بارگذاری و پاکسازی داده‌ها
data_file = Path("data/terms.yaml")
if not data_file.exists():
    print("❌ فایل terms.yaml وجود ندارد. یک نمونه ایجاد می‌شود.")
    raw_terms = []
else:
    with open(data_file, "r", encoding="utf-8") as f:
        try:
            raw_terms = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"❌ فایل YAML خراب است: {e}")
            raw_terms = []

if not isinstance(raw_terms, list):
    raw_terms = []

# فیلتر واژه‌های معتبر
valid_terms = []
for i, term in enumerate(raw_terms):
    if isinstance(term, dict) and 'term_fa' in term and term['term_fa']:
        valid_terms.append(term)
    else:
        print(f"⚠️ آیتم {i+1} نامعتبر است (نوع: {type(term).__name__}). نادیده گرفته شد.")

# اگر هیچ واژه معتبری نبود، فایل را با نمونه بازنویسی کن
if not valid_terms:
    print("❌ هیچ واژه معتبری با فیلد term_fa یافت نشد.")
    # پشتیبان‌گیری از فایل خراب
    if data_file.exists():
        backup_file = Path("data/terms_backup.yaml")
        shutil.copy2(data_file, backup_file)
        print(f"📁 یک نسخه پشتیبان از فایل قبلی در {backup_file} ذخیره شد.")
    # جایگزینی با نمونه صحیح
    sample_yaml = """- term_fa: "بتن"
  term_en: "concrete"
  term_fr: "béton"
  term_de: "Beton"
  term_ar: "خرسانة"
  category: "مصالح ساختمانی"
  definition: |
    مصالح ساختمانی مرکب از سیمان، آب، سنگدانه‌ها و مواد افزودنی که پس از اختلاط و گذشت زمان، سخت و مقاوم می‌شود.
  references:
    - "استاندارد ملی ایران شماره ۶۶۴"
    - "ACI 318-19"
  related_terms:
    - "siman"
    - "armator"
    - "aggregate"
  slug: "beton"

- term_fa: "سیمان"
  term_en: "cement"
  term_fr: "ciment"
  term_de: "Zement"
  term_ar: "أسمنت"
  category: "مصالح ساختمانی"
  definition: |
    ماده چسباننده‌ای که از پختن سنگ آهک و خاک رس به دست می‌آید و در ترکیب با آب، خاصیت سخت‌شوندگی دارد.
  references:
    - "استاندارد ملی ایران شماره ۳۸۹"
  related_terms:
    - "beton"
  slug: "siman"

- term_fa: "آرماتور"
  term_en: "rebar"
  term_fr: "armature"
  term_de: "Bewehrung"
  term_ar: "حديد التسليح"
  category: "سازه‌های بتنی"
  definition: |
    میلگرد فولادی که در بتن قرار داده می‌شود تا مقاومت کششی سازه را افزایش دهد.
  references:
    - "مبحث نهم مقررات ملی ساختمان"
  related_terms:
    - "beton"
    - "reinforced-concrete"
  slug: "armator"

- term_fa: "گشتاور"
  term_en: "torque"
  term_fr: "couple"
  term_de: "Drehmoment"
  term_ar: "عزم الدوران"
  category: "مکانیک"
  definition: |
    کمیت فیزیکی که تمایل یک نیرو به چرخاندن جسم حول یک محور را نشان می‌دهد.
  references:
    - "کتاب مکانیک تحلیلی"
  related_terms:
    - "force"
    - "moment"
  slug: "gashtavar"
"""
    with open(data_file, "w", encoding="utf-8") as f:
        f.write(sample_yaml)
    print("✅ فایل data/terms.yaml با داده‌های نمونه جایگزین شد.")
    valid_terms = yaml.safe_load(sample_yaml)

print(f"📚 {len(valid_terms)} واژه معتبر برای تولید صفحه بارگذاری شد.")

# ۴. ساخت نگاشت slug به نام فایل
def slugify(text):
    if not text:
        return ""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

slug_to_file = {}
for term in valid_terms:
    slug = term.get('slug', slugify(term.get('term_en', '')))
    slug_to_file[slug] = f"{term['term_fa']}.md"

# ۵. تولید صفحات واژگان
terms_dir = Path("docs/terms")
terms_dir.mkdir(parents=True, exist_ok=True)

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
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"   ✓ صفحه {term_fa} ساخته شد.")

# ۶. ساخت فهرست الفبایی
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

print("✅ فهرست الفبایی واژگان (index.md) ساخته شد.")
print("🎉 همه چیز با موفقیت انجام شد. اکنون می‌توانید commit و push کنید.")