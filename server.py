#!/usr/bin/env python3
"""
Combined web server and Strava proxy - serves everything from same origin to avoid CORS issues
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import requests
from flask import Flask, jsonify
from flask_cors import CORS
import threading

# Strava API Configuration
STRAVA_CONFIG = {
    'CLIENT_ID': '184712',
    'CLIENT_SECRET': '9a5f16cc1a3e830cd8a3e7a2e516f492a6b8ae09',
    'REFRESH_TOKEN': 'e95c9739e3b3da0e423e5348c0d4dea12c57f2d5'
}

# Flask app for API
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def get_access_token():
    """Get a new access token from Strava using refresh token"""
    response = requests.post('https://www.strava.com/oauth/token', json={
        'client_id': STRAVA_CONFIG['CLIENT_ID'],
        'client_secret': STRAVA_CONFIG['CLIENT_SECRET'],
        'refresh_token': STRAVA_CONFIG['REFRESH_TOKEN'],
        'grant_type': 'refresh_token'
    })
    
    if response.status_code != 200:
        error_msg = f'Failed to refresh access token: {response.status_code}'
        try:
            error_data = response.json()
            if 'message' in error_data:
                error_msg += f" - {error_data['message']}"
        except:
            pass
        raise Exception(error_msg)
    
    return response.json()['access_token']

def format_time(seconds):
    """Format time in seconds to HH:MM:SS or MM:SS"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"

def calculate_pace(distance_meters, time_seconds):
    """Calculate pace in min/km format"""
    if distance_meters == 0 or time_seconds == 0:
        return '-'
    
    distance_km = distance_meters / 1000
    pace_seconds_per_km = time_seconds / distance_km
    minutes = int(pace_seconds_per_km // 60)
    seconds = int(pace_seconds_per_km % 60)
    
    return f"{minutes}:{seconds:02d}/km"

@app.route('/api/strava/activities', methods=['GET', 'OPTIONS'])
def get_activities():
    """Proxy endpoint to fetch Strava activities"""
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    try:
        access_token = get_access_token()
        per_page = request.args.get('per_page', 30, type=int)
        
        response = requests.get(
            'https://www.strava.com/api/v3/athlete/activities',
            headers={'Authorization': f'Bearer {access_token}'},
            params={'per_page': per_page}
        )
        
        if response.status_code != 200:
            return jsonify({'error': f'Strava API error: {response.status_code}'}), response.status_code
        
        activities = response.json()
        
        # Filter only runs
        runs = [activity for activity in activities if activity.get('type') == 'Run']
        
        # Transform to our format
        formatted_runs = []
        for activity in runs:
            formatted_runs.append({
                'date': activity['start_date_local'].split('T')[0],
                'distance_km': f"{(activity['distance'] / 1000):.2f}",
                'time': format_time(activity['moving_time']),
                'pace': calculate_pace(activity['distance'], activity['moving_time']),
                'map': activity.get('map', {}).get('summary_polyline') or None,
                'name': activity.get('name') or 'Run'
            })
        
        result = jsonify(formatted_runs)
        result.headers.add('Access-Control-Allow-Origin', '*')
        result.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        result.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return result
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_flask():
    """Run Flask app on port 5000"""
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    print("=" * 60)
    print("Starting combined server...")
    print("=" * 60)
    print("Web server: http://localhost:8000")
    print("API proxy: http://localhost:5000")
    print("=" * 60)
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Start simple HTTP server for static files
    print("\nStarting web server on port 8000...")
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    print("✅ Web server running at http://localhost:8000")
    print("✅ API proxy running at http://localhost:5000")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        httpd.shutdown()

