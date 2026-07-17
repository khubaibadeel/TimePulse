import ast
from pathlib import Path


def test_main_source_parses():
    source = Path(__file__).resolve().parents[1] / "TimePulse.py"
    ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
