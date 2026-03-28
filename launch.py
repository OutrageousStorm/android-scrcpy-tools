#!/usr/bin/env python3
"""
launch.py -- Interactive scrcpy launcher with presets
Usage: python3 launch.py [profile]
       python3 launch.py gaming
       python3 launch.py record
"""
import subprocess, sys, shutil

if not shutil.which("scrcpy"):
    print("scrcpy not found. Install: https://github.com/Genymobile/scrcpy")
    sys.exit(1)

PROFILES = {
    "default": {
        "desc": "Standard mirror — 1080p, no audio",
        "args": ["--max-size", "1080", "--stay-awake"],
    },
    "gaming": {
        "desc": "Low latency gaming — no video buffer, max fps",
        "args": ["--max-size", "1080", "--max-fps", "60",
                 "--video-codec", "h265", "--video-bit-rate", "8M",
                 "--stay-awake", "--disable-screensaver"],
    },
    "record": {
        "desc": "Record screen to file",
        "args": ["--record", f"recording_{__import__('time').strftime('%Y%m%d_%H%M%S')}.mp4",
                 "--max-size", "1080", "--stay-awake"],
    },
    "audio": {
        "desc": "Mirror with audio (Android 11+)",
        "args": ["--max-size", "1080", "--audio-codec", "aac", "--stay-awake"],
    },
    "nocamera": {
        "desc": "Mirror without turning camera on — borderless window",
        "args": ["--max-size", "1080", "--window-borderless", "--stay-awake"],
    },
    "tiny": {
        "desc": "Small window for multitasking",
        "args": ["--max-size", "480", "--window-x", "0", "--window-y", "0",
                 "--window-width", "270", "--stay-awake"],
    },
    "landscape": {
        "desc": "Force landscape orientation",
        "args": ["--lock-video-orientation", "1", "--max-size", "1080", "--stay-awake"],
    },
}

def run_profile(name):
    p = PROFILES.get(name)
    if not p:
        print(f"Unknown profile: {name}")
        print_profiles()
        return
    print(f"\n🖥️  scrcpy — {p['desc']}")
    cmd = ["scrcpy"] + p["args"]
    print(f"  Running: {' '.join(cmd)}\n")
    subprocess.run(cmd)

def print_profiles():
    print("\nAvailable profiles:")
    for name, p in PROFILES.items():
        print(f"  {name:<12} {p['desc']}")

def main():
    if len(sys.argv) > 1:
        run_profile(sys.argv[1])
        return

    print_profiles()
    print("\nEnter profile name (or 'q' to quit):")
    choice = input("> ").strip()
    if choice != 'q':
        run_profile(choice)

if __name__ == "__main__":
    main()
