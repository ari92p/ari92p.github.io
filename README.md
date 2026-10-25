# ari92p web site

Jekyll site for GitHub Pages. You write Markdown, GitHub builds the HTML.

## Folders

| Folder | What is in it |
| --- | --- |
| `content/` | All your writing as Markdown: `_posts`, `_projects`, `_library`, `_inventory`, `_games` |
| `pages/` | The pages themselves: start page, project list, library, inventory, games, 404 (their addresses are set with `permalink:`) |
| `_layouts/` | The shared frame of every page: menu, black bar, footer |
| `static/` | Everything the browser loads: `css/`, `js/`, `fonts/`, `img/`, `favicons/`, `audio/` |
| `_tools/` | Scripts that draw the buttons and icons, and the project template (not part of the site) |

In the site root only the files that have to be there remain: `_config.yml`, `Gemfile`, `favicon.ico` and this README.

## Sections

| Button | What it is | Where to edit |
| --- | --- | --- |
| NEWS | The blog. The start page shows every post, newest first. | `content/_posts/YYYY-MM-DD-title.md` |
| PROJECTS | Overview list of everything I built. Each project has its own page in the style of the old product pages. | one file per project in `content/_projects/` (template: `_tools/project-template.md`) |
| LIBRARY | Tabs: What's on my mac, Useful stuff. | one file per tab in `content/_library/` |
| INVENTORY | Things you own: gaming PC, NAS, peripherals, settings. Grouped by `category`. | one file per item in `content/_inventory/` |
| GAMES | What I am playing now and what I am trying out. | one file per game in `content/_games/` |

## Edit

- **New post:** file in `content/_posts/` with `title:` and `date:` in the front matter, then Markdown. To link a post to a project add `projects: [homelab]` (the `key:` of the project). The post then shows a "Project" label, and the project page lists it under "Posts about this project".
- **New Library tab:** file in `content/_library/` with `title:`, `tab:` (used in the URL, for example `#tools`) and `order:`.
- **New game:** file in `content/_games/`:

      ---
      title: Valheim
      status: playing      # playing = "Current Rotation", trying = "Trying out"
      order: 4
      store: steam         # steam or battlenet: picks the icon and name of the button
      link: "https://..."  # the Steam or Battle.net page the button opens
      image: /static/img/games/valheim.jpg   # optional, adds a picture column
      ---
      A line or two about the game (optional).

- **New Inventory item:** file in `content/_inventory/` with `title:`, `category:` (items with the same category are grouped), `order:`, `status:` and optional `links:`.
- **Links in the black bar:** `_config.yml` (`github_url`, `discord_url`, `pixiv_url`, `twitter_url`). Leave `pixiv_url` empty until the account exists.
- **Profile photo:** `static/img/profile.jpg`. **Background:** `static/img/background.jpg`, enabled in `static/css/theme.css`.
- **Menu buttons and arrow:** pixel images in `static/img/`, drawn by `_tools/make_buttons.py`.
- **Music player:** put `.mp3` or `.ogg` files in `static/audio/` and run `python3 _tools/make_playlist.py`. The player (`static/js/player.js`) plays them in a fixed random order, starts by itself when the page opens (or on the first tap, if the browser blocks sound) and continues at the same spot after every page change. Page changes happen without a reload (`static/js/nav.js` swaps the page content), so the music keeps playing between pages. A browser refresh still stops it for a moment.
- **Look of every page:** `_layouts/default.html` and `static/css/style.css`.

## Pictures that are not there yet

Gray placeholder boxes (class `ph`) in the project pages are hidden by `static/css/style.css`, together with the frames and the gallery that only hold placeholders. To show a picture, replace the `<div class="ph …">…</div>` in the page by an `<img>` tag. The frame appears again by itself. Inventory and Games rows only get a photo column when the item has an `image:` line.

## Fonts, icons and meta tags

- **Fonts** are served from `static/fonts/` (latin subsets, SIL Open Font License), declared in `static/css/fonts.css`. Visitors never connect to Google.
- **Favicon** and touch icon: `favicon.ico` in the site root, the PNG versions in `static/favicons/`.
- **Meta description and link previews** come from `description:` in a page's front matter, else from the project summary or the first paragraph of a post, else from `_config.yml`.

## Preview locally (optional)

    export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
    bundle install
    bundle exec jekyll serve

Then open http://localhost:4000. On a Mac with Ruby 2.6 the Gemfile pins an older
github-pages release; GitHub builds with its own current version.
