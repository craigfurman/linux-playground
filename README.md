# linux-playground

## Host requirements

1. Vagrant, Virtualbox.
1. On macOS hosts, Homebrew.

## Usage

1. Clone this.
1. `./vmup.sh`. This will take a while and the VM will reboot several times, to
   load the new kernel and Virtualbox guest additions.
1. The first time you launch tmux, press prefix+I to install TPM plugins.
1. Run `~/.vim/update` in the VM. This is idempotent but extraordinarily slow,
   so I didn't want to have it run every time while developing this.
