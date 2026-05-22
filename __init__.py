"""tmux-title plugin — sync Hermes session title + status emoji to tmux.

Hooks:
- on_session_title: store current title, update tmux
- pre_llm_call:      set busy emoji (🔄)
- post_llm_call:     set done emoji (🛎️)
"""

from __future__ import annotations

import logging
import os
import subprocess

logger = logging.getLogger(__name__)

# Module-level state — survives across hook invocations.
_title: str = "Hermes"
_busy: bool = False


def _update_tmux() -> None:
    """Compose emoji + title and rename the tmux window."""
    pane = os.getenv("TMUX_PANE")
    if not pane:
        return
    emoji = "🔄" if _busy else "🛎️"
    label = f"{emoji} {_title}"
    try:
        subprocess.run(
            ["tmux", "rename-window", "-t", pane, label],
            timeout=3,
            capture_output=True,
        )
    except Exception:
        pass


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


def register(ctx) -> None:
    ctx.register_hook("on_session_title", _on_session_title)
    ctx.register_hook("pre_llm_call", _on_pre_llm_call)
    ctx.register_hook("post_llm_call", _on_post_llm_call)
