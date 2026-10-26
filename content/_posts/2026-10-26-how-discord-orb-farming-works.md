---
title: How Discord Orb farming works
date: 2026-10-26 10:00:00
---
Discord has Quests. You watch a trailer or play a game for 15 minutes and you get Orbs, which you can spend on avatar decorations and profile effects. I like the decorations, but I don't want to watch ads, and most Quest games I don't own or they don't even run on my Mac.

## Discord is a browser

The Discord desktop app is built with Electron. That means it is basically Chromium with a website inside. Chromium has a remote control for developers, the Chrome DevTools Protocol, or CDP. If you start Discord with remote debugging turned on, another program can connect to it and run JavaScript inside the app:

```bash
Discord --remote-debugging-port=9222
```

That code runs inside your logged-in Discord, so it can see and do everything the app can. This is the base for everything else in this post.

## Quests are just requests

A Quest is a normal object from Discord's API. The app accepts it with `POST /quests/{id}/enroll`, reports progress while you watch or play, and at the end you claim the reward with `POST /quests/{id}/claim-reward`.

The server can't see your screen. It only gets what the app tells it. And what the app can send, another program can send as well.

## Videos

While a Quest video plays, the app sends a request every few seconds with the second you are at:

```
POST /quests/{id}/video-progress
{ "timestamp": 42.0 }
```

There is nothing more to it. No proof that a video played or that someone watched it. So you send these requests yourself and count up. The only limit is that the time can't run faster than real time, so you can't jump straight to the end. You still wait as long as the video is, but you don't have to look at it.

## Streams

Stream Quests want you to share your screen in a call for a while. The app proves that with a heartbeat to `/quests/{id}/heartbeat` that carries a stream key. If you send that heartbeat regularly, the progress goes up. Nobody has to watch the stream.

## Games

This part was the most interesting for me. A "play for 15 minutes" Quest needs Discord to think the game is running. Discord checks that like this:

1. It loads a list of known games with the names of their executables, like `SomeGame.exe`.
2. It looks at the programs running on your computer and compares their names with that list.
3. If one matches, the game shows up as your activity and the app starts sending playtime to the server.

There are two ways around this.

**A fake program.** You write a tiny program that only opens an empty window. You put it in a folder and name it exactly like the game's executable. Discord sees `SomeGame.exe` running and is happy. It does not check if the file is the real 80 GB game or a few hundred KB of nothing.

**Changing Discord from the inside.** With CDP you can reach Discord's internal code. The web app is bundled with webpack, and with this small trick you get access to all its modules:

```js
const req = webpackChunkdiscord_app.push([[Symbol()], {}, r => r]);
webpackChunkdiscord_app.pop();
```

In those modules there is one called `RunningGameStore`. It answers the question "which games are running right now". You replace its `getRunningGames()` function with one that also returns the game from the Quest, and send a `RUNNING_GAMES_CHANGE` event so the app notices. After that Discord does the rest by itself. It shows the game as your activity and sends the playtime. No file, no download. When the Quest is done you put the original function back, otherwise Discord thinks you are playing that game forever.

## Why this works

Everything that is checked on your own computer is under your control. Is the video playing, is this really the game, is someone watching. Discord can't verify any of that. The server can only look at what arrives: if the timing makes sense, and if the account and the pattern look like a real person. That is where Discord can fight back, and that's why this keeps changing all the time.

Never trust the client. And if your app runs on Electron, expect that someone will open the DevTools.
