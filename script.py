import requests
import json
import sys
import boto3


def get_ssm_parameter(parameter_name):
    ssm = boto3.client("ssm")
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response["Parameter"]["Value"]


def disable_email(email):
    blazmeter_account_id = get_ssm_parameter("blazmeterAccountId")
    blazemeter_key = get_ssm_parameter("blazemeterKey")

    users_api = f"https://a.blazemeter.com/api/v4/accounts/{blazmeter_account_id}/users"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {blazemeter_key}",
    }

    response = requests.get(users_api, headers=headers)
    result = response.json()["result"]

    email_id = next(
        (record["id"] for record in result if record["email"] == email and record["enabled"]),
        None,
    )

    if not email_id:
        print(f"The email '{email}' does not exist or is already disabled!")
        sys.exit()

    disable_url = f"{users_api}/{email_id}"
    payload = json.dumps({"enabled": False})

    response = requests.put(disable_url, headers=headers, data=payload)

    if response.ok:
        print(f"The email '{email}' was deleted successfully!")


if __name__ == "__main__":
    EMAIL = "salahsaad308@gmail.com"
    disable_email(EMAIL)
