# unity_preset

A Unity demo of the HALO effect. Pick a voice and preset, toggle HALO on or off, and click Play.

The UI is built with Unity's immediate-mode GUI (IMGUI), so the scene requires no manual UI setup — just an empty GameObject with the script attached.

## Requirements

- Unity 2022.3 LTS (or later)

## Setup

**1. Open the project in Unity Hub** — add the `unity_preset/` folder as an existing project.

**2. Set up the scene:**

- Open the default scene (or create a new empty one).
- In the Hierarchy, create an empty GameObject (GameObject → Create Empty).
- In the Inspector, click Add Component → search for `HaloDemo` and add it.

**3. Press Play.**

## How it works

The HALO effect is applied using Unity's built-in `AudioEchoFilter`:

| Parameter    | Value | Purpose                          |
|--------------|-------|----------------------------------|
| `delay`      | 25 ms | Echo offset                      |
| `decayRatio` | 0     | Single echo only (no repetitions)|
| `dryMix`     | 1.0   | Original signal at full volume   |
| `wetMix`     | 1.0 / 0 | Echo on (HALO) or off          |

Audio clips are loaded at runtime from `Assets/Resources/preset_speech/` using `Resources.Load<AudioClip>()`.

