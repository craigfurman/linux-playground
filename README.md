# linux-playground

**This repository is no longer maintained**. I no longer use this and will no longer be
maintaining it. If you are interested in sharing contributions, please see whichever
[fork](https://github.com/craigfurman/linux-playground/network/members) looks to be the
most up-to-date. At the time of writing this looks like
https://github.com/masters-of-cats/linux-playground. If you want to see my dotfiles /
laptop config for Linux and macOS, please see https://github.com/craigfurman/ansible-home.

## Host requirements

1. Vagrant
1. Virtualbox
1. Ansible

## Usage

1. Clone this.
1. Set LINUX_PLAYGROUND_CPUS (default: number of cores on your host),
   LINUX_PLAYGROUND_MEMORY (in MB. Default: 2048), and
   LINUX_PLAYGROUND_SHARED_DIR (Default: ~/workspace. Mounted at
   /vagrant_data).
1. `./vmup.sh`.
1. The first time you launch tmux, press prefix+I to install TPM plugins. The
   default prefix is ctrl+space.
1. Run `~/.vim/update` in the VM. This is idempotent but slow, so I didn't want
   to have it run every time while developing this.
