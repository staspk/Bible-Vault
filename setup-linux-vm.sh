# ──────────────────────────────────────────────────────────────────────────────
#   Pre-Setup [My Bash Library/Runtime]          ...Copy/Paste into Terminal...
# ──────────────────────────────────────────────────────────────────────────────
<<'###BLOCK-COMMENT'

sudo apt update && sudo apt install -y git
git clone https://github.com/staspk/os-setup.git $HOME/os-setup
cp -r "$HOME/os-setup/ubuntu/home/." ~
(cat "$HOME/os-setup/ubuntu/.bashrc"; printf "\n\n\n"; cat ~/.bashrc) > "$HOME/.bashrc.new" && mv "$HOME/.bashrc.new" ~/.bashrc
cp -r "$HOME/os-setup/ubuntu/boilerplate" "$HOME/boilerplate"
rm -rf "$HOME/os-setup"
source ~/.bashrc

###BLOCK-COMMENT


# ─── Clone Project ──────────────────────────────────────────────────────────────
git clone https://github.com/staspk/Bible-Vault.git


# ─── Nvm/Nodejs ────────────────────────────────────────────────────────────────
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
export NVM_DIR="$HOME/.nvm"
nvm install --lts


# ───────────────────────────────────────────────────────────────────────────────
#   Dev Machine Config [allows node binary to bind to priviliged ports <1024]
# ───────────────────────────────────────────────────────────────────────────────
sudo setcap 'cap_net_bind_service=+ep' $(which node)


# ─── Build Vite FrontEnd  ──────────────────────────────────────────────────────
cd ~/Bible-Vault/node/_vite-frontend
npm install
npm run build


# ─── Start Server  ─────────────────────────────────────────────────────────────
cd ~/Bible-Vault
setStartDirectory
allow_execute start-server.sh
./start-server.sh