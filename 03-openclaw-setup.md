# OpenClaw Setup Guide

<!--
AGENT CONTEXT
=============
Purpose: Install and configure OpenClaw as an always-on local AI assistant daemon on the Mac Mini.

How to use this guide with a user:
  1. Confirm the user has completed 02-terminal-setup.md (Homebrew must be installed).
  2. Walk through Steps 1–5 in order — each step must succeed before the next.
  3. Step 6 (companion app) and Step 7 (sandboxing note) are optional — offer them after the core setup is verified.

At each "Verify" block: confirm the step worked before moving on.

Key terms used throughout:
  Gateway  = the OpenClaw daemon process that runs in the background and handles all channel traffic
  Channel  = a messaging platform OpenClaw connects to (Telegram, WhatsApp, iMessage, etc.)
  Pairing  = the one-time approval flow that links your account on a channel to the Gateway
-->

## What You're Building

OpenClaw is a locally-run AI assistant daemon that connects to messaging platforms and routes your messages to an AI model. By the end of this guide, you'll have:

- A persistent Gateway daemon that starts automatically on login
- OpenAI (GPT-4o) configured as the AI model
- Telegram connected as your first messaging channel

You talk to the assistant by messaging your Telegram bot. The Gateway handles everything in between.

> **Prerequisite:** Complete the [Terminal Setup](02-terminal-setup.md) guide first. Homebrew must be installed.

---

## Step 1 — Install Node.js via nvm

OpenClaw requires Node 22.16 or later. `nvm` (Node Version Manager) lets you install and switch Node versions without touching your system Node, and is the recommended approach.

**Install nvm:**

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

Close and reopen your terminal, or reload your shell:

```bash
source ~/.zshrc
```

**Install Node 24 (recommended):**

```bash
nvm install 24
nvm use 24
nvm alias default 24
```

Setting `default` means Node 24 is automatically active in every new terminal session.

**Verify:**

```bash
node --version
```

You should see `v24.x.x`. Also confirm npm is available:

```bash
npm --version
```

---

## Step 2 — Install OpenClaw

Install the OpenClaw CLI globally:

```bash
npm install -g openclaw@latest
```

**Verify:**

```bash
openclaw --version
```

You should see the installed version number.

---

## Step 3 — Configure OpenAI as Your Model

OpenClaw reads its configuration from `~/.openclaw/openclaw.json`. You'll create this file and point it at OpenAI's GPT-4o.

**Create the config directory and file:**

```bash
mkdir -p ~/.openclaw
```

```bash
cat > ~/.openclaw/openclaw.json << 'EOF'
{
  "agent": {
    "model": "openai/gpt-4o"
  }
}
EOF
```

**Add your OpenAI API key via macOS Keychain:**

Storing the key in `~/.zshrc` as plaintext means any process that reads your shell files can see it. Instead, store it in the macOS Keychain — encrypted on disk and protected by your login password.

Run this once to save the key (replace `your-api-key-here` with your actual key):

```bash
security add-generic-password -a "$USER" -s "OPENAI_API_KEY" -w "your-api-key-here"
```

Then add this to `~/.zshrc` so the key is loaded into your environment at login without ever being written to the file itself:

```bash
echo 'export OPENAI_API_KEY=$(security find-generic-password -a "$USER" -s "OPENAI_API_KEY" -w 2>/dev/null)' >> ~/.zshrc
source ~/.zshrc
```

To update the key later, delete the old entry and add a new one:

```bash
security delete-generic-password -a "$USER" -s "OPENAI_API_KEY"
security add-generic-password -a "$USER" -s "OPENAI_API_KEY" -w "your-new-key-here"
```

> **Note:** If you don't have an OpenAI account yet, sign up at [platform.openai.com](https://platform.openai.com) and create an API key under API Keys. Usage is billed per token — GPT-4o is typically a few cents per conversation.

**Lock down the config file:**

The `openclaw.json` file will eventually hold your Telegram bot token. Restrict it to your user only:

```bash
chmod 600 ~/.openclaw/openclaw.json
```

**Verify:**

```bash
openclaw agent --message "say hello"
```

You should see a response from the model in your terminal. If you see an authentication error, confirm the key loaded correctly:

```bash
echo $OPENAI_API_KEY
```

---

## Step 4 — Install the Gateway Daemon

The Gateway is the background process that keeps OpenClaw running at all times, receives messages from connected channels, and sends them to the model. Installing it as a daemon means it starts automatically on login without you doing anything.

```bash
openclaw onboard --install-daemon
```

The onboarding process installs the Gateway as a launchd user service on macOS. It will prompt you to confirm permissions.

**Verify the daemon is running:**

```bash
openclaw gateway --port 18789 --verbose
```

You should see the Gateway start up and report which channels are active (none yet — that's Step 5). Press `Ctrl+C` to stop the verbose session. The daemon continues running in the background.

**Verify the Gateway is only listening on localhost:**

The Gateway should not be reachable from other machines on your network. Check what address it's bound to:

```bash
lsof -i :18789 | grep LISTEN
```

Look at the `NAME` column in the output:

- `localhost:18789` or `127.0.0.1:18789` — the Gateway is only reachable from your Mac. You're good.
- `*:18789` — the Gateway is reachable from any machine on your network. In this case, add a firewall rule to block the port:

```bash
/usr/libexec/ApplicationFirewall/socketfilterfw --add $(which openclaw)
```

Then open **System Settings → Network → Firewall → Options** and confirm OpenClaw is listed as "Block incoming connections."

---

## Step 5 — Connect Telegram

Telegram is the easiest channel to set up: no app install required on the Mac Mini, and the connection is entirely token-based.

### 5.1 Create a Telegram Bot

1. Open Telegram on your phone or desktop and search for **@BotFather**
2. Start a chat and send `/newbot`
3. Follow the prompts — you'll be asked for a bot name and username (the username must end in `bot`, e.g. `myassistant_bot`)
4. BotFather will reply with a **bot token** that looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
5. Copy and save that token — you'll need it in the next step

### 5.2 Add the Bot Token to Your Config

Edit `~/.openclaw/openclaw.json` to add the Telegram channel:

```json
{
  "agent": {
    "model": "openai/gpt-4o"
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_BOT_TOKEN_HERE",
      "dmPolicy": "pairing"
    }
  }
}
```

Replace `YOUR_BOT_TOKEN_HERE` with the token from BotFather.

> **What `dmPolicy: "pairing"` means:** The bot won't respond to anyone by default. You'll approve your own Telegram account in the next step, keeping the bot private even if someone else finds its username.

### 5.3 Pair Your Telegram Account

Start the Gateway and complete the pairing flow:

```bash
openclaw gateway
```

In a second terminal window, send yourself a message via the bot on Telegram (just `/start` is enough), then check for the pending pairing request:

```bash
openclaw pairing list telegram
```

Approve your account using the pairing code shown:

```bash
openclaw pairing approve telegram <CODE>
```

**Verify:** Send a message to your Telegram bot. You should receive an AI-generated reply within a few seconds.

---

## Step 6 — macOS Companion App *(Optional)*

The OpenClaw companion app for macOS adds voice support with wake-word detection ("Hey Claw" or a custom phrase), a live canvas workspace, and a menu bar icon showing Gateway status.

Download it from [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) under the Releases section and install it like any `.dmg`. The companion app connects automatically to the running Gateway.

---

## Step 7 — Sandboxing *(Optional — future guide)*

By default, any tools OpenClaw uses run directly on your Mac. For group channels (shared Slack workspaces, Discord servers, etc.) where other users can interact with the bot, you should enable sandboxing so tool execution is isolated from your host system. This requires Docker.

Sandboxing setup is covered in a separate guide. Until then, keep OpenClaw to private DM channels where you control who can interact with it.

---

## Verification Checklist

- [ ] `node --version` shows `v24.x.x`
- [ ] `npm --version` returns a version number
- [ ] `openclaw --version` returns a version number
- [ ] `~/.openclaw/openclaw.json` exists with the `agent.model` and Telegram channel config
- [ ] `ls -l ~/.openclaw/openclaw.json` shows permissions `-rw-------` (600)
- [ ] `security find-generic-password -a "$USER" -s "OPENAI_API_KEY" -w` returns your API key
- [ ] `echo $OPENAI_API_KEY` prints your API key (not empty)
- [ ] `openclaw agent --message "say hello"` returns a response from GPT-4o
- [ ] `openclaw onboard --install-daemon` completed without errors
- [ ] `lsof -i :18789 | grep LISTEN` shows `localhost:18789` or `127.0.0.1:18789`, not `*:18789`
- [ ] Sending a message to your Telegram bot returns an AI reply
