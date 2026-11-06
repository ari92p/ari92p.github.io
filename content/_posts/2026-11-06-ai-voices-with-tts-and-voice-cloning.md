---
title: How AI voice cloning works, and how to run it locally
date: 2026-11-06 08:00:00
---
Modern text-to-speech (TTS) can copy a voice from a few seconds of audio. This post explains how that works inside the model, and then shows a local setup you can run yourself: voice cloning, picking good takes, word timestamps and loudness. Everything runs on your own GPU, nothing goes to a cloud service.

## What voice cloning really is

Old TTS sounded robotic because it glued pre-recorded snippets together or used rules to fake a voice. Modern TTS works like a chatbot:

1. **Audio becomes tokens.** A neural audio codec compresses speech into a stream of small codes, like a chatbot turns text into word pieces. Qwen3-TTS uses about 12 code frames per second of audio.
2. **The model predicts the next code.** A chatbot predicts the next word. The TTS model predicts the next audio code, again and again, based on the text it should speak.
3. **The reference sets the voice.** For cloning you give the model a short clip of the target voice (5 to 15 seconds works best) and a transcript of what is said in it. The model treats the clip as the start of the conversation and continues in the same voice, accent and energy.
4. **A decoder turns codes into sound.** The predicted codes become a normal waveform again.

That is why a few seconds are enough. The model is not trained on the new voice at all. It continues a pattern it was shown.

## What you need

- **Model:** [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base), 1.7B parameters, open weights. The "Base" version is the one that can clone.
- **Hardware:** an NVIDIA GPU. On a current card (RTX 40 or 50 series) one line takes a few seconds.
- **Python packages:** `qwen-tts`, `soundfile`, `torch`, `faster-whisper`.
- **A reference clip:** 5 to 15 seconds of clean speech, one speaker, no music, no echo, saved as WAV, plus the exact text that is said in it.

You can split the work over two machines (for example a laptop that sends jobs over SSH to a GPU PC), but one machine is enough.

## Step 1: Clone a voice and generate speech

```python
import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel

model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cuda:0",
    dtype=torch.bfloat16,
)

# The voice: reference audio + what is said in it
prompt = model.create_voice_clone_prompt(
    ref_audio="ref.wav",
    ref_text="The exact words spoken in ref.wav.",
)

wavs, sr = model.generate_voice_clone(
    text="Hello, this sentence was never recorded by anyone.",
    language="English",
    voice_clone_prompt=prompt,
)
sf.write("take.wav", wavs[0], sr)
```

`create_voice_clone_prompt` is done once per voice. You can reuse the prompt for every line.

## Step 2: Make several takes

Output is random. The same text sounds a bit different each time, like asking an actor for another take. Set a seed per take so you can reproduce a good one:

```python
for k in range(1, 5):
    torch.manual_seed(1000 + k)
    wavs, sr = model.generate_voice_clone(
        text=line, language="English", voice_clone_prompt=prompt
    )
    sf.write(f"line01_t{k}.wav", wavs[0], sr)
```

Two things that helped with quality:

- **Keep one voice in one run.** Generating every line in a separate run made the voice drift from line to line. Loading the model once and reusing the same prompt for all lines of a character keeps it much more consistent.
- **Set a maximum length per take.** Sometimes the model does not stop and keeps generating silence or noise. A hard limit catches that before it burns minutes of GPU time.

## Step 3: Listen with Whisper

A second model, Whisper, transcribes every take and gives each word a start and end time. With that a script can check what was really said:

```python
from faster_whisper import WhisperModel

whisper = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16")
segments, _ = whisper.transcribe("line01_t1.wav", language="en", word_timestamps=True)

words = [
    {"word": w.word.strip(), "start": w.start, "end": w.end}
    for s in segments for w in s.words
]
```

## Step 4: Let a script pick the best take

Compare the transcript of each take with the text you wanted. Normalize both (lowercase, no punctuation) and compare word by word. A take that skips, adds or mangles words gets thrown out. Of the rest, prefer the one with a natural speaking pace (characters per second close to the other takes).

## Problems you will run into

**Statements that sound like questions.** The model sometimes ends a normal sentence with a rising pitch, so "Charge it to a hundred." sounds like "Charge it to a hundred?". It is easy to hear and hard to find in a list of 30 lines, so check it with code. Take the last word of each sentence from the Whisper timestamps and measure how the pitch moves:

```python
import librosa
import numpy as np

def end_pitch_change(path, start, end):
    """Pitch change over a word in semitones. Positive = rising."""
    y, sr = librosa.load(path, sr=16000, offset=start, duration=end - start)
    f0, voiced, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr)
    f0 = f0[voiced]
    if len(f0) < 6:
        return 0.0
    q = max(1, len(f0) // 4)
    return 12 * np.log2(np.median(f0[-q:]) / np.median(f0[:q]))
```

A statement should end falling. If the value is clearly positive, reject the take. If no take gets every sentence right, generate the sentences one by one and join the best pieces with a short pause.

**The voice changing mid-line.** In longer lines with several sentences the tone sometimes shifts halfway. The same pitch measurement helps: compute the median pitch per sentence, and a jump between sentences means the voice changed.

**Numbers in the transcript.** Whisper writes "eighty percent" as "80%" and "sixty dollars" as "$60". If you need subtitles that match your script exactly, take only the timing from Whisper and the words from your own text.

**Wording that tricks the model.** Sentences that end on small words like "...is." tend to rise. Sometimes the best fix is not technical. Rewrite the sentence.

## Step 5: Join and normalize

Join the chosen takes with short pauses, a bit longer between sections. Then bring the track to the usual streaming loudness of -16 LUFS:

```bash
ffmpeg -i voice.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 voice_final.wav
```

Add no EQ and no compression. The voice sounds most natural the way the model delivers it.

## Why the word timestamps are useful

Because every word has a time, you can tie other things to speech: subtitles, animations, or a scene change exactly when a certain word is spoken.

## What it costs

Electricity, nothing else. The model is open, runs locally, and there is no per-minute fee. The real cost is time. Getting from "it talks" to "it sounds right" takes far more work than setting up the model.
