#!/usr/bin/env python3
"""Play pre-rendered speech samples from ../preset_speech/, with optional HALO effect."""

from math import gcd
from pathlib import Path

import numpy as np
import sounddevice as sd
from scipy.io import wavfile
from scipy.signal import resample_poly

VOICES = [
    ("af_heart",  "American female"),
    ("am_adam",   "American male"),
    ("bf_emma",   "British female"),
    ("bm_george", "British male"),
]

PRESETS = [
    "HALO is an audible effect that makes synthetic speech easily identifiable, yet still clear.",
    "You can apply HALO to real-time synthetic speech, or prerendered audio clips.",
    "Consider using HALO whenever you are rendering AI-generated speech.",
]

SPEECH_DIR = Path(__file__).parent.parent / "preset_speech"
_TARGET_SR  = int(sd.query_devices(kind='output')['default_samplerate'])


def apply_halo(audio: np.ndarray, sr: int,
               delay_s: float = 0.025, amp: float = 1.0) -> np.ndarray:
    d = int(sr * delay_s)
    echo = np.zeros_like(audio)
    echo[d:] = audio[:-d] * amp
    return (audio + echo).astype(audio.dtype)


def play(audio: np.ndarray, sr: int) -> None:
    if sr != _TARGET_SR:
        g = gcd(sr, _TARGET_SR)
        audio = resample_poly(audio, _TARGET_SR // g, sr // g).astype(np.float32)
        sr = _TARGET_SR
    peak = np.max(np.abs(audio))
    if peak > 1.0:
        audio = audio / peak
    sd.play(audio, sr)
    sd.wait()


def main() -> None:
    print("Preset speech player")
    print("--------------------\n")

    while True:
        # Voice
        print("Voices:")
        for i, (v, label) in enumerate(VOICES, 1):
            print(f"  {i}. {label}  ({v})")
        print("  Q. quit")
        raw = input("\nVoice [1]: ").strip() or "1"
        if raw.lower().startswith("q"):
            break
        if not raw.isdigit() or not (1 <= int(raw) <= len(VOICES)):
            print("Invalid choice.\n")
            continue
        voice = VOICES[int(raw) - 1][0]

        # Preset
        print("\nPresets:")
        for i, text in enumerate(PRESETS, 1):
            print(f"  {i}. {text}")
        raw = input("\nPreset [1]: ").strip() or "1"
        if not raw.isdigit() or not (1 <= int(raw) <= len(PRESETS)):
            print("Invalid choice.\n")
            continue
        n = int(raw)

        # HALO
        raw = input("Apply HALO effect [Y/n]: ").strip().lower() or "y"
        use_halo = raw.startswith("y")

        # Load and play
        path = SPEECH_DIR / f"{voice}_{n:02d}.wav"
        if not path.exists():
            print(f"File not found: {path}\n"
                  "Run python_kokoro/render_presets.py first.\n")
            continue

        sr, audio = wavfile.read(path)
        audio = audio.astype(np.float32)

        if use_halo:
            audio = apply_halo(audio, sr)

        print(f"\nPlaying: {voice}, preset {n}"
              f"{' + HALO' if use_halo else ''}\n")
        play(audio, sr)

        print()


if __name__ == "__main__":
    main()
