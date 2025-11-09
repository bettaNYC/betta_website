// Strava API Configuration
// TODO: Replace these with your actual Strava API credentials
// You can get these from: https://www.strava.com/settings/api
const STRAVA_CONFIG = {
    CLIENT_ID: '184712', // Your Strava Client ID
    CLIENT_SECRET: '9a5f16cc1a3e830cd8a3e7a2e516f492a6b8ae09', // Your Strava Client Secret
    REFRESH_TOKEN: '6d972e1b4681ac7cb1a0719c961492b5b9fef2d7' // Your Strava Refresh Token
};

// Check if credentials are provided
const hasCredentials = STRAVA_CONFIG.CLIENT_ID && 
                       STRAVA_CONFIG.CLIENT_SECRET && 
                       STRAVA_CONFIG.REFRESH_TOKEN;

/**
 * Fetch activities from Strava API via proxy server
 * This avoids CORS issues by making requests through our backend proxy
 */
async function fetchStravaActivities() {
    try {
        console.log('Attempting to fetch from Strava API...');
        // Use same origin (port 8000) to avoid CORS issues
        // If custom-server.py is running, use /api/strava/activities
        // Otherwise, fall back to port 5000 proxy
        let apiUrl = '/api/strava/activities?per_page=30';
        let response;
        
        try {
            // Try same-origin first (works with custom-server.py)
            response = await fetch(apiUrl);
        } catch (e) {
            console.log('Same-origin failed, trying port 5000 proxy...');
            // Fallback to separate proxy server
            try {
                response = await fetch('http://localhost:5000/api/strava/activities?per_page=30', {
                    mode: 'cors',
                    credentials: 'omit'
                });
            } catch (e2) {
                console.log('Port 5000 failed, trying 127.0.0.1...');
                response = await fetch('http://127.0.0.1:5000/api/strava/activities?per_page=30', {
                    mode: 'cors',
                    credentials: 'omit'
                });
            }
        }

        console.log('Response status:', response.status, response.statusText);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error('Error response:', errorData);
            throw new Error(errorData.error || `Strava API error: ${response.status}`);
        }

        const runs = await response.json();
        console.log('Successfully fetched runs:', runs.length, 'runs');
        return runs;
    } catch (error) {
        console.error('Error fetching Strava data:', error);
        // Check if it's a network/CORS error
        if (error.message.includes('Failed to fetch') || error.message.includes('CORS') || error.name === 'TypeError') {
            throw new Error('Cannot connect to Strava proxy server. Make sure strava-proxy.py is running on port 5000.');
        }
        throw error;
    }
}

/**
 * Format time in seconds to HH:MM:SS or MM:SS
 */
function formatStravaTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Calculate pace in min/km format
 */
function calculatePace(distanceMeters, timeSeconds) {
    if (distanceMeters === 0 || timeSeconds === 0) {
        return '-';
    }
    
    const distanceKm = distanceMeters / 1000;
    const paceSecondsPerKm = timeSeconds / distanceKm;
    const minutes = Math.floor(paceSecondsPerKm / 60);
    const seconds = Math.round(paceSecondsPerKm % 60);
    
    return `${minutes}:${seconds.toString().padStart(2, '0')}/km`;
}

/**
 * Decode polyline to map image URL (simplified - you may want to use a mapping service)
 * For now, we'll use a placeholder or you can integrate with Google Static Maps, Mapbox, etc.
 */
function getMapImageUrl(polyline) {
    if (!polyline) {
        return null;
    }
    
    // Placeholder: You can integrate with Google Static Maps API or Mapbox
    // Example with Google Static Maps:
    // return `https://maps.googleapis.com/maps/api/staticmap?size=600x300&path=enc:${polyline}&key=YOUR_API_KEY`;
    
    // For now, return null to use placeholder
    return null;
}

/**
 * Load runs from Strava or fallback to sample data
 */
async function loadRuns() {
    try {
        // Try to fetch from Strava if credentials are provided
        if (hasCredentials) {
            console.log('Fetching runs from Strava...');
            return await fetchStravaActivities();
        } else {
            // Fallback to sample data
            console.log('Strava credentials not configured. Using sample data...');
            const response = await fetch('runs-sample.json');
            if (!response.ok) {
                throw new Error('Failed to load sample data');
            }
            return await response.json();
        }
    } catch (error) {
        console.error('Error loading runs:', error);
        // Try fallback to sample data
        try {
            const response = await fetch('runs-sample.json');
            if (response.ok) {
                console.log('Using fallback sample data...');
                return await response.json();
            }
        } catch (fallbackError) {
            console.error('Fallback also failed:', fallbackError);
        }
        throw error;
    }
}

