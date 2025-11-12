# Strava API Setup Instructions

This guide will walk you through setting up Strava API integration to display your running data on your website.

## Step 1: Create a Strava Application

1. Go to **https://www.strava.com/settings/api**
2. Log in to your Strava account
3. Scroll down to **"My API Application"** section
4. Click **"Create App"** or use an existing app
5. Fill in the form:
   - **Application Name**: Your website name (e.g., "My Running Website")
   - **Category**: Website
   - **Website**: Your website URL (can be `http://localhost:8000` for testing)
   - **Authorization Callback Domain**: `localhost` (for local development)
   - **Description**: Optional description
6. Click **"Create"**
7. **IMPORTANT**: Save your **Client ID** and **Client Secret** - you'll need these!

## Step 2: Get Your Authorization Code

1. Open your browser and go to this URL (replace `YOUR_CLIENT_ID` with your actual Client ID):
   ```
   https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost:8000&approval_prompt=force&scope=activity:read_all
   ```

   For example, if your Client ID is `184712`, the URL would be:
   ```
   https://www.strava.com/oauth/authorize?client_id=184712&response_type=code&redirect_uri=http://localhost:8000&approval_prompt=force&scope=activity:read_all
   ```

2. You'll be redirected to Strava's authorization page
3. Click **"Authorize"** to grant permissions
4. After authorization, you'll be redirected to `http://localhost:8000?code=AUTHORIZATION_CODE`
5. **Copy the `code` parameter from the URL** - this is your authorization code
   - The URL will look like: `http://localhost:8000?code=abc123def456...`
   - Copy everything after `code=` and before any `&` symbol

## Step 3: Exchange Authorization Code for Tokens

You need to exchange the authorization code for an access token and refresh token. You can do this using curl or a tool like Postman.

### Option A: Using curl (Terminal)

Run this command in your terminal (replace the placeholders):

```bash
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d code=YOUR_AUTHORIZATION_CODE \
  -d grant_type=authorization_code
```

**Example:**
```bash
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=184712 \
  -d client_secret=9a5f16cc1a3e830cd8a3e7a2e516f492a6b8ae09 \
  -d code=abc123def456... \
  -d grant_type=authorization_code
```

The response will look like:
```json
{
  "token_type": "Bearer",
  "expires_at": 1234567890,
  "expires_in": 21600,
  "refresh_token": "YOUR_REFRESH_TOKEN_HERE",
  "access_token": "YOUR_ACCESS_TOKEN_HERE",
  "athlete": {...}
}
```

**Save the `refresh_token`** - this is what you'll use in your code!

### Option B: Using a Browser Extension or Online Tool

1. Install a REST client browser extension (like "REST Client" for Chrome/Firefox)
2. Make a POST request to: `https://www.strava.com/oauth/token`
3. Use form data with:
   - `client_id`: Your Client ID
   - `client_secret`: Your Client Secret
   - `code`: Your authorization code
   - `grant_type`: `authorization_code`

## Step 4: Update Your Code

1. Open `strava-proxy.py`
2. Update line 17 with your new refresh token:
   ```python
   'REFRESH_TOKEN': 'YOUR_NEW_REFRESH_TOKEN_HERE'
   ```
3. Make sure your Client ID and Client Secret are also correct (lines 15-16)

## Step 5: Test the Setup

1. Make sure both servers are running:
   - **Web server**: `python3 -m http.server 8000` (Terminal 1)
   - **Proxy server**: `python3 strava-proxy.py` (Terminal 2)

2. Open your browser and go to: `http://localhost:8000/running.html`

3. Check the browser console (F12) for any errors

4. If you see your runs data, you're all set! 🎉

## Troubleshooting

### Error: "Failed to refresh access token: 401"
- Your refresh token may have expired
- Get a new refresh token by repeating Steps 2-3

### Error: "Cannot connect to Strava proxy server"
- Make sure `strava-proxy.py` is running on port 5000
- Check Terminal 2 for any error messages

### Error: "Strava API error: 403"
- Your app may not have the correct permissions
- Make sure you included `scope=activity:read_all` in the authorization URL

### No data showing
- Check the browser console (F12) for JavaScript errors
- Check the proxy server terminal for error messages
- Verify your refresh token is correct

## Important Notes

- **Refresh tokens don't expire** (unless you revoke access), but access tokens expire after 6 hours
- The proxy server automatically refreshes access tokens using your refresh token
- Keep your Client Secret and Refresh Token **private** - don't commit them to public repositories
- For production, you should:
  - Use environment variables for credentials
  - Set up proper CORS on your production server
  - Use HTTPS instead of HTTP

## Quick Reference

**Files to update:**
- `strava-proxy.py` - Update Client ID, Client Secret, and Refresh Token

**URLs:**
- Authorization: `https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost:8000&approval_prompt=force&scope=activity:read_all`
- Token exchange: `https://www.strava.com/oauth/token`

**Required Permissions:**
- `activity:read_all` - To read all your activities (including private ones)


