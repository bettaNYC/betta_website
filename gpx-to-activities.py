#!/usr/bin/env python3
"""
Build activities.json for the running page from Strava GPX exports.

No Strava API, no tokens, no subscription needed. Only Python's standard
library is used, so you can run it with a plain `python3` — nothing to install.

------------------------------------------------------------------------------
HOW TO USE (no coding needed)
------------------------------------------------------------------------------
1. On any Strava activity page, open the "..." menu and choose "Export GPX".
   (This is free and separate from the paid API.) Save the .gpx file into the
   `gpx/` folder that sits next to this script.

2. Do that for each run/ride you want to show. The page shows the most recent
   few, so a handful is plenty.

   Tip: to control how an activity is labelled, put a hint in the file name:
     - contains "ride", "bike" or "cycl"  -> shown as Cycling
     - contains "hike"                    -> shown as Hiking
     - contains "walk"                    -> shown as Walking
     - contains "swim"                    -> shown as Swimming
     - anything else                      -> shown as Running
   (If the GPX file already records the sport type, that wins over the name.)

3. In Terminal, from this project folder, run:

       python3 gpx-to-activities.py

   It rewrites activities.json. Then commit & push the change (or ask Claude to).

Everything below is the machinery — you don't need to read it.
"""

import os
import re
import json
import glob
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from math import radians, sin, cos, sqrt, atan2

HERE = os.path.dirname(os.path.abspath(__file__))
GPX_DIR = os.path.join(HERE, "gpx")
OUTPUT = os.path.join(HERE, "activities.json")

MAX_ACTIVITIES = 6    # how many of the most recent activities to publish
MAX_POINTS = 300      # simplify each route to at most this many points

TYPE_LABELS = {  # just so warnings read nicely; the page has its own map
    "Run": "Running", "Ride": "Cycling", "Hike": "Hiking",
    "Walk": "Walking", "Swim": "Swimming",
}


def strip_ns(tag):
    """'{http://...}trkpt' -> 'trkpt' so we don't care about GPX namespaces."""
    return tag.rsplit("}", 1)[-1]


def findall_local(elem, name):
    return [e for e in elem.iter() if strip_ns(e.tag) == name]


def parse_time(text):
    if not text:
        return None
    text = text.strip()
    # Handle the trailing 'Z' and offsets; normalise to aware UTC.
    try:
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def haversine_m(a, b):
    R = 6371000.0  # metres
    lat1, lon1, lat2, lon2 = map(radians, (a[0], a[1], b[0], b[1]))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * R * atan2(sqrt(h), sqrt(1 - h))


def encode_polyline(points):
    """Google encoded-polyline format — exactly what running.html decodes."""
    out = []
    prev_lat = prev_lon = 0
    for lat, lon in points:
        lat_e5 = int(round(lat * 1e5))
        lon_e5 = int(round(lon * 1e5))
        for delta in (lat_e5 - prev_lat, lon_e5 - prev_lon):
            delta = ~(delta << 1) if delta < 0 else (delta << 1)
            while delta >= 0x20:
                out.append(chr((0x20 | (delta & 0x1F)) + 63))
                delta >>= 5
            out.append(chr(delta + 63))
        prev_lat, prev_lon = lat_e5, lon_e5
    return "".join(out)


def downsample(points, limit):
    if len(points) <= limit:
        return points
    step = len(points) / limit
    picked = [points[int(i * step)] for i in range(limit)]
    if picked[-1] != points[-1]:
        picked[-1] = points[-1]
    return picked


def fmt_time(seconds):
    seconds = int(round(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m}:{s:02d}"


def pace_per_km(distance_m, seconds):
    if distance_m <= 0 or seconds <= 0:
        return "-"
    p = seconds / (distance_m / 1000.0)
    return f"{int(p // 60)}:{int(p % 60):02d}/km"


def type_from_gpx_value(value):
    if not value:
        return None
    v = value.strip().lower()
    if any(k in v for k in ("ride", "bike", "cycl")):
        return "Ride"
    if "hik" in v:
        return "Hike"
    if "walk" in v:
        return "Walk"
    if "swim" in v:
        return "Swim"
    if "run" in v:
        return "Run"
    return None  # unknown / numeric sport id


def type_from_filename(path):
    name = os.path.basename(path).lower()
    if any(k in name for k in ("ride", "bike", "cycl")):
        return "Ride"
    if "hike" in name:
        return "Hike"
    if "walk" in name:
        return "Walk"
    if "swim" in name:
        return "Swim"
    return None


def parse_gpx(path):
    tree = ET.parse(path)
    root = tree.getroot()

    coords, times = [], []
    for pt in findall_local(root, "trkpt"):
        try:
            lat = float(pt.attrib["lat"])
            lon = float(pt.attrib["lon"])
        except (KeyError, ValueError):
            continue
        coords.append((lat, lon))
        t = None
        for child in pt:
            if strip_ns(child.tag) == "time":
                t = parse_time(child.text)
                break
        times.append(t)

    if not coords:
        return None

    # Distance from every point (not the downsampled route) for accuracy.
    distance_m = sum(haversine_m(coords[i - 1], coords[i]) for i in range(1, len(coords)))

    stamped = [t for t in times if t is not None]
    if stamped:
        elapsed = (max(stamped) - min(stamped)).total_seconds()
        start_dt = min(stamped)
    else:
        elapsed = 0
        # Fall back to <metadata><time> or the file's modification date.
        meta = findall_local(root, "time")
        start_dt = parse_time(meta[0].text) if meta else None
        if start_dt is None:
            start_dt = datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc)

    # Sport type: GPX <type> wins, then filename hint, then default to Run.
    gpx_type = None
    trk_types = findall_local(root, "type")
    if trk_types:
        gpx_type = type_from_gpx_value(trk_types[0].text)
    activity_type = gpx_type or type_from_filename(path) or "Run"

    # Name: GPX <name> wins, else a readable version of the filename.
    name = None
    names = findall_local(root, "name")
    if names and names[0].text and names[0].text.strip():
        name = names[0].text.strip()
    if not name:
        stem = re.sub(r"\.gpx$", "", os.path.basename(path), flags=re.I)
        stem = re.sub(r"[_\-]+", " ", stem).strip()
        name = stem.title() if stem else TYPE_LABELS.get(activity_type, activity_type)

    route = downsample(coords, MAX_POINTS)

    return {
        "date": start_dt.strftime("%Y-%m-%d"),
        "distance_km": f"{distance_m / 1000:.2f}",
        "time": fmt_time(elapsed),
        "moving_time": int(round(elapsed)),
        "pace": pace_per_km(distance_m, elapsed),
        "map": encode_polyline(route) if len(route) > 1 else None,
        "name": name,
        "type": activity_type,
        "_sort": start_dt,          # internal, stripped before writing
        "_gpx_type_known": gpx_type is not None,
        "_has_time": bool(stamped),
    }


def main():
    if not os.path.isdir(GPX_DIR):
        os.makedirs(GPX_DIR)
    files = sorted(glob.glob(os.path.join(GPX_DIR, "*.gpx")))
    if not files:
        print(f"No .gpx files found in {GPX_DIR}/")
        print("Export activities from Strava (activity page -> ... -> Export GPX),")
        print("drop the files into that folder, then run this script again.")
        return

    parsed = []
    for path in files:
        try:
            activity = parse_gpx(path)
        except ET.ParseError as e:
            print(f"  ! Skipped {os.path.basename(path)} (not valid GPX: {e})")
            continue
        if not activity:
            print(f"  ! Skipped {os.path.basename(path)} (no track points)")
            continue
        parsed.append(activity)
        warn = ""
        if not activity["_gpx_type_known"]:
            warn += f"  [type guessed as {activity['type']} — rename file to change]"
        if not activity["_has_time"]:
            warn += "  [no timestamps in GPX — time/pace unavailable]"
        print(f"  + {os.path.basename(path)}: {activity['name']} "
              f"({activity['distance_km']} km, {activity['time']}){warn}")

    parsed.sort(key=lambda a: a["_sort"], reverse=True)
    published = parsed[:MAX_ACTIVITIES]

    clean = []
    for a in published:
        clean.append({k: a[k] for k in
                      ("date", "distance_km", "time", "moving_time",
                       "pace", "map", "name", "type")})

    with open(OUTPUT, "w") as f:
        json.dump(clean, f)

    print(f"\nWrote {len(clean)} activit{'y' if len(clean) == 1 else 'ies'} "
          f"to {os.path.relpath(OUTPUT, HERE)} "
          f"(from {len(parsed)} GPX file{'s' if len(parsed) != 1 else ''}).")
    if len(parsed) > MAX_ACTIVITIES:
        print(f"Only the {MAX_ACTIVITIES} most recent are published "
              f"(change MAX_ACTIVITIES near the top to adjust).")


if __name__ == "__main__":
    main()
