#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ALIASES_FILE="$SCRIPT_DIR/aliases.sh"

SHELL_NAME="$(basename "$SHELL")"
if [ "$SHELL_NAME" = "zsh" ]; then
  RC_FILE="$HOME/.zshrc"
else
  RC_FILE="$HOME/.bashrc"
fi

SOURCE_LINE="source \"$ALIASES_FILE\""

echo "📂 Current Dir: $SCRIPT_DIR"
echo "⚙️  Shell name: $SHELL_NAME"
echo "🗂  RC file: $RC_FILE"
echo "--------------------------------------"

# Verifica se o aliases.sh existe
if [ ! -f "$ALIASES_FILE" ]; then
  echo "❌ The file $ALIASES_FILE wasn't found!"
  exit 1
fi

# Verifica se já foi adicionado
if grep -Fxq "$SOURCE_LINE" "$RC_FILE"; then
  echo "✅ Alias has ever added in $RC_FILE"
else
  echo "$SOURCE_LINE" >> "$RC_FILE"
  echo "✅ Alias has already added in $RC_FILE"
fi

echo "⚡ Run: source $RC_FILE to activate"
source $RC_FILE
