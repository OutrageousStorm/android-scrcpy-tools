#!/usr/bin/env python3
"""
automate.py -- Replay tap/swipe/key sequences on Android via ADB
Define automation scripts in JSON and play them back.
Usage: python3 automate.py --script scripts/swipe_test.json
       python3 automate.py --record   (interactive recorder)

Script format:
[
  {"action": "tap",   "x": 540, "y": 960, "delay": 0.5},
  {"action": "swipe", "x1": 540, "y1": 1500, "x2": 540, "y2": 500, "duration": 300},
  {"action": "key",   "code": 4, "delay": 0.3},
  {"action": "text",  "input": "hello world", "delay": 0.5},
  {"action": "wait",  "seconds": 2}
]
"""
import subprocess, json, time, argparse, sys
from datetime import datetime

def adb(cmd):
    subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True)

def tap(x, y):
    adb(f"input tap {x} {y}")

def swipe(x1, y1, x2, y2, duration=300):
    adb(f"input swipe {x1} {y1} {x2} {y2} {duration}")

def key(code):
    adb(f"input keyevent {code}")

def text(t):
    escaped = t.replace(" ", "%s").replace("'", "\\'")
    adb(f"input text '{escaped}'")

KEYCODES = {
    "home": 3, "back": 4, "power": 26, "vol_up": 24, "vol_down": 25,
    "enter": 66, "delete": 67, "tab": 61, "menu": 82, "app_switch": 187,
}

def play_script(steps, repeat=1, delay_mult=1.0):
    print(f"\n▶️  Playing {len(steps)} steps × {repeat}")
    for r in range(repeat):
        if repeat > 1: print(f"\n  Run {r+1}/{repeat}")
        for i, step in enumerate(steps):
            action = step.get("action", "")
            delay = step.get("delay", 0) * delay_mult

            if action == "tap":
                print(f"  [{i+1}] tap({step['x']}, {step['y']})")
                tap(step["x"], step["y"])
            elif action == "swipe":
                dur = step.get("duration", 300)
                print(f"  [{i+1}] swipe ({step['x1']},{step['y1']}) → ({step['x2']},{step['y2']}) {dur}ms")
                swipe(step["x1"], step["y1"], step["x2"], step["y2"], dur)
            elif action == "key":
                code = step.get("code") or KEYCODES.get(step.get("name", ""), 0)
                print(f"  [{i+1}] key({code})")
                key(code)
            elif action == "text":
                print(f"  [{i+1}] text: {step['input'][:30]}")
                text(step["input"])
            elif action == "wait":
                secs = step.get("seconds", 1)
                print(f"  [{i+1}] wait {secs}s")
                time.sleep(secs)
                continue
            elif action == "screenshot":
                fname = step.get("file", f"screenshot_{datetime.now().strftime('%H%M%S')}.png")
                subprocess.run(f"adb exec-out screencap -p > {fname}", shell=True)
                print(f"  [{i+1}] screenshot → {fname}")

            if delay > 0:
                time.sleep(delay)

    print("\n✅ Done.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", help="JSON script file to play")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--speed", type=float, default=1.0, help="Delay multiplier (0.5=fast, 2.0=slow)")
    args = parser.parse_args()

    if not args.script:
        print("Usage: python3 automate.py --script <file.json>")
        print('\nExample script saved to: example_script.json')
        with open("example_script.json", "w") as f:
            json.dump([
                {"action": "tap",   "x": 540, "y": 960, "delay": 0.5},
                {"action": "swipe", "x1": 540, "y1": 1500, "x2": 540, "y2": 500, "duration": 400, "delay": 0.5},
                {"action": "key",   "name": "home", "delay": 0.3},
                {"action": "wait",  "seconds": 1},
                {"action": "screenshot", "file": "result.png"},
            ], f, indent=2)
        return

    with open(args.script) as f:
        steps = json.load(f)
    play_script(steps, repeat=args.repeat, delay_mult=args.speed)

if __name__ == "__main__":
    main()
