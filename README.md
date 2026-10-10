# Expire TestFlight Builds

Expire **all** TestFlight builds of an app in one command using the App Store Connect API.

## Why?

Before you can [transfer an app](https://developer.apple.com/help/app-store-connect/transfer-an-app/overview-of-app-transfer) to another Apple Developer account, its TestFlight builds need to be expired.
App Store Connect has no **"Expire All"** button, so you'd have to open and expire every build by hand. With dozens of builds, that takes hours.

This script does it in seconds.

## How it works

1. Authenticates with an App Store Connect API key (short-lived ES256 JWT).
2. Fetches every **non-expired** build for the app (handles pagination, 200 per page).
3. Sends a `PATCH` to each build with `expired: true`.
4. Prints each build version with the HTTP status code.

## Requirements

- Python 3.8+
- An App Store Connect API key with the **Admin** or **App Manager** role

```bash
pip3 install pyjwt cryptography requests
```

## Setup

### 1. Create an API key

1. Open **App Store Connect → Users and Access → Integrations → App Store Connect API**.
2. Click **+**, name the key, and pick the **Admin** or **App Manager** role.
3. Download the `.p8` file. You can only download it **once**.
4. Note the **Key ID** (shown next to the key) and the **Issuer ID** (shown at the top of the page).

### 2. Find your App ID

Open your app in App Store Connect. The App ID is the number in the URL:

```
https://appstoreconnect.apple.com/apps/1234567890/...
                                       ^^^^^^^^^^
```

You can also find it under **App Information → Apple ID**.

### 3. Set environment variables

> Use the exact variable names the script reads.

```bash
export ASC_KEY_ID="XXXXXXXXXX"
export ASC_ISSUER_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export ASC_KEY_PATH="./AuthKey_XXXXXXXXXX.p8"
export ASC_APP_ID="1234567890"
```

## Usage

```bash
python3 expire_testflight_builds.py
```

Example output:

```
Expiring 42 builds...
1.0.0 200
1.0.1 200
1.1.0 200
...
```

`200` means the build was expired successfully. Refresh TestFlight in App Store Connect to confirm.

## ⚠️ Warning

- **Expiring a build cannot be undone.** Testers lose access to expired builds immediately.
- The script expires builds on **all platforms** (iOS, macOS, tvOS, visionOS) for the given app.
- Double-check the App ID before you run it.

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Wrong Key ID, Issuer ID, or `.p8` file | Check the values in App Store Connect |
| `403 Forbidden` | The key's role is too low | Use a key with the **Admin** or **App Manager** role |
| `python3: command not found` (macOS) | Python isn't installed | Run `xcode-select --install` |
| `externally-managed-environment` | pip is blocked by the system Python | `pip3 install --user ...` or use a virtualenv |

## Security

- **Never commit your `.p8` key.** Add this to `.gitignore`:
  ```
  *.p8
  .env
  ```
- Revoke the API key in App Store Connect when you no longer need it.

## Before transferring your app

Expiring builds is only one requirement. Open **App Information → Transfer App** in App Store Connect to see everything that is still blocking the transfer.

## License

MIT
