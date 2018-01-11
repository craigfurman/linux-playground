# linux-playground

## Host requirements

1. Vagrant, Virtualbox.
1. On macOS hosts, Homebrew.

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
