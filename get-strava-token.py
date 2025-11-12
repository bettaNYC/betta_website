#!/usr/bin/env python3
"""
Helper script to exchange Strava authorization code for refresh token
"""
import requests
import sys

def get_tokens(client_id, client_secret, authorization_code):
    """Exchange authorization code for access and refresh tokens"""
    url = 'https://www.strava.com/oauth/token'
    
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'grant_type': 'authorization_code'
    }
    
    print("Requesting tokens from Strava...")
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        tokens = response.json()
        print("\n✅ Success! Here are your tokens:\n")
        print(f"Access Token: {tokens.get('access_token')}")
        print(f"Refresh Token: {tokens.get('refresh_token')}")
        print(f"Expires At: {tokens.get('expires_at')}")
        print("\n⚠️  IMPORTANT: Save your REFRESH TOKEN!")
        print("   Update it in strava-proxy.py on line 17\n")
        return tokens
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        return None

if __name__ == '__main__':
    print("=" * 60)
    print("Strava Token Exchange Helper")
    print("=" * 60)
    print()
    
    # Get credentials
    if len(sys.argv) >= 4:
        client_id = sys.argv[1]
        client_secret = sys.argv[2]
        auth_code = sys.argv[3]
    else:
        print("Usage: python3 get-strava-token.py <CLIENT_ID> <CLIENT_SECRET> <AUTHORIZATION_CODE>")
        print()
        print("Or run interactively:")
        client_id = input("Enter your Strava Client ID: ").strip()
        client_secret = input("Enter your Strava Client Secret: ").strip()
        print("\nTo get your authorization code:")
        print("1. Go to: https://www.strava.com/oauth/authorize?client_id=" + client_id + "&response_type=code&redirect_uri=http://localhost:8000&approval_prompt=force&scope=activity:read_all")
        print("2. Authorize the app")
        print("3. Copy the 'code' parameter from the redirect URL")
        print()
        auth_code = input("Enter your authorization code: ").strip()
    
    if not all([client_id, client_secret, auth_code]):
        print("\n❌ Error: All fields are required!")
        sys.exit(1)
    
    tokens = get_tokens(client_id, client_secret, auth_code)
    
    if tokens:
        print("\n" + "=" * 60)
        print("Next steps:")
        print("1. Copy the Refresh Token above")
        print("2. Open strava-proxy.py")
        print("3. Replace the REFRESH_TOKEN on line 17")
        print("4. Restart the proxy server (Ctrl+C and run again)")
        print("=" * 60)


