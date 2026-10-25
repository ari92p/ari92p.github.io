---
title: DisplayVolumeKeys
key: display-volume-keys
order: 4
logo: Volume
logo_class: plate
summary: A small Mac menu bar app that makes the volume keys control your external monitor's speakers.
note: macOS on Apple silicon. Swift. MIT license.
permalink: /projects/display-volume-keys/
award_left: "Menu<br>bar app"
award_right: "Open<br>source"
features:
  - icon: laptop
    text: macOS
  - icon: chip
    text: Apple silicon
  - icon: code
    text: Swift
  - icon: monitorspeaker
    text: DDC/CI
---
<div class="pj-row">
<figure class="figl"><img src="/static/img/projects/display-volume-keys/about.png" width="260" alt="The About window of DisplayVolumeKeys with the app icon, version and status lines" height="268"><figcaption>The About window shows what the app sees.</figcaption></figure>
<p class="it">When a Mac sends sound to an external monitor, the volume keys usually stop working. macOS shows a crossed-out speaker, and the volume can only be changed with the buttons on the monitor. This app fixes that.</p>
<p><b>DisplayVolumeKeys:</b> it sends volume up, volume down and mute to the display over DDC/CI, the same channel the monitor's own menu uses. It does only this one job, needs no settings and runs entirely on your Mac.</p>
<p>It becomes active only while the external display is the chosen sound output. Otherwise the keys work as usual. It never changes your sound output, and it finds the display by itself. Holding a key speeds up the change, up to four steps at a time.</p>
<p>The app starts at login, which you can turn off in its menu. Its monitor icon is dimmed while it leaves the keys to macOS.</p>
</div>

<figure class="hero clear"><img src="/static/img/projects/display-volume-keys/menu.png" width="420" alt="The DisplayVolumeKeys menu in the macOS menu bar" height="196"><figcaption>The menu: Launch at Login, About, Quit.</figcaption></figure>

<h2 class="hd">Install</h2>
<div class="codebox">brew install --cask ari92p/tap/display-volume-keys</div>
<div class="boxrow stepsrow">
<fieldset class="tbox"><legend>Open</legend>Start DisplayVolumeKeys from the Applications folder.</fieldset>
<fieldset class="tbox"><legend>Allow</legend>Allow it under System Settings, Privacy and Security, Accessibility, so it can receive the volume keys.</fieldset>
<fieldset class="tbox"><legend>Done</legend>A monitor icon appears in the menu bar. The permission stays in place across updates.</fieldset>
</div>
<p>The command also installs the small helper <code>m1ddc</code>, which talks to the display. The app is signed with my own certificate but not notarized by Apple, which needs a paid developer account. The Homebrew cask therefore removes the download quarantine, so macOS does not block the first start.</p>

<div class="specs clear">
<fieldset class="spec"><legend>You need</legend>A Mac with<br>Apple silicon<br>A monitor with DDC/CI<br>Accessibility permission</fieldset>
<img class="appicon" style="float:none;width:78px;height:78px" src="/static/img/projects/display-volume-keys/icon.png" alt="DisplayVolumeKeys app icon" width="1024" height="1024">
<fieldset class="spec"><legend>Update</legend>brew upgrade --cask<br>display-volume-keys<br>&nbsp;<br>&nbsp;</fieldset>
</div>

<p class="avail">Source code and downloads<br><a class="phone" href="https://github.com/ari92p/display-volume-keys" target="_blank" rel="noopener noreferrer">github.com/ari92p/display-volume-keys</a></p>
