#!/usr/bin/env python3
import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

"""Render the first three preset messages in four voices to WAV files.

Output goes to ../preset_speech/, one file per voice+message combination.
File names: {voice}_{n:02d}.wav  (e.g. af_heart_01.wav)
"""

from pathlib import Path
from scipy.io import wavfile

from speak import _load_model, PRESETS

VOICES = [
    "af_heart",   # American female
    "am_adam",    # American male
    "bf_emma",    # British female
    "bm_george",  # British male
]

SPEED    = 1.2
MESSAGES = PRESETS[:3]

OUT_DIR = Path(__file__).parent.parent / "preset_speech"
OUT_DIR.mkdir(exist_ok=True)

def main() -> None:
    print("Loading model...")
    kokoro = _load_model()
    print(f"Rendering {len(VOICES)} voices × {len(MESSAGES)} messages "
          f"→ {OUT_DIR}\n")

    for voice in VOICES:
        for i, text in enumerate(MESSAGES, 1):
            label = f"{voice}_{i:02d}"
            preview = text[:60] + ("…" if len(text) > 60 else "")
            print(f'  {label}  "{preview}"')
            audio, sr = kokoro.create(text, voice=voice, speed=SPEED, lang="en-us")
            peak = max(abs(audio).max(), 1e-6)
            if peak > 1.0:
                audio = audio / peak
            wavfile.write(OUT_DIR / f"{label}.wav", sr, audio)

    print(f"\nDone. {len(VOICES) * len(MESSAGES)} files written to {OUT_DIR}")


if __name__ == "__main__":
    main()
