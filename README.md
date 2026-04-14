The following readme was made with AI because I have no skill creating proper READMEs :D

# github-app-updater

A CLI tool to automatically track and install the latest releases of your favorite GitHub projects, designed for Fedora Linux.

## Overview

`github-app-updater` lets you maintain a personal list of GitHub repositories and install their latest `.rpm` releases with a single command. Instead of manually checking each project's GitHub page, the tool queries the GitHub API, finds the correct package for your system, downloads it to your `~/Downloads` folder, and installs it via `dnf`.

## Features

- Persistent repository list stored in a local `.txt` file
- Validates repos against the GitHub API before adding them
- Automatically detects the correct asset based on configurable filters (e.g. `rpm`, `64`)
- Skips already-downloaded packages to avoid redundant downloads
- Installs packages directly via `sudo dnf install`
- Error handling per repo — a failed install won't stop the rest

## Requirements

- Python 3.x
- [`gh` CLI](https://cli.github.com/) installed and authenticated (`gh auth login`)
- `dnf` package manager (Fedora / RHEL-based distros)

### Python dependencies

```bash
pip install PyGithub requests
```

## Usage

Run the script:

```bash
python main.py
```

You'll be presented with a menu:

```
==========
Current repo list:
owner/repo-one
owner/repo-two
What's your command?
1- Update repo list
2- Install packages
>>
```

### Option 1 — Add a repo

Enter a repository in `owner/repo` format (e.g. `Eugeny/tabby`). The tool will validate it against the GitHub API before saving it to `repo_list.txt`.

### Option 2 — Install packages

Iterates over every repo in your list, finds the latest release asset matching your filters, downloads it to `~/Downloads`, and installs it.

## Configuration

At the top of `main.py`, two variables control which assets get selected:

```python
golden_list = ["rpm", "64"]
```

An asset is selected only if **all** strings in `golden_list` appear in its filename. Adjust this list to match your system architecture or preferred package format.

## How it works

1. Reads `repo_list.txt` on every run to load the current repo list.
2. For each repo, fetches the latest release from the GitHub API via `PyGithub`.
3. Iterates over release assets and checks each filename against `golden_list`.
4. Downloads the matching asset using the `gh` CLI (`--skip-existing` prevents re-downloads).
5. Installs the package with `sudo dnf install`.

## Notes

- The `gh` CLI must be on your system PATH. If you're running from a restricted shell (e.g. VSCode's integrated terminal using `sh`), you may need to use its full path (`/usr/bin/gh`) or launch from a proper `bash` terminal.
- The GitHub API allows 60 unauthenticated requests per hour. If you have many repos or run the tool frequently, authenticate `gh` or set a `GITHUB_TOKEN` environment variable.
- Only Fedora / RPM-based distros are supported out of the box due to the `dnf` dependency.

## Project structure

```
github-app-updater/
├── main.py          # Main script
├── repo_list.txt    # Auto-generated list of tracked repositories
└── README.md
```

## License

MIT
