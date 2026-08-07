import subprocess
import os
import sys


def main():
    # سرکوب هشدارهای DeprecationWarning
    os.environ["PYTHONWARNINGS"] = "ignore::DeprecationWarning"

    print("🔨 ساخت صفحات...")
    subprocess.run([sys.executable, "scripts/build_pages.py"], check=True)

    print("🧪 اجرای تست‌ها...")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q"])
    if result.returncode != 0:
        print("❌ تست‌ها شکست خوردند!")
        return

    print("🌐 راه‌اندازی سرور...")
    subprocess.run(["mkdocs", "serve", "--dev-addr", "127.0.0.1:8000"])


if __name__ == "__main__":
    main()
