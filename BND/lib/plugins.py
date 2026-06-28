"""Load custom plugins from tools/custom/."""
import glob
import os

from . import constants as C
from .runner import run_plugin


def _is_safe_plugin_path(path):
    """Only allow plugins inside the designated custom tools directory."""
    real_path = os.path.realpath(path)
    safe_dir = os.path.realpath(C.CUSTOM_TOOLS_DIR)
    return real_path.startswith(safe_dir + os.sep) or real_path == safe_dir


def discover_plugins():
    os.makedirs(C.CUSTOM_TOOLS_DIR, exist_ok=True)
    items = []
    for i, path in enumerate(sorted(glob.glob(os.path.join(C.CUSTOM_TOOLS_DIR, "*.py"))), 1):
        name = os.path.splitext(os.path.basename(path))[0]
        if name.startswith("_") or name.startswith("."):
            continue
        if not _is_safe_plugin_path(path):
            continue
        label = name.replace("-", " ").replace("_", " ").title()
        code = f"P{i:02d}"
        items.append((code, f"{label} [PLUGIN]", lambda p=path: run_plugin(p)))
    return items