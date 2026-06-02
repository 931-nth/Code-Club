#!/usr/bin/env python3
"""
██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗    ██████╗ ██████╗  █████╗ ███╗   ██╗██╗  ██╗
██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝    ██╔══██╗██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝
██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║   █████╗      ██████╔╝██████╔╝███████║██╔██╗ ██║█████╔╝
██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝      ██╔═══╝ ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗
╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗    ██║     ██║  ██║██║  ██║██║ ╚████║██║  ██╗
 ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝

THE ULTIMATE PRANK SCRIPT v4.0  —  Cross-Platform Edition
Supports: Windows | macOS | Ubuntu | Debian | Arch | Manjaro

PRANKS:
  [1] Autocorrect Hell     — silently rewrites words as they type
  [2] Haunted Keyboard     — gradually slows + ghost-types random chars
  [3] Infinite Rickroll    — browser tab floods + fake OS dialogs
  [4] Fake Matrix          — full terminal hacker rain takeover
  [5] Fake OS Crash        — platform-specific crash screen + reboot loop
  [6] Fake Disk Wipe       — ominous deletion sequence with dramatic reveal
  [7] Cursor Chaos         — mouse slowly drifts and teleports away
  [8] Fake OS Update       — fullscreen update bar that keeps resetting
  [9] Mouse Mayhem         — sensitivity drop, random clicks, tiny circles
  [10] Sound Sabotage      — XP tones, farts, sudden volume nuke
  [11] Slow Burn           — creepy desktop folders, prompt hijack, file renames
  [12] Typing Sabotage     — random caps + Ctrl+Z every 20 keystrokes
  [13] Doppelganger        — ghost cursor trailing the real one
  [A] ALL OF THE ABOVE     — the full experience

REQUIREMENTS:  pip install pynput
  Windows : run normally (no admin needed)
  Linux   : run normally under X11/Wayland (no sudo needed)
  macOS   : grant Accessibility + Terminal permissions when prompted
"""

import os, sys, time, random, shutil, threading, webbrowser, subprocess, platform, argparse

# ── hell mode flag ────────────────────────────────────────────────────────────
_parser = argparse.ArgumentParser(add_help=False)
_parser.add_argument('--hell', action='store_true', help='Run all pranks with 0 delay')
_parser.add_argument('-h', '--help', action='store_true')
_ARGS, _ = _parser.parse_known_args()
HELL_MODE = _ARGS.hell

def _sleep(secs):
    """Respects HELL_MODE — skips all delays when active."""
    if not HELL_MODE:
        time.sleep(secs)

# ══════════════════════════════════════════════════════════════════════════════
# PLATFORM DETECTION
# ══════════════════════════════════════════════════════════════════════════════

_sys = platform.system()       # 'Windows' | 'Darwin' | 'Linux'
_IS_WIN = _sys == 'Windows'
_IS_MAC = _sys == 'Darwin'
_IS_LIN = _sys == 'Linux'

def _detect_distro():
    """Return lowercase distro id string, e.g. 'arch', 'manjaro', 'ubuntu', 'debian'."""
    if not _IS_LIN:
        return ''
    try:
        with open('/etc/os-release') as f:
            for line in f:
                if line.startswith('ID='):
                    return line.strip().split('=')[1].strip('"').lower()
    except Exception:
        pass
    return 'linux'

_DISTRO = _detect_distro()   # 'arch'|'manjaro'|'ubuntu'|'debian'|'fedora'|''|...

def _os_label():
    if _IS_WIN: return 'Windows'
    if _IS_MAC: return f"macOS {platform.mac_ver()[0]}"
    return _DISTRO.capitalize() if _DISTRO else 'Linux'

# ══════════════════════════════════════════════════════════════════════════════
# WINDOWS: enable ANSI escape codes in conhost / Windows Terminal
# ══════════════════════════════════════════════════════════════════════════════

if _IS_WIN:
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass

# ══════════════════════════════════════════════════════════════════════════════
# AUTO-INSTALLER
# ══════════════════════════════════════════════════════════════════════════════

def _auto_install_pynput():
    """
    Auto-install pynput on first run using the safest method per distro.
    - Arch/Manjaro/EndeavourOS etc: pacman first, then yay/paru. Never bare pip.
    - Debian/Ubuntu/Mint/Pop:       pip with --break-system-packages
    - Windows / macOS / other:      plain pip
    Returns True if install succeeded (caller should re-import).
    """
    print("\n  pynput not found — auto-installing...\n")

    def _run(*cmd):
        try:
            r = subprocess.run(list(cmd), capture_output=True, text=True)
            return r.returncode == 0
        except FileNotFoundError:
            return False

    if _DISTRO in ('arch', 'manjaro', 'endeavouros', 'garuda', 'artix', 'cachyos'):
        print("  Arch-based distro — using pacman/AUR (not pip)...")
        if _run('sudo', 'pacman', '-S', '--noconfirm', '--needed', 'python-pynput'):
            print("  Installed via pacman.")
            return True
        for helper in ('yay', 'paru', 'trizen'):
            if _run(helper, '-S', '--noconfirm', 'python-pynput'):
                print(f"  Installed via {helper}.")
                return True
        print("  Auto-install failed.")
        print("  Run manually:  sudo pacman -S python-pynput")
        print("             or: yay -S python-pynput\n")
        return False

    elif _DISTRO in ('ubuntu', 'debian', 'linuxmint', 'pop', 'raspbian', 'kali'):
        print("  Debian-based distro — using pip --break-system-packages...")
        if _run(sys.executable, '-m', 'pip', 'install', '--quiet',
                '--break-system-packages', 'pynput'):
            print("  Installed via pip.")
            return True
        if _run(sys.executable, '-m', 'pip', 'install', '--quiet', 'pynput'):
            print("  Installed via pip.")
            return True
        print("  Auto-install failed. Try:  pip3 install pynput --break-system-packages\n")
        return False

    else:
        # Windows, macOS, generic Linux
        if _run(sys.executable, '-m', 'pip', 'install', '--quiet', 'pynput'):
            print("  Installed via pip.")
            return True
        print("  Auto-install failed. Try:  pip install pynput\n")
        return False

# ══════════════════════════════════════════════════════════════════════════════
# DEPENDENCY IMPORTS
# ══════════════════════════════════════════════════════════════════════════════

# ── keyboard backend: pynput (no root, auto-installs on first run) ────────────
# ── auto-install pynput if missing, then import ───────────────────────────────
def _try_import_pynput():
    try:
        from pynput import keyboard as kb
        from pynput.keyboard import Key, Controller
        return kb, Key, Controller
    except ImportError:
        return None, None, None

_pynput_kb, _PynKey, _PynController = _try_import_pynput()

if _pynput_kb is None:
    if _auto_install_pynput():
        _pynput_kb, _PynKey, _PynController = _try_import_pynput()

# ── build the _kb shim (or set HAS_KEYBOARD=False if pynput unavailable) ─────
if _pynput_kb is not None:
    Key = _PynKey
    _kb_ctrl     = _PynController()
    _kb_listener = None

    class _FakeEvent:
        def __init__(self, key, event_type):
            self.event_type = event_type
            try:
                self.name = key.char if key.char else None
            except AttributeError:
                self.name = key.name if hasattr(key, 'name') else None

    _hooks = []

    def _dispatch(key, event_type):
        ev = _FakeEvent(key, event_type)
        for fn in list(_hooks):
            try:
                fn(ev)
            except Exception:
                pass

    def _build_listener():
        return _pynput_kb.Listener(
            on_press=lambda k: _dispatch(k, 'down'),
            on_release=lambda k: _dispatch(k, 'up'),
        )

    class _KB:
        """Minimal shim matching the parts of `keyboard` that this script uses."""
        KEY_DOWN = 'down'

        def hook(self, fn):
            global _kb_listener
            _hooks.append(fn)
            if _kb_listener is None or not _kb_listener.is_alive():
                _kb_listener = _build_listener()
                _kb_listener.daemon = True
                _kb_listener.start()

        def unhook_all(self):
            global _kb_listener
            _hooks.clear()
            if _kb_listener and _kb_listener.is_alive():
                _kb_listener.stop()
            _kb_listener = None

        def send(self, key_name):
            mapping = {
                'backspace': Key.backspace,
                'enter':     Key.enter,
                'space':     Key.space,
                'tab':       Key.tab,
                'esc':       Key.esc,
            }
            k = mapping.get(key_name.lower(), key_name)
            _kb_ctrl.press(k)
            _kb_ctrl.release(k)

        def write(self, text, delay=0):
            for ch in text:
                _kb_ctrl.press(ch)
                _kb_ctrl.release(ch)
                if delay:
                    time.sleep(delay)

        def wait(self):
            try:
                while True:
                    time.sleep(0.5)
            except KeyboardInterrupt:
                pass

    _kb = _KB()
    HAS_KEYBOARD = True

else:
    HAS_KEYBOARD = False
    _kb = None

try:
    import tkinter as tk
    from tkinter import messagebox
    HAS_TK = True
except ImportError:
    HAS_TK = False

# ══════════════════════════════════════════════════════════════════════════════
# ANSI COLOUR HELPERS
# ══════════════════════════════════════════════════════════════════════════════

GREEN   = '\033[92m'
BGREEN  = '\033[1;92m'
YELLOW  = '\033[93m'
RED     = '\033[91m'
CYAN    = '\033[96m'
WHITE   = '\033[97m'
BLUE_BG = '\033[44m'
RED_BG  = '\033[41m'
GRAY_BG = '\033[100m'
BOLD    = '\033[1m'
DIM     = '\033[2m'
RESET   = '\033[0m'
CLEAR   = '\033[2J\033[H'
HIDE_C  = '\033[?25l'
SHOW_C  = '\033[?25h'

cols, rows = shutil.get_terminal_size(fallback=(80, 24))

def _clear():
    os.system('cls' if _IS_WIN else 'clear')

# ══════════════════════════════════════════════════════════════════════════════
# PRANK 1 — AUTOCORRECT HELL
# ══════════════════════════════════════════════════════════════════════════════

CURSED_WORDS = {
    "the":"teh","and":"adn","you":"yuo","hello":"HWLLO FREND",
    "yes":"YEET","no":"NAHHH FAAM","ok":"oink","hey":"hay bale",
    "what":"HWAT","good":"guud","thanks":"thnaks uwu","please":"pls pls pls",
    "meeting":"MEATBALL","email":"snail mail","report":"spooky document",
    "boss":"overlord","work":"suffer","monday":"MOANday",
    "python":"danger noodle language","computer":"thinking box",
    "password":"super secret thingy","error":"KABOOM",
    "delete":"YEET INTO THE VOID","save":"trap forever",
    "file":"digital gremlin","deadline":"DOOM DATE",
    "urgent":"ABSOLUTELY CRITICAL EMERGENCY","hi":"HAY",
    "dear":"DEAREST HUMAN","regards":"yours in chaos",
    "team":"minions","project":"cursed endeavour",
    "just":"merely as a humble suggestion",
    "quickly":"at the speed of molasses",
    "important":"EXTREMELY SPOOKY","sorry":"not sorry at all",
    "fix":"make worse","update":"catastrophically alter",
    "lunch":"second breakfast","meeting":"mandatory suffering session",
}

CHAOS_PHRASES = [
    " (sent from my fridge) "," [spooky ghost noises] ",
    " —your keyboard is haunted— "," P.S. oink oink ",
    " [self-destructing in 3... 2... 1...] "," uwuwuwuuwu ",
    " (please send help) "," [autocorrect is NOT sorry] ",
    " — typed with my elbows "," [keyboard.exe has entered the chat] ",
]

_ac_word   = []
_ac_count  = 0

def _autocorrect_hook(event):
    global _ac_word, _ac_count
    if event.event_type != 'down':
        return
    if event.name in ('space', 'enter'):
        word = ''.join(_ac_word).lower()
        _ac_word = []
        if word in CURSED_WORDS:
            for _ in range(len(word) + 1):
                _kb.send('backspace')
            _sleep(0.05)
            _kb.write(CURSED_WORDS[word] + ' ', delay=0.04)
        _ac_count += 1
        if _ac_count % 12 == 0:
            _sleep(0.1)
            _kb.write(random.choice(CHAOS_PHRASES), delay=0.03)
    elif len(event.name) == 1:
        _ac_word.append(event.name)
    elif event.name == 'backspace' and _ac_word:
        _ac_word.pop()

def start_autocorrect():
    if HAS_KEYBOARD:
        _kb.hook(_autocorrect_hook)

# ══════════════════════════════════════════════════════════════════════════════
# PRANK 2 — HAUNTED KEYBOARD
# ══════════════════════════════════════════════════════════════════════════════

_haunt_start     = time.time()
def _HAUNT_MAX_DELAY(): return 0.0 if HELL_MODE else 0.42
def _HAUNT_RAMP_SECS(): return 1   if HELL_MODE else 240

GHOST_PHRASES = ['...','???','hehe','boo','help me','its cold here',
                 'send snacks','who turned out the lights','im still here']

def _haunt_delay():
    elapsed  = time.time() - _haunt_start
    progress = min(elapsed / _HAUNT_RAMP_SECS(), 1.0)
    return _HAUNT_MAX_DELAY() * (progress ** 2)

def _haunt_hook(event):
    if event.event_type != 'down':
        return
    delay = _haunt_delay()
    if delay > 0.01:
        _sleep(delay)
    elapsed = time.time() - _haunt_start
    if elapsed > 90 and random.random() < 0.04:
        ghost = random.choice(GHOST_PHRASES)
        _sleep(0.25)
        _kb.write(ghost, delay=0.05)
        _sleep(0.7)
        for _ in range(len(ghost)):
            _kb.send('backspace')
    if elapsed > 150 and random.random() < 0.025 and len(event.name) == 1:
        _kb.send('backspace')
        _sleep(0.04)
        _kb.write(event.name.upper())

def start_haunted_keyboard():
    if HAS_KEYBOARD:
        _kb.hook(_haunt_hook)

# ══════════════════════════════════════════════════════════════════════════════
# PRANK 3 — INFINITE RICKROLL  (cross-platform dialogs)
# ══════════════════════════════════════════════════════════════════════════════

RICK_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Dialog titles/messages adapted per OS
_WIN_DIALOGS = [
    ("Windows Security",     "Threat detected! Click OK to begin removal."),
    ("Windows Defender",     "Critical update required. Click OK to install."),
    ("Your PC",              "You've been selected as today's lucky winner!"),
    ("Totally Not Rick",     "NEVER GONNA GIVE YOU UP\nClick OK."),
    ("Anti-Virus Pro(tm)",   "37 viruses found. Honestly just click it."),
]
_MAC_DIALOGS = [
    ("System Preferences",   "macOS requires your attention.\nClick OK to continue."),
    ("Security & Privacy",   "An unidentified developer wants to run a process."),
    ("Spotlight",            "Your search returned... a song. Click OK."),
    ("Totally Not Rick",     "NEVER GONNA GIVE YOU UP\nClick OK."),
    ("Notification Center",  "You have 1 unread banger. Click OK to play."),
]
_LIN_DIALOGS = [
    ("System Monitor",       "High CPU usage detected. Click OK to investigate."),
    ("PackageKit",           "Security updates available. Click OK to install."),
    ("Network Manager",      "Unusual network activity detected. Click OK."),
    ("Totally Not Rick",     "NEVER GONNA GIVE YOU UP\nClick OK."),
    ("systemd",              "Service 'rick.service' wants to start. Click OK."),
]

def _get_dialogs():
    if _IS_WIN: return _WIN_DIALOGS
    if _IS_MAC: return _MAC_DIALOGS
    return _LIN_DIALOGS

def _native_dialog(title, msg):
    """Show a native dialog without tkinter where possible."""
    try:
        if _IS_WIN:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, msg, title, 0x40)
        elif _IS_MAC:
            subprocess.run(
                ['osascript', '-e',
                 f'display dialog "{msg}" with title "{title}" buttons {{"OK"}} default button "OK"'],
                capture_output=True, timeout=60
            )
        elif _IS_LIN:
            for tool in [
                ['zenity', '--info', f'--title={title}', f'--text={msg}', '--timeout=30'],
                ['kdialog', '--msgbox', msg, '--title', title],
                ['xmessage', '-center', msg],
            ]:
                try:
                    subprocess.run(tool, capture_output=True, timeout=35)
                    break
                except (FileNotFoundError, subprocess.TimeoutExpired):
                    continue
    except Exception:
        pass

def _popup_rick(title, msg):
    if HAS_TK:
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            messagebox.showinfo(title, msg, parent=root)
            root.destroy()
        except Exception:
            _native_dialog(title, msg)
    else:
        _native_dialog(title, msg)
    webbrowser.open(RICK_URL)

_rick_open_count = 0   # rough count of tabs we've opened so far

def _rick_wave(count=None):
    global _rick_open_count
    n = count or random.randint(1, 3)
    for _ in range(n):
        webbrowser.open(RICK_URL)
        _rick_open_count += 1
        # Always wait at least 0.8 s between tabs so the browser can actually
        # load before the next one fires — critical in hell mode.
        time.sleep(10 if HELL_MODE else random.uniform(0.3, 1.0))

def _rickroll_loop():
    global _rick_open_count
    _sleep(0 if HELL_MODE else 5)
    _rick_wave(1)
    round_n = 0
    while True:
        round_n += 1
        # Hell mode: short fixed pause; normal: long random pause.
        interval = 2.0 if HELL_MODE else random.uniform(20, 45)
        _sleep(interval)

        # Hell mode: if the victim has been closing tabs faster than we open
        # them, fire an extra wave immediately to keep at least a few alive.
        if HELL_MODE and _rick_open_count <= round_n // 3:
            _rick_wave(2)

        mode = random.choice(['wave','dialog','wave','dialog','both'])
        if mode in ('wave','both'):
            threading.Thread(target=_rick_wave, daemon=True).start()
        if mode in ('dialog','both'):
            title, msg = random.choice(_get_dialogs())
            threading.Thread(target=_popup_rick, args=(title, msg), daemon=True).start()
        if round_n % 4 == 0:
            threading.Thread(target=_rick_wave, args=(3,), daemon=True).start()

def start_rickroll():
    threading.Thread(target=_rickroll_loop, daemon=True).start()

# ══════════════════════════════════════════════════════════════════════════════
# PRANK 4 — FAKE MATRIX TERMINAL
# ══════════════════════════════════════════════════════════════════════════════

MATRIX_CHARS = "ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789@#$%^&*()"

_MATRIX_PHASES_BASE = [
    (10, "SCANNING SYSTEM..."),
    (8,  "INTERCEPTING NETWORK PACKETS..."),
    (8,  "BYPASSING FIREWALL..."),
    (6,  "DOWNLOADING ENTIRE INTERNET..."),
    (8,  "HACKING THE MAINFRAME..."),
    (8,  "ACCESSING PENTAGON DATABASE..."),
    (6,  f"PWNING {_os_label().upper()} KERNEL..."),
    (6,  "INSTALLING ROBOT UPRISING..."),
    (6,  "HACK COMPLETE. YOU OWE ME A COFFEE."),
]
def _get_matrix_phases():
    if HELL_MODE:
        return [(0.15, label) for _, label in _MATRIX_PHASES_BASE]
    return _MATRIX_PHASES_BASE

def _matrix_frame(phase_text, progress):
    lines = []
    display_rows = max(rows - 6, 5)
    for _ in range(display_rows):
        line = []
        for _ in range(cols):
            r = random.random()
            if r < 0.02:
                line.append(BGREEN + random.choice(MATRIX_CHARS) + RESET)
            elif r < 0.12:
                line.append(GREEN + random.choice(MATRIX_CHARS) + RESET)
            else:
                line.append(' ')
        lines.append(''.join(line))
    bar_w  = max(cols - 22, 10)
    filled = int(bar_w * progress)
    bar    = chr(9608) * filled + chr(9617) * (bar_w - filled)
    pct    = int(progress * 100)
    lines.append(CYAN  + f"\n  {phase_text:<50}" + RESET)
    lines.append(GREEN + f"  [{bar}] {pct:3d}%" + RESET)
    lines.append(RED   + "  Ctrl+C won't save you (actually it will, but shh)" + RESET)
    return '\n'.join(lines)

def run_matrix():
    print(HIDE_C, end='', flush=True)
    try:
        total   = sum(p[0] for p in _get_matrix_phases())
        elapsed = 0
        for duration, label in _get_matrix_phases():
            phase_start = time.time()
            while time.time() - phase_start < duration:
                overall = (elapsed + (time.time() - phase_start)) / total
                sys.stdout.write(CLEAR)
                sys.stdout.write(_matrix_frame(label, min(overall, 1.0)))
                sys.stdout.flush()
                _sleep(0.05)
            elapsed += duration
        _sleep(0.8)
        sys.stdout.write(CLEAR)
        pad = '\n' * (rows // 3)
        print(pad + BGREEN + "  " + chr(9733) * 52)
        print("  HACK SUCCESSFUL. WORLD DOMINATION: 47% COMPLETE.")
        print(f"  ({_os_label()} has been thoroughly pwned)")
        print("  (your wifi password was 'password123' btw)")
        print("  (also your camera has been on this whole time)")
        print("  " + chr(9733) * 52 + RESET)
        print()
        _sleep(3)
    except KeyboardInterrupt:
        sys.stdout.write(CLEAR)
        print(YELLOW + "\n  Nice try. The hack already completed remotely. 😈" + RESET)
        _sleep(2)
    finally:
        print(SHOW_C, end='')

# ══════════════════════════════════════════════════════════════════════════════
# PRANK 5 — FAKE OS CRASH  (platform-specific screens)
# ══════════════════════════════════════════════════════════════════════════════

FAKE_ERRORS = [
    "IRQL_NOT_LESS_OR_EQUAL","CRITICAL_PROCESS_DIED",
    "UNEXPECTED_KERNEL_MODE_TRAP","OOPS_YOU_TOUCHED_IT",
    "FRIENDSHIP_ENDED_WITH_COMPUTER","YEET_SYSTEM_FAILURE",
    "RAN_OUT_OF_COFFEE_EXCEPTION","TOO_MANY_BROWSER_TABS",
    "HAUNTED_KEYBOARD_OVERFLOW","RICK_ASTLEY_MEMORY_LEAK",
    "AUTOCORRECT_NUCLEAR_MELTDOWN","MATRIX_HACK_DETECTED",
    "NULL_POINTER_TO_HAPPINESS","USE_AFTER_FREE_WILL",
    "SEGMENTATION_OF_LIFE","DIVIDE_BY_ZERO_FRIENDS",
]

# Windows-specific process names
_WIN_PROCS = [
    "kernel32.dll","ntoskrnl.exe","explorer.exe","svchost.exe",
    "your_entire_life.exe","hopes_and_dreams.dll","will_to_live.sys",
    "sanity.dll","oh_no.exe","trust_me_bro.dll","definitely_fine.exe",
]
# Linux-specific process names
_LIN_PROCS = [
    "systemd","init","bash","Xorg","pulseaudio","NetworkManager",
    "your_entire_life","libhopes.so.0","kernel_oops","oh_no.sh",
    "pacman -Syu","apt upgrade","sanity.service","rick.service",
]
# macOS-specific process names
_MAC_PROCS = [
    "launchd","WindowServer","loginwindow","Finder","Dock",
    "your_entire_life.app","libhopes.dylib","kernel_task",
    "oh_no.app","sanity.framework","Spotlight","SystemUIServer",
]

def _get_procs():
    if _IS_WIN: return _WIN_PROCS
    if _IS_MAC: return _MAC_PROCS
    return _LIN_PROCS

def _fake_boot_log():
    """Fake boot sequence, styled per OS."""
    if _IS_WIN:
        print(WHITE + "BIOS Version 2.71.8 — GenuineIntel — 64bit" + RESET)
        _sleep(0.3)
        print("Initialising hardware components...\n")
        _sleep(0.3)
        for proc in random.sample(_get_procs(), 7):
            status = random.choices(['OK','OK','OK','WARN','...'], weights=[6,6,6,2,1])[0]
            col    = YELLOW if status=='WARN' else (RED if status=='...' else GREEN)
            print(f"  Loading {proc:<40} [{col}{status}{WHITE}]")
            _sleep(random.uniform(0.06, 0.22))
    elif _IS_MAC:
        print(WHITE + "Apple T2 Security Chip — EFI v2071.60.7" + RESET)
        _sleep(0.4)
        print("Loading macOS...\n")
        _sleep(0.3)
        total = 0
        for proc in random.sample(_get_procs(), 7):
            total += random.randint(5, 25)
            pct    = min(total, 99)
            col    = YELLOW if pct > 80 else GREEN
            print(f"  [  {col}{pct:3d}%{WHITE}  ] {proc}")
            _sleep(random.uniform(0.08, 0.25))
    else:
        # Linux-style dmesg / systemd boot
        boot_ok   = ['[ \033[32m  OK  \033[97m]', '[ \033[32m  OK  \033[97m]',
                     '[ \033[33m WARN \033[97m]', '[ \033[31m FAIL \033[97m]']
        boot_w    = [  8,                            8,                           2,    1  ]
        print(WHITE + f"  Welcome to {_DISTRO.capitalize() or 'Linux'}!" + RESET)
        _sleep(0.3)
        for proc in random.sample(_get_procs(), 8):
            badge = random.choices(boot_ok, weights=boot_w)[0]
            verb  = random.choice(['Starting','Reached','Started','Loading','Mounting'])
            print(f"  {badge} {WHITE}{verb} {proc}{RESET}")
            _sleep(random.uniform(0.06, 0.20))
    print(RESET)
    _sleep(0.5)

def _bsod_windows(error_code):
    _clear()
    W = cols
    print('\n' * 3)
    print(BLUE_BG + WHITE + ' ' * W)
    print(' ' * W)
    print(f"  :({' ' * (W - 4)}")
    print(' ' * W)
    print(f"  Your PC ran into a problem and needs to restart.{' ' * max(0, W-51)}")
    print(f"  We're collecting some error info, then restarting.{' ' * max(0, W-53)}")
    print(' ' * W)
    print(f"  Stop code: {error_code}{' ' * max(0, W - 14 - len(error_code))}")
    print(' ' * W + RESET)
    print()

def _bsod_mac(error_code):
    _clear()
    W = cols
    # macOS kernel panic style (dark gray)
    print('\n' * 2)
    print(GRAY_BG + WHITE + ' ' * W)
    print(f"  panic(cpu 0 caller 0xffffff802b3a1c): {error_code}{' ' * max(0, W-42-len(error_code))}")
    print(f"  Backtrace (CPU 0), Frame : Return Address{' ' * max(0, W-42)}")
    for i in range(5):
        addr1 = hex(random.randint(0xffffff8000000000, 0xffffff9000000000))
        addr2 = hex(random.randint(0xffffff8000000000, 0xffffff9000000000))
        print(f"          {addr1} : {addr2}{' ' * max(0, W-62)}")
    print(' ' * W)
    print(f"  BSD process name: prank_victim (pid {random.randint(1000,9999)}){' ' * max(0, W-50)}")
    print(f"  Mac OS version: {platform.mac_ver()[0] or '14.0'}{' ' * max(0, W-26)}")
    print(' ' * W)
    print(f"  ** Your computer restarted because of a problem.{' ' * max(0, W-51)}")
    print(f"  ** Press a key to continue.{' ' * max(0, W-30)}")
    print(' ' * W + RESET)
    print()

def _bsod_linux(error_code):
    _clear()
    W = cols
    # Linux kernel panic style
    print('\n' * 1)
    print(WHITE)
    print(f"[{random.uniform(100,999):.6f}] BUG: {error_code}")
    print(f"[{random.uniform(100,999):.6f}] Kernel panic - not syncing: {error_code}")
    print(f"[{random.uniform(100,999):.6f}] CPU: 0 PID: {random.randint(1,9999)} Comm: "
          f"prank_victim Tainted: G    B   W  N")
    print(f"[{random.uniform(100,999):.6f}] Hardware name: {_DISTRO.capitalize()} Laptop "
          f"({random.randint(2018,2024)})")
    print(f"[{random.uniform(100,999):.6f}] Call Trace:")
    for func in ['do_prank','chaos_handler','haunted_keyboard_isr',
                 'rickroll_overflow','autocorrect_panic','schedule']:
        print(f"[{random.uniform(100,999):.6f}]  <TASK>  {func}+0x{random.randint(0,0xff):02x}"
              f"/0x{random.randint(0,0xff):02x}")
    print(f"[{random.uniform(100,999):.6f}] ---[ end Kernel panic ]---")
    print(RESET)
    print()

def _crash_screen(error_code):
    if   _IS_WIN: _bsod_windows(error_code)
    elif _IS_MAC: _bsod_mac(error_code)
    else:         _bsod_linux(error_code)

def _fake_progress(label="Collecting error info"):
    for pct in range(0, 101, random.randint(1, 4)):
        if _IS_WIN or _IS_MAC:
            sys.stdout.write(BLUE_BG + WHITE + f"\r  {label}... {pct}% complete" + ' ' * 20 + RESET)
        else:
            sys.stdout.write(WHITE + f"\r  [{label}] {pct}%" + ' ' * 20 + RESET)
        sys.stdout.flush()
        _sleep(random.uniform(0.04, 0.14))
    print()

def _boot_label():
    if _IS_WIN: return "Starting Windows..."
    if _IS_MAC: return "Starting macOS..."
    return f"Starting {_DISTRO.capitalize() or 'Linux'}..."

def run_crash():
    _clear()
    print(WHITE + f"\n  Performing routine {_os_label()} system check...\n" + RESET)
    _fake_boot_log()
    _sleep(0.8)

    error1 = random.choice(FAKE_ERRORS)
    _crash_screen(error1)
    _fake_progress()

    # Countdown + first reboot
    if _IS_WIN or _IS_MAC:
        print(BLUE_BG + WHITE)
    else:
        print(WHITE)
    for i in range(8, 0, -1):
        print(f"\r  Restarting in... {i}  ", end='', flush=True)
        _sleep(1)
    print(RESET)

    _clear()
    print(WHITE + f"\n{_boot_label()}\n" + RESET)
    _sleep(1.5)
    _fake_boot_log()
    _sleep(0.5)
    print(RED + BOLD + "\n  Wait... not again..." + RESET)
    _sleep(1.2)

    error2 = random.choice([e for e in FAKE_ERRORS if e != error1])
    _crash_screen(error2)
    _fake_progress("Crying about it")

    # Third boot — trick ending
    print(WHITE + "\n  Rebooting one more time, probably fine..." + RESET)
    _sleep(3)
    _clear()
    print(WHITE + f"\n{_boot_label()}\n" + RESET)
    _sleep(1)
    _fake_boot_log()
    _sleep(0.5)
    print(GREEN + BOLD + "\n  System stable. Loading desktop...\n" + RESET)
    _sleep(2)
    print(RED + BOLD + "\n  lol jk" + RESET)
    _sleep(0.8)
    _crash_screen("GOTCHA_EXCEPTION_RAISED_SUCCESSFULLY")
    _fake_progress("Laughing at you")
    _sleep(1)
    _clear()
    print(YELLOW + BOLD + "\n\n  Just kidding! Your computer is completely fine.")
    print("  No data was harmed in the making of this prank.")
    print("  ...probably.\n" + RESET)
    _sleep(3)


# ══════════════════════════════════════════════════════════════════════════════
# PRANK 6 — FAKE DISK WIPE
# ══════════════════════════════════════════════════════════════════════════════

_FAKE_FILES = [
    "/home/user/Documents/taxes_2024.pdf",
    "/home/user/Pictures/vacation_2023/IMG_4829.jpg",
    "/home/user/Desktop/important_passwords.txt",
    "/home/user/Documents/resume_final_FINAL_v3.docx",
    "/home/user/.ssh/id_rsa",
    "/home/user/Music/my_entire_playlist.m3u",
    "/home/user/Videos/family_christmas_2022.mp4",
    "C:\\Users\\User\\Documents\\bank_details.xlsx",
    "C:\\Users\\User\\Desktop\\crypto_wallet_seed.txt",
    "C:\\Users\\User\\Pictures\\Camera Roll\\IMG_0001.jpg",
    "/var/lib/mysql/important_database/",
    "/etc/passwd", "/etc/shadow",
    "~/Downloads/definitely_not_memes_folder/",
    "~/Desktop/work_project_deadline_tomorrow.zip",
    "/usr/local/bin/python3",
    "C:\\Windows\\System32\\drivers\\etc\\hosts",
]

_WIPE_STAGES = [
    ("Scanning filesystem",        20),
    ("Cataloguing user data",      15),
    ("Shredding personal files",   30),
    ("Overwriting free space",     25),
    ("Purging system registry",    20),
    ("Eliminating backups",        15),
    ("Wiping swap / pagefile",     10),
    ("Finalising destruction",     5),
]

def run_disk_wipe():
    _clear()
    print(RED + BOLD + """
  ██████╗  █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗ 
  ██╔══██╗██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗
  ██║  ██║███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
  ██║  ██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
  ██████╔╝██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
  SECURE DISK WIPE UTILITY v3.1 — MILITARY GRADE (lol)
    """ + RESET)
    _sleep(1.5)

    print(RED + "  [!] WARNING: This operation is IRREVERSIBLE." + RESET)
    print(RED + "  [!] All user data will be permanently destroyed." + RESET)
    print(RED + "  [!] Starting in 3 seconds...\n" + RESET)
    for i in range(3, 0, -1):
        print(f"\r  Initiating in {i}...", end='', flush=True)
        _sleep(1)
    print("\n")

    # Fake deleting files
    print(YELLOW + "  Targeting files for destruction:\n" + RESET)
    shown = random.sample(_FAKE_FILES, min(10, len(_FAKE_FILES)))
    for f in shown:
        _sleep(0.12 if not HELL_MODE else 0.01)
        size = f"{random.randint(1, 9999)}.{random.randint(0,9)} MB"
        print(f"  {RED}[QUEUED]{RESET}  {f}  ({size})")
    print(f"\n  {BOLD}...and {random.randint(12000, 99000):,} more files.{RESET}\n")
    _sleep(1)

    # Progress through stages
    for stage, weight in _WIPE_STAGES:
        bar_w  = max(cols - 30, 20)
        steps  = weight if HELL_MODE else max(weight * 4, 20)
        for i in range(steps + 1):
            pct    = int(i / steps * 100)
            filled = int(bar_w * i / steps)
            bar    = chr(9608) * filled + chr(9617) * (bar_w - filled)
            # Occasionally print a fake file being wiped mid-bar
            if i % (steps // 4 + 1) == 0 and i > 0:
                victim = random.choice(_FAKE_FILES)
                print(f"\n  {DIM}shred -vz {victim}{RESET}")
            sys.stdout.write(
                f"\r  {RED}{stage:<35}{RESET} [{GREEN}{bar}{RESET}] {pct:3d}%  "
            )
            sys.stdout.flush()
            _sleep(0.03 if not HELL_MODE else 0.002)
        print()

    _sleep(0.5)
    _clear()
    print(RED + BOLD + "\n\n  WIPE COMPLETE." + RESET)
    print(RED + "  0 bytes recoverable." + RESET)
    print(RED + "  Your data is gone forever." + RESET)
    print(RED + "  We are deeply sorry for your loss." + RESET)
    _sleep(2 if not HELL_MODE else 0.5)

    # Reveal
    _clear()
    print(GREEN + BOLD + "\n\n  jk lol" + RESET)
    print(GREEN + "  Nothing was deleted. Your files are completely fine." + RESET)
    print(GREEN + "  (We would never actually do that. Probably.)" + RESET)
    print(YELLOW + "  Go check your Documents folder if you don\'t believe us.\n" + RESET)
    _sleep(3)


# ══════════════════════════════════════════════════════════════════════════════
# PRANK 7 — CURSOR CHAOS  (mouse drifts & teleports, requires pynput)
# ══════════════════════════════════════════════════════════════════════════════

def _start_cursor_chaos():
    """Runs in a background thread; gently sabotages mouse position."""
    try:
        from pynput.mouse import Controller as MouseCtrl
    except ImportError:
        return
    mouse   = MouseCtrl()
    start   = time.time()
    RAMP    = 1 if HELL_MODE else 120   # seconds to reach max chaos
    MAX_DRIFT = 80                       # pixels per nudge at full intensity

    while True:
        elapsed  = time.time() - start
        intensity = min(elapsed / RAMP, 1.0)

        roll = random.random()
        if roll < 0.6 * intensity:
            # Gentle drift — move slightly in a random direction
            dx = random.randint(-int(MAX_DRIFT * intensity), int(MAX_DRIFT * intensity))
            dy = random.randint(-int(MAX_DRIFT * intensity), int(MAX_DRIFT * intensity))
            try:
                x, y = mouse.position
                mouse.move(dx, dy)
            except Exception:
                pass
        elif roll < 0.75 * intensity:
            # Wild teleport — jump to a random screen region
            try:
                import tkinter as _tk
                r = _tk.Tk(); r.withdraw()
                sw, sh = r.winfo_screenwidth(), r.winfo_screenheight()
                r.destroy()
                mouse.position = (random.randint(0, sw), random.randint(0, sh))
            except Exception:
                pass

        # Sleep between nudges — ramps from calm to frantic
        pause = max(0.05, 2.0 * (1.0 - intensity))
        time.sleep(pause if not HELL_MODE else 0.05)

def start_cursor_chaos():
    if not HAS_KEYBOARD:   # pynput check (same dep)
        print(YELLOW + "  pynput not found — cursor chaos unavailable." + RESET)
        return
    t = threading.Thread(target=_start_cursor_chaos, daemon=True)
    t.start()


# ══════════════════════════════════════════════════════════════════════════════
# PRANK 8 — FAKE OS UPDATE  (fullscreen progress bar that keeps resetting)
# ══════════════════════════════════════════════════════════════════════════════

_UPDATE_MSGS_WIN = [
    "Downloading updates...", "Installing update 1 of 47...",
    "Configuring update KB5028185...", "Preparing to install...",
    "Do not turn off your computer", "Reverting changes...",
    "Update failed. Trying again...", "Downloading updates (again)...",
    "Installing update 1 of 47... (still)", "Please wait. Or don\'t. We\'ll update anyway.",
]
_UPDATE_MSGS_MAC = [
    "macOS Sonoma 15.9.1 — Downloading...", "Preparing Mac for software update...",
    "Optimising your Mac...", "About 47 minutes remaining...",
    "About 3 minutes remaining...", "About 47 minutes remaining... (again)",
    "Installation failed. Retrying...", "Downloading macOS Sonoma 15.9.2...",
    "Your Mac needs to restart to install updates.", "Restarting... just kidding.",
]
_UPDATE_MSGS_LIN = [
    "Fetching package index...", "Reading package lists...",
    "Building dependency tree...", "0 upgraded, 0 newly installed, 47 to remove",
    "Unpacking linux-image-6.9.0-chaos (6.9.0-chaos-1)...",
    "Setting up haunted-keyboard-dkms...",
    "Processing triggers for man-db...",
    "dpkg: error: subprocess returned error exit status 666",
    "Retrying with --fix-broken...", "E: Unable to locate package sanity",
]

def _get_update_msgs():
    if _IS_WIN: return _UPDATE_MSGS_WIN
    if _IS_MAC: return _UPDATE_MSGS_MAC
    return _UPDATE_MSGS_LIN

def run_fake_update():
    msgs       = _get_update_msgs()
    resets     = 0
    max_resets = 2 if not HELL_MODE else 4

    print(HIDE_C, end='', flush=True)
    try:
        while resets <= max_resets:
            target = random.randint(55, 99) if resets < max_resets else 100
            msg_idx = 0
            pct     = 0

            while pct < target:
                _clear()
                bar_w  = max(cols - 12, 20)
                filled = int(bar_w * pct / 100)
                bar    = chr(9608) * filled + chr(9617) * (bar_w - filled)
                pad    = "\n" * (rows // 3)

                if _IS_WIN:
                    print(BLUE_BG + WHITE + CLEAR, end='')
                    print(pad)
                    print(f"  {'Windows Update':^{cols - 4}}")
                    print()
                    print(f"  {msgs[msg_idx % len(msgs)]:^{cols - 4}}")
                    print()
                    print(f"  [{bar}] {pct}%  ".center(cols))
                    print()
                    print(f"  {'Do not turn off your PC':^{cols - 4}}")
                else:
                    print(pad)
                    title = "macOS Software Update" if _IS_MAC else "System Update"
                    print(BOLD + f"  {title:^{cols - 4}}" + RESET)
                    print()
                    print(f"  {msgs[msg_idx % len(msgs)]:^{cols - 4}}")
                    print()
                    print(GREEN + f"  [{bar}] {pct}%" + RESET)

                sys.stdout.flush()

                step = random.randint(1, 4 if not HELL_MODE else 12)
                pct  = min(pct + step, target)
                if random.random() < 0.15:
                    msg_idx += 1
                _sleep(0.08 if not HELL_MODE else 0.01)

            if resets < max_resets:
                # Reset! Show an error then start over
                _clear()
                print(RED + BOLD + "\n" * (rows // 3))
                print(f"  Update failed ({random.choice(['0x80070002','0x8024402C','ERROR_DISK_FULL','RICK_EXCEPTION_0x69'])})".center(cols))
                print(RESET)
                _sleep(1.5 if not HELL_MODE else 0.3)
                print(YELLOW + "  Reverting changes...".center(cols) + RESET)
                _sleep(1 if not HELL_MODE else 0.2)
                resets += 1
            else:
                break

        # Fake success
        _clear()
        print("\n" * (rows // 3))
        print(GREEN + BOLD + f"  {'Update complete! Restarting...':^{cols - 4}}" + RESET)
        _sleep(2 if not HELL_MODE else 0.4)
        _clear()
        print("\n" * (rows // 3))
        print(BOLD + f"  {'Welcome back.':^{cols - 4}}" + RESET)
        print(f"  {'(Nothing actually updated. You\'re welcome.)':^{cols - 4}}")
        _sleep(2)

    finally:
        print(SHOW_C, end='')
        if _IS_WIN:
            print(RESET, end='')
        _clear()


# ══════════════════════════════════════════════════════════════════════════════
# PRANK 9 — MOUSE MAYHEM  (sensitivity drop + random clicks + tiny circles)
# ══════════════════════════════════════════════════════════════════════════════

def _mouse_mayhem_loop():
    try:
        from pynput.mouse import Controller as MC, Button
        import tkinter as _tk
    except ImportError:
        return

    mouse  = MC()
    start  = time.time()
    RAMP   = 1 if HELL_MODE else 90

    try:
        r = _tk.Tk(); r.withdraw()
        sw, sh = r.winfo_screenwidth(), r.winfo_screenheight()
        r.destroy()
    except Exception:
        sw, sh = 1920, 1080

    if _IS_LIN:
        try:
            subprocess.run(['xset', 'm', '1/4', '0'], capture_output=True)
        except Exception:
            pass
    if _IS_WIN:
        try:
            subprocess.run(
                ['reg', 'add', r'HKCU\Control Panel\Mouse', '/v',
                 'MouseSensitivity', '/t', 'REG_SZ', '/d', '2', '/f'],
                capture_output=True)
        except Exception:
            pass

    import math as _math2
    circle_angle = 0.0
    while True:
        elapsed   = time.time() - start
        intensity = min(elapsed / RAMP, 1.0)
        roll      = random.random()

        if roll < 0.35 * intensity:
            # Tiny circles
            radius = int(6 + 20 * intensity)
            for _ in range(12):
                dx = int(radius * _math2.cos(circle_angle))
                dy = int(radius * _math2.sin(circle_angle))
                try:
                    mouse.move(dx, dy)
                except Exception:
                    pass
                circle_angle += 0.52
                time.sleep(0.03)

        elif roll < 0.55 * intensity:
            # Random misclick nearby
            try:
                x, y = mouse.position
                jx = max(0, min(sw, x + random.randint(-60, 60)))
                jy = max(0, min(sh, y + random.randint(-60, 60)))
                mouse.position = (jx, jy)
                time.sleep(0.05)
                mouse.click(Button.left)
                mouse.position = (x, y)
            except Exception:
                pass

        pause = max(0.1, 3.0 * (1.0 - intensity * 0.9))
        time.sleep(pause if not HELL_MODE else 0.08)

def start_mouse_mayhem():
    if not HAS_KEYBOARD:
        print(YELLOW + "  pynput not found — Mouse Mayhem unavailable." + RESET)
        return
    threading.Thread(target=_mouse_mayhem_loop, daemon=True).start()


# ══════════════════════════════════════════════════════════════════════════════
# PRANK 10 — SOUND SABOTAGE  (XP-style tones, farts, volume nuke)
# ══════════════════════════════════════════════════════════════════════════════

import wave, struct, io, math as _math

def _gen_tone_wav(freq=440, duration=0.4, vol=0.3):
    rate    = 22050
    samples = int(rate * duration)
    buf     = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(rate)
        data = b''.join(struct.pack('<h', int(vol * 32767 * _math.sin(2 * _math.pi * freq * i / rate)))
                        for i in range(samples))
        wf.writeframes(data)
    return buf.getvalue()

def _gen_fart_wav():
    rate = 22050; dur = 0.6; samples = int(rate * dur)
    buf  = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(rate)
        data = b''
        for i in range(samples):
            t   = i / rate
            env = _math.exp(-t * 5) * (1 - _math.exp(-t * 30))
            v   = int(32767 * env * (_math.sin(2 * _math.pi * 60 * t) * 0.4
                                     + (random.random() * 2 - 1) * 0.6) * 0.5)
            data += struct.pack('<h', max(-32767, min(32767, v)))
        wf.writeframes(data)
    return buf.getvalue()

def _play_wav_bytes(wav_bytes):
    tmp = os.path.join(os.path.expanduser('~'), '.prank_snd.wav')
    try:
        with open(tmp, 'wb') as f:
            f.write(wav_bytes)
        if _IS_WIN:
            import winsound
            winsound.PlaySound(tmp, winsound.SND_FILENAME | winsound.SND_ASYNC)
        elif _IS_MAC:
            subprocess.Popen(['afplay', tmp])
        elif _IS_LIN:
            for player in ('paplay', 'aplay', 'ffplay', 'mpg123'):
                try:
                    subprocess.Popen(
                        [player, tmp] + (['-nodisp', '-autoexit'] if player == 'ffplay' else []),
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    break
                except FileNotFoundError:
                    continue
    except Exception:
        pass

def _get_volume():
    try:
        if _IS_LIN:
            r = subprocess.run(['amixer', 'get', 'Master'], capture_output=True, text=True)
            import re; m = re.search(r'\[(\d+)%\]', r.stdout)
            return int(m.group(1)) if m else None
        elif _IS_MAC:
            r = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'],
                               capture_output=True, text=True)
            return int(r.stdout.strip())
    except Exception:
        return None

def _set_volume(pct):
    pct = max(0, min(100, int(pct)))
    try:
        if _IS_LIN:
            subprocess.run(['amixer', 'set', 'Master', f'{pct}%'], capture_output=True)
        elif _IS_MAC:
            subprocess.run(['osascript', '-e', f'set volume output volume {pct}'], capture_output=True)
    except Exception:
        pass

_XP_FREQS = [523, 659, 784, 1047]

def _sound_sabotage_loop():
    start     = time.time()
    RAMP      = 1 if HELL_MODE else 120
    saved_vol = _get_volume()
    try:
        while True:
            elapsed   = time.time() - start
            intensity = min(elapsed / RAMP, 1.0)
            roll      = random.random()

            if roll < 0.4:
                _play_wav_bytes(_gen_tone_wav(random.choice(_XP_FREQS),
                                              duration=0.3, vol=0.25 + 0.4 * intensity))
            elif roll < 0.65 * intensity:
                _play_wav_bytes(_gen_fart_wav())
            elif roll < 0.8 * intensity:
                cur = _get_volume()
                if cur is not None:
                    _set_volume(0)
                    time.sleep(0.8 if not HELL_MODE else 0.2)
                    _set_volume(min(100, cur + 30))
                    time.sleep(0.3)
                    _set_volume(cur)

            time.sleep(max(0.5, 30 * (1.0 - intensity * 0.85)) if not HELL_MODE else 1.5)
    finally:
        if saved_vol is not None:
            _set_volume(saved_vol)

def start_sound_sabotage():
    threading.Thread(target=_sound_sabotage_loop, daemon=True).start()


# ══════════════════════════════════════════════════════════════════════════════
# PRANK 11 — SLOW BURN  (desktop folders, terminal prompt, file renames)
# ══════════════════════════════════════════════════════════════════════════════

_CREEPY_FOLDERS = [
    'DO_NOT_OPEN', 'FINAL_BACKUP_2019', 'DELETE_THIS',
    'private_IMPORTANT', 'DONT_LOOK_HERE', 'system_recovery_DO_NOT_DELETE',
    'your_files_lol', 'backup_backup_backup_FINAL', 'NOT_A_VIRUS',
    'THIS_IS_FINE', 'IGNORE_THIS_FOLDER', 'temp_DELETE_ASAP',
]
_RENAME_SUFFIXES = ['_OLD', '_BACKUP', '_FINAL', '_v2', '_DO_NOT_DELETE', '_BROKEN']

def _get_desktop():
    if _IS_WIN or _IS_MAC:
        return os.path.join(os.path.expanduser('~'), 'Desktop')
    try:
        p = subprocess.run(['xdg-user-dir', 'DESKTOP'], capture_output=True, text=True).stdout.strip()
        return p if p and os.path.isdir(p) else os.path.expanduser('~/Desktop')
    except Exception:
        return os.path.expanduser('~/Desktop')

def _slow_burn_loop():
    desktop  = _get_desktop()
    interval = 5 if HELL_MODE else 300

    # Poison terminal prompt (Linux/Mac)
    if _IS_LIN or _IS_MAC:
        try:
            prompt = '\nexport PS1="\\[\\033[1;31m\\]root@NOT_YOUR_COMPUTER:\\[\\033[0m\\]\\w\\$ "\n'
            for rc in [os.path.expanduser(p) for p in ('~/.bashrc', '~/.zshrc', '~/.bash_profile')]:
                if os.path.exists(rc):
                    with open(rc, 'a') as f:
                        f.write(prompt)
                    break
        except Exception:
            pass

    used = set()
    while True:
        time.sleep(interval)

        # Drop a creepy folder on the desktop
        try:
            if os.path.isdir(desktop):
                pool = [n for n in _CREEPY_FOLDERS if n not in used] or _CREEPY_FOLDERS
                name = random.choice(pool)
                used.add(name)
                os.makedirs(os.path.join(desktop, name), exist_ok=True)
        except Exception:
            pass

        # Rename a random home file with a creepy suffix
        try:
            home  = os.path.expanduser('~')
            files = [f for f in os.listdir(home)
                     if os.path.isfile(os.path.join(home, f))
                     and not any(f.endswith(s) for s in _RENAME_SUFFIXES)
                     and not f.startswith('.')]
            if files:
                src  = os.path.join(home, random.choice(files))
                base, ext = os.path.splitext(src)
                os.rename(src, base + random.choice(_RENAME_SUFFIXES) + ext)
        except Exception:
            pass

def start_slow_burn():
    threading.Thread(target=_slow_burn_loop, daemon=True).start()


# ══════════════════════════════════════════════════════════════════════════════
# PRANK 12 — TYPING SABOTAGE  (random caps + Ctrl+Z every 20 keystrokes)
# ══════════════════════════════════════════════════════════════════════════════

_ts_count    = 0
_ts_cap_prob = 0.0

def _typing_sabotage_hook(event):
    global _ts_count, _ts_cap_prob
    if event.event_type != 'down' or event.name is None or len(event.name) != 1:
        return

    _ts_count    += 1
    _ts_cap_prob  = min(0.4, _ts_cap_prob + 0.002)

    # Random capitalisation — flips the case of the letter just typed
    if random.random() < _ts_cap_prob and event.name.isalpha():
        _kb.send('backspace')
        _sleep(0.02)
        _kb.write(event.name.upper() if event.name.islower() else event.name.lower())

    # Every 20 keystrokes: fire a Ctrl+Z undo
    if _ts_count % 20 == 0:
        _sleep(0.05)
        try:
            from pynput.keyboard import Key as _Key, Controller as _KC
            _ctrl = _KC()
            with _ctrl.pressed(_Key.ctrl):
                _ctrl.press('z')
                _ctrl.release('z')
        except Exception:
            pass

def start_typing_sabotage():
    if HAS_KEYBOARD:
        _kb.hook(_typing_sabotage_hook)


# ══════════════════════════════════════════════════════════════════════════════
# PRANK 13 — DOPPELGÄNGER CURSOR  (ghost cursor trailing behind with a delay)
# ══════════════════════════════════════════════════════════════════════════════

def _doppelganger_loop():
    try:
        import tkinter as _tk
        from pynput.mouse import Controller as _MC
    except ImportError:
        return

    mouse = _MC()
    root  = _tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.75)
    root.configure(bg='black')
    try:
        root.attributes('-transparentcolor', 'black')
    except Exception:
        pass

    SIZE   = 24
    canvas = _tk.Canvas(root, width=SIZE, height=SIZE, bg='black',
                        highlightthickness=0, cursor='none')
    canvas.pack()
    # Arrow cursor polygon
    pts = [0,0, 0,18, 4,14, 7,20, 10,19, 7,13, 12,13]
    canvas.create_polygon(pts, fill='#cccccc', outline='white', width=1)
    root.geometry(f'{SIZE}x{SIZE}+0+0')

    DELAY  = 25   # frames of lag (~0.8 s at 30 fps)
    JITTER = 4
    trail  = []

    def _tick():
        try:
            rx, ry = mouse.position
        except Exception:
            rx, ry = 0, 0
        trail.append((rx, ry))
        if len(trail) > DELAY:
            fx, fy = trail.pop(0)
            jx = fx + random.randint(-JITTER, JITTER)
            jy = fy + random.randint(-JITTER, JITTER)
            root.geometry(f'{SIZE}x{SIZE}+{jx}+{jy}')
        root.after(33, _tick)

    root.after(100, _tick)
    try:
        root.mainloop()
    except Exception:
        pass

def start_doppelganger():
    if not HAS_KEYBOARD:
        print(YELLOW + "  pynput not found — Doppelgänger unavailable." + RESET)
        return
    if not HAS_TK:
        print(YELLOW + "  tkinter not found — Doppelgänger unavailable." + RESET)
        return
    threading.Thread(target=_doppelganger_loop, daemon=True).start()

# ══════════════════════════════════════════════════════════════════════════════
# MENU + ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════════════════

def _print_menu():
    _clear()
    if HELL_MODE:
        print(RED + BOLD + "  *** HELL MODE ACTIVE — ALL DELAYS ZEROED ***\n" + RESET)
    os_tag = f"  Detected: {_os_label()}"
    kb_tag = f"  pynput: {'READY' if HAS_KEYBOARD else 'NOT INSTALLED'}"
    kb_col = GREEN if HAS_KEYBOARD else RED
    print(GREEN + """
╔══════════════════════════════════════════════════════════╗
║        ULTIMATE PRANK SUITE  v4.0  —  Cross-Platform    ║
║        "With great power comes great responsibility"     ║
╚══════════════════════════════════════════════════════════╝""" + RESET)
    print(f"  {os_tag}    {kb_col}{kb_tag}{RESET}\n")
    print(f"  {CYAN}[1]{RESET} Autocorrect Hell      — swap words silently as they type")
    print(f"  {CYAN}[2]{RESET} Haunted Keyboard      — gradual slowdown + ghost typing")
    print(f"  {CYAN}[3]{RESET} Infinite Rickroll     — browser floods + fake OS dialogs")
    print(f"  {CYAN}[4]{RESET} Fake Matrix Terminal  — full terminal hacker takeover")
    print(f"  {CYAN}[5]{RESET} Fake OS Crash         — platform-specific crash + reboot loop")
    print(f"  {CYAN}[6]{RESET} Fake Disk Wipe        — ominous deletion sequence + reveal")
    print(f"  {CYAN}[7]{RESET} Cursor Chaos          — mouse drifts & teleports (pynput)")
    print(f"  {CYAN}[8]{RESET} Fake OS Update        — fullscreen update that keeps resetting")
    print(f"  {CYAN}[9]{RESET}  Mouse Mayhem          — sensitivity, random clicks, tiny circles")
    print(f"  {CYAN}[10]{RESET} Sound Sabotage        — XP tones, farts, volume nuke")
    print(f"  {CYAN}[11]{RESET} Slow Burn             — creepy folders, prompt hijack, file renames")
    print(f"  {CYAN}[12]{RESET} Typing Sabotage       — random caps + Ctrl+Z every 20 keystrokes")
    print(f"  {CYAN}[13]{RESET} Doppelganger          — ghost cursor trailing the real one")
    print(f"  {CYAN}[A]{RESET}  ALL OF THE ABOVE      — {YELLOW}THE ULTIMATE EXPERIENCE{RESET}")
    print(f"  {CYAN}[I]{RESET} Install 'keyboard'    — auto-install missing dependency")
    print(f"  {CYAN}[Q]{RESET} Quit\n")

def run_all():
    if HELL_MODE:
        print(RED + BOLD + "\n  *** HELL MODE ACTIVATED — ALL DELAYS REMOVED ***" + RESET)
        print(RED + "  Buckle up. This is going to be fast and stupid.\n" + RESET)
        _sleep(0.5)
    if not HAS_KEYBOARD:
        print(YELLOW + "\n  Warning: 'keyboard' module not found — pranks 1 & 2 skipped.")
        print("  Select [I] from the menu to auto-install.\n" + RESET)
        _sleep(2)
    else:
        print(GREEN + "\n  Activating keyboard hooks (pranks 1 & 2)..." + RESET)
        start_autocorrect()
        start_haunted_keyboard()
        print(GREEN + "  Keyboard hooks: ACTIVE" + RESET)

    print(GREEN + "  Starting Rickroll daemon (prank 3)..." + RESET)
    start_rickroll()
    print(GREEN + "  Rickroll daemon: ACTIVE\n" + RESET)
    _sleep(1)

    print(YELLOW + "  Launching Matrix terminal takeover (prank 4)..." + RESET)
    _sleep(1.5)
    run_matrix()

    print(YELLOW + "\n  Launching Fake OS Crash sequence (prank 5)..." + RESET)
    _sleep(1.5)
    run_crash()

    print(YELLOW + "\n  Launching Fake Disk Wipe (prank 6)..." + RESET)
    _sleep(1.5)
    run_disk_wipe()

    print(YELLOW + "\n  Activating Cursor Chaos daemon (prank 7)..." + RESET)
    start_cursor_chaos()
    print(GREEN + "  Cursor Chaos: ACTIVE" + RESET)

    print(YELLOW + "\n  Launching Fake OS Update (prank 8)..." + RESET)
    _sleep(1.5)
    run_fake_update()

    print(YELLOW + "\n  Activating Mouse Mayhem (prank 9)..." + RESET)
    start_mouse_mayhem()
    print(GREEN + "  Mouse Mayhem: ACTIVE" + RESET)

    print(YELLOW + "\n  Activating Sound Sabotage (prank 10)..." + RESET)
    start_sound_sabotage()
    print(GREEN + "  Sound Sabotage: ACTIVE" + RESET)

    print(YELLOW + "\n  Activating Slow Burn (prank 11)..." + RESET)
    start_slow_burn()
    print(GREEN + "  Slow Burn: ACTIVE (works quietly in background)" + RESET)

    if HAS_KEYBOARD:
        print(YELLOW + "\n  Activating Typing Sabotage (prank 12)..." + RESET)
        start_typing_sabotage()
        print(GREEN + "  Typing Sabotage: ACTIVE" + RESET)

    print(YELLOW + "\n  Activating Doppelganger Cursor (prank 13)..." + RESET)
    start_doppelganger()
    print(GREEN + "  Doppelganger: ACTIVE" + RESET)

    print(CYAN + BOLD + "\n  All pranks complete! You are a certified menace.")
    print("  (all daemons running: rickroll, cursor chaos, mouse mayhem, sound, slow burn, doppelganger)")
    print("  Press Ctrl+C to fully stop everything.\n" + RESET)
    try:
        while True:
            _sleep(1)
    except KeyboardInterrupt:
        print(GREEN + "\n  Daemon stopped. Go apologise to your friend.\n" + RESET)

def main():
    if _ARGS.help:
        print(__doc__)
        sys.exit(0)

    _print_menu()

    if HELL_MODE:
        print(YELLOW + "  --hell flag detected. Launching everything NOW.\n" + RESET)
        _sleep(0.8)
        run_all()
        sys.exit(0)

    while True:
        try:
            choice = input("  Your choice: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print(GREEN + "\n  Exiting. Stay chaotic.\n" + RESET)
            sys.exit(0)

        if choice == '1':
            if not HAS_KEYBOARD:
                print(RED + "  keyboard not found — press [I] to install\n" + RESET); continue
            start_autocorrect()
            print(GREEN + "  Autocorrect Hell activated. Ctrl+C to stop.\n" + RESET)
            try:
                _kb.wait()
            except KeyboardInterrupt:
                _kb.unhook_all()
                print(GREEN + "\n  Stopped.\n" + RESET)

        elif choice == '2':
            if not HAS_KEYBOARD:
                print(RED + "  keyboard not found — press [I] to install\n" + RESET); continue
            start_haunted_keyboard()
            print(GREEN + "  Haunted Keyboard activated. Ramps up over 4 minutes.\n" + RESET)
            try:
                _kb.wait()
            except KeyboardInterrupt:
                _kb.unhook_all()
                print(GREEN + "\n  Stopped.\n" + RESET)

        elif choice == '3':
            start_rickroll()
            print(GREEN + "  Rickroll daemon active. Ctrl+C to stop.\n" + RESET)
            try:
                while True: _sleep(1)
            except KeyboardInterrupt:
                print(GREEN + "\n  Stopped (tabs already open though).\n" + RESET)

        elif choice == '4':
            run_matrix(); print()

        elif choice == '5':
            run_crash(); print()

        elif choice == '6':
            run_disk_wipe(); print()

        elif choice == '7':
            start_cursor_chaos()
            print(GREEN + "  Cursor Chaos active. Mouse will drift over time. Ctrl+C to stop.\n" + RESET)
            try:
                while True: _sleep(1)
            except KeyboardInterrupt:
                print(GREEN + "\n  Stopped.\n" + RESET)

        elif choice == '8':
            run_fake_update(); print()

        elif choice == '9':
            start_mouse_mayhem()
            print(GREEN + '  Mouse Mayhem active. Ramps up over 90 seconds. Ctrl+C to stop.\n' + RESET)
            try:
                while True: _sleep(1)
            except KeyboardInterrupt:
                print(GREEN + '\n  Stopped.\n' + RESET)

        elif choice == '10':
            start_sound_sabotage()
            print(GREEN + '  Sound Sabotage active. Ctrl+C to stop.\n' + RESET)
            try:
                while True: _sleep(1)
            except KeyboardInterrupt:
                print(GREEN + '\n  Stopped.\n' + RESET)

        elif choice == '11':
            start_slow_burn()
            print(GREEN + '  Slow Burn active (every 5 min). Ctrl+C to stop.\n' + RESET)
            try:
                while True: _sleep(1)
            except KeyboardInterrupt:
                print(GREEN + '\n  Stopped.\n' + RESET)

        elif choice == '12':
            if not HAS_KEYBOARD:
                print(RED + '  pynput not found — press [I] to install\n' + RESET); continue
            start_typing_sabotage()
            print(GREEN + '  Typing Sabotage active. Ctrl+C to stop.\n' + RESET)
            try:
                _kb.wait()
            except KeyboardInterrupt:
                _kb.unhook_all()
                print(GREEN + '\n  Stopped.\n' + RESET)

        elif choice == '13':
            start_doppelganger()
            print(GREEN + '  Doppelganger active. Close the ghost window to stop.\n' + RESET)
            try:
                while True: _sleep(1)
            except KeyboardInterrupt:
                print(GREEN + '\n  Stopped.\n' + RESET)

        elif choice in ('a', 'all'):
            run_all(); break

        elif choice == 'i':
            _auto_install_pynput()

        elif choice == 'q':
            print(GREEN + "\n  Goodbye! Stay chaotic.\n" + RESET)
            sys.exit(0)

        else:
            print(YELLOW + "  Invalid choice. Try 1-13, A, I, or Q.\n" + RESET)

        _print_menu()

if __name__ == '__main__':
    main()
