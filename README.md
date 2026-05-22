# tmux-title: Hermes Plugin

Sync Hermes session title to the tmux window name.

## Features

- Automatically renames the tmux window to "Hermes" on fresh sessions
- Syncs the tmux window to the session title on `/title`, auto-title, `/new`, `/branch`, and resume
- Uses `$TMUX_PANE` to target the correct tmux window even when the user switches tabs
- Graceful no-op when not running inside tmux

## Installation

```bash
# Copy to user plugins directory
cp -r tmux-title ~/.hermes/plugins/

# Enable
hermes plugins enable tmux-title
```

## How It Works

The plugin hooks into `on_session_title` — a lifecycle event fired whenever a Hermes session title changes. On each event, it runs:

```bash
tmux rename-window -t $TMUX_PANE "<session title>"
```

`$TMUX_PANE` is set by tmux for each pane and does not change when the user switches tabs, ensuring the correct window is always targeted.

## Requirements

- tmux (the plugin is a no-op outside tmux)
- Hermes Agent with `on_session_title` hook support (hermes-agent >= commit `TBD`)
