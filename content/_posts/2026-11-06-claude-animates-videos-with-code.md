---
title: How Claude makes animated videos with code
date: 2026-11-06 09:00:00
---
A video is just a lot of pictures per second. If every picture is computed from a number, the frame number, then a video is a function: give it frame 0, frame 1, frame 2 and it draws each one. That is the whole trick behind letting Claude make videos. Claude can't drag clips around in an editor, but it is very good at writing functions. This post shows how that works, how a full video comes together from a single idea, and how you can build the same thing at home.

## Video as code

The tool for this is [Remotion](https://www.remotion.dev/). It lets you write a video as a React component. React draws a web page; Remotion draws that page once per frame, takes a screenshot of each one and gives the frames to ffmpeg. You get an MP4.

The smallest useful example:

{% raw %}
```tsx
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from "remotion";

export const Hello = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // 0 -> 1 with a little bounce, starting at frame 15
  const pop = spring({frame: frame - 15, fps, config: {damping: 10}});
  // fade in over the first half second
  const fade = interpolate(frame, [0, fps / 2], [0, 1], {extrapolateRight: "clamp"});

  return (
    <AbsoluteFill style={{background: "#102030", alignItems: "center", justifyContent: "center"}}>
      <div style={{opacity: fade, transform: `scale(${pop})`, color: "white", fontSize: 120}}>
        Hello
      </div>
    </AbsoluteFill>
  );
};
```
{% endraw %}

Nothing in it moves on its own. The word "Hello" has a size and an opacity that are calculated from the frame number. That has two big advantages for an AI:

- **It is text.** Claude reads and writes it like any other code, and can fix a bug in an animation the same way it fixes one in a website.
- **It is deterministic.** Frame 87 always looks the same. If something is wrong at 2.9 seconds, Claude can render exactly that frame, look at it and correct it.

## The pipeline from idea to MP4

Here is how a short explainer video is made, step by step. Claude runs all the steps from the terminal with Claude Code.

1. **Script.** Claude researches the topic, checks the facts, and writes a short script, one sentence per line.
2. **Voice.** A local text-to-speech model reads the script (see the [voice cloning post](/blog/ai-voices-with-tts-and-voice-cloning/)). A second model, Whisper, writes down every spoken word with its start and end time. This gives a file `words.json`.
3. **Pictures.** Backdrops, characters and props are generated with image models in ComfyUI on a GPU PC, then cut out from their background so they can be layered.
4. **Scene list.** Claude writes a JSON file that describes the video: which picture, which animation, and *when*.
5. **Render.** Remotion turns the scene list into frames and an MP4. A script checks duration, loudness and sudden jumps.
6. **Look at it.** Claude renders a contact sheet, a grid of frames from the video, and looks at every one of them before anyone else sees the result.

## The key idea: tie animation to words

The most useful part is step 4. Instead of writing "show the speech bubble at 7.4 seconds", the scene list says "show it when the word *mics* is spoken":

```json
{
  "kind": "bubble",
  "text": "TINY MICS",
  "at": { "w": "mics" },
  "tail": "left"
}
```

The engine looks up *mics* in `words.json` and gets the time. If the voice is regenerated and is half a second slower, everything still lands on the right word. With a fixed time in seconds, every re-recording would break the whole video.

In code, this is only a lookup from word to frame:

```ts
type Word = {word: string; start: number; end: number};

export const frameOf = (words: Word[], target: string, fps: number, n = 1) => {
  const hits = words.filter(
    (w) => w.word.toLowerCase().replace(/[^a-z0-9']/g, "") === target.toLowerCase()
  );
  const hit = hits[n - 1];
  if (!hit) throw new Error(`word not found: ${target}`); // fail loudly, never guess
  return Math.round(hit.start * fps);
};
```

If a word doesn't exist, the render stops with an error. A silent fallback would produce a video where something shows at the wrong moment, and nobody would notice until it is online.

## Building blocks instead of one-off code

At first Claude wrote every video as a hand-made component. That looks great, but each video is a lot of work. Now the videos are made from reusable blocks, and the scene list only chooses and combines them:

| Block | What it does |
| --- | --- |
| `backdrop` | Background with slow zoom and blur |
| `closeup`, `figure` | A character, with pose changes and a little squash when the pose switches |
| `bubble` | Speech or sound bubble |
| `chips` | Labels that pop up one after the other |
| `prop` | An object that falls, slides or spins into the frame |
| `counter` | A number that counts up |
| `card` | Small explainer animations: waves cancelling out, a lock being picked, steps with arrows |

The quality of a video is the size of this library. If a video needs something that doesn't exist yet, Claude builds the new block once, tests it, and every later video can use it.

## Where the pictures come from

All pictures are generated locally with [ComfyUI](https://github.com/comfyanonymous/ComfyUI) on your own GPU. ComfyUI is a node-based image tool, but it also has an HTTP API, and that is what makes it usable for Claude: a script sends a workflow as JSON and gets a PNG back.

Two models are enough, for two jobs:

| Model | Used for | Speed (1024 px) |
| --- | --- | ---: |
| Qwen-Image 2.1 (edit) | Characters in new poses, objects in the same style as a reference picture | 25 to 40 s |
| Krea 2 Turbo | Fresh pictures from text: backdrops, props, style LoRAs | about 8 s |

### Keeping a character the same

The hard part of AI images is not one good picture, it is the same character in forty pictures. What works:

1. **One hero image.** The character is created once and approved by a human. It is never overwritten.
2. **Always edit the hero.** Every new pose is an *edit* of the hero picture, with the hero as `<image1>` in the prompt. Never use the last generated picture as input. Faces drift a little with every generation, and after ten copies it is a different person.
3. **A fixed style block.** The same paragraph is pasted into every prompt:

```
Draw the person from <image1> in a new pose. Waist-up close-up, facing the viewer.
She rests one finger on her chin and looks up thoughtfully.
Keep exactly the same person, face, hair, beanie, clothes, proportions and cozy
chibi comic drawing style as <image1> (thick smooth dark brown-black outlines,
simple solid black oval dot eyes, warm muted earthy colours, soft subtle shading).
Only this one person, nobody else. Plain flat cream background (#FBF5E9),
nothing else, no text, no frame.
```

4. **A new random seed for every edit.** If you edit with the same seed that made the input picture, the model repeats its own noise and returns an over-sharpened copy.
5. **Don't guess in descriptions.** If the character description says "elf" and the picture shows no elf, that wrong word is sent with every prompt and bends the face.

Backdrops and props use the same trick with a *style reference*: the logo picture is `<image1>`, and the prompt says "draw a new picture in exactly the drawing style of image 1, no people". That keeps everything in one look.

### Flat background, then cut out

Every character and prop is generated on a plain flat colour, never inside a scene. A background-removal model (BiRefNet, as a ComfyUI node) makes a mask from it, and the mask becomes the alpha channel of the PNG. Two small cleanups matter:

- Semi-transparent edge pixels still contain the old background colour and give a light fringe. A script removes the background colour from them.
- Close-ups are cropped at the bottom so that the figure sits flush on the lower edge of the video, instead of floating above it.

Cut-outs are the reason the animation looks alive: the character, a speech bubble and a falling object are separate layers that Remotion can move on their own.

### Jobs as a JSON file

Claude doesn't click in the ComfyUI interface. It writes a list of jobs, and a script runs them:

```json
{
  "out": "assets/characters/raw",
  "jobs": [
    {
      "name": "she_close_curious",
      "engine": "qwen",
      "size": [1024, 1024],
      "seeds": [3001, 3002],
      "prompt": "Draw the person from <image1> in a new pose ...",
      "refs": ["assets/hero/she_hero.png"]
    }
  ]
}
```

Each seed becomes one picture (`she_close_curious_s3001.png`), and existing files are skipped. The seeds are in the file name, so a good picture can be reproduced later. Poses that turn out well go into a library, so the next video doesn't need to generate them again.

### The same thing in plain Python

You can do the same with a few lines of Python. In ComfyUI open your workflow and use *Save (API Format)* (you may need to enable dev mode options in the settings). Then:

```python
import json, random, time, urllib.request, uuid

BASE = "http://127.0.0.1:8188"

def post(path, data):
    req = urllib.request.Request(BASE + path, json.dumps(data).encode(),
                                 {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))

workflow = json.load(open("workflow_api.json"))
workflow["6"]["inputs"]["text"] = "a cozy kitchen, no people, flat colours"   # your prompt node id
workflow["3"]["inputs"]["seed"] = random.randint(0, 2**32)                     # your sampler node id

prompt_id = post("/prompt", {"prompt": workflow, "client_id": str(uuid.uuid4())})["prompt_id"]

while True:                                    # wait until the job is done
    history = json.load(urllib.request.urlopen(f"{BASE}/history/{prompt_id}"))
    if prompt_id in history:
        break
    time.sleep(1)

for node in history[prompt_id]["outputs"].values():
    for img in node.get("images", []):
        url = f"{BASE}/view?filename={img['filename']}&subfolder={img['subfolder']}&type={img['type']}"
        open(img["filename"], "wb").write(urllib.request.urlopen(url).read())
```

The numbers `"6"` and `"3"` are the node ids in your own exported file. Open it and look for the text and seed inputs. If ComfyUI runs on another machine, forward its port with SSH (`ssh -L 8188:127.0.0.1:8188 pc`), so you don't have to expose it to your network.

Once this works, Claude can take over: tell it where the script is and what the workflow file expects, and it writes the job files and checks the results.

## Checking what is on screen

Claude can't "see" a video as it plays, but it can look at single frames. After every render it makes a grid of frames, one every 1.5 seconds, and reads it like a storyboard. That found a lot of mistakes that code alone can't see:

- a card that is empty for a second,
- text that is cut off at the edge,
- an overlay on a screen that is shifted because the drawing has a bit of perspective,
- a car that stops *behind* an object instead of in front of it.

The fix for the overlay one is worth knowing: **measure instead of guess.** Where something has to sit exactly on a part of a picture, a small script measures the four corners of the real screen and the animation uses those numbers. Claude guessing "about 62% from the left" is wrong too often.

## Try it yourself

You don't need a GPU PC for a first video. You need Node.js and Claude Code.

**1. Create a project**

```bash
npx create-video@latest
```

Pick the blank template. Then start the preview:

```bash
npm run dev
```

**2. Ask Claude for a first scene.** Open the folder in Claude Code and describe what you want, as concrete as possible: format (1080x1920 for vertical, 1920x1080 for horizontal), duration, colours, and what happens in what order. For example: "A 10 second vertical video. Dark blue background. The text 'How does noise cancelling work?' bounces in, then two sine waves slide in from the sides, and when they overlap they flatten to a straight line."

**3. Render a single frame to check it**

```bash
npx remotion still src/index.ts Hello out/frame.png --frame=90
```

Give the PNG back to Claude and tell it what is wrong. This loop (render a frame, look, fix) is faster than rendering the full video.

**4. Render the video**

```bash
npx remotion render src/index.ts Hello out/hello.mp4
```

**5. Add a voice.** Generate the speech with a local TTS model, run Whisper over it with `word_timestamps=True`, and put the word list next to your code. Use the `frameOf` function above and tie each animation to a word. Add the audio with `<Audio src={staticFile("vo.wav")} />`.

**6. Add pictures.** Install ComfyUI, load any image model, and use the script from the section above. Ask for a flat colour background behind the object, remove it, and place the cut-outs in the `public` folder of your Remotion project. Show them with `<Img src={staticFile("cutout.png")} />`. Layered cut-outs are what make the animation feel alive, because you can move them separately.

No GPU? Use the tools you have for the pictures (any image generator, or free vector graphics) and let Remotion draw the rest. Shapes, text, charts and waves are plain SVG and need no images at all.

## Tips that save time

- **Describe timing with words, not seconds.** It is the only way to make later changes cheap.
- **Fail loudly.** A missing word or image should stop the render.
- **Don't let images be cropped by the video.** Scale a picture to the frame size instead of using `cover`. Otherwise measured positions are wrong.
- **Change something every 4 to 6 seconds.** A new picture, a new camera position, a new card. Long static shots feel dead.
- **Put your rules in a file.** Claude Code reads a `CLAUDE.md` in the project folder. Style rules ("no glow around overlays", "never crop backdrops") go there, so you only explain a mistake once.

## What Claude is good at here, and what not

It is very good at the structure: composing scenes, writing the animation maths, keeping a library of blocks, building the checks around it. It needs a human for taste. Is the voice natural? Is a joke funny? Is the colour right? So the working loop is that Claude produces, looks at what it made and fixes the obvious, and you decide whether it is good.
