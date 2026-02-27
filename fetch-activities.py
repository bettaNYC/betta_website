#!/usr/bin/env python3
"""
Fetches recent Strava activities and saves them to activities.json.
Run by GitHub Actions on a schedule so GitHub Pages always has fresh data.
"""
import os
import json
import requests

CLIENT_ID     = os.environ['STRAVA_CLIENT_ID']
CLIENT_SECRET = os.environ['STRAVA_CLIENT_SECRET']
REFRESH_TOKEN = os.environ['STRAVA_REFRESH_TOKEN']

def get_access_token():
    res = requests.post('https://www.strava.com/oauth/token', json={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    })
    res.raise_for_status()
    return res.json()['access_token']

def format_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m}:{s:02d}"

def calculate_pace(distance_m, time_s):
    if distance_m == 0 or time_s == 0:
        return '-'
    pace_s = time_s / (distance_m / 1000)
    return f"{int(pace_s // 60)}:{int(pace_s % 60):02d}/km"

token = get_access_token()
res = requests.get(
    'https://www.strava.com/api/v3/athlete/activities',
    headers={'Authorization': f'Bearer {token}'},
    params={'per_page': 6}
)
res.raise_for_status()

activities = []
for a in res.json():
    activities.append({
        'date':         a['start_date_local'].split('T')[0],
        'distance_km':  f"{a['distance'] / 1000:.2f}",
        'time':         format_time(a['moving_time']),
        'moving_time':  a['moving_time'],
        'pace':         calculate_pace(a['distance'], a['moving_time']),
        'map':          a.get('map', {}).get('summary_polyline') or None,
        'name':         a.get('name') or a.get('type', 'Activity'),
        'type':         a.get('type', 'Workout')
    })

with open('activities.json', 'w') as f:
    json.dump(activities, f)

print(f"Saved {len(activities)} activities to activities.json")
