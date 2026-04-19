#!/usr/bin/env python3
import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")  # prevent libomp/libiomp5 dual-runtime crash

"""Kokoro TTS demo with echo effect.

Run:
    pip install -r requirements.txt
    python speak.py

Model files (~300 MB total) are downloaded automatically on first run
to ~/.cache/kokoro-onnx/ and reused on subsequent runs.
"""

import urllib.request
from pathlib import Path

from math import gcd

import numpy as np
import sounddevice as sd
from scipy.signal import resample_poly

# On some platforms, the built-in sound device resamples poorly, causing                     
# crackling when there is a mismatch between the STT sample rate and the                            
# output sample rate.  We work around this by looking up the output sample
# rate, and resampling smoothly with scipy.
_TARGET_SR = int(sd.query_devices(kind='output')['default_samplerate'])
print(f"Output sample rate: {_TARGET_SR}")

# ---------------------------------------------------------------------------
# Voices
# ---------------------------------------------------------------------------

VOICES = [
    # American female
    "af_heart", "af_bella", "af_nicole", "af_sarah", "af_sky",
    # American male
    "am_adam", "am_michael",
    # British female
    "bf_emma", "bf_isabella",
    # British male
    "bm_george", "bm_lewis",
]

DEFAULT_VOICE = "bf_emma"
DEFAULT_SPEED = 1.2

# ---------------------------------------------------------------------------
# Preset messages
# ---------------------------------------------------------------------------

PRESETS = [
    "HALO is an audible effect that makes synthetic speech easily identifiable, yet still clear.",
    "You can apply HALO to real-time synthetic speech, or prerendered audio clips.",
    "Consider using HALO whenever you are rendering AI-generated speech.",
    "It was the best of times, it was the worst of times.",
    "In a hole in the ground there lived a hobbit.",
    "The answer to life, the universe, and everything, is... forty-two.",
]

# ---------------------------------------------------------------------------
# Model download
# ---------------------------------------------------------------------------

_CACHE      = Path.home() / ".cache" / "kokoro-onnx"
_MODEL_URL  = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
_VOICES_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"


def _download(url: str, dest: Path) -> None:
    print(f"  Downloading {dest.name}...", end=" ", flush=True)
    urllib.request.urlretrieve(url, dest)
    print("done.")


def _load_model():
    _CACHE.mkdir(parents=True, exist_ok=True)
    model_path  = _CACHE / "kokoro-v1.0.onnx"
    voices_path = _CACHE / "voices-v1.0.bin"
    if not model_path.exists():
        _download(_MODEL_URL, model_path)
    if not voices_path.exists():
        _download(_VOICES_URL, voices_path)
    from kokoro_onnx import Kokoro
    return Kokoro(str(model_path), str(voices_path))

# ---------------------------------------------------------------------------
# Audio effect
# ---------------------------------------------------------------------------

def applyHaloEffect(audio: np.ndarray, sample_rate: int,
          delay_s: float = 0.025, amp: float = 1.0) -> np.ndarray:
    """Add a single echo (100 % amplitude, 25 ms delay by default)."""
    d = int(sample_rate * delay_s)
    echo = np.zeros_like(audio)
    echo[d:] = audio[:-d] * amp
    return (audio + echo).astype(audio.dtype)

# ---------------------------------------------------------------------------
# Speak
# ---------------------------------------------------------------------------

def speak(kokoro, text: str, voice: str, speed: float,
          delay_s: float, amp: float) -> None:
    audio, sr = kokoro.create(text, voice=voice, speed=speed, lang="en-us")
    if amp > 0:
        audio = applyHaloEffect(audio, sr, delay_s=delay_s, amp=amp)
    if sr != _TARGET_SR and _TARGET_SR > 0:
        g = gcd(sr, _TARGET_SR)
        audio = resample_poly(audio, _TARGET_SR // g, sr // g).astype(np.float32)
        sr = _TARGET_SR
    peak = np.max(np.abs(audio))
    if peak > 1.0:
        audio = audio / peak
    sd.play(audio, sr)
    sd.wait()

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("Kokoro TTS demo")
    print("---------------")
    print("Loading model (first run downloads ~300 MB to ~/.cache/kokoro-onnx/)...")
    kokoro = _load_model()
    print("Model ready.\n")

    # Voice selection
    print("Voices:")
    for i, v in enumerate(VOICES, 1):
        marker = " *" if v == DEFAULT_VOICE else ""
        print(f"  {i:2d}. {v}{marker}")
    raw = input(f"\nVoice number or name [default {DEFAULT_VOICE}]: ").strip()
    if raw.isdigit() and 1 <= int(raw) <= len(VOICES):
        voice = VOICES[int(raw) - 1]
    elif raw in VOICES:
        voice = raw
    else:
        voice = DEFAULT_VOICE
    print(f"Using: {voice}")

    raw = input(f"Speed [default {DEFAULT_SPEED}]: ").strip()
    try:
        speed = float(raw)
    except ValueError:
        speed = DEFAULT_SPEED

    print()

    # Playback loop
    while True:
        print("Preset messages:")
        for i, msg in enumerate(PRESETS, 1):
            print(f"  {i}. {msg}")
        print(f"  {len(PRESETS) + 1}. [Type your own]")
        print("  0. [Quit]")

        raw = input("\nChoice: ").strip()

        if raw == "0":
            break
        elif raw.isdigit() and 1 <= int(raw) <= len(PRESETS):
            text = PRESETS[int(raw) - 1]
        elif raw == str(len(PRESETS) + 1):
            text = input("Text: ").strip()
            if not text:
                continue
        else:
            print("Invalid choice, try again.")
            continue

        raw = input("Halo delay in ms [default 25]: ").strip()
        try:
            delay_s = float(raw) / 1000.0
        except ValueError:
            delay_s = 0.025
    
        raw = input("Halo amplitude 0–1 [default 1.0]: ").strip()
        try:
            amp = float(raw)
        except ValueError:
            amp = 1.0

        print(f"Speaking: {text!r}")
        speak(kokoro, text, voice, speed, delay_s, amp)
        print()


if __name__ == "__main__":
    main()
