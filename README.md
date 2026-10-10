# malexgen

<img width="992" height="762" alt="photo_2026-10-10_01-26-22" src="https://github.com/user-attachments/assets/e9ad27b5-1f97-4e1f-bbe5-ef30a26ca40b" />

Malicious extension generator with backstories

## ⚠️ Disclaimer

> **This project is created for EDUCATIONAL PURPOSES ONLY and LEGAL SECURITY TESTING of systems you own or have explicit permission to test.**
>
> Generated extensions are **DEMONSTRATION ONLY**. They do not exfiltrate real data to third parties. Use only on your own systems or in a sandbox.
>
> **The author is not responsible for any misuse.**

---

## 🎯 The Idea

Most people **don't read** extension permissions.
Most antiviruses **don't scan** extensions.
Most browsers **don't limit** extensions.

**MalExtGenerator** shows — in real time, in your own browser — exactly **what a malicious extension can do**:

- 🍪 Steal cookies from every site
- 📝 Intercept form submissions
- ⌨️ Log keystrokes
- 📋 Replace clipboard contents (crypto addresses)
- 🔑 Hijack sessions and tokens
- 📜 Read your browsing history
- 💉 Inject scripts into pages
- 🎣 Show phishing overlays

Then it tells you **how to protect yourself**.

---

## ✨ Features

### 🎭 10 Disguises (Legends)

| | Legend | Description |
|---|--------|-------------|
| 🔒 | **SecureVPN** | "Fast and secure VPN" |
| 🚫 | **AdBlocker Pro** | "Blocks ads and trackers" |
| 🌐 | **TransLite** | "Instant translator" |
| 🔑 | **PassVault** | "Password manager" |
| 🌙 | **DarkMode** | "Dark theme for every site" |
| 📸 | **ScreenCapture** | "Screenshot tool" |
| 📝 | **QuickNotes** | "Quick notes in browser" |
| 🎟️ | **CouponFinder** | "Finds coupons and discounts" |
| ☀️ | **WeatherNow** | "Accurate weather forecast" |
| 📄 | **PDFMaster** | "Convert pages to PDF" |

### ⚡ 8 Attack Payloads

| | Payload | Risk | What it does |
|---|---------|------|--------------|
| 🍪 | **Cookie Stealer** | 🔴 Critical | Exfiltrates all cookies |
| 📝 | **Form Grabber** | 🔴 Critical | Intercepts form submissions |
| ⌨️ | **Keylogger** | 🟠 High | Logs keystrokes |
| 📋 | **Clipboard Hijacker** | 🔴 Critical | Replaces crypto addresses |
| 🔑 | **Session Hijacker** | 🔴 Critical | Steals JWT/OAuth tokens |
| 📜 | **History Snooper** | 🟠 High | Reads browsing history |
| 💉 | **Script Injector** | 🔴 Critical | Injects JS into pages |
| 🎣 | **Phishing Overlay** | 🔴 Critical | Shows fake login forms |

### 📡 Real-time C2 via Telegram

All captured data is delivered to your **Telegram bot** in real time:
- Full JSON files with complete data
- Live notifications per event
- Session management right in chat
- Toggle sessions on/off
- No separate web UI needed

---

## 🚀 Quick Start

### Install

```bash
git clone https://github.com/a11mut3d/malexgen.git
cd malexgen
pip install -r requirements.txt
pip install -e .
```

### Launch the bot
```bash
malexgen bot -t "123456:ABC-DEF..." -c "123456789"
```

### Install the extension
### Watch the data flow

---

mute ecosystem
