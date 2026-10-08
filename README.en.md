# RDR2 Cheat Paster

> Type all 37 official Red Dead Redemption 2 cheat codes into the game with a single hotkey.

**English** | [简体中文](README.md)

Still hand-typing phrases like `Abundance is the dullest desire` one character at a time?
This tiny tool bundles all 37 cheat codes — press `Ctrl + ,` and it types the code into the game's
cheat box for you. Flip through codes with `Ctrl + ↑` / `Ctrl + ↓`.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Cheats](https://img.shields.io/badge/Cheats-37-orange)

---

## Features

- **All 37 official cheat codes built in** — punctuation matches the game exactly, so codes never silently fail
- **Global hotkeys** — works while the game is fullscreen; no alt-tabbing needed
- **Cycle through codes** — `Ctrl + ↑` / `Ctrl + ↓` to step, `Home` / `End` to jump to the ends
- **Automatic input** — simulates character-by-character typing plus an Enter keystroke (the game's cheat box does not accept `Ctrl + V`)
- **Search + category filter** — search in English or Chinese; filter by 6 categories (money, weapons, horses, honor, …)
- **Prerequisite labels** — the 8 codes that require a newspaper tell you exactly which chapter to buy it in
- **Remembers your position** — reopens on the code you last selected
- **Portable exe** — a single-file build, double-click to run, no Python required

---

## Quick Start

### Option 1: Run the exe (recommended)

1. Download `RDR2作弊码速贴器.exe` from [Releases](https://github.com/Binbin-miao/rdr2-cheat-paster/releases)
2. Double-click to run
3. In game: `ESC` → **Settings** → **Cheats** at the bottom, leave the cursor in the text box
4. Pick a code with `Ctrl + ↑` / `Ctrl + ↓`, then press `Ctrl + ,`

> If your antivirus flags it on first run, that is the usual PyInstaller false positive — just add an exception.
> Prefer not to trust a binary? Run it from source instead (Option 2).

### Option 2: Run from source

```bash
git clone https://github.com/Binbin-miao/rdr2-cheat-paster.git
cd rdr2-cheat-paster
pip install pynput
python rdr2_cheat_paster.py
```

---

## Hotkeys

| Hotkey | Action |
|---|---|
| `Ctrl + ,` | **Type the selected cheat code into the game** (main hotkey) |
| `Ctrl + ↑` | Previous code |
| `Ctrl + ↓` | Next code |
| `Ctrl + Home` | Jump to the first code |
| `Ctrl + End` | Jump to the last code |
| `Ctrl + Shift + ,` | Copy to clipboard only, no simulated typing |
| `Ctrl + Shift + C` | Show / hide the main window |
| `Ctrl + Shift + Q` | Quit the program |
| `ESC` (in window) | Minimize to background |

All hotkeys are **global** — they work while the game is fullscreen.

---

## Bundled Cheat Codes

All **37** codes, in 6 categories:

| Category | Count | Example |
|---|---|---|
| Money & Stats | 7 | `Greed is now a virtue` — add $500 |
| Dead Eye Levels | 5 | `Guide me better` — Dead Eye level 1 |
| Weapons | 4 | `A simple life, a beautiful death` — basic weapons |
| Horses & Vehicles | 10 | `Run! Run! Run!` — spawn a race horse |
| Honor & Wanted | 6 | `Virtue unearned is not virtue` — max honor |
| Map & Appearance | 5 | `Vanity. All is vanity` — unlock all outfits |

Full data lives in [`cheats.py`](cheats.py).

---

## Important Notes

- Cheat codes are **punctuation-sensitive**; capitalization does not matter.
  This tool ships the exact strings, so you cannot mistype them.
- **8 codes require you to own the matching newspaper first**, otherwise the game says
  *"You do not meet the prerequisites to unlock this cheat"*:

  | Cheat code | Prerequisite |
  |---|---|
  | `Abundance is the dullest desire` | Buy a newspaper from Chapter 1 onward |
  | `Greed is American virtue` | Newspaper after Ch. 3 "Advertising, the New American Art" |
  | `You long for sight and see nothing` | Newspaper after Ch. 3 "Blood Feuds, Ancient and Modern" |
  | `Virtue unearned is not virtue` | Newspaper after Ch. 4 "Urban Pleasures" |
  | `The lucky be strong evermore` | Newspaper after completing Chapter 5 |
  | `You seek more than the world offers` | Newspaper after Ch. 6 "The King's Son" |
  | `You are a beast built for war` | Newspaper after completing the Epilogue |
  | `Would you be happier as a clown?` | Newspaper after completing the Epilogue |

- **While any cheat is active you cannot save your progress, and achievements/trophies are disabled.**
  For a normal playthrough, turn cheats off first or load a save that never used them.

---

## Configuration

Config file: `~/.rdr2_cheat_paster.json` (created automatically on first run):

```json
{
  "type_mode": "type",
  "key_interval": 0.012,
  "last_index": 0
}
```

| Field | Description |
|---|---|
| `type_mode` | `type` = simulated typing (default, best compatibility); `paste` = clipboard only |
| `key_interval` | Delay in seconds between simulated keystrokes. Raise to `0.03` if the game drops characters |
| `last_index` | Index of the last selected code (maintained automatically) |

---

## Building the exe

Double-click `build.bat`, or run manually:

```bash
pip install pynput pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --noconsole \
  --name "RDR2作弊码速贴器" \
  --hidden-import pynput.keyboard._win32 \
  --hidden-import pynput.mouse._win32 \
  rdr2_cheat_paster.py
```

> Both `--hidden-import` flags are required, or the packaged exe will fail at launch
> with a pynput backend import error.

---

## Project Structure

```
rdr2-cheat-paster/
├── rdr2_cheat_paster.py    # Main app: Tkinter GUI + pynput global hotkeys
├── cheats.py               # The 37 cheat codes
├── build.bat               # One-click build script
├── 使用说明.md              # Detailed guide (Chinese)
├── README.md               # Chinese README
├── README.en.md            # This file
├── requirements.txt
└── LICENSE
```

---

## How It Works

- **GUI**: standard-library `tkinter`, no extra UI dependencies
- **Hotkeys & input simulation**: `pynput` — hotkey callbacks fire on the listener thread,
  so UI updates are marshalled back with `root.after(0, fn)`
- **Why simulated typing instead of clipboard paste**: RDR2's cheat box does not accept `Ctrl + V`;
  keys have to be sent one at a time
- **Input delay**: the tool waits 0.45 s after the hotkey before typing, giving you a moment
  to bring the game back into focus

---

## Adding / Editing Cheat Codes

Edit `cheats.py` and append an entry — the app picks it up automatically:

```python
{"cat": "Category", "name": "What it does", "code": "Cheat Phrase Here",
 "req": "Prerequisite (use 无 for none)", "type": "paste"},
```

---

## License

[MIT](LICENSE)

---

## Disclaimer

This project is intended for **single-player entertainment only**. It contains no online-game
cheating, save editing, or trainer functionality whatsoever. Enabling in-game cheat codes prevents
saving and disables achievements — that is the game's own behaviour, not something this tool causes.

Red Dead Redemption 2 is a trademark of Take-Two Interactive / Rockstar Games.
This project is unofficial and is not affiliated with or endorsed by them.
