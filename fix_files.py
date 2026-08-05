#!/usr/bin/env python3
"""
پاک‌سازی نهایی: تبدیل تمام فایل‌های docs به UTF-8 بدون BOM + LF
و اصلاح لینک‌های شکسته در armator.md, beton.md, siman.md
"""

from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent / "docs"


def clean_encoding_and_line_endings(file_path: Path):
    """خواندن فایل با تشخیص encoding، تبدیل به UTF-8 بدون BOM و LF"""
    try:
        # سعی می‌کنیم با UTF-8 بخوانیم، در صورت خطا با cp1256 (ویندوز فارسی)
        try:
            text = file_path.read_text(encoding="utf-8-sig")  # utf-8-sig BOM را حذف می‌کند
        except UnicodeDecodeError:
            text = file_path.read_text(encoding="cp1256")

        # تبدیل CRLF به LF
        text = text.replace('\r\n', '\n').replace('\r', '\n')

        # بازنویسی با UTF-8 بدون BOM
        file_path.write_text(text, encoding="utf-8", newline='\n')
        return True
    except Exception as e:
        print(f"❌ خطا در {file_path}: {e}")
        return False


def fix_broken_links(file_path: Path):
    """حذف لینک‌های شکسته به صفحاتی که هنوز وجود ندارند"""
    # فقط برای armator.md, beton.md, siman.md
    fixes = {
        "terms/armator.md": ["./concrete.md"],
        "terms/beton.md": ["./cement.md", "./rebar.md", "./admixture.md"],
        "terms/siman.md": ["./concrete.md", "./clinker.md"]
    }

    rel_path = str(file_path.relative_to(DOCS_DIR))
    if rel_path not in fixes:
        return

    try:
        text = file_path.read_text(encoding="utf-8")
        original = text
        for broken_link in fixes[rel_path]:
            # لینک‌ها را با یک متن جایگزین (مثلاً نام لینک بدون لینک) عوض می‌کنیم
            # یا کلاً خط حاوی لینک را حذف می‌کنیم. اینجا روش ساده: تبدیل به متن ساده
            text = text.replace(f"[{broken_link}]({broken_link})", broken_link)
            text = text.replace(f"({broken_link})", "")  # اگر فقط لینک باشد
            # حذف خطوط حاوی لینک شکسته (محافظه‌کارانه‌تر)
            lines = text.splitlines()
            new_lines = []
            for line in lines:
                if broken_link in line:
                    continue  # خط را حذف کن
                new_lines.append(line)
            text = "\n".join(new_lines)

        if text != original:
            file_path.write_text(text, encoding="utf-8", newline='\n')
            print(f"🔧 لینک‌های شکسته در {rel_path} اصلاح شدند")
    except Exception as e:
        print(f"❌ خطا در اصلاح لینک‌های {file_path}: {e}")


def main():
    print("🧹 پاک‌سازی encoding و خطوط...")
    count = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        if clean_encoding_and_line_endings(md_file):
            count += 1
    print(f"✅ {count} فایل Markdown اصلاح شدند.\n")

    print("🔗 بررسی و اصلاح لینک‌های شکسته...")
    for target in ["terms/armator.md", "terms/beton.md", "terms/siman.md"]:
        fix_broken_links(DOCS_DIR / target)
    print("\n✨ پاک‌سازی کامل شد. حالا mkdocs serve را دوباره اجرا کنید.")


if __name__ == "__main__":
    main()