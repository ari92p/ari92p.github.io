---
title: A DNS filter with its own resolver
date: 2026-10-21 09:00:00
projects: [homelab]
---
My home network filters ads and trackers with Pi-hole. By default Pi-hole asks a public DNS server for everything it does not block. I wanted to cut out that third party, so I run my own resolver, Unbound, in a container next to it.

Pi-hole now asks only Unbound, and Unbound talks to the internet itself and checks the answers for forgery. It lives in a small private network that nothing else can reach.

There was one trap. My first idea was to let the resolver share Pi-hole's network connection. It works until Pi-hole restarts: the resolver then stays attached to the old connection, and DNS fails without any error message. A separate private network fixed it for good.

The block lists cover about 278,000 domains. When an app stops working, the query log shows what was blocked, and one command lets it through again.

**Lesson:** shared network connections between containers break quietly after a restart. Give them a network of their own.
