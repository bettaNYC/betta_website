# Quick Start: Strava Setup

## 🚀 Fast Setup (5 minutes)

### Step 1: Get Your Strava App Credentials
1. Go to: **https://www.strava.com/settings/api**
2. Create a new app (or use existing)
3. Copy your **Client ID** and **Client Secret**

### Step 2: Get Authorization Code
Open this URL in your browser (replace `YOUR_CLIENT_ID`):
```
https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost:8000&approval_prompt=force&scope=activity:read_all
```

After clicking "Authorize", copy the `code` from the redirect URL.

### Step 3: Get Refresh Token (Easiest Method)
Run this helper script:
```bash
python3 get-strava-token.py
```

Or with your credentials directly:
```bash
python3 get-strava-token.py YOUR_CLIENT_ID YOUR_CLIENT_SECRET YOUR_AUTHORIZATION_CODE
```

### Step 4: Update Your Code
1. Open `strava-proxy.py`
2. Replace the `REFRESH_TOKEN` on line 17 with your new token

### Step 5: Start Servers
**Terminal 1:**
```bash
python3 -m http.server 8000
```

**Terminal 2:**
```bash
python3 strava-proxy.py
```

### Step 6: View Your Site
Open: **http://localhost:8000/running.html**

---

## 📋 What You Need

- ✅ Strava account
- ✅ Client ID (from Strava API settings)
- ✅ Client Secret (from Strava API settings)
- ✅ Authorization code (from OAuth flow)
- ✅ Refresh token (from token exchange)

## 🔗 Important Links

- **Strava API Settings**: https://www.strava.com/settings/api
- **Authorization URL**: `https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost:8000&approval_prompt=force&scope=activity:read_all`

## ❓ Need More Help?

See `STRAVA_SETUP.md` for detailed instructions.

