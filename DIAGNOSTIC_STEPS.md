# Diagnostic Steps for "Failed to fetch" Error

## Step 1: Test Direct Access
Open this URL directly in your browser:
```
http://localhost:5000/api/strava/activities?per_page=5
```

**What should happen:**
- ✅ **If you see JSON data**: The proxy is working! The issue is with the JavaScript fetch.
- ❌ **If you see an error or "can't connect"**: The browser can't reach the proxy server.

## Step 2: Check Browser Console
1. Open `http://localhost:8000/test-strava.html`
2. Press **F12** to open Developer Tools
3. Go to **Console** tab
4. Click "Test Connection"
5. Look for **red error messages**
6. Share the **exact error message** you see

## Step 3: Check Network Tab
1. With Developer Tools open (F12)
2. Go to **Network** tab
3. Click "Test Connection" on the test page
4. Look for a request to `localhost:5000`
5. Click on it to see:
   - **Status code** (should be 200)
   - **Response** (should be JSON)
   - **Headers** (check for CORS headers)

## Step 4: Try Different Browser
- If using Chrome, try Firefox or Safari
- If using Firefox, try Chrome
- This helps identify browser-specific issues

## Step 5: Check for Browser Extensions
Some browser extensions block localhost connections:
- Ad blockers
- Privacy extensions
- Security extensions

**Try:**
1. Open browser in **Incognito/Private mode**
2. Test the connection again
3. If it works in incognito, an extension is blocking it

## Step 6: Check Firewall/Security Software
Your Mac's firewall or security software might be blocking port 5000.

**To check:**
1. System Settings → Network → Firewall
2. Make sure it's not blocking Python or port 5000

## Step 7: Verify Servers Are Running
Run this command in terminal:
```bash
./check-servers.sh
```

Or manually:
```bash
# Check web server
lsof -ti:8000 && echo "✅ Web server running" || echo "❌ Web server NOT running"

# Check proxy server  
lsof -ti:5000 && echo "✅ Proxy server running" || echo "❌ Proxy server NOT running"
```

## Step 8: Restart Everything
1. Stop both servers (Ctrl+C in their terminals)
2. Restart proxy server:
   ```bash
   python3 strava-proxy.py
   ```
3. Restart web server (if needed):
   ```bash
   python3 -m http.server 8000
   ```
4. Hard refresh browser (Cmd+Shift+R)

## Common Solutions

### Solution 1: Use 127.0.0.1 instead of localhost
Try accessing:
```
http://127.0.0.1:5000/api/strava/activities?per_page=5
```

### Solution 2: Disable Browser Extensions
1. Open browser in Incognito/Private mode
2. Test again

### Solution 3: Check Browser Security Settings
Some browsers have strict localhost policies. Check:
- Chrome: `chrome://flags/#block-insecure-private-network-requests`
- Firefox: Check privacy settings

### Solution 4: Use Combined Server
I've created `server.py` that runs both servers together. Try:
```bash
python3 server.py
```
Then access: `http://localhost:8000`

## What to Report Back

Please share:
1. ✅ or ❌ from Step 1 (direct browser access)
2. Exact error message from browser console (Step 2)
3. What you see in Network tab (Step 3)
4. Does it work in incognito mode? (Step 5)
5. Results from `check-servers.sh` (Step 7)

This will help identify the exact issue!

