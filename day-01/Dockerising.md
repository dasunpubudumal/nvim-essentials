1. Update the Dockerfile:

FROM archlinux:latest
RUN pacman -Syu --noconfirm neovim git gcc make ripgrep fd nodejs npm unzip curl tree-sitter-cli
CMD ["bash"]

2. Build the image:

docker build -t nvim .

3. Start the container from your project directory:

docker run -it --rm \
  --user "$(id -u):$(id -g)" \
  --detach-keys="ctrl-@" \
  -e HOME=/nvim -e TERM -e COLORTERM \
  -v ~/.local/share/nvim-fresh:/nvim \
  -v "$PWD":/work -w /work \
  nvim

Run mkdir -p ~/.local/share/nvim-fresh once before the first start, so that Docker doesn't create the folder as root.

The container doesn't see your host's ~/.config/nvim. Anything you customise inside it is saved in ~/.local/share/nvim-fresh, so it survives container restarts. To go back to a fresh start, exit the container and run:

rm -rf ~/.local/share/nvim-fresh && mkdir -p ~/.local/share/nvim-fresh

4. At the container's shell prompt, open Neovim:

`nvim`

## Using Podman instead of Docker

Podman can use the same Dockerfile. Only the setup and the `run` flags are different.

1. Install Podman and start its VM (macOS only; on Linux Podman runs natively, so skip this step):

brew install podman
podman machine init
podman machine start

The VM mounts your home directory by default, so the `-v` paths below work as they are.

2. Build the image:

podman build -t nvim .

If Podman asks which registry to pull `archlinux:latest` from, choose `docker.io`. To skip the question, change the first line of the Dockerfile to `FROM docker.io/library/archlinux:latest`.

The Arch Linux image is only available for x86_64. On Apple Silicon, add `--platform linux/amd64` to both the `build` and `run` commands.

3. Start the container from your project directory:

mkdir -p ~/.local/share/nvim-fresh

podman run -it --rm \
  --userns=keep-id \
  --detach-keys="ctrl-@" \
  -e HOME=/nvim -e TERM -e COLORTERM \
  -v ~/.local/share/nvim-fresh:/nvim \
  -v "$PWD":/work -w /work \
  nvim

How this differs from the Docker command:

- `--userns=keep-id` replaces `--user "$(id -u):$(id -g)"`. Podman runs rootless, and this flag maps your host user to the same UID inside the container, so files you create in `/work` and `/nvim` are owned by you on the host.
- Podman won't create a missing host folder for a `-v` mount, so the `mkdir -p` is required, not just a recommendation.
- On Linux with SELinux enabled (Fedora, RHEL), add `:Z` to each mount, for example `-v "$PWD":/work:Z`, or Neovim will get "permission denied" errors.

To reset to a fresh start, use the same `rm -rf` command as in step 3 above.

4. At the container's shell prompt, open Neovim:

`nvim`

Tip: if you'd like to keep typing `docker`, run `alias docker=podman`. Note that the Docker step-3 command still needs `--userns=keep-id` in place of `--user` to get the right file ownership.
