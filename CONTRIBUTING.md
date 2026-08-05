# راهنمای مشارکت

## راه‌ها

1. **ساده‌ترین:** Issue بسازید با [این فرم](https://github.com/bmhmdyan279-png/Eng-dict/issues/new?template=new-term.yml)
2. **فنی‌تر:** روی `data/terms.yaml` Pull Request بزنید

```bash
git checkout -b add-term-beton
# ویرایش data/terms.yaml
python scripts/build_pages.py
mkdocs serve
git add .
git commit -m "Add term: بتن"
git push
```

## معیارها

- دقت فنی
- ذکر منبع
- ارتباط با حوزهٔ بتن

## مجوز

- کد: MIT
- محتوا: CC BY-SA 4.0
