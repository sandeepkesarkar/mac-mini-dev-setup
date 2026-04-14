# Mac Mini Terminal Setup Guide

A complete guide to setting up a polished, productive terminal environment on a Mac Mini intended as a dedicated development machine.

> **Prerequisite:** Complete the [System Preparation & Remote Access](01-system-preparation.md) guide first.

## Step 1 — Homebrew

Homebrew is the foundation. Every other tool installs through it.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the post-install instructions to add Homebrew to your PATH. On Apple Silicon Macs, this typically means adding the following to `~/.zprofile`:

```bash
eval "$(/opt/homebrew/bin/brew shellenv)"
```

## Step 2 — iTerm2

A more capable terminal emulator than the default Terminal.app, with split panes, profiles, and deep customization.

```bash
brew install --cask iterm2
```

## Step 3 — Oh My Zsh

A framework for managing your zsh configuration with themes, plugins, and sensible defaults.

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

## Step 4 — Nerd Font

Nerd Fonts patch developer fonts with icons and glyphs needed by modern CLI tools and prompt themes.

```bash
brew install --cask font-meslo-lg-nerd-font
```

After installing, configure iTerm2 to use it:

1. Open iTerm2 → Settings → Profiles → Text
2. Set the font to **MesloLGS Nerd Font**
3. Recommended size: 13–14pt

## Step 5 — Powerlevel10k Theme

A fast, highly configurable prompt theme for zsh that pairs perfectly with Oh My Zsh.

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
  ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

Edit `~/.zshrc` and set the theme:

```bash
ZSH_THEME="powerlevel10k/powerlevel10k"
```

Restart your shell and the Powerlevel10k configuration wizard will launch automatically, walking you through prompt styling options.

## Step 6 — Plugins

### External plugins (install first)

**zsh-autosuggestions** — suggests commands as you type based on your shell history:

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

**zsh-syntax-highlighting** — colors valid and invalid commands in real time as you type:

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

### Enable all plugins

Edit `~/.zshrc` and update the plugins line:

```bash
plugins=(git node npm docker zsh-autosuggestions zsh-syntax-highlighting z)
```

The `z` plugin is built into Oh My Zsh and lets you jump to frequently used directories by typing partial names.

## Step 7 — iTerm2 Configuration

A few settings worth changing from the defaults:

- **Disable close confirmations**: Settings → General → Closing → uncheck the confirmation prompts
- **Natural text editing**: Settings → Profiles → Keys → Key Mappings → Presets → select "Natural Text Editing" (makes Option+Arrow keys jump by word, Option+Delete deletes a word, etc.)
- **Window appearance**: Settings → Profiles → Window → adjust transparency and blur to taste
- **Color scheme**: Import a color scheme from [iterm2colorschemes.com](https://iterm2colorschemes.com). Popular choices include Catppuccin, Dracula, and Tokyo Night.

## Step 8 — CLI Tools

Install the essential modern CLI replacements in one command:

```bash
brew install eza bat ripgrep fzf zoxide jq htop tldr
```

| Tool | Replaces | Purpose |
|------|----------|---------|
| `eza` | `ls` | File listing with colors, icons, and git integration |
| `bat` | `cat` | File viewing with syntax highlighting and line numbers |
| `ripgrep` (`rg`) | `grep` | Extremely fast recursive text search |
| `fzf` | — | Fuzzy finder for files, command history, and more |
| `zoxide` | `cd` | Smarter directory navigation that learns your habits |
| `jq` | — | JSON processing and pretty-printing from the command line |
| `htop` | `top` | Interactive process viewer |
| `tldr` | `man` | Simplified, example-driven command documentation |

### Shell aliases and initialization

Add the following to the bottom of `~/.zshrc`:

```bash
# Modern CLI replacements
alias ls="eza --icons"
alias ll="eza -la --icons"
alias cat="bat"

# Smart directory jumping
eval "$(zoxide init zsh)"
```

## Applying Changes

After completing all the steps, reload your shell configuration:

```bash
source ~/.zshrc
```

## Dotfiles Backup

To make this setup reproducible, consider versioning your dotfiles with Git. A simple approach using a bare repository:

```bash
git init --bare $HOME/.dotfiles
alias dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
dotfiles config --local status.showUntrackedFiles no
```

Then track your configuration files:

```bash
dotfiles add ~/.zshrc
dotfiles commit -m "initial terminal setup"
dotfiles remote add origin <your-repo-url>
dotfiles push -u origin main
```

Alternatively, tools like `chezmoi` or GNU `stow` offer more structured dotfile management.
