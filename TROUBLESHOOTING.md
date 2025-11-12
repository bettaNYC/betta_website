# Troubleshooting Guide

## Quick Diagnostic Steps

### 1. Check if servers are running

**Check web server (port 8000):**
```bash
lsof -ti:8000
```
If nothing shows, start it:
```bash
python3 -m http.server 8000
```

**Check proxy server (port 5000):**
```bash
lsof -ti:5000
```
If nothing shows, start it:
```bash
python3 strava-proxy.py
```

### 2. Test the proxy server directly

Open in browser or use curl:
```bash
curl http://localhost:5000/api/strava/activities?per_page=5
```

You should see JSON data with your runs. If you see an error, check:
- Is your refresh token valid?
- Are your credentials correct in `strava-proxy.py`?

### 3. Test the connection from browser

1. Open: `http://localhost:8000/test-strava.html`
2. Click "Test Connection"
3. Check what error (if any) appears

### 4. Check browser console

1. Open `http://localhost:8000/running.html`
2. Press **F12** to open developer tools
3. Go to **Console** tab
4. Look for any red error messages
5. Check the **Network** tab to see if requests are being made

## Common Issues

### Issue: "Cannot connect to Strava proxy server"

**Symptoms:**
- Error message about proxy server
- Empty page or "Loading runs..." forever

**Solutions:**
1. Make sure `strava-proxy.py` is running:
   ```bash
   python3 strava-proxy.py
   ```
2. Check if port 5000 is in use:
   ```bash
   lsof -ti:5000
   ```
3. Try restarting the proxy server

### Issue: "Strava API error: 401"

**Symptoms:**
- Error about failed to refresh access token
- 401 Unauthorized error

**Solutions:**
1. Your refresh token has expired
2. Get a new refresh token following the setup instructions
3. Update `strava-proxy.py` line 17 with new token
4. Restart the proxy server

### Issue: Empty array returned `[]`

**Symptoms:**
- Proxy works but returns no runs
- Stats show 0 runs

**Solutions:**
1. Check if you have any "Run" activities in Strava
2. The API only returns "Run" type activities (not walks, rides, etc.)
3. Check if activities are private - you need `activity:read_all` scope

### Issue: Data loads but doesn't display

**Symptoms:**
- Console shows data received
- But page shows "Loading..." or nothing

**Solutions:**
1. Check browser console for JavaScript errors
2. Verify `running.html` is loading `strava-fetch.js` correctly
3. Check if CSS is hiding the content

### Issue: CORS errors in console

**Symptoms:**
- Browser console shows "CORS policy" errors
- "Access-Control-Allow-Origin" errors

**Solutions:**
1. Make sure `flask-cors` is installed:
   ```bash
   pip3 install flask-cors
   ```
2. Restart the proxy server
3. Check that `CORS(app)` is in `strava-proxy.py`

## Step-by-Step Debugging

### Step 1: Verify Proxy Server
```bash
# Test directly
curl http://localhost:5000/api/strava/activities?per_page=1

# Should return JSON with runs or error message
```

### Step 2: Verify Web Server
```bash
# Open in browser
http://localhost:8000

# Should show your homepage
```

### Step 3: Test Connection
```bash
# Open test page
http://localhost:8000/test-strava.html

# Click "Test Connection" button
# Should show success or specific error
```

### Step 4: Check Browser Console
1. Open `http://localhost:8000/running.html`
2. Press F12
3. Check Console tab for errors
4. Check Network tab - look for request to `localhost:5000`
5. Click on the request to see response

## Getting Help

If nothing works, check:

1. **Proxy server logs** - Look at the terminal where `strava-proxy.py` is running
2. **Browser console** - F12 → Console tab
3. **Network tab** - F12 → Network tab → Look for failed requests
4. **Test page** - `http://localhost:8000/test-strava.html`

## Expected Behavior

✅ **Working correctly:**
- Proxy server returns JSON with runs
- Browser console shows "Successfully fetched runs: X runs"
- Runs appear on the page
- Stats are calculated and displayed

❌ **Not working:**
- Error messages in console
- "Loading runs..." forever
- Empty page
- 401 or other HTTP errors


