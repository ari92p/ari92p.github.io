---
title: This Site
key: this-site
order: 7
logo: ari92p
logo_class: script
summary: A web site in the style of 1996, written in Markdown.
note: Jekyll on GitHub Pages, no framework.
permalink: /projects/this-site/
award_left: "Hand-<br>written"
award_right: "No<br>cookies"
features:
  - icon: markdown
    text: Markdown
  - icon: code
    text: Jekyll
  - icon: globe
    text: GitHub Pages
  - icon: shield
    text: No tracking
---
<figure class="hero"><img src="/static/img/projects/this-site/home.jpg" width="620" height="394" alt="The start page of this site: a black menu bar on the left, a white column with the news in the middle"><figcaption>The start page: black bar on the left, white column in the middle.</figcaption></figure>

<div class="cols2">
<div>
<p class="it">I wanted a place that is mine, without an algorithm, ads or sign-up. So I built it the way the web looked in 1996, modeled on an old Blizzard page I found in the Web Design Museum.</p>
<p><b>This Site</b> is a small Jekyll project that GitHub Pages builds by itself. Every page is a Markdown file: news posts, projects, the library tabs, the inventory and the games each have their own folder, and a new entry is just a new file with a few lines of front matter. There is no framework and nothing to install in the browser.</p>
<p>The menu buttons, the red arrow and the small feature icons are drawn pixel by pixel by short Python scripts without any libraries, and they are shown without smoothing so every pixel stays a hard square. The headings use fonts that are stored on this site, so no request goes to a font service.</p>
</div>
<div>
<fieldset class="tbox"><legend>Privacy</legend>No cookies, no trackers, no analytics. The page only remembers your layout choice and a small visit counter in your browser, and both stay on your computer.</fieldset>
<fieldset class="tbox"><legend>Source</legend>The whole site is public on <a href="https://github.com/ari92p/ari92p.github.io">GitHub</a>, including the scripts that draw the buttons.</fieldset>
</div>
</div>

<div class="shots">
<figure class="shot"><img src="/static/img/projects/this-site/games.jpg" alt="The Games page with a cover image, the title and a note for every game" loading="lazy" width="1100" height="760"><figcaption>Games: what I am playing right now.</figcaption></figure>
<figure class="shot"><img src="/static/img/projects/this-site/inventory.jpg" alt="The Inventory page, grouped by category" loading="lazy" width="1100" height="760"><figcaption>Inventory: the hardware I use, grouped by category.</figcaption></figure>
</div>

<ul class="pj-list">
<li>News with sorting and pages, and a project label on each post</li>
<li>Switch between a centered and a left-aligned layout</li>
<li>A custom mouse pointer, and a different one over links to other sites</li>
<li>Works without JavaScript, it only adds sorting and the layout switch</li>
<li>Skip link, readable contrast and short page titles for screen readers</li>
</ul>
