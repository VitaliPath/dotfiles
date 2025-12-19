#!/bin/bash
# --- install.sh ---

echo "🔗 Linking Vim configurations..."

# Function to link and backup
link_file() {
    src="$PWD/vim/$1"
    dest="$HOME/.$1"

    if [ -f "$dest" ]; then
        echo "   backing up existing .$1 to .$1.bak"
        mv "$dest" "$dest.bak"
    fi
    
    ln -s "$src" "$dest"
    echo "   linked $src -> $dest"
}

link_file "vimrc"
link_file "vimspector.json"

# Setup Vim Plug (Auto-install if missing)
if [ ! -f "$HOME/.vim/autoload/plug.vim" ]; then
    echo "🔌 Installing vim-plug..."
    curl -fLo "$HOME/.vim/autoload/plug.vim" --create-dirs \
        https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
fi

echo "✅ Setup complete! Restart your terminal and open Vim to install plugins."