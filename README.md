# linux-training VM

## Usage

1. Clone this.
1. `./vmup.sh`
1. If this is the first time you've provisioned the box, it will have a new
   Linux kernel waiting.  Try a `vagrant reload`.
1. The first time you launch tmux, press prefix+I to install TPM plugins.
1. Run `vim-update` in the VM. This is idempotent but extraordinarily slow, so
   I didn't want to have it run every time while developing this.
