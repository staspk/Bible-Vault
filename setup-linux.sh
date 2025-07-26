
latest_version=$(curl -fsSL https://nodejs.org/dist/index.json | grep '"version"' | grep -m1 -B1 '"lts": false' | head -n1 | sed 's/.*"version": "\(v[0-9.]*\)".*/\1/')

echo "Latest current stable Node.js version: $latest_version"

return

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

export NVM_DIR="$HOME/.nvm"