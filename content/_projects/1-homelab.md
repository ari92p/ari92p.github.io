---
title: My Homelab
key: homelab
order: 1
logo: Homelab
logo_class: gold
summary: A four-bay NAS at home that runs around thirty self-hosted containers.
note: Photos, media, a DNS filter and daily backups. Technical notes are on the page.
permalink: /projects/homelab/
award_left: "Always<br>on"
award_right: "Self<br>hosted"
features:
  - icon: boxes
    text: Docker
  - icon: network
    text: Private access
  - icon: disk
    text: Backups
  - icon: monitoring
    text: Monitoring
---
<div class="pj-row">
<div class="pj-img l"><div class="ph tall">The NAS</div></div>
<p class="it">A quiet box at home that keeps my photos, my media and a few services I would rather not hand to anyone else. It runs around the clock and mostly looks after itself.</p>
</div>

<div class="pj-row">
<div class="pj-img r"><div class="ph tall">The services</div></div>
<p class="it">It started small and grew one container at a time. Every change got a backup first, and most of what I know about networks I learned from things that broke.</p>
</div>

<div class="pj-row">
<div class="pj-img l big"><div class="ph tall2">Dashboard</div></div>
<p><b>My Homelab:</b> around thirty containers run on a four-bay NAS. There is a photo library that keeps a copy of my phone pictures, a media server with tools that sort the library, a password manager, a DNS filter that blocks ads for the whole house, and a dashboard that ties everything together.</p>
<p>Access from outside goes through a private VPN only. Updates and monitoring run on their own, and when something looks wrong a message arrives on my phone.</p>
<p>Backups go to two places every morning. All the heavy background work runs in one block, so the hard drive can sleep for the rest of the day.</p>
</div>

<div class="pj-row clear">
<div class="demo-box"><b>Read the technical notes</b><div class="ph s">Icon</div></div>
<p>What runs where and what to watch out for is further down under <a href="#notes">Technical notes</a>. The mistakes I made on the way are in the <a href="/index.html">news</a>: backups that ran twice a day, a fan warning for a fan that does not exist, and a router that insisted a name did not exist.</p>
</div>

<div class="pj-row clear">
<div class="pj-img l"><div class="ph tall">Photo</div></div>
<ul class="pj-list">
<li>Photos and media stay in my own house</li>
<li>Ads and trackers are filtered for every device at home</li>
<li>Backups every morning to two places</li>
<li>Alerts on my phone when a service or a drive has a problem</li>
</ul>
</div>

<p class="gal-t clear">Image gallery</p>
<div class="gal">
<figure><div class="ph">Image 1</div><figcaption>The NAS</figcaption></figure>
<figure><div class="ph">Image 2</div><figcaption>The dashboard</figcaption></figure>
<figure><div class="ph">Image 3</div><figcaption>The network</figcaption></figure>
<figure><div class="ph">Image 4</div><figcaption>The backups</figcaption></figure>
</div>

<div class="specs clear">
<fieldset class="spec"><legend>Runs on</legend>4-bay NAS<br>2x 12 TB hard drive<br>NVMe for containers<br>Always on</fieldset>
<div class="ph box">NAS</div>
<fieldset class="spec"><legend>Access</legend>Private VPN only<br>Login on every service<br>Backups every morning<br>Alerts by message</fieldset>
</div>

<h2 class="hd clear" id="notes">Technical notes</h2>

- **Hardware:** one four-bay NAS. Two 12 TB hard drive holds the data, an NVMe drive holds the containers. Always on.
- **Software:** 30 Docker containers in 16 small projects. 27 run all the time, 3 are stopped on purpose.
- **Access:** only through a private VPN. Every service has a login.
- **Backups:** every morning to a USB drive, and the photo library additionally to an SSD. A daily check sends me a message if a backup is too old or a disk is too full.
- **Updates:** most containers update themselves. A few important ones, the DNS filter and the password manager among them, I update by hand after reading the release notes.

<h3 class="sub">Everything that runs on it</h3>

Here is every container, grouped by what it does. Each one lives in its own small Docker Compose project, so I can change one without touching the rest.

**The front door and the network**

- [Caddy](https://caddyserver.com/) is the front door. Every service has its own address, and Caddy passes each request on to the right container. It fetches and renews the HTTPS certificates by itself, using one wildcard certificate that it proves through DNS.
- [Tailscale](https://tailscale.com/) is the private VPN I use to reach everything from outside. My phone and my Mac join it, and then every service answers as if I were at home.
- [Pi-hole](https://pi-hole.net/) is the DNS filter for the whole house. It blocks about 280,000 ad and tracker domains and gives my services their short names inside the home network.
- [Unbound](https://nlnetlabs.nl/projects/unbound/about/) is Pi-hole's own resolver. It asks the internet itself instead of a public DNS server and checks that the answers are genuine.
- [Gluetun](https://github.com/qdm12/gluetun) is a VPN client in a container that other containers can be attached to. It is stopped right now and waits for the day I need it.

**Photos**

- [Immich](https://immich.app/) is the photo library. It keeps a copy of my iCloud photos at home, with a web page and a phone app.

**Movies and series**

- [Jellyfin](https://jellyfin.org/) and [Plex](https://www.plex.tv/) are the two media servers. Both serve the same library of movies and series.
- [Sonarr](https://sonarr.tv/) looks after the series and [Radarr](https://radarr.video/) after the movies. They watch for new releases and keep the files in order.
- [Prowlarr](https://prowlarr.com/) manages the sources for both, so I set them up once.
- [SABnzbd](https://sabnzbd.org/) is the download client that fetches what Sonarr and Radarr ask for. It is paused every night from midnight to nine so the hard drive can sleep.
- [Bazarr](https://www.bazarr.media/) fetches subtitles for what is in the library.
- [Seerr](https://github.com/seerr-team/seerr) is a request page where people can ask for a movie or series.
- [Recyclarr](https://recyclarr.dev/) keeps the quality settings of Sonarr and Radarr in sync with a config file, so a fresh install gets the same rules.

**Backups and passwords**

- [Kopia](https://kopia.io/) makes an encrypted snapshot of all container data every morning at 09:00 onto a USB drive.
- A second Kopia container has its own repository on the SSD. It saves the original photos and the database dumps of the photo library every morning at 09:10.
- [Vaultwarden](https://github.com/dani-garcia/vaultwarden) is my password manager, a server that speaks the Bitwarden protocol. It also gets its own consistent copy of the database every morning, with an integrity check.

**Watching and updating**

- [Beszel](https://beszel.dev/) shows load, temperature and drive health. It sends me a message when the agent is gone for five minutes, a disk is more than 85 percent full, the temperature stays above 75 degrees, or a container turns unhealthy.
- The Beszel agent runs next to it on the NAS and reports the numbers, including the SMART data of the drives.
- [Dozzle](https://dozzle.dev/) reads the logs of every container in the browser. It is read-only and behind a login.
- [Diun](https://crazymax.dev/diun/) tells me when there is a new version of the four images I update by hand: the DNS filter, the VPN, the password manager and the photo database.
- [Watchtower](https://github.com/nicholas-fedor/watchtower) updates the containers I marked for automatic updates every morning at 09:45 and sends a message when something changed.
- The dashboard is my own: a small web page served by nginx, plus a helper that rebuilds its tiles from the front-door configuration, so a new service shows up after one click on refresh.

**Everything else**

- [Valheim](https://www.valheimgame.com/) has a dedicated game server container. It is stopped until someone plays.

**Scripts that are not containers**

- A daily check at 11:00 sends me a message when a backup is older than 26 hours or has an error, or when a disk is too full (SSD 85 percent, hard drive 90 percent, USB drive 85 percent).
- Alerts from Beszel, Watchtower and Diun all arrive as messages on my phone.

**A day in the homelab**

All times are local.

- **00:00 to 09:00:** quiet. The download client is paused and the hard drive can sleep.
- **09:00:** backups of the container data and of the password database.
- **09:10:** backup of the photo originals to the SSD.
- **09:15 and 09:30:** the photo library scans its files and runs its nightly jobs.
- **09:40 and 09:45:** the version report, then the container updates.
- **10:00 to 12:00:** the maintenance window of Plex. Jellyfin does its housekeeping between 10:15 and 10:50.
- **11:00:** the backup check.
- **Sunday 04:30:** Pi-hole refreshes its block lists.
