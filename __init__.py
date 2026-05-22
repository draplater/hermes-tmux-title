"""tmux-title plugin — sync Hermes session title to tmux window.

Hooks:
- on_session_title: rename tmux window to match session title
"""

from __future__ import annotations

import logging
import os
import subprocess

logger = logging.getLogger(__name__)


def _rename_tmux_window(title: str) -> None:
    """Rename the tmux window that Hermes is running in.

    Uses $TMUX_PANE so the correct window is targeted even when
    the user switches to a different tmux tab.
    """
    pane = os.getenv("TMUX_PANE")
    if not pane:
        return
    try:
        subprocess.run(
            ["tmux", "rename-window", "-t", pane, title],
            timeout=3,
            capture_output=True,
        )
    except Exception:
        pass  # Best-effort


def _on_session_title(title: str, session_id: str, **kwargs) -> None:
    """Rename tmux window when session title changes."""
    _rename_tmux_window(title)


def register(ctx) -> None:
    ctx.register_hook("on_session_title", _on_session_title)
