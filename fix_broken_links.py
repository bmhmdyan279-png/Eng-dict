import re
from pathlib import Path


def fix_broken_links():
    file_path = Path("docs/construction-terms.md")
    content = file_path.read_text(encoding="utf-8")

    # الگو برای پیدا کردن لینک‌های خراب و تبدیل آن‌ها به متن ساده
    # مثلاً: **[آب بندی](terms/abbndy-2.md)** -> **آب بندی**
    broken_links = ["terms/abbndy-2.md", "terms/askvp-1.md", "terms/znjab-1.md"]

    for link in broken_links:
        # الگوی رگولار برای پیدا کردن **[متن](لینک)**
        pattern = rf"\*\*\[([^\]]+)\]\({re.escape(link)}\)\*\*"
        replacement = r"**\1**"
        content = re.sub(pattern, replacement, content)

    file_path.write_text(content, encoding="utf-8")
    print(f"✅ لینک‌های خراب در {file_path} با موفقیت اصلاح شدند!")


if __name__ == "__main__":
    fix_broken_links()
