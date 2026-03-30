#!/usr/bin/env python3
"""
Patch notebooks: remove hardcoded paths, add portable bootstrap, fix config paths.

Run from repo root:
  python scripts/patch_notebooks_portable.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NOTEBOOKS = REPO / "notebooks"

OLD_PATH = "/Users/kumar/Documents/projects/li-ion battery"

BOOTSTRAP = """# --- Portable setup (Windows / macOS / Linux) — do not hardcode paths ---
import importlib.util
from pathlib import Path

def _load_notebook_setup():
    cwd = Path.cwd().resolve()
    candidates = [
        cwd / "notebooks" / "notebook_setup.py",
        cwd / "notebook_setup.py",
    ]
    if cwd.name == "notebooks":
        candidates.insert(0, cwd / "notebook_setup.py")
    for fp in candidates:
        if fp.is_file():
            spec = importlib.util.spec_from_file_location("_notebook_setup", fp)
            mod = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(mod)
            return mod
    raise FileNotFoundError(
        "Missing notebooks/notebook_setup.py. Unzip the full project, open a terminal, "
        "cd into the repo root, then run: jupyter notebook"
    )

_ns = _load_notebook_setup()
PROJECT_ROOT = _ns.setup()
print(f"PROJECT_ROOT = {PROJECT_ROOT}")

"""

BOOTSTRAP_API = BOOTSTRAP.replace(
    "PROJECT_ROOT = _ns.setup()",
    "PROJECT_ROOT = _ns.setup(with_api=True)",
)


def _needs_api(text: str) -> bool:
    return "os.path.join(PROJECT_ROOT, 'api')" in text or "join(PROJECT_ROOT, 'api'" in text


def _strip_old_setup(text: str) -> str:
    patterns = [
        r"# CRITICAL: Change to project root directory\n",
        r"PROJECT_ROOT = ['\"].*?['\"]\n",
        r"os\.chdir\(PROJECT_ROOT\)\n",
        r'print\(f["\']Working directory: \{os\.getcwd\(\)\}["\']\)\n',
        r"sys\.path\.insert\(0, os\.path\.join\(PROJECT_ROOT, 'api'\)\)\n",
        r"sys\.path\.insert\(0, os\.path\.join\(PROJECT_ROOT, 'src', 'phase3'\)\)\n",
        r"sys\.path\.insert\(0, os\.path\.join\(PROJECT_ROOT, 'src', 'phase2'\)\)\n",
        r"sys\.path\.insert\(0, os\.path\.join\(PROJECT_ROOT, 'src'\)\)\n",
        r"sys\.path\.insert\(0, 'src'\)\n",
        r"# Add source path\n",
        r'^\s*cd\s+["\'][^"\']+["\']\s*\n',
        r"^\s*cd\s+[^\n]+\n",
    ]
    for pat in patterns:
        text = re.sub(pat, "", text, flags=re.MULTILINE)
    return re.sub(r"^\n+", "", text)


def patch_cell_source(text: str) -> str:
    if "_load_notebook_setup" in text:
        t = text.replace("load_config('../config.yaml')", "load_config('config.yaml')")
        t = t.replace('load_config("../config.yaml")', 'load_config("config.yaml")')
        return t if t != text else text

    orig = text
    text = text.replace("load_config('../config.yaml')", "load_config('config.yaml')")
    text = text.replace('load_config("../config.yaml")', 'load_config("config.yaml")')

    if OLD_PATH not in text and not re.search(r"PROJECT_ROOT\s*=\s*['\"]/Users/", text):
        return text

    api = _needs_api(orig)
    rest = _strip_old_setup(text)
    if not rest.strip():
        return orig

    head = BOOTSTRAP_API if api else BOOTSTRAP
    return head + "\n" + rest


def replace_path_in_str(s: str) -> str:
    if OLD_PATH not in s:
        return s
    return s.replace(OLD_PATH, "<PROJECT_ROOT>")


def process_notebook(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False

    for cell in data.get("cells", []):
        src = cell.get("source", [])
        text = "".join(src) if isinstance(src, list) else src

        if cell.get("cell_type") == "code":
            new_text = patch_cell_source(text)
            if new_text != text:
                changed = True
                cell["source"] = new_text.splitlines(keepends=True)
            cell["outputs"] = []
            cell["execution_count"] = None
        elif cell.get("cell_type") == "markdown":
            new_text = replace_path_in_str(text)
            if new_text != text:
                changed = True
                cell["source"] = new_text.splitlines(keepends=True)

    if changed:
        path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def main() -> None:
    n = 0
    for p in sorted(NOTEBOOKS.glob("*.ipynb")):
        if process_notebook(p):
            print(f"Patched: {p.relative_to(REPO)}")
            n += 1
    print(f"Done. Updated {n} notebook(s).")


if __name__ == "__main__":
    main()
