# Mac Mini Setup Guide

<!--
AGENT CONTEXT
=============
Purpose: Configure an Apple M4 or M4 Pro Mac Mini as a reliable, always-on development machine.

How to use this guide with a user:
  1. Ask the user: "How do you plan to use your Mac Mini?" then route to the matching option:
       → "Sit at it directly with a keyboard, mouse, and monitor" → Option A
       → "Control it from my MacBook in the same room or on the same network" → Option B (Luna Display)
       → "Access it from anywhere, including remotely over the internet" → Option C (Jump Desktop)
  2. Have the user complete Part 1 (Common Baseline) first — all options require it.
  3. Then walk through exactly ONE of Option A, B, or C. Skip the other two.
  4. Offer Part 3 (Tailscale) to any user who wants remote access from outside their home network.
  5. Offer Part 4 (Security Hardening) after setup is fully verified.

At each "Verify" block: confirm the step worked before moving on.

Terminology used throughout this guide:
  Primary   = Mac Mini (the machine being set up)
  Secondary = MacBook Pro (used to control the Mac Mini in Options B and C)

Prerequisites before starting:
  - Mac Mini is powered on with macOS initial setup complete
  - You have an Apple ID signed in on the Mac Mini
  - For Option B: Luna Display dongle purchased from astropad.com
  - For Option C: Jump Desktop account created at jumpdesktop.com
-->

## What You're Building

This guide sets up a Mac Mini as a dedicated development machine. By the end, you'll be able to use it reliably — whether sitting at it directly, controlling it from your MacBook, or accessing it from anywhere in the world.

Regardless of which option you choose, the Mac Mini will be configured to:

- Stay awake and accessible at all times
- Start up automatically without requiring someone to type a password
- Be reachable by a consistent name on your network (`your_project.local`)

---

## Step 0: Choose Your Setup

Pick the option that matches how you want to use the Mac Mini. You only need to follow one.

| | Option A: Standard | Option B: Luna Display | Option C: Jump Desktop |
|---|---|---|---|
| **Best for** | Sitting at the Mac Mini directly | Controlling it from your MacBook, same room or home | Accessing it from anywhere |
| **What you see** | Mac Mini's own screen | Mac Mini's desktop in a window on your MacBook | Mac Mini's desktop in an app on any device |
| **Extra hardware needed** | Monitor, keyboard, mouse | Luna Display dongle (~$70) | None |
| **Cost** | Free | ~$70 (dongle) | $34 (app) |
| **Works remotely (away from home)?** | No | Only with Tailscale (see Part 3) | Yes, built-in |
| **Performance** | Native | Near-native on local network | Good over internet |
| **Complexity** | Low | Medium | Low |

**Not sure?** Start with **Option C (Jump Desktop)** — no extra hardware, works from anywhere, and you can always add Luna Display later.

> 🚀 **Recommended first-time approach:** Start with **Option A (Standard)** using a keyboard, mouse, and monitor. Get the Mac Mini up and running, confirm everything works, then come back and layer on Option B or C at your own pace. The goal is a working machine today — not a perfect setup before you've used it once.

---

## Part 1: Common Baseline

<!-- AGENT: All users complete this section before continuing to their chosen option. -->

These settings ensure the Mac Mini stays accessible and responsive at all times. Complete all steps in this section regardless of which option you chose.

### 1.1 Keep the Mac Mini Awake

A Mac Mini used as a server or remote machine must never go to sleep on its own.

1. Open **System Settings**
2. Navigate to **Energy** (on older macOS versions this may be called **Energy Saver**)
3. Set **Turn display off after** → **Never**
4. Disable **Put hard disks to sleep when possible**
5. Enable **Prevent your Mac from automatically sleeping when the display is off**
6. Enable **Wake for network access**

> **What "Wake for network access" does:** If the Mac Mini ever goes to sleep, this allows it to be woken remotely over the network without physically pressing the power button.

**Verify:** Leave the Mac Mini idle for 10 minutes with no input. It should remain on and responsive.

### 1.2 Set a Hostname

A hostname lets you find the Mac Mini on your network using a memorable name instead of a numeric IP address.

1. Open **System Settings**
2. Navigate to **General → Sharing**
3. Click **Edit** next to the computer name
4. Set the **Hostname** to something short and recognizable, such as `your_project`
5. Click **OK**

The Mac Mini will now be reachable at `your_project.local` on your local network.

**Verify:** Open Terminal on another Mac on the same network and run:

```bash
ping your_project.local
```

You should see replies. Press `Ctrl+C` to stop.

### 1.3 Use a Stable Network Connection

The Mac Mini should always be reachable at the same address on your network.

**Use Ethernet instead of WiFi (strongly recommended):**

1. Connect the Mac Mini to your router with an Ethernet cable
2. Open **System Settings → Network** and confirm Ethernet shows as connected
3. If WiFi is also active, drag Ethernet above WiFi in the service order to give it priority

> **Why Ethernet?** WiFi connections can drop, vary in speed, or conflict with Luna Display's wireless streaming. A wired connection is more stable and predictable.

**Give it a stable IP address — DHCP reservation (recommended):**

1. Log into your router's admin panel (typically at `192.168.1.1` or `192.168.0.1` in a browser)
2. Find the Mac Mini in the connected devices list — it will appear by its hostname `your_project`
3. Create a DHCP reservation so the router always assigns it the same IP (e.g. `192.168.1.100`)

> **Why this matters:** Without a stable IP, the Mac Mini's address can change after a reboot, breaking saved SSH connections and remote desktop shortcuts.

**Alternative — set a static IP directly on the Mac:**

1. Open **System Settings → Network → Ethernet → Details**
2. Under **TCP/IP**, change Configure IPv4 from **Using DHCP** to **Manually**
3. Enter an IP address outside your router's DHCP range (e.g. `192.168.1.200`)
4. Set the subnet mask (typically `255.255.255.0`) and your router's IP as the gateway

### 1.4 Enable Basic Remote Access (Screen Sharing)

This gives you a simple fallback to view and control the Mac Mini from any other Mac on the same network — useful during setup and as a backup access method regardless of which option you use.

1. Open **System Settings → General → Sharing**
2. Toggle on **Screen Sharing**
3. Under "Allow access for," select **All users** or add your specific user account

**Verify:** From your MacBook, open Finder → **Go → Connect to Server** → type `vnc://your_project.local` → Connect. You should see the Mac Mini's screen.

---

After completing Part 1, continue to **your chosen option** below. Skip the options you are not using.

---

## Option A: Standard Setup

<!-- AGENT: Follow this section only if the user chose Option A. Skip Options B and C entirely. -->

**What you need:** An external monitor, a keyboard, and a mouse or trackpad.

This is the simplest setup. The Mac Mini works like any desktop computer — you interact with it directly using connected peripherals. The Common Baseline (Part 1) covers most of what you need.

### Steps

1. Connect your monitor to the Mac Mini using an HDMI cable or a USB-C/Thunderbolt cable into one of the back ports
2. Connect a USB keyboard and mouse, or pair Bluetooth peripherals via **System Settings → Bluetooth**
3. Power on the Mac Mini — it will boot to the login screen

### Optional: Automatic Login

If the Mac Mini restarts unexpectedly (power outage, macOS update), automatic login brings it back to a usable desktop on its own.

1. Open **System Settings → Users & Groups**
2. Click the **info (i)** button next to your user account
3. Enable **Automatic login** and select your user account

> **Note:** On Apple Silicon Macs, automatic login may require FileVault to be configured to allow it, or disabled. You will be prompted to choose during setup. Test by rebooting and confirming the Mac Mini reaches the desktop without a password prompt.

### Verification

- [ ] Mac Mini boots and shows a desktop
- [ ] Monitor, keyboard, and mouse all respond correctly
- [ ] `ping your_project.local` resolves from another Mac on the same network
- [ ] Screen Sharing connects from the MacBook via `vnc://your_project.local`
- [ ] Mac Mini stays awake with no input for 10+ minutes

---

## Option B: Luna Display

<!-- AGENT: Follow this section only if the user chose Option B. Skip Options A and C entirely.
Walk through sub-sections B.1 through B.8 in order. Confirm each "Verify" block before proceeding. -->

Luna Display is a hardware dongle that lets you use your MacBook as a high-quality display for the Mac Mini with near-native responsiveness. This guide sets up **Headless Mode**, where the Mac Mini runs without any monitor attached and the MacBook acts as its only screen.

**Terminology:** In Luna's world, **Primary** = Mac Mini (the machine the dongle plugs into). **Secondary** = MacBook Pro (the screen you look at). The dongle defines the Primary.

### What You Need

- Luna Display dongle (USB-C model) — purchase at [astropad.com](https://astropad.com/product/lunadisplay/)
- A USB-C cable rated **USB 3.1 or later** with data transfer support (details in section B.7)
- A temporary monitor, keyboard, and mouse for initial setup on the Mac Mini — you will disconnect them once setup is complete

### B.1 Disable FileVault

Luna's headless mode requires automatic login, which requires FileVault to be turned off.

> **What FileVault is:** FileVault encrypts the Mac Mini's storage so data cannot be read if someone steals the drive. Turning it off is a deliberate security tradeoff — the Mac Mini can log in automatically on boot, but its storage is no longer encrypted at rest. For a home development machine on a trusted network, this is typically acceptable.

1. Open **System Settings → Privacy & Security**
2. Scroll to **FileVault** and click **Turn Off**
3. Confirm and save the recovery key before the Mac begins decryption
4. Wait for decryption to complete (this runs in the background and may take several minutes)

**Verify:** Return to **System Settings → Privacy & Security → FileVault**. It should show "FileVault is turned off."

### B.2 Enable Automatic Login

With FileVault off, the Mac Mini can boot directly to the desktop without waiting for a password.

1. Open **System Settings → Users & Groups**
2. Click the **info (i)** button next to your user account
3. Enable **Automatic login** and select your user account

**Verify:** Reboot the Mac Mini. It should reach the desktop on its own without you typing a password.

### B.3 Where to Plug the Luna Dongle

The M4 Mac Mini has five USB-C ports, but only the three on the **back** support displays. The two on the front are USB 3 only and will not work with Luna.

```
  BACK OF MAC MINI (looking at the back panel)
  ┌──────────────────────────────────────┐
  │                                      │
  │  ⚡ ⚡ ⚡   🔌    📺    ⏻          │
  │  TB TB TB  ETH   HDMI  POWER        │
  │                                      │
  └──────────────────────────────────────┘

  ⚡ = Thunderbolt 4/5 (USB-C shaped) ← PLUG LUNA DONGLE HERE
  🔌 = Ethernet (RJ-45)
  📺 = HDMI
  ⏻  = Power
```

- **M4 Mac Mini:** Back ports are Thunderbolt 4
- **M4 Pro Mac Mini:** Back ports are Thunderbolt 5 (backward compatible with Thunderbolt 4 accessories)

Plug the Luna dongle into any one of the three back Thunderbolt ports.

**Verify:** Go to **Apple menu → About This Mac → System Report → Thunderbolt/USB4**. The Luna dongle should appear in the list.

### B.4 Install the Luna Apps

**On the Mac Mini (Primary) — connect your temporary monitor, keyboard, and mouse first:**

1. Confirm the Luna dongle is plugged into a back Thunderbolt port
2. Download and install the **Luna Primary app** from [astropad.com/app-downloads](https://astropad.com/app-downloads-luna-display/)
3. Add Luna to Login Items so it launches automatically on every boot:
   - Open **System Settings → General → Login Items**
   - Click **+** under "Open at Login" and add Luna Display
   - Alternatively: right-click the Luna icon in the Dock → **Options → Open at Login**

**On your MacBook Pro (Secondary):**

4. Download and install the **Luna Secondary app** from [downloads.astropad.com/luna-secondary/mac/latest](https://downloads.astropad.com/luna-secondary/mac/latest)
5. **Disable Exclusive Fullscreen Mode** — by default, Luna Secondary takes over your entire MacBook screen and locks all input to the Mac Mini, making it impossible to use both machines simultaneously. To disable it:
   1. Open the Luna Secondary app — it will immediately go fullscreen
   2. Quickly press **Cmd + ,** (comma) to open Preferences before it connects
   3. Uncheck **Exclusive Fullscreen Mode**
   4. Close Preferences and restart the Luna Secondary app

   > With Exclusive Fullscreen Mode off, Luna runs as a regular macOS window you can resize, move to another monitor, and switch away from using Cmd+Tab or trackpad gestures.

### B.5 Connect the Two Macs

1. Make sure both Macs are on the same WiFi network

   > **Better performance with a cable:** WiFi works for initial discovery and connection, but Luna performs best over a direct USB-C cable. Per [Astropad's Mac-to-Mac USB Connection Guide](https://support.astropad.com/en/articles/11879034-luna-display-usb-mac-to-mac-connection-guide), the cable must be rated **USB 3.1 or later** with data transfer support. Apple's standard USB-C charging cables — including those bundled with Macs — are USB 2.0 and will not work. Luna silently falls back to WiFi with incompatible cables. See section B.7 for connection options and cable recommendations.

2. Launch **Luna Primary** on the Mac Mini first, then open **Luna Secondary** on your MacBook — they should discover each other automatically
3. Once the Mac Mini's desktop is visible on your MacBook, disconnect the temporary monitor, keyboard, and mouse from the Mac Mini

**Verify:** The Mac Mini's desktop appears in a Luna window on your MacBook. Move the mouse and confirm it controls the Mac Mini. Type something in a text field on the Mac Mini and confirm input works.

### B.6 Daily Workflow

After setup, you no longer need a monitor, keyboard, or mouse connected to the Mac Mini. The daily routine is:

1. Power on the Mac Mini (or confirm it is already on)
2. It auto-logs in → Luna Primary launches automatically
3. Open Luna Secondary on your MacBook → the Mac Mini desktop appears

### B.7 Connection Options

Luna supports multiple connection types between the two Macs. Listed from best to worst performance:

| Connection | Latency | What you need |
|------------|---------|---------------|
| Thunderbolt cable | Lowest | Thunderbolt cable between both Macs |
| Ethernet cable | Very low | Ethernet cable (direct or both through router) |
| USB-C cable | Very low | USB 3.1+ data cable — not a standard charging cable |
| Peer-to-Peer WiFi | Low | WiFi enabled on both Macs (bypasses router, up to 46% lower latency than standard WiFi) |
| WiFi (through router) | Variable | Both Macs on the same WiFi network |

**If WiFi feels laggy:** Try **Peer-to-Peer** first — select it in Luna's connection dropdown menu. It creates a direct wireless link between the Macs, bypassing your router.

**If Peer-to-Peer still isn't smooth:** Use a **USB-C cable** rated USB 3.1 Gen 2 or higher. Look for cables explicitly labeled with data transfer speeds — an Anker USB-C to USB-C 3.1 Gen 2 cable (~$10–15) works well. Plug directly into both Macs with no hubs, adapters, or docking stations in between.

### B.8 Performance Tips

- **Lower the display resolution** — Retina/HiDPI mode doubles the pixel count Luna has to stream and is the most common cause of lag
- **Keep the Mac Mini on Ethernet** — even if Luna uses peer-to-peer or USB between the Macs, having the Mini on Ethernet keeps its internet traffic off WiFi and reduces interference
- **Close bandwidth-heavy apps** on both machines during Luna sessions (video streaming, large downloads)
- **Re-enable Exclusive Fullscreen Mode** if you only need to use the Mac Mini and not the MacBook simultaneously — it provides a small performance boost

### B.9 Set Up SSH Access (Recommended)

SSH gives you terminal access to the Mac Mini from your MacBook, which is useful for running commands, transferring files, and connecting from other tools.

**Enable Remote Login on the Mac Mini:**

1. Open **System Settings → General → Sharing**
2. Toggle on **Remote Login**
3. Under "Allow access for," select **All users** or add your specific user account

**Set up key-based authentication (no password required) — run this on your MacBook:**

```bash
# Generate a key pair if you don't already have one
ssh-keygen -t ed25519 -C "macbook-pro"

# Copy your public key to the Mac Mini
ssh-copy-id yourname@your_project.local
```

**Verify:**

```bash
ssh yourname@your_project.local
```

You should connect without being prompted for a password.

### Verification

- [ ] FileVault is turned off (System Settings → Privacy & Security → FileVault)
- [ ] Mac Mini boots to the desktop automatically after a restart — no password required
- [ ] Luna dongle appears in System Report → Thunderbolt/USB4
- [ ] Luna Secondary's Exclusive Fullscreen Mode is disabled (press Cmd + , in Luna Secondary to confirm)
- [ ] Mac Mini desktop is visible in a Luna window on the MacBook
- [ ] Mouse and keyboard input works on the Mac Mini from the MacBook
- [ ] Connection type is USB-C, Ethernet, or Thunderbolt for best performance (check Luna's connection indicator)
- [ ] (If SSH set up) `ssh yourname@your_project.local` connects without a password prompt

---

## Option C: Jump Desktop

<!-- AGENT: Follow this section only if the user chose Option C. Skip Options A and B entirely.
Walk through sub-sections C.1 through C.3 in order. Confirm each "Verify" block before proceeding. -->

Jump Desktop is a software-only remote desktop tool with hardware-accelerated streaming. It works over the internet with no VPN, port forwarding, or extra hardware required.

### What You Need

- Jump Desktop app on the Mac Mini and on your MacBook (or any other device)
- A free Jump Desktop account — create one at [jumpdesktop.com](https://jumpdesktop.com)

### C.1 Enable Automatic Login

If the Mac Mini restarts, you want it to boot back to a usable desktop on its own so Jump Desktop can reconnect to it.

1. Open **System Settings → Users & Groups**
2. Click the **info (i)** button next to your user account
3. Enable **Automatic login** and select your user account

> **Note:** On Apple Silicon Macs, automatic login may conflict with FileVault. If prompted, either disable FileVault or configure it to allow automatic login, then test by rebooting the Mac Mini.

**Verify:** Reboot the Mac Mini. It should reach the desktop on its own without a password prompt.

### C.2 Install and Configure Jump Desktop

**On the Mac Mini:**

1. Install Jump Desktop from the [Mac App Store](https://apps.apple.com/app/jump-desktop-remote-desktop/id364876095) or [jumpdesktop.com](https://jumpdesktop.com)
2. Open Jump Desktop and sign in with your Jump Desktop account
3. Grant the permissions Jump requests — screen recording and accessibility access are required for remote control to work
4. The Mac Mini will now appear in your device list from any signed-in device

**On your MacBook Pro (or any other device):**

5. Install Jump Desktop from the App Store or [jumpdesktop.com](https://jumpdesktop.com)
6. Sign in with the same Jump Desktop account
7. The Mac Mini should appear in your device list automatically

**Verify:** On your MacBook, open Jump Desktop and connect to the Mac Mini using the **Fluid Remote Desktop** protocol. The Mac Mini's desktop should appear within a few seconds.

### C.3 Set Up SSH Access (Recommended)

SSH gives you terminal access to the Mac Mini for running commands and file transfers — a useful complement to Jump Desktop's graphical access.

**Enable Remote Login on the Mac Mini:**

1. Open **System Settings → General → Sharing**
2. Toggle on **Remote Login**
3. Under "Allow access for," select **All users** or add your specific user account

**Set up key-based authentication — run this on your MacBook:**

```bash
# Generate a key pair if you don't already have one
ssh-keygen -t ed25519 -C "macbook-pro"

# Copy your public key to the Mac Mini
ssh-copy-id yourname@your_project.local
```

**Verify:**

```bash
ssh yourname@your_project.local
```

You should connect without being prompted for a password.

### Verification

- [ ] Mac Mini boots to the desktop automatically after a restart
- [ ] Mac Mini appears in the Jump Desktop device list on the MacBook
- [ ] Jump Desktop connects and shows the Mac Mini's desktop
- [ ] To confirm remote access works: connect from a different network (e.g. a cellular hotspot) and verify Jump Desktop still connects
- [ ] (If SSH set up) `ssh yourname@your_project.local` connects without a password prompt

---

## Part 3: Tailscale (Optional — Access from Any Network)

<!-- AGENT: This section is optional and applies to all options.
Recommend it when: the user chose Option B and wants Luna to work from outside their home network,
or any user who wants SSH access from outside their home network.
Not needed for Option C users who are happy with Jump Desktop for remote access. -->

Tailscale creates a private encrypted network between your devices, making them appear on the same network regardless of physical location. This is the simplest way to add remote access to a Luna Display setup, and a useful complement to Jump Desktop for terminal access.

**Install on the Mac Mini:**

```bash
brew install --cask tailscale
```

Or download from [tailscale.com](https://tailscale.com).

**Install on your MacBook Pro** using the same method.

**Set up:**

1. Open Tailscale on each machine and sign in with the same account (Google, GitHub, or other SSO)
2. Each device gets a stable Tailscale address (e.g. `100.x.x.x`) and hostname that works from anywhere
3. Tailscale's MagicDNS feature makes the Mac Mini reachable by hostname from any network:

```bash
ssh yourname@your_project
```

**Verify:** Switch your MacBook to a cellular hotspot (to leave your home network) and run:

```bash
ssh yourname@your_project
```

You should connect successfully. Tailscale is free for personal use with up to 100 devices.

---

## Part 4: Security Hardening (Optional)

<!-- AGENT: Offer this section after the user's chosen option is fully verified and working.
Important: Option B users must keep FileVault OFF — do not recommend the FileVault step to them. -->

These steps improve the security of a machine that is always on and network-accessible. Complete them after your primary setup is confirmed working.

### Firewall

1. Open **System Settings → Network → Firewall**
2. Toggle the firewall **on**
3. Click **Options** and confirm that any services you enabled (SSH, Screen Sharing, Remote Management) are listed as allowed

### FileVault — Option A and C only

> **Skip this step if you are using Option B (Luna Display).** FileVault must remain off for Luna headless mode to work.

1. Open **System Settings → Privacy & Security → FileVault**
2. Click **Turn On** and follow the prompts
3. Save the recovery key in a secure location

### Strong Password

Your user password protects SSH access, Screen Sharing, and `sudo` commands even when automatic login is enabled. Use a strong, unique password for your Mac Mini user account.

### Disable SSH Password Authentication

Once key-based SSH is working, disable password login to prevent brute-force attacks from the network:

1. On the Mac Mini, open Terminal and edit the SSH config file:

```bash
sudo nano /etc/ssh/sshd_config
```

2. Find the `PasswordAuthentication` line and set it to `no`. If the line is commented out (starts with `#`), remove the `#` first:

```
PasswordAuthentication no
```

3. Save the file (`Ctrl+O`, then `Enter`, then `Ctrl+X`), then restart SSH:

```bash
sudo launchctl kickstart -k system/com.openssh.sshd
```

**Verify:** Try connecting with a wrong password — it should be rejected immediately. Key-based login should still work.

---

## Workspace Tips: Using Both Machines Simultaneously

<!-- AGENT: This section is relevant for Option B users who want to use both the Mac Mini and the MacBook Pro at the same time. -->

If you are using **Option B (Luna Display)** and want the Mac Mini and MacBook Pro working side by side:

### Recommended: External Monitor

Dedicate an external monitor to the Mac Mini via Luna and use the MacBook's built-in display for your own apps.

1. Confirm Exclusive Fullscreen Mode is disabled in Luna Secondary — press **Cmd + ,** to check
2. Open Luna Secondary — it will connect as a regular window
3. Drag the Luna window to your external monitor
4. Click the **green traffic light button** to make Luna fullscreen on that monitor only
5. Your MacBook's built-in screen stays free for email, Slack, browser, and other apps

```
  ┌─────────────────┐    ┌─────────────┐
  │  External       │    │  MacBook    │
  │  Monitor        │    │  Pro        │
  │                 │    │             │
  │  Mac Mini via   │    │  Email,     │
  │  Luna Display   │    │  Slack,     │
  │                 │    │  Browser    │
  └─────────────────┘    └─────────────┘
         │
    Connected to
     MacBook Pro
```

Click inside the Luna window to control the Mac Mini. Click outside it to control the MacBook. One keyboard and trackpad; the context switch is instant.

### Alternative: macOS Spaces (No External Monitor)

Run Luna fullscreen in its own Space and use a three-finger swipe to switch between the Mac Mini and MacBook desktops.

1. Open Luna Secondary and go fullscreen — click the green traffic light button or press **Ctrl+Cmd+F**
2. Open Mission Control — swipe up with three fingers or press F3
3. Luna fullscreen and your MacBook desktop appear as separate Spaces in the top bar
4. Swipe left or right with three fingers to switch between them

Each machine gets the full screen resolution. It takes about a day to build the muscle memory.

---

## Master Verification Checklist

Run through this after completing your chosen option and any optional add-ons.

**Part 1 — Common Baseline (everyone)**
- [ ] Mac Mini stays awake indefinitely with the display off
- [ ] `ping your_project.local` resolves from another Mac on the same network
- [ ] Screen Sharing connects via `vnc://your_project.local`
- [ ] Mac Mini has a stable IP address (DHCP reservation or static)

**Option A — Standard**
- [ ] Mac Mini boots to desktop after a restart
- [ ] Monitor, keyboard, and mouse all work correctly

**Option B — Luna Display**
- [ ] FileVault is turned off
- [ ] Mac Mini boots to desktop after restart — no password required
- [ ] Luna dongle appears in System Report → Thunderbolt/USB4
- [ ] Luna Secondary's Exclusive Fullscreen Mode is disabled
- [ ] Mac Mini desktop is visible in a Luna window on the MacBook
- [ ] Mouse and keyboard input on the MacBook controls the Mac Mini
- [ ] Connection is using USB-C, Ethernet, or Thunderbolt — not WiFi

**Option C — Jump Desktop**
- [ ] Mac Mini boots to desktop after restart — no password required
- [ ] Mac Mini appears in the Jump Desktop device list on the MacBook
- [ ] Jump Desktop connects and shows the Mac Mini desktop
- [ ] Jump Desktop connects successfully from a different network (e.g. cellular hotspot)

**Part 3 — Tailscale (if installed)**
- [ ] `ssh yourname@your_project` connects from outside the home network

**SSH (if set up)**
- [ ] `ssh yourname@your_project.local` connects without a password prompt
- [ ] SSH password authentication is disabled (if Part 4 hardening was applied)
