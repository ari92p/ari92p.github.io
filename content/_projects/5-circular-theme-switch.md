---
title: Circular Theme Switch
key: circular-theme-switch
order: 5
logo: Theme
logo_class: ice
summary: A dark and light theme switch that expands in a circle from the click. No dependencies.
note: JavaScript for websites and apps. MIT license.
permalink: /projects/circular-theme-switch/
award_left: "Zero<br>dependencies"
features:
  - icon: code
    text: JavaScript
  - icon: layers
    text: Vue and React
  - icon: license
    text: MIT license
  - icon: eye
    text: Accessible
---
<figure class="hero"><img src="/static/img/projects/circular-theme-switch/demo.gif" width="600" alt="A website and an app switching between dark and light with a circle that grows from the click" height="338"><figcaption>A website and an embedded app, each with its own switch.</figcaption></figure>

<p class="pull">Switching between dark and light is usually a flash. Here the new theme grows out of the spot you clicked.</p>

<p><b>Circular Theme Switch</b> is a small library with no runtime dependencies. The circle takes 500 ms in both directions. When you press the button with the keyboard, the circle starts at the center of the button.</p>

<h2 class="hd">Style the two themes</h2>
<p>You style your themes with the classes <code>.dark</code> and <code>.light</code> on the root element:</p>
<div class="codebox">:root.dark  { color-scheme: dark;  background: #191b19; color: #eeeee7; }
:root.light { color-scheme: light; background: #faf8f1; color: #292d26; }</div>

<div class="boxrow">
<fieldset class="tbox"><legend>Keyboard</legend>A click from the keyboard starts the circle at the center of the button.</fieldset>
<fieldset class="tbox"><legend>Reduced motion</legend>With a reduced-motion setting, and in browsers that do not support the effect, the theme switches instantly.</fieldset>
<fieldset class="tbox"><legend>Guides</legend>The repository has guides for Vue and React and a reference for the API.</fieldset>
</div>

<div class="pj-row clear">
<div class="demo-box"><b>Try the live demo</b><div class="ph s">Demo</div></div>
<p>See it in action on the <a href="https://ari92p.github.io/circular-theme-switch/demo/" target="_blank" rel="noopener noreferrer">demo page</a>. The website and the embedded app there have independent switches.</p>
</div>

<p class="avail">Source code and guides<br><a class="phone" href="https://github.com/ari92p/circular-theme-switch" target="_blank" rel="noopener noreferrer">github.com/ari92p/circular-theme-switch</a></p>
