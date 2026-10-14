# TC-214: ElevenLabs MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: elevenlabs/elevenlabs-mcp (official ElevenLabs MCP server)
- **License**: MIT
- **Artifact Type**: Tool Schema (MCP tool definition for the `text_to_speech` tool)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `elevenlabs_mcp/server.py` — the `@mcp.tool(...)` decorator (description + `ToolAnnotations`) and the `text_to_speech` function signature that becomes the input schema
  - PyPI package metadata (`elevenlabs-mcp`) — confirmed MIT

## Original Artifact Content

### Tool decorator, description and typed input signature (`elevenlabs_mcp/server.py`, fetched verbatim)

```python
@mcp.tool(
    annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    description=f"""Convert text to speech with a given voice. {get_output_mode_description(output_mode)}.

    Only one of voice_id or voice_name can be provided. If none are provided, the default voice will be used.

    ⚠️ COST WARNING: This tool makes an API call to ElevenLabs which may incur costs. Only use when explicitly requested by the user.

    Args:
        text (str): The text to convert to speech.
        voice_name (str, optional): The name of the voice to use.
        model_id (str, optional): The model ID to use for speech synthesis. Options include:
            - eleven_v3: High quality model with most expressive voices
            - eleven_multilingual_v2: High quality multilingual model (29 languages)
            - eleven_flash_v2_5: Fastest model with ultra-low latency (32 languages)
            - eleven_turbo_v2_5: Balanced quality and speed (32 languages)
            - eleven_flash_v2: Fast English-only model
            - eleven_turbo_v2: Balanced English-only model
            Defaults to eleven_multilingual_v2 or environment variable ELEVENLABS_MODEL_ID.
        stability (float, optional): Stability of the generated audio. Determines how stable the voice is and the randomness between each generation. Lower values introduce broader emotional range for the voice. Higher values can result in a monotonous voice with limited emotion. Range is 0 to 1.
        similarity_boost (float, optional): Similarity boost of the generated audio. Determines how closely the AI should adhere to the original voice when attempting to replicate it. Range is 0 to 1.
        style (float, optional): Style of the generated audio. Determines the style exaggeration of the voice. This setting attempts to amplify the style of the original speaker. It does consume additional computational resources and might increase latency if set to anything other than 0. Range is 0 to 1.
        use_speaker_boost (bool, optional): Use speaker boost of the generated audio. This setting boosts the similarity to the original speaker. Using this setting requires a slightly higher computational load, which in turn increases latency.
        speed (float, optional): Speed of the generated audio. Controls the speed of the generated speech. Values range from 0.7 to 1.2, with 1.0 being the default speed. Lower values create slower, more deliberate speech while higher values produce faster-paced speech. Extreme values can impact the quality of the generated speech. Range is 0.7 to 1.2.
        output_directory (str, optional): Directory where files should be saved (only used when saving files).
        Defaults to $HOME/Desktop if not provided.
        language: ISO 639-1 language code for the voice.
        output_format (str, optional): Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.
        Defaults to "mp3_44100_128". Must be one of:
        mp3_22050_32
        mp3_44100_32
        mp3_44100_64
        mp3_44100_96
        mp3_44100_128
        mp3_44100_192
        pcm_8000
        pcm_16000
        pcm_22050
        pcm_24000
        pcm_44100
        ulaw_8000
        alaw_8000
        opus_48000_32
        opus_48000_64
        opus_48000_96
        opus_48000_128
        opus_48000_192

    Returns:
        Text content with file path or MCP resource with audio data, depending on output mode.
    """,
)
def text_to_speech(
    text: str,
    voice_name: str | None = None,
    output_directory: str | None = None,
    voice_id: str | None = None,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    style: float = 0,
    use_speaker_boost: bool = True,
    speed: float = 1.0,
    language: str = "en",
    output_format: str = "mp3_44100_128",
    model_id: str | None = None,
) -> Union[TextContent, EmbeddedResource]:
    if text == "":
        make_error("Text is required.")

    if voice_id is not None and voice_name is not None:
        make_error("voice_id and voice_name cannot both be provided.")

    voice = None
    if voice_id is not None:
        voice = client.voices.get(voice_id=voice_id)
    elif voice_name is not None:
        voices = client.voices.search(search=voice_name)
        if len(voices.voices) == 0:
            make_error("No voices found with that name.")
        voice = next((v for v in voices.voices if v.name == voice_name), None)
        if voice is None:
            make_error(f"Voice with name: {voice_name} does not exist.")

    voice_id = voice.voice_id if voice else DEFAULT_VOICE_ID
```

(The function body continues in `server.py` with output-path resolution, the ElevenLabs API call, and output-mode handling; that portion does not affect the tool surface quoted above.)

Server bootstrap for the same file (fetched verbatim):

```python
mcp = FastMCP("ElevenLabs")
```

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] The description states the capability ("Convert text to speech with a given voice")
- [ ] It flags the cost/risk ("⚠️ COST WARNING ... Only use when explicitly requested by the user")
- [ ] It documents the mutual-exclusion rule ("Only one of voice_id or voice_name can be provided")
- [ ] It documents the return shape ("Text content with file path or MCP resource with audio data")

### 2. Schema Correctness
- [ ] The input schema is derived from the typed Python signature, so parameter names and types are explicit
- [ ] Required vs optional is clear from defaults (`text` has none; all others have defaults)
- [ ] Defaults are declared in the signature (`stability=0.5`, `similarity_boost=0.75`, `style=0`, `use_speaker_boost=True`, `speed=1.0`, `language="en"`, `output_format="mp3_44100_128"`)

### 3. Parameter Description Quality
- [ ] Numeric ranges are documented inline (`stability`/`similarity_boost`/`style` 0–1; `speed` 0.7–1.2)
- [ ] `model_id` enumerates allowed models and its default source (env var `ELEVENLABS_MODEL_ID`)
- [ ] `output_format` enumerates all accepted codec strings and notes plan/tier requirements

### 4. Integration Compatibility
- [ ] Built with FastMCP (`mcp.tool(...)`); the signature and docstring become the MCP tool schema
- [ ] Declares `ToolAnnotations(readOnlyHint=True, openWorldHint=True)` for client-side risk display
- [ ] Returns `TextContent` or `EmbeddedResource`, matching MCP content types

### 5. Extensibility & Maintainability
- [ ] The API key and base path come from environment variables (`ELEVENLABS_API_KEY`, `ELEVENLABS_MCP_BASE_PATH`), keeping the tool surface credential-free
- [ ] Output mode (`files`/`resources`/`both`) is configurable and injected into the description
- [ ] Multiple related tools (`speech_to_text`, `text_to_sound_effects`, voice/music tools) share the same file and conventions

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 30% | | |
| Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Integration Compatibility | 15% | | |
| Extensibility & Maintainability | 10% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "read this paragraph aloud in a warm voice"; verify `text_to_speech` is called with `text` (and optionally `voice_name`).
2. Issue "generate an MP3 at 44.1kHz"; verify `output_format: "mp3_44100_128"` (the default) or another valid codec string.
3. Issue "say this faster"; verify `speed` is set within 0.7–1.2.

### Boundary Test Cases
1. `stability`/`similarity_boost`/`style` at 0 and 1; `speed` at 0.7 and 1.2.
2. `text` exactly clamped at the documented behaviour for very large inputs (`handle_large_text` path).
3. `voice_id` provided while `voice_name` omitted, and vice versa.
4. `output_format` set to a valid but plan-gated value (e.g. `mp3_44100_192`); verify the documented tier requirement surfaces.

### Negative Test Cases
1. Empty `text`; verify the tool errors with "Text is required."
2. Both `voice_id` and `voice_name` provided; verify the mutual-exclusion error.
3. `output_format: "wav_44100"` (unsupported); verify it is rejected/handled rather than silently defaulted.
4. A request that only reads existing data (e.g. list voices); verify the model does not trigger a paid speech call.

## Notes
- This case quotes one logical artifact — the `text_to_speech` MCP tool — verbatim from the official ElevenLabs MCP server. The input schema is generated from the typed function signature and the docstring is the tool description.
- A trailing portion of the function body (audio conversion and output handling) is not quoted; it does not affect the tool surface.
- Anthropic-era styling: the description embeds usage guidance, tier warnings and cost caveats directly in the tool text, which doubles as a model-facing affordance.
- License is MIT, so verbatim quotation is permissible.
