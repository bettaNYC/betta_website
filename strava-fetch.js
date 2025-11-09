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
 * Get a new access token from Strava using refresh token
 */
async function getAccessToken() {
    if (!hasCredentials) {
        throw new Error('Strava credentials not configured');
    }

    const response = await fetch('https://www.strava.com/oauth/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            client_id: STRAVA_CONFIG.CLIENT_ID,
            client_secret: STRAVA_CONFIG.CLIENT_SECRET,
            refresh_token: STRAVA_CONFIG.REFRESH_TOKEN,
            grant_type: 'refresh_token'
        })
    });

    if (!response.ok) {
        throw new Error('Failed to refresh access token');
    }

    const data = await response.json();
    return data.access_token;
}

/**
 * Fetch activities from Strava API
 */
async function fetchStravaActivities() {
    try {
        const accessToken = await getAccessToken();
        
        // Fetch recent activities (last 30 activities)
        const response = await fetch('https://www.strava.com/api/v3/athlete/activities?per_page=30', {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!response.ok) {
            throw new Error(`Strava API error: ${response.status}`);
        }

        const activities = await response.json();
        
        // Filter only runs
        const runs = activities.filter(activity => activity.type === 'Run');
        
        // Transform Strava data to our format
        return runs.map(activity => ({
            date: activity.start_date_local.split('T')[0],
            distance_km: (activity.distance / 1000).toFixed(2),
            time: formatStravaTime(activity.moving_time),
            pace: calculatePace(activity.distance, activity.moving_time),
            map: activity.map?.summary_polyline || null,
            name: activity.name || 'Run'
        }));
    } catch (error) {
        console.error('Error fetching Strava data:', error);
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

