"""Механическая синхронизация эталонных частот в автономном marimo-приложении.

Считает частоты из оригинального CSV и вставляет сжатый массив пар
«число страниц / частота» непосредственно в исходник, чтобы HTML-WASM
работал на GitHub Pages без сетевой загрузки данных.
"""

from base64 import b85encode
from pathlib import Path
import json
import re
import zlib

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "online_shoppers_intention.csv")
freq = df["ProductRelated"].value_counts().sort_index()
payload = [[int(k), int(v)] for k, v in freq.items()]
packed = b85encode(zlib.compress(json.dumps(payload, separators=(",", ":")).encode(), 9)).decode()
path = ROOT / "marimo_app.py"
original = path.read_text(encoding="utf-8")
pattern = r'COUNTS_B85 = "[^"]*"'
replaced, n = re.subn(pattern, lambda _: f'COUNTS_B85 = "{packed}"', original)
if n != 1:
    raise SystemExit("Не найден ровно один маркер COUNTS_B85")
path.write_text(replaced, encoding="utf-8")
print(f"Эталонные частоты встроены: {int(freq.sum())} сессий, {len(payload)} значений")

