# tmux-title: Hermes Plugin

Sync Hermes session title and status to the tmux window name.

## What it does

| Hermes state | tmux tab shows |
|-------------|---------------|
| Fresh session | `🔔 Hermes` |
| Processing (LLM call) | `🔄 Shopping cart debug` |
| Done, waiting for input | `🔔 Shopping cart debug` |
| Title changed (/title) | `🔄` or `🔔` persists, title updates |

Uses `$TMUX_PANE` to target the correct window even when the user switches tabs.

## Installation

```bash
cp -r tmux-title ~/.hermes/plugins/
hermes plugins enable tmux-title
```

## Requirements

- tmux (graceful no-op outside tmux)
- Hermes Agent with `on_session_title`, `pre_llm_call`, `post_llm_call` hooks
