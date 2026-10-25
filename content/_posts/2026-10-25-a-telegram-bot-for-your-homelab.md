---
title: A Telegram bot for your homelab
date: 2026-10-25 07:30:00
projects: [homelab]
---
My homelab tells me when something is wrong, and it does it through Telegram. The bot costs nothing, it takes about five minutes to set up, and it works with almost every self-hosted tool. This is the short how-to, followed by what my bot sends me.

## Create the bot

1. Open Telegram and start a chat with **@BotFather**, the official bot for making bots.
2. Send `/newbot`.
3. Pick a display name, then a username that ends in `bot`.
4. BotFather answers with a **token**, a long string like `123456:ABC...`.

Treat the token like a password. Everyone who has it can send messages as your bot. Never put it in a public repository. If it leaks, send `/revoke` to BotFather and get a new one.

## Find your chat ID

The bot can only write to you after you have written to it first.

1. Open your new bot in Telegram and send it any message, for example `hello`.
2. Open this address in a browser, with your own token:

```
https://api.telegram.org/bot<TOKEN>/getUpdates
```

3. In the answer, look for `"chat":{"id":123456789,...`. That number is your **chat ID**.

## Send a test message

```bash
curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d chat_id=<CHAT_ID> \
  -d text="Hello from my homelab"
```

If the message shows up in Telegram, you are done with the Telegram part. Everything else is just a tool that calls this same address.

## Let your tools use it

Most tools already know Telegram. They ask for the same two values, the token and the chat ID:

- **Watchtower** takes a notification URL like `telegram://<TOKEN>@telegram?channels=<CHAT_ID>`.
- **Diun**, **Beszel**, **Sonarr** and **Radarr** have a Telegram option in their notification settings.
- For your own scripts, the `curl` call above is enough.

Keep the token in an `.env` file or in the tool's own settings, never in a compose file you share.

## What my bot sends me

Only things that need my attention, so that silence means everything is fine:

- **Watchtower:** a note when it has updated a container, or when an update failed.
- **Diun:** a daily check for new versions of the few containers I update by hand, like Pi-hole, Tailscale and Vaultwarden. It only tells me, it never updates anything.
- **Beszel:** an alarm when the monitoring agent is gone for five minutes, when the disk is over 85 percent full, when it gets too hot, when a container turns unhealthy, and when a drive reports a SMART error.
- **Backup check:** a message when a backup is too old or has errors, or when a disk is getting full.
- **Sonarr and Radarr:** download and import notices.

One more bot exists that answered commands and reported crashes, but I switched it off, because the other tools already cover what I need.

## Tips

- Use one bot for everything. A single chat is easier to follow than many.
- Send only problems. A bot that talks all day gets muted, and then it is useless.
- Test each tool once on purpose, for example with a test message, so you know the alert really arrives.
- If you rotate the token, remember every place that uses it. I keep a small script for that.
