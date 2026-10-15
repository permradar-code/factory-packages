#!/usr/bin/env python3
"""Russian SRT for film 4 «The Widow's Rifle», timed to the factory render.

Inputs (same folder):
  events.json   — [id, from_s, to_s] from film_timeline of the final render
  en_cues.json  — [from_s, to_s, text] English subtitles/long.srt (via film_short_scenes)
  ../../briefs/western_widows_rifle/ru_lines.json — translation, key = timeline id

Rules: a line/narration block gets the English cues inside its window; RU and EN
are split into sentences — if counts match, RU sentence i takes EN sentence i's
time, otherwise RU is spread over the speech window by length. Cue ≤ 2 lines of
~42 chars and ≤ ~6.5 s. Output: briefs/western_widows_rifle/long_ru.srt
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
events = json.loads((HERE / "events.json").read_text())
en = json.loads((HERE / "en_cues.json").read_text())
ru = json.loads((ROOT / "briefs/western_widows_rifle/ru_lines.json").read_text())
OUT = ROOT / "briefs/western_widows_rifle/long_ru.srt"

LINE, MAXC, MAXD, MIND = 42, 84, 6.5, 1.0
ABBR = {"Mr.", "Mrs.", "Dr.", "Дж.", "St."}


def sentences(text):
    toks = text.split()
    out, cur = [], []
    for i, t in enumerate(toks):
        cur.append(t)
        nxt = toks[i + 1] if i + 1 < len(toks) else None
        if nxt is None:
            break
        if re.search(r"[.!?…]['\"»]?$", t) and t not in ABBR and re.match(r"[«\"A-ZА-ЯЁ—]", nxt):
            if t.endswith("...") and not re.match(r"[A-ZА-ЯЁ]", nxt):
                continue
            out.append(" ".join(cur)); cur = []
    if cur:
        out.append(" ".join(cur))
    return out


def en_sentence_spans(cues):
    """Time span of every EN sentence, by char interpolation inside cues."""
    text, marks = "", []  # marks: (char_start, char_end, t0, t1)
    for a, b, t in cues:
        if text:
            text += " "
        s = len(text); text += t; marks.append((s, len(text), a, b))

    def t_at(pos, end=False):
        for s, e, a, b in marks:
            if s <= pos <= e:
                return a + (b - a) * (pos - s) / max(1, e - s)
        return marks[-1][3] if end else marks[0][2]

    spans, pos = [], 0
    for sen in sentences(text):
        i = text.index(sen, pos)
        spans.append((t_at(i), t_at(i + len(sen), True)))
        pos = i + len(sen)
    return spans


def split_long(text, a, b):
    """Split a RU sentence into pieces that fit ≤ MAXC chars and ≤ MAXD s."""
    if (len(text) <= MAXC and b - a <= MAXD) or " " not in text:
        return [(text, a, b)]
    mid, best = len(text) / 2, None
    for m in re.finditer(" ", text):
        i = m.start()
        punct = re.search(r"[,;:—]$", text[:i]) is not None or text[i + 1:i + 2] == "—"
        last = text[:i].split()[-1]
        weak = len(last) <= 2 and last.isalpha() and last.islower()
        score = abs(i - mid) / len(text) - (0.18 if punct else 0) + (0.15 if weak else 0)
        if best is None or score < best[0]:
            best = (score, i)
    i = best[1]
    l, r = text[:i], text[i + 1:]
    tm = a + (b - a) * len(l) / (len(l) + len(r))
    return split_long(l, a, tm) + split_long(r, tm, b)


def spread(sens, a, b):
    total = sum(len(s) for s in sens)
    out, t = [], a
    for s in sens:
        d = (b - a) * len(s) / total
        out.append((s, t, t + d)); t += d
    return out


def wrap(text):
    if len(text) <= LINE:
        return text
    best = None
    for m in re.finditer(" ", text):
        i = m.start(); l1, l2 = text[:i], text[i + 1:]
        last = l1.split()[-1]
        score = max(len(l1), len(l2)) + (0 if re.search(r"[,.;:!?—]$", l1) else 3)
        if last.lower() in {"мистер", "миссис", "мисс", "джона", "клэй", "томми", "ханна", "эмброуз"}:
            score += 12  # keep "миссис Коул" together
        if len(last) <= 2 and last.isalpha() and last.islower():
            score += 5  # no hanging "и", "со", "на" at line end
        if best is None or score < best[0]:
            best = (score, l1, l2)
    return best[1] + "\n" + best[2]


cues = []
for eid, f, t in events:
    if eid not in ru:
        continue
    inside = [c for c in en if f - 0.05 <= (c[0] + c[1]) / 2 <= t + 0.05]
    rs = sentences(ru[eid])
    if inside:
        a, b = inside[0][0], inside[-1][1]
        es = en_sentence_spans(inside)
        if len(es) == len(rs):
            parts = [(s, x, y) for s, (x, y) in zip(rs, es)]
        else:
            parts = spread(rs, a, b)
    else:  # title card T02: whole card time
        a, b = f + 0.1, t - 0.1
        parts = spread(rs, a, b)
    block = []
    for s, x, y in parts:
        block += split_long(s, x, y)
    # merge too-short neighbours inside one event ("Рид." + "Джона Рид.")
    merged = []
    for p in block:
        if merged:
            q = merged[-1]
            short = (q[2] - q[1] < MIND) or (p[2] - p[1] < MIND)
            dialogue = eid.startswith("C")  # one speaker per clip: keep a line together
            joined = q[0] + " " + p[0]
            fits = max(map(len, wrap(joined).split("\n"))) <= 44
            if (short or dialogue) and len(joined) <= MAXC and fits and p[2] - q[1] <= MAXD:
                merged[-1] = (q[0] + " " + p[0], q[1], p[2]); continue
        merged.append(p)
    cues += [(x, y, s, eid) for s, x, y in merged]

# no overlaps, minimum readable length when there is room
cues.sort(key=lambda c: c[0])
fixed = []
for i, (a, b, s, eid) in enumerate(cues):
    nxt = cues[i + 1][0] if i + 1 < len(cues) else b + 5
    if b - a < MIND:
        b = min(a + MIND, nxt - 0.04)
    b = min(b, nxt - 0.04)
    fixed.append((a, b, s, eid))


def ts(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


lines = []
for n, (a, b, s, eid) in enumerate(fixed, 1):
    lines.append(f"{n}\n{ts(a)} --> {ts(b)}\n{wrap(s)}\n")
OUT.write_text("\n".join(lines), encoding="utf-8")

# report
issues = []
for a, b, s, eid in fixed:
    w = wrap(s).split("\n")
    if len(w) > 2 or max(map(len, w)) > 46:
        issues.append(f"{eid} long text: {s}")
    if b - a > 7.0:
        issues.append(f"{eid} long cue {b-a:.1f}s")
    if b - a < 0.8:
        issues.append(f"{eid} short cue {b-a:.2f}s: {s}")
used = {c[3] for c in fixed}
missing = [k for k in ru if k not in used]
print(f"cues: {len(fixed)}  missing ids: {missing}")
print("\n".join(issues) or "no issues")
