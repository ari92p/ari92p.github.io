---
title: MoonDock
key: moondock
order: 6
logo: MoonDock
logo_class: fire
summary: A small Mac menu bar companion for Moonlight game streaming.
note: macOS. Swift. MIT license.
permalink: /projects/moondock/
award_left: "Menu<br>bar app"
award_right: "Open<br>source"
features:
  - icon: laptop
    text: macOS
  - icon: computer
    text: Menu bar app
  - icon: network
    text: Game streaming
  - icon: license
    text: MIT license
---
<div class="pj-row">
<img class="appicon" style="width:120px;height:120px" src="/static/img/projects/moondock/icon.png" alt="MoonDock app icon" width="256" height="256">
<p class="it">Moonlight streams a game from your gaming PC to your Mac. It has no menu bar presence, no way to end a stream without quitting, and no help with the display. MoonDock adds the missing pieces.</p>
<p><b>MoonDock</b> is a small menu bar app that sits next to Moonlight. It opens and raises the Moonlight window, can end a running stream without quitting Moonlight, and offers a menu to switch an external 4K, 120-Hz display between native 4K and HiDPI modes.</p>
<p>It does not bundle, patch or configure Moonlight or Sunshine, and the source contains no host names, credentials or pairing data. The interface comes in English and German and follows the macOS system language.</p>
</div>

<div class="boxrow">
<fieldset class="tbox"><legend>Open Moonlight</legend>Opens or raises the main window. During a stream it raises the stream instead, without disconnecting.</fieldset>
<fieldset class="tbox"><legend>End Stream</legend>Enabled only while a stream runs. Closes the local stream and reopens Moonlight's main window.</fieldset>
<fieldset class="tbox"><legend>Mac Resolution</legend>Lists the 120-Hz modes of your main display, from 2560 &times; 1440 HiDPI to native 3840 &times; 2160.</fieldset>
</div>

<p class="pull">Option + Command + Tab hides Moonlight and returns to your previous Mac app, even while a stream captures the keyboard.</p>

<div class="pj-row">
<p>Closing Moonlight itself leaves MoonDock in the menu bar, so you can reopen Moonlight from there. Quitting MoonDock closes Moonlight and restores the display mode that was active at the start, but only if you changed it from the menu. Starting MoonDock never changes the display mode. Display changes are app-only, so macOS reverts them if MoonDock crashes.</p>
</div>

<h2 class="hd">Build and install</h2>
<div class="codebox">./scripts/build.sh
./scripts/install.sh
open /Applications/MoonDock.app</div>
<p>MoonDock is built from source with the Xcode Command Line Tools. The shortcut needs the Accessibility permission. macOS ties that permission to the signature of the app, so a build signed with a stable identity from your keychain keeps it across updates. The README explains how.</p>

<div class="specs clear">
<fieldset class="spec"><legend>You need</legend>macOS 13 or later<br>Moonlight installed<br>Xcode Command<br>Line Tools</fieldset>
<img class="appicon" style="float:none;width:78px;height:78px" src="/static/img/projects/moondock/icon.png" alt="MoonDock app icon" width="256" height="256">
<fieldset class="spec"><legend>For resolutions</legend>An external main<br>display with 4K<br>modes at 120 Hz<br>&nbsp;</fieldset>
</div>

<div class="pj-row clear">
<div class="demo-box"><b>Optional mouse helper</b><div class="ph s">Mouse</div></div>
<p>A small per-user helper pauses Logi Options+ while Moonlight runs and restarts it afterwards. That frees the mouse side buttons for the stream, but also pauses all other Options+ features during that time. Install it only if you want that.</p>
</div>

<p class="avail">Source code<br><a class="phone" href="https://github.com/ari92p/MoonDock" target="_blank" rel="noopener noreferrer">github.com/ari92p/MoonDock</a></p>
