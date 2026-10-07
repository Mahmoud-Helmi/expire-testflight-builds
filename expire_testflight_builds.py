import os, time, jwt, requests

# Set these environment variables before running:
#   ASC_KEY_ID     - App Store Connect API key ID
#   ASC_ISSUER_ID  - App Store Connect issuer ID
#   ASC_P8_PATH    - path to the AuthKey_<KEY_ID>.p8 private key file
#   ASC_APP_ID     - Apple ID of the app whose builds should be expired
KEY_ID    = os.environ["ASC_KEY_ID"]
ISSUER_ID = os.environ["ASC_ISSUER_ID"]
P8_PATH   = os.environ["ASC_P8_PATH"]
APP_ID    = os.environ["ASC_APP_ID"]

def token():
    return jwt.encode(
        {"iss": ISSUER_ID, "iat": int(time.time()), "exp": int(time.time()) + 1200, "aud": "appstoreconnect-v1"},
        open(P8_PATH).read(), algorithm="ES256",
        headers={"kid": KEY_ID, "typ": "JWT"})

H = {"Authorization": f"Bearer {token()}", "Content-Type": "application/json"}
url = f"https://api.appstoreconnect.apple.com/v1/builds?filter[app]={APP_ID}&filter[expired]=false&limit=200"

builds = []
while url:
    r = requests.get(url, headers=H).json()
    builds += r["data"]
    url = r.get("links", {}).get("next")

print(f"Expiring {len(builds)} builds...")
for b in builds:
    r = requests.patch(f"https://api.appstoreconnect.apple.com/v1/builds/{b['id']}", headers=H,
        json={"data": {"type": "builds", "id": b["id"], "attributes": {"expired": True}}})
    print(b["attributes"]["version"], r.status_code)
