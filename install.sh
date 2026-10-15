#!/bin/sh
# Links the CLI into ~/.local/bin and builds the drag-and-drop app into ~/Applications.
set -e
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$HOME/.local/bin" "$HOME/Applications"
ln -sf "$here/ferry" "$HOME/.local/bin/ferry"
osacompile -o "$HOME/Applications/Send to Homelab.app" "$here/Send to Homelab.applescript"
echo "installed: ~/.local/bin/ferry, ~/Applications/Send to Homelab.app"
