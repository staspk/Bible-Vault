sudo apt-get update


curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# export NVM_DIR="$HOME/.nvm"


latest_lts_version=$(nvm list-remote --lts | tail -1 | grep -Eo 'v[0-9]+\.[0-9]+\.[0-9]+')
echo "Latest LTS Node.js version: $latest_lts_version"