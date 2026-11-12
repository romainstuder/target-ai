# Installation Instructions

## Prerequisites

- Python 3.14+ (the scoring script uses only the standard library, so no packages are needed to run it)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview), with an Anthropic API key
  or a Claude Pro/Max subscription
- No Open Targets API key — the Platform is free and open

On macOS, install Python and uv with [Homebrew](https://brew.sh/)
(on Linux, [Linuxbrew](https://docs.brew.sh/Homebrew-on-Linux)):

```shell
brew install python uv
```

Install Claude Code:

```shell
npm install -g @anthropic-ai/claude-code
```

## Setup

```shell
git clone https://github.com/romainstuder/target-ai
cd target-ai

# Start Claude Code; it reads CLAUDE.md and becomes the validation assistant
claude
```

## Running the scripts directly

```shell
uv run python open_targets_client.py validate "BRAF,KRAS" "melanoma"
uv run python open_targets_client.py pathways "PCSK9,HMGCR,ANGPTL3"
```

Output is written to `results/`. Open `results/validation_{slug}.html` in a browser.

## Development setup

Dev tools (ruff, pytest, pre-commit) are declared in `pyproject.toml` and locked in `uv.lock`.
uv manages the virtual environment — do not create or activate `.venv` yourself.

```shell
uv sync --group dev

# Install pre-commit hooks (uvx keeps it out of the project venv)
uvx pre-commit install

uv run ruff check .
uv run pytest
```
