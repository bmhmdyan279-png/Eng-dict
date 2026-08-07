import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
from build_pages import normalize_persian

def test_normalize():
    assert normalize_persian('كتاب') == 'کتاب'
