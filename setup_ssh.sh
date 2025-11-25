#!/bin/bash
set -e

echo "Resetting SSH setup..."

rm -rf ~/.ssh
mkdir -p ~/.ssh
chmod 700 ~/.ssh

echo "Generating PERSONAL SSH key..."
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_personal -C "gauravadlakha1509@gmail.com" -N ""

echo "Generating WORK SSH key..."
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_work -C "your_work_email@company.com" -N ""

echo "Creating SSH config..."
cat <<EOF > ~/.ssh/config
# Personal GitHub
Host github.com-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal

# Work GitHub
Host github.com-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work
EOF

chmod 600 ~/.ssh/config

echo
echo "----- PERSONAL PUBLIC KEY -----"
cat ~/.ssh/id_ed25519_personal.pub
echo "Add this to: https://github.com/settings/keys"
echo
echo "----- WORK PUBLIC KEY -----"
cat ~/.ssh/id_ed25519_work.pub
echo "Add this to your WORK GitHub account settings"
echo
echo "Done. Keys reset and config rebuilt."
