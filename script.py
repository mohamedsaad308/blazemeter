import requests
import json
import sys


# Email to be deleted
EMAIL = "salahsaad308@gmail.com"

# API endpoint URLs
users_url = "https://a.blazemeter.com/api/v4/accounts/1590235/users"
disable_url = f"https://a.blazemeter.com/api/v4/accounts/1590235/users/"

# Request headers
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Basic YmRlNDYzOTYxN2UxNTEwNGM0NmMwODA1OmU3MWU1OGU0ZDZiY2I5OWE2ODFhMjEzZTczZWMwYmZkMTJjOGY2NmVhNTM4NDgzZjNiYjA1ZTk0NjlmYjQ4MjE4ODdkNWE0Yw==",
}

# Send GET request to retrieve users
response = requests.get(users_url, headers=headers)
result = response.json()["result"]

# Find the email ID to disable
email_id = next(
    (
        record["id"]
        for record in result
        if record["email"] == EMAIL and record["enabled"]
    ),
    None,
)

if not email_id:
    print("This email does not exist or is already disabled!")
    sys.exit()

# Send PUT request to disable the email
disable_url += str(email_id)
payload = json.dumps({"enabled": False})

response = requests.put(disable_url, headers=headers, data=payload)

print(response.json())
