<div align="center">
<img src="day-01/assets/neovim-logo.svg" width="200" alt="Neovim"/>
<h1>Neovim Essentials</h1>
</div>

A day-by-day series on getting started with [Neovim](https://neovim.io/). Each day is a Jupyter notebook that you read through while following along in your own terminal.

## Sessions

| Day | Read online | Notebook | What it covers | Status |
|---|---|---|---|---|
| 1 | [Day 1](https://dasunpubudumal.github.io/nvim-essentials/day-01/) | [`day-01/day-1.ipynb`](day-01/day-1.ipynb) | The mindset Neovim requires, installing it, and `:Tutor` (Lessons 1 and 2) | Available |
| 2 | [Day 2](https://dasunpubudumal.github.io/nvim-essentials/day-02/) | [`day-02/day-02.ipynb`](day-02/day-02.ipynb) | LazyVim, and hands-on work in a project | In progress |

## File structure

Everything for a day lives in that day's folder:

```
nvim-essentials/
├── README.md
├── .github/
│   ├── workflows/
│   │   └── pages.yml       # Publishes the notebooks to GitHub Pages
│   ├── scripts/            # Build the sessions page, theme the notebook pages, add contents lists
│   └── site/               # Sessions page template and the shared Neovim theme (CSS)
├── assets/                 # Favicons for the published site
├── day-01/
│   ├── day-1.ipynb         # Day 1 notebook
│   ├── Dockerfile          # Optional: a clean Neovim environment
│   ├── Dockerising.md      # How to build and run the Dockerfile
│   └── assets/             # Images used by the Day 1 notebook
└── day-02/
    ├── day-02.ipynb        # Day 2 notebook
    └── assets/             # Images used by the Day 2 notebook
```

- Each new day gets its own `day-NN/` folder, with the number zero-padded so that the folders stay in order.
- A notebook's images go in the `assets/` folder next to it, and are referenced with relative paths (e.g., `assets/tutor.png`).

## Setup

You only need to do this once. You'll need `git` and Python 3.

**1. Clone the repository:**

```bash
git clone https://github.com/dasunpubudumal/nvim-essentials.git
cd nvim-essentials
```

**2. Create and activate a virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell), use `py -m venv .venv` and then `.venv\Scripts\Activate.ps1`.

**3. Install Jupyter:**

```bash
pip install jupyter
```

## Opening the notebooks

From the root of the repository, with the virtual environment activated:

```bash
jupyter lab
```

This opens JupyterLab in your browser. Use the file browser on the left to go to a `day-NN/` folder, and double-click the notebook to open it.

When you're done, press `Ctrl+C` twice in the terminal to stop Jupyter, and run `deactivate` to leave the virtual environment. Next time, you only need to run `source .venv/bin/activate` and `jupyter lab` again.

## Reading online (GitHub Pages)

If you just want to read, you can skip the setup. Every notebook is published as a web page on GitHub Pages, at:

```
https://dasunpubudumal.github.io/nvim-essentials/day-NN/
```

Replace `NN` with the two-digit day number. For example, Day 1 is at [dasunpubudumal.github.io/nvim-essentials/day-01](https://dasunpubudumal.github.io/nvim-essentials/day-01/). The [site's home page](https://dasunpubudumal.github.io/nvim-essentials/) lists every day, and the [Sessions](#sessions) table links to each one too.

The pages are rebuilt on every push to `main` (see [`.github/workflows/pages.yml`](.github/workflows/pages.yml)), so a new `day-NN/` folder shows up online on its own a minute or two after it's pushed.

## Optional: a clean Neovim environment

If you want to try things out without touching your existing Neovim setup, `day-01/` includes a Dockerfile for a fresh environment. This is for running Neovim only, not the notebooks. See [`day-01/Dockerising.md`](day-01/Dockerising.md) for the steps.
