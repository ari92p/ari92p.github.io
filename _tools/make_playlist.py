"""Builds static/audio/playlist.json from the files in static/audio/.

Run:  python3 _tools/make_playlist.py
Add .mp3 or .ogg files to static/audio/, run this, commit. The player reads the list.
Stations are picked by file name (see STATIONS); edit the table to rename or regroup them.
"""
import json, os, re

AUDIO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "audio")

# (station name, pattern matched against the lower-case file name), first match wins
STATIONS = [
    ("Elwynn Forest", r"forest"),
    ("Westfall", r"westfall"),
    ("Stormwind", r"stormwind"),
    ("Taverns and inns", r"tavern|resta?rea"),
    ("More music", r".*"),
]

def title(name):
    base = os.path.splitext(name)[0]
    base = re.sub(r"^(MUS_\d+_|MUS_|RA_)", "", base)
    base = base.replace("_", " ").replace("-", " ")
    base = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", base)
    base = re.sub(r"(?<=[A-Za-z])(?=\d)", " ", base)
    base = re.sub(r"\b(GU|UU)\b", "", base)
    base = re.sub(r"\s+", " ", base).strip()
    base = re.sub(r"\b0+(\d)", r"\1", base)
    base = base.replace("Canticleof", "Canticle of")
    return base[:1].upper() + base[1:]

def natural(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

files = sorted((f for f in os.listdir(AUDIO) if f.lower().endswith((".mp3", ".ogg"))), key=natural)
out = []
for name, pat in STATIONS:
    picked = [f for f in files if re.search(pat, f.lower())]
    files = [f for f in files if f not in picked]
    if picked:
        out.append({"name": name, "tracks": [{"file": f, "title": title(f)} for f in picked]})
with open(os.path.join(AUDIO, "playlist.json"), "w") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
print("ok:", ", ".join("%s (%d)" % (s["name"], len(s["tracks"])) for s in out))
