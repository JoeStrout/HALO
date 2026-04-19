# js_preset

A browser-based HALO demo. Pick a voice and preset, toggle the HALO effect on or off, and click Play to hear the difference.

## Requirements

Pre-rendered WAV files in `../preset_speech/`. If that directory is empty, run:

```bash
cd ../python_kokoro
python render_presets.py
```

## Usage

Browsers block `fetch()` on `file://` URLs, so the page must be served over HTTP. From the HALO root directory:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/js_preset/` in any browser.

## How it works

The HALO effect is applied in real time via the Web Audio API: a delayed copy of the decoded audio buffer is mixed back in at the configured amplitude, using a `DelayNode` and `GainNode`. A `DynamicsCompressorNode` acts as a limiter to prevent clipping when the echo pushes peaks above 1.0.
