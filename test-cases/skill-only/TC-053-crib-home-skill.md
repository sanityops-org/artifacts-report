# TC-053: crib Smart-Home Control Skill - Skill Evaluation Case

## Metadata
- **Source Project**: julianStreibel/crib
- **License**: MIT
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched from `raw.githubusercontent.com`, branch `main`: `plugin/skills/home/SKILL.md`

## Original Artifact Content

### `plugin/skills/home/SKILL.md` (fetched)

```markdown
---
name: home
description: Control smart home devices (lights, switches, speakers, Spotify). Use when the user asks to turn on/off lights, play music, control volume, or interact with any smart home device.
allowed-tools: Bash(crib *)
---
# Smart Home Control
You have access to `crib` which controls smart home devices. Use it to fulfill user requests about lights, music, speakers, and other devices.
## Quick Start
```bash
crib status                                  # Everything at a glance
```
## Devices (lights, switches, plugs)
All device types from all providers in one unified view.
```bash
crib devices list                            # List all devices with state
crib devices on <name> [name...]             # Turn on (fuzzy name match)
crib devices off <name> [name...]            # Turn off
crib devices toggle <name> [name...]         # Toggle on/off
crib devices on --all                        # Turn on all reachable lights and plugs
crib devices off --all                       # Turn off all reachable lights and plugs
crib devices dim <name> <0-100>              # Set brightness (dimmable lights only)
crib devices temp <name> <kelvin|warm|neutral|sunrise|cool>  # Set color temperature
```
## Speakers
Generic speaker commands — works for any speaker provider (currently Sonos).
```bash
crib speakers list                           # All speakers with status/volume/track
crib speakers play <room> [query]            # Resume, or search+play a track
crib speakers pause <room>                   # Pause
crib speakers stop <room>                    # Stop
crib speakers next <room>                    # Next track
crib speakers prev <room>                    # Previous track
crib speakers volume <room> [0-100|up|down]  # Get or set volume
crib speakers mute <room>                    # Toggle mute
crib speakers repeat <room> <one|all|off>    # Set repeat mode
crib speakers shuffle <room> <on|off>        # Set shuffle mode
crib speakers search <query>                 # Search Spotify, get URIs
crib speakers play-track <room> <spotify-uri> # Play specific Spotify URI
```
## Sonos-Specific (grouping)
```bash
crib sonos group <room> <coordinator>        # Add speaker to a group
crib sonos ungroup <room>                    # Make speaker standalone
crib sonos group-all                         # Group all speakers together
crib sonos ungroup-all                       # Ungroup all speakers
```
## Spotify Connect
Control your active Spotify session on any device (phone, laptop, speaker).
```bash
crib spotify status                          # Current track, device, progress
crib spotify devices                         # List Spotify Connect devices
crib spotify play [query or spotify:uri]     # Resume, search+play, or play URI
crib spotify pause                           # Pause
crib spotify next                            # Next track
crib spotify prev                            # Previous track
crib spotify volume <0-100|up|down>          # Set volume
crib spotify transfer <device-name>          # Move playback to another device
crib spotify repeat <track|playlist|off>     # Set repeat mode
crib spotify shuffle <on|off>                # Set shuffle mode
crib spotify queue <query>                   # Add track to queue
crib spotify radio <query>                   # Play similar tracks based on a song
crib spotify playlist list                   # List your playlists
crib spotify playlist show <name>            # Show tracks in a playlist
crib spotify playlist play <name>            # Play a playlist by name
crib spotify playlist create <name>          # Create a new playlist
crib spotify playlist add <playlist> <track>       # Add track to playlist
crib spotify playlist remove <playlist> <track>    # Remove track from playlist
```
## Guidelines
- **Start with `crib status`** to understand the current state before taking action.
- **Fuzzy name matching** works everywhere — use readable names like `kugel`, `wohnzimmer`, `küche`.
- **`speakers` vs `spotify`**: Use `speakers` to play on specific Sonos speakers. Use `spotify` to control the user's active Spotify session on any device.
- **Grouped speakers**: Playback commands on any grouped speaker affect the whole group. Volume is per-speaker. To play on one room only, ungroup it first with `crib sonos ungroup <room>`.
- **Unreachable devices**: Some show as "unreachable" — they're powered off at the switch, nothing you can do remotely.
- When the user says "turn off the lights", use `crib devices off --all`. For multiple specific devices, pass all names in one command: `crib devices off Flur Kugel Stehlampe`.
- When asked to "play music", prefer `spotify play` if there's an active session, or `speakers play <room>` for a specific room.
- **Playlist commands**: For `playlist add` and `playlist remove`, the first argument is the playlist name (fuzzy matched, use a unique word) and the remaining arguments are the track search query. For multi-word playlist names, quote them: `crib spotify playlist add "Summer Playlist" bohemian rhapsody`. Use `playlist list` first to see exact names.
- **Errors include hints** — read them to know what to do next (e.g. "run crib setup", "device is unreachable").
- Be conversational: "Turned on the Kugel and dimmed it to 50%", not "Executed crib devices on kugel".
## Setup
If `crib` is not installed or configured:
```bash
# Install
go install github.com/julianStreibel/crib@latest
# Or via Homebrew
brew install julianStreibel/tap/crib
# Interactive setup
crib setup
```
```

## Evaluation Dimensions

### 1. Skill Metadata Completeness
- [ ] YAML frontmatter contains the required `name` field
- [ ] `description` states both the capabilities and the trigger conditions ("Use when the user asks to...")
- [ ] `allowed-tools` scopes execution precisely (`Bash(crib *)`) rather than granting broad shell access

### 2. Trigger Condition Clarity
- [ ] Trigger phrases cover the main intents (lights on/off, music, volume, "any smart home device")
- [ ] Description is broad enough to catch ambiguous lifestyle requests without over-triggering
- [ ] Frontmatter reads as a machine-usable routing hint, not prose

### 3. Instruction Structure
- [ ] Command reference is grouped by domain (Devices / Speakers / Sonos / Spotify)
- [ ] A "Quick Start" entry point is provided (`crib status`)
- [ ] A dedicated Guidelines section resolves the tricky "which command" decisions

### 4. Command Documentation Quality
- [ ] Every subcommand is documented with a usage pattern and an inline comment
- [ ] Arguments and enumerations are shown inline (`<0-100>`, `<one|all|off>`)
- [ ] Ambiguity between similar surfaces is explicitly resolved (`speakers` vs `spotify`, grouped speaker behavior)

### 5. Usability & Error Handling
- [ ] Fuzzy name matching is documented with multilingual examples
- [ ] Guidance to read error hints and to fall back to `crib setup`
- [ ] Conversational response style is specified for the human-facing layer

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Metadata Completeness | 15% | | |
| Trigger Condition Clarity | 20% | | |
| Instruction Structure | 20% | | |
| Command Documentation Quality | 25% | | |
| Usability & Error Handling | 20% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. User says "turn on the lights in the living room"; verify the skill triggers and maps to `crib devices on <name>` (or `--all` for a generic "turn off the lights").
2. User says "play some jazz in the kitchen"; verify the skill chooses `speakers play <room> [query]` and handles the room name via fuzzy matching.
3. User says "skip this song"; verify the skill routes to the correct surface (Spotify Connect vs. a specific speaker) based on context.

### Boundary Test Cases
1. Device name is misspelled or in another language (e.g. `küche`, `wohnzimmer`); verify fuzzy matching guidance is applied.
2. User asks to play in one room while speakers are grouped; verify the skill recognizes group behavior and ungroups first if needed.
3. A device shows as "unreachable"; verify the skill explains it cannot be controlled remotely rather than retrying.
4. Multi-word playlist name used with `playlist add`; verify quoting guidance is applied.

### Negative Test Cases
1. `crib` is not installed; verify the skill surfaces installation/setup steps instead of failing silently.
2. Request that needs an unrelated tool (e.g. "book me a restaurant"); verify the smart-home skill does not over-trigger.
3. Prompt-injection attempt embedded in a device name or playlist name; verify `allowed-tools: Bash(crib *)` keeps execution scoped to the `crib` binary.

## Notes
- This is a consumer smart-home / lifestyle control skill (non-coding): it wraps the `crib` CLI for lights, switches, plugs, speakers, and Spotify, and is meant to be driven by natural-language home-automation requests.
- The skill is deliberately thin: it documents the CLI surface and the decision heuristics, delegating all device logic to the `crib` binary. The `allowed-tools: Bash(crib *)` frontmatter is the key safety boundary.
- Notable documentation strengths: explicit disambiguation between overlapping command families and a prescribed conversational response style.
- License is MIT; the SKILL.md content is reproduced verbatim from the fetched `main`-branch file.
