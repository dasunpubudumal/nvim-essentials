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
