# HALO (Human Audible Label of Origin)

_An audible watermark for synthetic speech_

## The Problem: Synthetic voices are now indistinguishable from human

Speech synthesis and natural language processing have both gotten so good in recent years, that it can be very difficult to know when you are listening or even speaking with an AI rather than a real human.

In some contexts, that may be fine.  But in many cases, knowing whether an entity is a human or an AI is very useful.  We can no longer rely on the quality of the speech to make this distinction.

## The Solution: HALO

HALO is a simple audio transformation that can be applied to synthetic speech, whether it's rendered in real-time by a text-to-speech (TTS) system, or pre-rendered sound files.

The HALO algorithm is simple: **Add a second copy of the audio stream, delayed by 25 milliseconds.**  This gives the speech a simple "reverb" quality that is easy to recognize, but does not make the speech any harder to understand.  In fact you may find the effect rather pleasant.

## Try it now!

This repo has demonstration code to apply the HALO effect, either to live (TTS) speech, or to prerendered speech clips, in a variety of languages:

| Demo | Description |
|------|-------------|
| [python_kokoro](python_kokoro/) | Interactive Python demo: type any text, choose a voice, hear it spoken with or without HALO. Uses the Kokoro TTS engine. |
| [python_preset](python_preset/) | Python demo using pre-rendered WAV files. No TTS library required — pick a voice, pick a preset, toggle HALO. |
| [js_preset](js_preset/) | Browser-based demo. Same voice/preset/HALO controls, implemented with the Web Audio API. **[Try it live](https://JoeStrout.github.io/HALO/js_preset/)** |
| [unity_preset](unity_preset/) | Unity demo. Same controls in a self-contained C# script; HALO applied via Unity's built-in `AudioEchoFilter`. |
