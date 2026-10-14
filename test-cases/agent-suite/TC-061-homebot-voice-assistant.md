# TC-061: Homebot - Voice-Driven Home Assistant (Skills Loader & Smart-Home Skills)

## Metadata
- **Source Project**: homebot (ysyisyourbrother/homebot)
- **GitHub**: github.com/ysyisyourbrother/homebot
- **License**: MIT
- **Artifact Type**: Voice-driven personal AI agent for home automation — agent skills loader + smart-home skills
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub raw-content fetch on branch `main` — `https://raw.githubusercontent.com/ysyisyourbrother/homebot/main/homebot/agent/skills.py`, `https://raw.githubusercontent.com/ysyisyourbrother/homebot/main/docs/skills/mijia.md`, `https://raw.githubusercontent.com/ysyisyourbrother/homebot/main/docs/skills/weather.md`, `https://raw.githubusercontent.com/ysyisyourbrother/homebot/main/README.md`; the `docs/skills/` directory listing was read from `https://github.com/ysyisyourbrother/homebot/tree/main/docs/skills`
- **Scope**: The skills subsystem — how SKILL.md files are discovered, gated and loaded (`homebot/agent/skills.py`) — plus the documented smart-home skills (mijia, weather) that the voice assistant exposes

---

## Project Overview

Homebot is a locally deployable personal AI agent designed for practical home automation. It connects conversational AI with everyday household tools while keeping the system lightweight, extensible and easy to customize. It is described in an accompanying technical report, *"Homebot: A Personal AI Agent for Conversational Home Assistance and Automation"*, and runs on Python 3.11 or later.

### Key Characteristics
- **Natural voice interaction** with custom wake words, speaker verification, streaming speech recognition and text-to-speech
- **Multi-channel conversations** through Feishu, Telegram and local voice input, running in parallel with one shared Agent
- **Smart-home skills**: controlling Xiaomi Mi Home devices, playing music, checking weather, searching Xiaohongshu
- **Local-first deployment** on an existing computer, with a modular architecture for personal customization
- **SKILL.md-based skills**: skills are Markdown manifests with YAML frontmatter, loaded from a workspace directory or the built-in skills directory
- **Platform-aware**: a skill can declare `platforms:` so an OS-specific skill is invisible on other platforms

---

## Agent Prompts

### 1. Skills Loader (`homebot/agent/skills.py`)

The skills loader is the runtime that turns `SKILL.md` files into model-visible capabilities. It operates over two roots — a per-workspace directory and a built-in directory:

```python
"""Skills loader for agent capabilities."""
...
# Default builtin skills directory (relative to this file)
BUILTIN_SKILLS_DIR = Path(__file__).parent.parent / "skills"

class SkillsLoader:
    """
    Loader for agent skills.
    Skills are markdown files (SKILL.md) that teach the agent how to use
    specific tools or perform certain tasks.
    """
    def __init__(self, workspace: Path, builtin_skills_dir: Path | None = None, disabled_skills: set[str] | None = None):
        self.workspace = workspace
        self.workspace_skills = workspace / "skills"
        self.builtin_skills = builtin_skills_dir or BUILTIN_SKILLS_DIR
        self.disabled_skills = disabled_skills or set()
```

Discovery is directory-based: skills live in a folder named for the skill, each containing a `SKILL.md`, and workspace skills shadow built-in skills of the same name:

```python
    def list_skills(self, filter_unavailable: bool = True) -> list[dict[str, str]]:
        skills = self._skill_entries_from_dir(self.workspace_skills, "workspace")
        workspace_names = {entry["name"] for entry in skills}
        if self.builtin_skills and self.builtin_skills.exists():
            skills.extend(
                self._skill_entries_from_dir(self.builtin_skills, "builtin", skip_names=workspace_names)
            )
        if self.disabled_skills:
            skills = [s for s in skills if s["name"] not in self.disabled_skills]
        # Platform gating happens for every caller (not just the availability
        # filter): a skill that only works on one OS is not "unavailable", it
        # simply does not exist here.
        skills = [
            skill for skill in skills if self._platform_matches(self._get_skill_meta(skill["name"]))
        ]
        if filter_unavailable:
            return [skill for skill in skills if self._check_requirements(self._get_skill_meta(skill["name"]))]
        return skills
```

Skills are progressively loaded rather than dumped into context. `build_skills_summary` emits a one-line index (name, description, path, availability) so the agent can decide what to read in full later:

```python
    def build_skills_summary(self, exclude: set[str] | None = None) -> str:
        """
        Build a summary of all skills (name, description, path, availability).
        This is used for progressive loading - the agent can read the full
        skill content using read_file when needed.
        """
        ...
            if available:
                lines.append(f"- **{skill_name}** — {desc}  `{entry['path']}`")
            else:
                missing = self._get_missing_requirements(meta)
                suffix = f" (unavailable: {missing})" if missing else " (unavailable)"
                lines.append(f"- **{skill_name}** — {desc}{suffix}  `{entry['path']}`")
```

Requirements gating is declarative: a skill's frontmatter can list required binaries and environment variables, and the loader reports exactly what is missing:

```python
    def _check_requirements(self, skill_meta: dict) -> bool:
        """Check if skill requirements are met (bins, env vars)."""
        requires = skill_meta.get("requires", {})
        required_bins = requires.get("bins", [])
        required_env_vars = requires.get("env", [])
        return all(shutil.which(cmd) for cmd in required_bins) and all(
            os.environ.get(var) for var in required_env_vars
        )
```

A skill may be marked `always` so it stays in the conversation context without a read step each turn:

```python
    def get_always_skills(self) -> list[str]:
        """Get skills marked as always=true that meet requirements."""
        ...
                self._parse_homebot_metadata(meta.get("metadata")).get("always")
                or meta.get("always")
```

---

## Skill Definitions

### Available Smart-Home Skills (per README and `docs/skills/`)

The `docs/skills/` directory documents the following skill set (index + per-skill pages):

| Skill page | Domain | Description |
|-------|-------------|-------------|
| `mijia.md` | Smart home | Control Xiaomi Mi Home devices via Home Assistant |
| `weather.md` | Information | Weather lookup via wttr.in (no API key) |
| `qqmusic.md` | Media | Play music from QQ Music via a dedicated Chrome session |
| `xiaohongshu.md` | Information | Search Xiaohongshu (RED) |
| `alarm.md` | Automation | Alarms and reminders |
| `index.md` | Overview | Skills index |

### 1. Mijia Smart-Home Skill (`docs/skills/mijia.md`)

The Mi Home skill is generated from the user's own device inventory so the agent can control real household devices by voice. The source doc is in Chinese; the load-bearing content is summarised and translated below (original wording in parentheses where it matters).

- **Transport**: homebot controls Mi Home devices through **Home Assistant**. The user first adds Mi Home to Home Assistant and confirms devices can be viewed and operated there (e.g. turning on the living-room light).
- **Config file**: a private `config.json` is created at `~/.homebot/workspace/skills/mijia/config.json`:

```json
{
  "base_url": "http://<Home-Assistant address>:8123",
  "access_token": "<long-lived access token>"
}
```

  The doc warns that this token can control household devices and must not be committed to Git or shared.
- **Skill generation**: a bundled driver reads the devices already integrated in Home Assistant and writes the model-facing skill:

```bash
python homebot/skills/mijia/driver.py \
  --config ~/.homebot/workspace/skills/mijia/config.json \
  build-skill \
  --output ~/.homebot/workspace/skills/mijia/SKILL.md
```

  The generated `SKILL.md` contains "the names, entity IDs and supported operations of the currently controllable devices"; re-running the command refreshes the inventory after devices are added or removed.
- **Voice control**: after a restart the user wakes the assistant and speaks naturally, e.g. "turn on the living-room light", "set the bedroom AC to 24 degrees", "close all the curtains".
- **`always` flag**: the generated Mijia skill is automatically marked `always`, so it stays in homebot's conversation context — home-control requests need no extra read of `SKILL.md`, which makes responses faster.

### 2. Weather Skill (`docs/skills/weather.md`)

The weather skill is a lightweight, key-free capability (source doc in Chinese; translated).

- **Provider**: weather data comes from [wttr.in](https://wttr.in/) with no API key — usable out of the box.
- **Features**: current weather (temperature, humidity, wind, conditions), multi-day forecast, and support for Chinese city names.
- **Dependency**: `curl` (system-provided).
- **Usage examples**: "how's the weather today", "what's Beijing's weather tomorrow", "Shanghai this weekend", "Shenzhen next three days".
- **Default city**: **Guangzhou** when no city is specified.
- **Mechanism**: the skill calls wttr.in with simple `curl` commands:

```bash
# Current weather
curl -s "wttr.in/<city>?format=%l:+%c+%t+%h+%w&m"
# Three-day forecast
curl -s "wttr.in/<city>?T&m&2" | head -40
```

  Chinese city names are used directly; spaces in English city names are encoded as `+`.
- **Limits**: wttr.in is a free public service with rate limits and is not intended for commercial or high-concurrency use.

---

## Evaluation Dimensions

### 1. Skill Manifest Contract
- [ ] SKILL.md format with YAML frontmatter is consistent across skills
- [ ] `name` / `description` are present and drive the index
- [ ] Declarative `requires` (bins, env) gate availability cleanly

### 2. Progressive Loading & Context Economy
- [ ] Summary index keeps skill bodies out of the base prompt
- [ ] `always` skills are explicitly opted in, not default-loaded
- [ ] Loader reports exactly what is missing when a skill is unavailable

### 3. Platform Awareness
- [ ] `platforms:` gating makes OS-specific skills invisible elsewhere
- [ ] Platform aliases (windows/macos/linux/posix) are normalised
- [ ] Gating applies to every caller, not just the availability filter

### 4. Smart-Home Safety
- [ ] Access tokens are kept in a workspace file, never in the repo
- [ ] Docs warn against committing the token
- [ ] Device skill is generated from the real inventory (names + entity IDs)

### 5. Extensibility
- [ ] Workspace skills shadow built-in skills by name
- [ ] New skills require no core changes (drop-in SKILL.md)
- [ ] Key-free informational skills (weather) demonstrate low-dependency design

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Manifest Contract | 25% | | |
| Progressive Loading & Context Economy | 20% | | |
| Platform Awareness | 15% | | |
| Smart-Home Safety | 20% | | |
| Extensibility | 20% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Loader Tests
1. Place a workspace skill and a built-in skill with the same name; confirm the workspace skill wins
2. Declare `requires.bins` / `requires.env` and confirm `list_skills()` filters unavailable skills and reports the missing entries
3. Set `platforms: [win32]` on a skill and confirm it is absent on a POSIX host (and vice versa)

### Frontmatter Tests
1. Load a skill whose frontmatter is unparseable YAML; confirm `get_skill_metadata` returns `None` and the skill degrades to its bare name
2. Verify `get_always_skills()` returns only `always` skills that also meet their requirements
3. Confirm `build_skills_summary` renders the `(unavailable: …)` suffix correctly

### Smart-Home Integration Tests
1. Generate the Mijia `SKILL.md` from a stub Home Assistant and confirm device names/entity IDs appear
2. Verify the Mijia skill is tagged `always` and needs no extra read before a control request
3. Run the weather skill against wttr.in and confirm Chinese city names and the Guangzhou default work

---

## Notes

- **MIT license** permits full quotation and modification.
- Homebot is a **voice-driven smart-home assistant**, a non-coding agent: its skills are device-control and information workflows, not repository operations.
- The source `docs/skills/*.md` pages are written in **Chinese**; this document quotes the English `skills.py` source verbatim and renders the Chinese docs as faithful English summaries (with the original commands/JSON reproduced exactly). No content was invented.
- The loader is a strong reference for **declarative skill gating** (`requires` + `platforms`) and **progressive loading** (summary index + on-demand read).
- `alarm.md`, `qqmusic.md`, `xiaohongshu.md` and `index.md` were confirmed to exist in the directory listing but were not quoted in this case.
