"""Воспроизводит ячейки и сохраняет outputs без запуска сетевого Jupyter kernel.

Полезно в средах, где запуск kernel блокируется системными ограничениями.
Это НЕ заменяет обычный запуск Notebook пользователем: все ячейки — обычный Python.
"""

from __future__ import annotations

from base64 import b64encode
from contextlib import redirect_stdout, redirect_stderr
from io import BytesIO, StringIO
from pathlib import Path
import os
import traceback

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nbformat
from nbformat.v4 import new_output
import IPython.display as ipydisplay


ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
path = ROOT / "notebooks" / "lab01_ktvd_online_shop.ipynb"
nb = nbformat.read(path, as_version=4)
namespace: dict[str, object] = {"__name__": "__main__"}
active_outputs: list = []


def capture_figure(*args, **kwargs) -> None:
    for num in plt.get_fignums():
        fig = plt.figure(num)
        buffer = BytesIO()
        fig.savefig(buffer, format="png", dpi=120, bbox_inches="tight")
        image_b64 = b64encode(buffer.getvalue()).decode("ascii")
        active_outputs.append(new_output("display_data", data={"image/png": image_b64}, metadata={}))
    plt.close("all")


def capture_display(*items, **kwargs) -> None:
    for obj in items:
        if hasattr(obj, "to_html"):
            active_outputs.append(new_output("display_data", data={"text/html": obj.to_html()}, metadata={}))
        elif isinstance(obj, ipydisplay.Markdown):
            active_outputs.append(new_output("display_data", data={"text/markdown": obj.data}, metadata={}))
        else:
            active_outputs.append(new_output("display_data", data={"text/plain": repr(obj)}, metadata={}))


plt.show = capture_figure
ipydisplay.display = capture_display
execution_count = 0
for cell_number, cell in enumerate(nb.cells, 1):
    if cell.cell_type != "code":
        continue
    execution_count += 1
    cell.execution_count = execution_count
    active_outputs = []
    stdout = StringIO()
    stderr = StringIO()
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exec(compile(cell.source, f"<notebook-cell-{cell_number}>", "exec"), namespace)
    except Exception:
        print(f"ОШИБКА в ячейке {cell_number}:", flush=True)
        traceback.print_exc()
        raise
    if stdout.getvalue():
        active_outputs.insert(0, new_output("stream", name="stdout", text=stdout.getvalue()))
    if stderr.getvalue():
        active_outputs.append(new_output("stream", name="stderr", text=stderr.getvalue()))
    cell.outputs = active_outputs

nbformat.validate(nb)
nbformat.write(nb, path)
print(f"Исполнено {execution_count} ячеек, сохранены графики и таблицы: {path}")

