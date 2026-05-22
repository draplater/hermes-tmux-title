# tmux-title: Hermes Plugin

Sync Hermes session title and status emoji to the tmux window name.
Restores the original window name on exit.

## What it does

| Hermes state | tmux tab shows |
|-------------|---------------|
| Fresh session | `🛎️ Hermes` |
| Processing | `🔄 Shopping cart debug` |
| Waiting for approval | `🚨 Shopping cart debug` |
| Done, waiting for input | `🛎️ Shopping cart debug` |
| Exit (/quit) | restores original name (e.g. `bash`) |

Uses `$TMUX_PANE` to target the correct window even when the user switches tabs.

## Installation

```bash
cp -r tmux-title ~/.hermes/plugins/
hermes plugins enable tmux-title
```

## Requirements

- tmux (graceful no-op outside tmux)
- Hermes Agent with `on_session_title`, `pre_llm_call`, `post_llm_call`, `pre_approval_request`, `post_approval_response`, `on_session_end` hooks
