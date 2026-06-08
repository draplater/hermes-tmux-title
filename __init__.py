"""tmux-title plugin — sync Hermes session title + status emoji to tmux.

Hooks:
- on_session_title:       store current title, update tmux
- pre_llm_call / pre_tool_call:      → 🔄 busy
- post_llm_call / post_tool_call:    → 🛎️ idle
- pre_approval_request:              → 🚨 waiting for user
- post_approval_response:            → restore busy/idle

On process exit (atexit): restore original tmux window name.
"""

from __future__ import annotations

import atexit
import logging
import os
import subprocess

logger = logging.getLogger(__name__)

_title: str = "Hermes"
_busy: bool = False
_awaiting_approval: bool = False
_original_name: str | None = None
_atexit_registered: bool = False


def _tmux_get_window_name() -> str | None:
    pane = os.getenv("TMUX_PANE")
    if not pane:
        return None
    try:
        r = subprocess.run(
            ["tmux", "display-message", "-t", pane, "-p", "#{window_name}"],
            timeout=2, capture_output=True, text=True,
        )
        return r.stdout.strip() or None
    except Exception:
        return None


def _tmux_rename(label: str) -> None:
    pane = os.getenv("TMUX_PANE")
    if not pane:
        return
    try:
        subprocess.run(
            ["tmux", "rename-window", "-t", pane, label],
            timeout=3, capture_output=True,
        )
    except Exception:
        pass


def _ensure_original_name() -> None:
    global _original_name, _atexit_registered
    if _original_name is None:
        _original_name = _tmux_get_window_name() or ""
    if not _atexit_registered:
        atexit.register(_restore_tmux)
        _atexit_registered = True


def _restore_tmux() -> None:
    if _original_name:
        _tmux_rename(_original_name)


def _update_tmux() -> None:
    _ensure_original_name()
    if _awaiting_approval:
        emoji = "\U0001f6a8"       # 🚨
    elif _busy:
        emoji = "\U0001f504"       # 🔄
    else:
        emoji = "\U0001f6ce\ufe0f"  # 🛎️
    _tmux_rename(f"{emoji} {_title}")


def _on_session_title(title: str, session_id: str, **kwargs) -> None:
    global _title
    _title = title
    _update_tmux()


def _on_pre_llm_call(**kwargs) -> None:
    global _busy
    _busy = True
    _update_tmux()


def _on_post_llm_call(**kwargs) -> None:
    global _busy
    _busy = False
    _update_tmux()


def _on_pre_tool_call(**kwargs) -> None:
    global _busy
    _busy = True
    _update_tmux()


def _on_post_tool_call(**kwargs) -> None:
    global _busy
    _busy = False
    _update_tmux()


def _on_pre_approval_request(command: str, description: str,
                              surface: str, **kwargs) -> None:
    global _awaiting_approval
    _awaiting_approval = True
    _update_tmux()


def _on_post_approval_response(choice: str, **kwargs) -> None:
    global _awaiting_approval
    _awaiting_approval = False
    _update_tmux()


def register(ctx) -> None:
    ctx.register_hook("on_session_title", _on_session_title)
    ctx.register_hook("pre_llm_call", _on_pre_llm_call)
    ctx.register_hook("post_llm_call", _on_post_llm_call)
    ctx.register_hook("pre_tool_call", _on_pre_tool_call)
    ctx.register_hook("post_tool_call", _on_post_tool_call)
    ctx.register_hook("pre_approval_request", _on_pre_approval_request)
    ctx.register_hook("post_approval_response", _on_post_approval_response)
