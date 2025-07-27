import json
import os

# Step 1: Load original service account file
service_account_path = "flask-oauth-app-447004-ec18978777f9.json"  # Change if needed

with open(service_account_path, "r") as f:
    data = json.load(f)

# Step 2: Fix the private_key by escaping newlines
if "private_key" in data:
    data["private_key"] = data["private_key"].replace("\n", "\\n")

# Step 3: Minify the full JSON
minified_json = json.dumps(data, separators=(",", ":"))

# Step 4: Save to `.env` (replace or append)
env_path = ".env"

# Read existing content
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        lines = f.readlines()
else:
    lines = []

# Remove existing GOOGLE_CREDENTIALS_JSON if present
lines = [line for line in lines if not line.startswith("GOOGLE_CREDENTIALS_JSON=")]

# Add new line
lines.append(f'GOOGLE_CREDENTIALS_JSON={minified_json}\n')

# Write back to .env
with open(env_path, "w") as f:
    f.writelines(lines)

print("✅ GOOGLE_CREDENTIALS_JSON saved to .env successfully!")
