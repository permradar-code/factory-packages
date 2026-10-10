#!/usr/bin/env python3
"""Sound for the animated SUBSCRIBE badge (subscribe_badge.py, 5.5 s): a soft mouse click when the cursor
presses the button (t = 1.62 s) and a clear two-strike hand-bell "ding-ding" while the bell icon rings
(t = 1.85 s and 2.12 s). Without sound the badge is easy to miss.

Writes a 5.5 s 48 kHz stereo WAV aligned to the badge: drop it into the mix at the same second as the badge.
Peak about -9 dBFS before the final loudnorm: clearly audible over dialogue and music, not shrill.

Usage: python3 subscribe_bell.py --out bell.wav
"""
import argparse, math, struct, wave

RATE, DUR = 48000, 5.5
CLICK_AT, DINGS = 1.62, ((1.85, 1.0), (2.12, 0.75))
F0 = 1568.0                                    # G6, a small brass hand bell
PARTIALS = ((1.0, 1.0, 0.9), (2.0, 0.55, 0.6), (2.76, 0.35, 0.45), (5.40, 0.18, 0.25), (8.93, 0.08, 0.15))
PEAK = 10 ** (-9 / 20)


def render():
    n = int(RATE * DUR)
    buf = [0.0] * n
    # click: 6 ms burst of a damped 3 kHz tone, quiet
    s0 = int(CLICK_AT * RATE)
    for i in range(int(0.006 * RATE)):
        t = i / RATE
        buf[s0 + i] += 0.25 * math.sin(2 * math.pi * 3000 * t) * math.exp(-t / 0.0015)
    for at, gain in DINGS:
        s0 = int(at * RATE)
        for i in range(int(1.4 * RATE)):
            if s0 + i >= n:
                break
            t = i / RATE
            attack = min(1.0, t / 0.002)
            v = sum(a * math.sin(2 * math.pi * F0 * r * t) * math.exp(-t / tau) for r, a, tau in PARTIALS)
            buf[s0 + i] += gain * attack * v
    m = max(abs(x) for x in buf) or 1.0
    return [x / m * PEAK for x in buf]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    data = render()
    with wave.open(a.out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<hh", int(x * 32767), int(x * 32767)) for x in data))
    print(a.out)


if __name__ == "__main__":
    main()
