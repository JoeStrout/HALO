using System.Collections;
using UnityEngine;

/// Attach to any GameObject in an empty scene to run the HALO preset demo.
/// WAV files must be in Assets/Resources/preset_speech/{voice}_{n:D2}.wav
[RequireComponent(typeof(AudioSource))]
public class HaloDemo : MonoBehaviour
{
    static readonly string[] Voices = { "af_heart", "am_adam", "bf_emma", "bm_george" };
    static readonly string[] VoiceLabels = {
        "American female (af_heart)", "American male (am_adam)",
        "British female (bf_emma)",   "British male (bm_george)",
    };
    static readonly string[] Presets = {
        "HALO is an audible effect that makes synthetic speech easily identifiable, yet still clear.",
        "You can apply HALO to real-time synthetic speech, or prerendered audio clips.",
        "Consider using HALO whenever you are rendering AI-generated speech.",
    };

    const float HaloDelayMs = 25f;

    AudioSource     _src;
    AudioEchoFilter _echo;
    int             _voiceIdx  = 2;    // bf_emma, matching the other demos
    int             _presetIdx = 0;
    bool            _haloOn    = true;
    string          _status    = "";

    bool      _stylesReady;
    GUIStyle  _boxStyle, _headerStyle, _subtitleStyle, _sectionLabelStyle,
              _radioStyle, _toggleStyle, _btnStyle, _bodyStyle;

    void Start()
    {
        _src  = GetComponent<AudioSource>();
        _echo = gameObject.AddComponent<AudioEchoFilter>();
        _echo.delay      = HaloDelayMs;
        _echo.decayRatio = 0f;   // single echo, no feedback repetitions
        _echo.dryMix     = 1f;
        _echo.wetMix     = 0f;
    }

    // ── Playback ──────────────────────────────────────────────────────────────

    void Play()
    {
        var path = $"preset_speech/{Voices[_voiceIdx]}_{_presetIdx + 1:D2}";
        var clip = Resources.Load<AudioClip>(path);
        if (clip == null)
        {
            _status = $"Not found: Assets/Resources/{path}.wav — copy files and reimport.";
            return;
        }
        _echo.wetMix = _haloOn ? 1f : 0f;
        _src.clip    = clip;
        _src.Play();
        _status = $"Playing {Voices[_voiceIdx]}, preset {_presetIdx + 1}{(_haloOn ? " + HALO" : "")}";
        StartCoroutine(ClearStatusWhenDone());
    }

    IEnumerator ClearStatusWhenDone()
    {
        yield return new WaitWhile(() => _src.isPlaying);
        _status = "";
    }

    // ── IMGUI ─────────────────────────────────────────────────────────────────

    void OnGUI()
    {
        EnsureStyles();

        const float W = 500f, H = 490f;
        var rect = new Rect((Screen.width - W) * 0.5f, (Screen.height - H) * 0.5f, W, H);
        GUI.Box(rect, GUIContent.none, _boxStyle);
        GUILayout.BeginArea(new Rect(rect.x + 24, rect.y + 24, W - 48, H - 48));

        GUILayout.Label("HALO", _headerStyle);
        GUILayout.Label("An audible watermark for synthetic speech", _subtitleStyle);
        GUILayout.Space(14);

        GUILayout.Label("VOICE", _sectionLabelStyle);
        for (int i = 0; i < Voices.Length; i++)
            if (GUILayout.Toggle(_voiceIdx == i, VoiceLabels[i], _radioStyle))
                _voiceIdx = i;
        GUILayout.Space(12);

        GUILayout.Label("PRESET", _sectionLabelStyle);
        for (int i = 0; i < Presets.Length; i++)
        {
            var snippet = Presets[i].Length > 55 ? Presets[i][..55] + "…" : Presets[i];
            if (GUILayout.Toggle(_presetIdx == i, $"{i + 1}. {snippet}", _radioStyle))
                _presetIdx = i;
        }
        GUILayout.Space(4);
        GUILayout.Label(Presets[_presetIdx], _bodyStyle);
        GUILayout.Space(12);

        _haloOn = GUILayout.Toggle(_haloOn, "Apply HALO effect", _toggleStyle);
        GUILayout.Space(14);

        GUI.enabled = !_src.isPlaying;
        if (GUILayout.Button("▶  Play", _btnStyle, GUILayout.Height(42)))
            Play();
        GUI.enabled = true;

        GUILayout.Space(6);
        if (!string.IsNullOrEmpty(_status))
            GUILayout.Label(_status, _bodyStyle);

        GUILayout.EndArea();
    }

    // ── Style helpers ─────────────────────────────────────────────────────────

    void EnsureStyles()
    {
        if (_stylesReady) return;
        _stylesReady = true;

        var light  = new Color(0.87f, 0.87f, 0.87f);
        var dim    = new Color(0.53f, 0.53f, 0.53f);
        var accent = new Color(0.914f, 0.271f, 0.376f);

        _boxStyle = new GUIStyle { normal = { background = Solid(new Color(0.086f, 0.129f, 0.243f)) } };

        _headerStyle = new GUIStyle(GUI.skin.label) { fontSize = 24, fontStyle = FontStyle.Bold };
        _headerStyle.normal.textColor = accent;

        _subtitleStyle = new GUIStyle(GUI.skin.label) { fontSize = 13 };
        _subtitleStyle.normal.textColor = dim;

        _sectionLabelStyle = new GUIStyle(GUI.skin.label) { fontSize = 11, fontStyle = FontStyle.Bold };
        _sectionLabelStyle.normal.textColor = new Color(0.67f, 0.67f, 0.67f);

        _radioStyle = new GUIStyle(GUI.skin.toggle) { fontSize = 13 };
        _radioStyle.normal.textColor   = light;
        _radioStyle.onNormal.textColor = light;

        _toggleStyle = new GUIStyle(GUI.skin.toggle) { fontSize = 14 };
        _toggleStyle.normal.textColor   = light;
        _toggleStyle.onNormal.textColor = light;

        _btnStyle = new GUIStyle(GUI.skin.button) { fontSize = 16, fontStyle = FontStyle.Bold };
        _btnStyle.normal.background  = Solid(accent);
        _btnStyle.normal.textColor   = Color.white;
        _btnStyle.hover.background   = Solid(new Color(0.78f, 0.21f, 0.32f));
        _btnStyle.hover.textColor    = Color.white;
        _btnStyle.active.background  = Solid(new Color(0.65f, 0.18f, 0.27f));
        _btnStyle.active.textColor   = Color.white;
        _btnStyle.disabled.background = Solid(new Color(0.33f, 0.33f, 0.33f));
        _btnStyle.disabled.textColor  = new Color(0.6f, 0.6f, 0.6f);

        _bodyStyle = new GUIStyle(GUI.skin.label) { fontSize = 13, fontStyle = FontStyle.Italic, wordWrap = true };
        _bodyStyle.normal.textColor = new Color(0.73f, 0.73f, 0.73f);
    }

    static Texture2D Solid(Color c)
    {
        var t = new Texture2D(1, 1);
        t.SetPixel(0, 0, c);
        t.Apply();
        return t;
    }
}
