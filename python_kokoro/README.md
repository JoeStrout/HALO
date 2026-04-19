# python_kokoro

A minimal demo of the [Kokoro](https://github.com/thewh1teagle/kokoro-onnx) text-to-speech engine with the **HALO effect** — a short echo that makes synthetic speech audibly identifiable.

## Requirements

- Python 3.9+
- A working audio output device

## Installation

```bash
pip install -r requirements.txt
```

Model files (~300 MB total) are downloaded automatically on first run to `~/.cache/kokoro-onnx/` and reused on subsequent runs.

## Usage

```bash
python speak.py
```

The script will prompt you for:

- **Voice** — choose from 11 English voices (American and British, male and female)
- **Speed** — speech rate multiplier (default 1.2)

Then, for each utterance:

- **Message** — pick a preset or type your own
- **Halo delay** — echo delay in milliseconds (default 25 ms)
- **Halo amplitude** — echo level from 0 to 1 (default 1.0; set to 0 to hear plain TTS)

## Pre-rendering samples

To render the first three preset messages in four voices (American/British × male/female) as WAV files:

```bash
python render_presets.py
```

Output goes to `../preset_speech/`, one file per voice+message combination (e.g. `af_heart_01.wav`).  These renderings are _without_ the HALO effect; they are source files for the preset demos (like python_preset), for those who want to hear the effect without installing a Speech-to-Text library.

## How the HALO effect works

A single delayed copy of the audio is mixed back in at the specified amplitude:

```
output = original + (original shifted by delay) × amplitude
```

This produces a subtle but consistent audible cue that distinguishes AI-generated speech from a human voice, without significantly affecting intelligibility.
