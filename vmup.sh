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
  log "ansible-playbook not found on \$PATH, installing"
  unix install_ansible
fi

if ! vagrant plugin list | grep vbguest > /dev/null 2>&1 ; then
  log "installing vagrant-vbguest plugin..."
  vagrant plugin install vagrant-vbguest
fi

(
cd "$(dirname "$0")"
vagrant up --provision --provider virtualbox

if ! vagrant ssh -c 'uname -r | grep 4.12' >/dev/null 2>&1 ; then
  log "Old kernel running, reinstalling guest additions"

  set +e
  vagrant reload
  set -e

  if [ ! -f cache/guest_additions.iso ]; then
    mkdir -p cache
    wget -O cache/guest_additions.iso https://www.virtualbox.org/download/testcase/VBoxGuestAdditions_5.1.23-116467.iso
  fi

  vagrant vbguest --do install
  vagrant reload
fi
)

log "Don't forget to read the post install steps for your OS in README.md."
