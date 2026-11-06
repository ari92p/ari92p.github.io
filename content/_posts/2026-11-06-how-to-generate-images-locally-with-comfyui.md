---
title: How to generate images locally with ComfyUI
date: 2026-11-06 08:30:00
---
You can generate images on your own computer, without a subscription, without a cloud service and without anyone else seeing your prompts. The tool for it is [ComfyUI](https://github.com/comfyanonymous/ComfyUI). This post shows how to install it, make a first image, understand what the files and settings mean, keep a character consistent over many pictures, cut objects out of their background, and finally control all of it from a script.

## What ComfyUI is

ComfyUI is a graph editor for image models. Instead of one text box and a button, you see boxes (nodes) connected by wires: load a model, encode the prompt, sample, decode, save. It looks complicated at first, but it has two big advantages:

- **You see what happens.** Every step of image generation is a node you can replace or reuse.
- **It has an API.** A workflow is a JSON file, and a program can send it to ComfyUI and get the picture back. That makes it possible to let a script, or Claude, generate hundreds of images.

## What you need

- **A GPU with enough memory.** NVIDIA is the easiest. 8 GB VRAM is enough for smaller models, 16 GB or more is comfortable for current ones. Apple Silicon works too, but is slower.
- **Disk space.** A single model file is 5 to 25 GB. Plan for 100 GB if you want to try several.
- **Python 3.12 or newer** and Git, unless you use the desktop app.

## Install

The simplest way is the official desktop app for Windows and macOS from [comfy.org](https://www.comfy.org/). It installs everything and updates itself.

If you want more control, install it by hand:

```bash
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

Install PyTorch for your GPU first, using the command from [pytorch.org](https://pytorch.org/get-started/locally/) (it differs for NVIDIA, AMD and Apple), then the rest:

```bash
pip install -r requirements.txt
python main.py
```

Open `http://127.0.0.1:8188` in your browser. You should see the graph editor with a default workflow.

## Your first image

1. **Get a model.** Models are single files. Download one from [Hugging Face](https://huggingface.co/) or [Civitai](https://civitai.com/) and put it in the right folder inside `ComfyUI/models/`. The folder depends on the type:

| Folder | Contents |
| --- | --- |
| `checkpoints/` | Complete models in one file (for example SDXL-based models) |
| `diffusion_models/` or `unet/` | The image model alone, for newer models that ship their parts separately |
| `text_encoders/` or `clip/` | The text part of such a model |
| `vae/` | Turns the model's internal picture into pixels |
| `loras/` | Small add-ons for style or characters |

Every model page tells you which files you need and where to put them. Newer models come with a ready-made workflow. In ComfyUI, open the template browser (Workflow → Browse Templates), pick your model and the right nodes appear with the right file names.

2. **Write a prompt.** Click the text box of the prompt node and describe the picture.
3. **Press Run.** The first run takes longer because the model has to be loaded into GPU memory. After that it is much faster.

The picture is saved in `ComfyUI/output/`. The PNG contains the whole workflow, so you can drag any PNG back onto the editor to get the exact setup again.

## The settings that matter

You can ignore most nodes for a long time. These you will touch:

- **Seed.** The random number the picture starts from. Same seed, same prompt, same settings gives the same picture. Change the seed to get a different variation. Keep a good seed in a note.
- **Steps.** How many refinement rounds. More is slower, and past a point it doesn't help. The model page says what is right. Fast "turbo" models use 4 to 8 steps, others 20 to 30.
- **CFG.** How strongly the model follows your prompt. Again the model page tells you: turbo models often want 1, others 4 to 8.
- **Size.** Use the size the model was trained on, usually around 1024 x 1024. Much bigger sizes in one go give repeated limbs and strange composition. Make big pictures in a second step (upscaling).

## Prompts

Two prompt styles exist, depending on the model:

- **Full sentences** (most new models): "A cozy kitchen with a wooden table, warm morning light, flat colours, no people."
- **Tags** (many anime models): `1girl, red scarf, snowy street, looking at viewer`.

Tips that work with both:

- Say what you want, not what you don't. Many models ignore or misread negative wording; "no people" can still produce people. If it fails, describe the empty scene positively ("empty room, only furniture").
- Describe style in the same way every time. A fixed style paragraph that you paste into every prompt is the cheapest way to get pictures that belong together.
- Check the result. Models love to paint faces onto objects and people into empty rooms. Look at every image and generate again with a new seed when needed.

## Styles with LoRAs

A LoRA is a small file (often 50 to 500 MB) that teaches a model a style, a character or a concept. Put it in `models/loras/` and add a *Load LoRA* node between the model and the sampler. Two rules:

- A LoRA only works with the model family it was trained for. A LoRA for SDXL does nothing useful with another architecture.
- Many LoRAs have a trigger word that must be in the prompt. The download page lists it. With several LoRAs at once, start with a strength of about 0.6 each and raise it slowly.

## Editing pictures and keeping a character the same

Text-to-image gives you a new person every time. For the *same* character in many pictures you need a model that can **edit** an image or take a reference image. In ComfyUI you load the picture with a *Load Image* node and connect it to the model's edit node. In the prompt the images are usually called `<image1>`, `<image2>` and so on (check your model's template). What works:

1. **Create one hero image** and keep it. Never overwrite it.
2. **Always edit the hero.** Give the hero as `<image1>` for every new pose. Never feed the last result back in: the face drifts a little with every generation, and after ten rounds it is another person.
3. **Use a fixed style block** at the end of every prompt:

```
Draw the person from <image1> in a new pose. Waist-up close-up, facing the viewer.
She rests one finger on her chin and looks up thoughtfully.
Keep exactly the same person, face, hair, clothes, proportions and drawing style
as <image1>. Only this one person, nobody else. Plain flat cream background,
nothing else, no text, no frame.
```

4. **Use a new seed for every edit.** If you edit with the same seed that created the input picture, many edit models repeat their own noise and return an over-sharpened copy.
5. **Don't guess in your character description.** A wrong word like "elf" for a person without pointed ears is sent with every prompt and bends the face. Describe only what is in the picture.

The same trick works for objects and backgrounds. Give a picture in your target style as `<image1>` and ask for a new object "in exactly the drawing style of image 1".

## Cutting objects out

If you want to animate a picture or put it into a layout, you need the object without its background. Generate it on a **plain flat colour** and never inside a scene. Then remove the background:

- In ComfyUI, a background-removal model such as BiRefNet (available as a custom node) turns the picture into a mask.
- The mask becomes the alpha channel of a PNG. Crop the PNG to its content plus a small margin.
- Semi-transparent edge pixels still contain the old background colour and give a light fringe. Remove the background colour from them in a small script, or look at the result on a dark background before you use it.

## Control ComfyUI from a script

This is where it becomes powerful. In the ComfyUI menu use *Export (API)* (in older versions: *Save (API Format)* after enabling dev mode options in the settings). You get a JSON file with every node and its inputs. A script can load it, change values and send it:

```python
import json, random, time, urllib.request, uuid

BASE = "http://127.0.0.1:8188"

def post(path, data):
    req = urllib.request.Request(BASE + path, json.dumps(data).encode(),
                                 {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))

workflow = json.load(open("workflow_api.json"))
workflow["6"]["inputs"]["text"] = "a cozy kitchen, flat colours, empty room"   # your prompt node id
workflow["3"]["inputs"]["seed"] = random.randint(0, 2**32)                      # your sampler node id

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

The numbers `"6"` and `"3"` are the node ids in your own exported file. Open it and look for the text and seed inputs. To use a reference image, upload it first with `POST /upload/image` (a multipart form with the file) and put the returned file name into the *Load Image* node of the workflow.

### Jobs as a JSON file

Once the script works, put the variable parts into a list of jobs, one entry per picture, with one or more seeds:

```json
{
  "out": "pictures",
  "jobs": [
    {
      "name": "kitchen",
      "prompt": "A cozy kitchen with a wooden table, warm morning light, flat colours, empty room.",
      "seeds": [101, 102, 103],
      "size": [1344, 768]
    }
  ]
}
```

Name the output files after the job and the seed (`kitchen_s101.png`) and skip files that already exist. A good picture can then be reproduced, and a crash in the middle of a batch costs nothing. This is also exactly what you hand to Claude: it writes the job list, runs it, looks at the results and generates again where something went wrong.

## Running ComfyUI on another machine

If your GPU is in a different computer, you don't need to open ComfyUI to your network. Forward the port over SSH and use it as if it were local:

```bash
ssh -N -L 8188:127.0.0.1:8188 user@gpu-pc
```

Now `http://127.0.0.1:8188` on your laptop is the ComfyUI on the GPU machine.

To keep model files in one place, or on another drive, ComfyUI reads an `extra_model_paths.yaml` in its folder. Copy the example `extra_model_paths.yaml.example` and set the paths.

## Problems you will run into

- **Out of memory.** Use a smaller model or a quantized version (files with `fp8` or `Q6`, `Q4` in the name are smaller), lower the size, or start ComfyUI with `--lowvram`.
- **The first picture takes minutes.** The model is loading. The second one is fast.
- **Pictures look burnt or over-sharpened.** Check CFG and steps against the model page, and in edit workflows change the seed.
- **A LoRA does nothing.** Wrong model family, a missing trigger word, or the strength is too low.
- **Faces drift between pictures.** You are editing the last result instead of the hero image.

## Next

With a script that turns a text into a PNG, you can build bigger things on top of it. One of them is animated videos where every picture, voice line and animation is generated or written as code. That is the next post.
