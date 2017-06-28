#!/bin/bash

set -euo pipefail

unix() {
  flavour="$(uname)"
  if [ "$flavour" == "Linux" ]; then
    "$1"__Linux
  elif [ "$flavour" == "Darwin" ]; then
    "$1"__Darwin
  else
    echo "$flavour doesn't sound like a Unix"
  fi
}

install_ansible__Linux() {
  sudo apt-get update
  sudo apt-get install -y python-pip libssl-dev
  pip install --upgrade --user pip
  pip install --user ansible
}

install_ansible__Darwin() {
  log "installing/upgrading Homebrew"
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  brew install ansible
}

log() {
  echo
  echo "----------------------------------------------------------------------"
  echo "$1"
  echo "----------------------------------------------------------------------"
  echo
}

log "Oh boy, here I go installin' again!"

if ! which ansible-playbook > /dev/null 2>&1 ; then
  echo "ansible-playbook not found on \$PATH, installing"
  unix install_ansible
fi

(
cd "$(dirname "$0")"
vagrant up --provision
)

log "Don't forget to read the post install steps for your OS in README.md."
