"""Unified tool runner — uses saved language, no repeated prompts."""
import os
import subprocess
import sys

from . import constants as C
from .config import get_settings
from .void_common import cls, console, error_box, pause, panel, success_box


SELF_PAUSE_DIRS = (
    f"{os.sep}tools{os.sep}discord{os.sep}",
    f"{os.sep}tools{os.sep}roblox{os.sep}",
    f"{os.sep}tools{os.sep}social{os.sep}",
    f"{os.sep}tools{os.sep}webhook{os.sep}",
)


def run_script(fr_path, en_path, tool_name=None, extra_args=None):
    s = get_settings()
    lang = s.lang if s.lang in ("fr", "de", "en") else "de"
    src = fr_path if lang in ("fr", "de") else en_path

    if not os.path.exists(src):
        error_box("Script missing", os.path.basename(src), src)
        pause()
        return

    try:
        cmd = [sys.executable, src]
        if tool_name:
            cmd.append(tool_name)
        if extra_args:
            cmd.extend(extra_args)
        result = subprocess.run(cmd, shell=False)
        if result.returncode not in (0, None):
            error_box("Tool error", tool_name or os.path.basename(src), f"exit {result.returncode}")
    except FileNotFoundError:
        error_box("Python not found", sys.executable or "python")
    except Exception as e:
        error_box("Runtime", tool_name or "tool", str(e))

    if not any(d in src for d in SELF_PAUSE_DIRS):
        pause()


def run(folder, fr_name="fr.py", en_name="en.py", tool_name=None):
    run_script(C.sp(folder, fr_name), C.sp(folder, en_name), tool_name)


def run_discord(tool_key):
    run_script(C.sp_discord("fr.py"), C.sp_discord("en.py"), tool_key)


def run_roblox(tool_key):
    run_script(C.sp_roblox("fr.py"), C.sp_roblox("en.py"), tool_key)


def run_social(tool_key):
    run_script(C.sp_social("fr.py"), C.sp_social("en.py"), tool_key)


def run_webhook(tool_key):
    run_script(C.sp_webhook("fr.py"), C.sp_webhook("en.py"), tool_key)


def run_premium(name):
    run("premium-tools", "fr.py", "en.py", name)


def run_nuker(action=None):
    cls()
    src = C.sp_nuker()
    if not os.path.exists(src):
        error_box("BND-NUKE missing", "tools/bnd-nuke/", src)
        pause()
        return
    try:
        cmd = [sys.executable, src]
        if action:
            cmd.extend(["--action", action])
        result = subprocess.run(cmd, shell=False)
        if result.returncode not in (0, None):
            error_box("NUKER", action or "menu", f"exit {result.returncode}")
    except Exception as e:
        error_box("NUKER", action or "menu", str(e))
    pause()


def run_plugin(plugin_path):
    cls()
    if not os.path.isfile(plugin_path):
        error_box("Plugin", "not found", plugin_path)
        pause()
        return
    try:
        subprocess.run([sys.executable, plugin_path], shell=False)
    except Exception as e:
        error_box("Plugin", os.path.basename(plugin_path), str(e))
    pause()