# Put your Strava GPX files here

This folder feeds your running page — no Strava API or subscription needed.

## How to update your runs

1. Open an activity on Strava → **"..." menu → Export GPX** (this is free).
2. Save the `.gpx` file into **this folder**.
3. Repeat for each run/ride you want to show (the page shows the 6 most recent).
4. From the project folder, run:

   ```bash
   python3 gpx-to-activities.py
   ```

   That rebuilds `activities.json`. Commit and push (or ask Claude to).

## Naming tip

To control how an activity is labelled, include a word in the file name:

| File name contains        | Shown as   |
| ------------------------- | ---------- |
| `ride`, `bike`, or `cycl` | Cycling    |
| `hike`                    | Hiking     |
| `walk`                    | Walking    |
| `swim`                    | Swimming   |
| anything else             | Running    |

If the GPX file already records the sport type, that takes priority.
