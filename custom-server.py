#!/usr/bin/env python3
"""
Custom HTTP server that serves static files AND handles Strava API requests
This avoids CORS issues by serving everything from the same origin (port 8000)
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import requests
import os

# Strava API Configuration
STRAVA_CONFIG = {
    'CLIENT_ID': '184712',
    'CLIENT_SECRET': '9a5f16cc1a3e830cd8a3e7a2e516f492a6b8ae09',
    'REFRESH_TOKEN': 'e95c9739e3b3da0e423e5348c0d4dea12c57f2d5'
}

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

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        # Handle Strava API endpoint
        if parsed_path.path == '/api/strava/activities':
            self.handle_strava_api(parsed_path)
        else:
            # Serve static files
            self.serve_static_file(parsed_path.path)
    
    def handle_strava_api(self, parsed_path):
        """Handle Strava API requests"""
        try:
            # Parse query parameters
            query_params = parse_qs(parsed_path.query)
            per_page = int(query_params.get('per_page', [30])[0])
            
            # Get access token
            access_token = get_access_token()
            
            # Fetch activities from Strava
            response = requests.get(
                'https://www.strava.com/api/v3/athlete/activities',
                headers={'Authorization': f'Bearer {access_token}'},
                params={'per_page': per_page}
            )
            
            if response.status_code != 200:
                self.send_error_response(response.status_code, {'error': f'Strava API error: {response.status_code}'})
                return
            
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
            
            self.send_json_response(formatted_runs)
            
        except Exception as e:
            self.send_error_response(500, {'error': str(e)})
    
    def serve_static_file(self, path):
        """Serve static files"""
        # Default to index.html if root
        if path == '/':
            path = '/index.html'
        
        # Remove leading slash
        file_path = path.lstrip('/')
        
        # Security: prevent directory traversal
        if '..' in file_path or file_path.startswith('/'):
            self.send_error(403, "Forbidden")
            return
        
        # Check if file exists
        if not os.path.exists(file_path):
            self.send_error(404, "File not found")
            return
        
        # Determine content type
        content_type = 'text/html'
        if file_path.endswith('.js'):
            content_type = 'application/javascript'
        elif file_path.endswith('.css'):
            content_type = 'text/css'
        elif file_path.endswith('.json'):
            content_type = 'application/json'
        elif file_path.endswith('.png'):
            content_type = 'image/png'
        elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            content_type = 'image/jpeg'
        elif file_path.endswith('.svg'):
            content_type = 'image/svg+xml'
        
        # Read and send file
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {str(e)}")
    
    def send_json_response(self, data):
        """Send JSON response"""
        json_data = json.dumps(data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(json_data)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json_data)
    
    def send_error_response(self, status_code, error_data):
        """Send error response"""
        json_data = json.dumps(error_data).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(json_data)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json_data)
    
    def log_message(self, format, *args):
        """Override to reduce log noise"""
        pass

if __name__ == '__main__':
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomHandler)
    
    print("=" * 60)
    print("🚀 Custom Server Starting")
    print("=" * 60)
    print(f"✅ Web server: http://localhost:{port}")
    print(f"✅ API endpoint: http://localhost:{port}/api/strava/activities")
    print("=" * 60)
    print("\nServing everything from the same origin (no CORS issues!)")
    print("Press Ctrl+C to stop\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        httpd.shutdown()

