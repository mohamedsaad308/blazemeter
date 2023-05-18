import requests
import json
import sys
import boto3


def get_ssm_parameter(parameter_name):
    ssm = boto3.client("ssm")
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response["Parameter"]["Value"]


def send_sqs_message(queue_name, message):
    sqs = boto3.resource("sqs")
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    response = queue.send_message(MessageBody=json.dumps(message))
    return response


def disable_email(email):
    blazemeter_account_id = get_ssm_parameter("blazmeterAccountId")
    blazemeter_key = get_ssm_parameter("blazemeterKey")

    users_api = f"https://a.blazemeter.com/api/v4/accounts/{blazemeter_account_id}/users"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {blazemeter_key}",
    }

    response = requests.get(users_api, headers=headers)
    result = response.json().get("result", [])

    email_records = [record for record in result if record.get("email") == email and record.get("enabled")]
    if not email_records:
        message = {
            "email": email,
            "deleted": False,
            "message": f"The email '{email}' does not exist or is already disabled!",
        }
        send_sqs_message("deletedFail", message)
        print(message["message"])
        return

    email_id = email_records[0].get("id")
    disable_url = f"{users_api}/{email_id}"
    payload = json.dumps({"enabled": False})

    response = requests.put(disable_url, headers=headers, data=payload)

    if response.ok:
        message = {
            "email": email,
            "deleted": True,
            "message": f"The email '{email}' was deleted successfully!",
        }
        send_sqs_message("deletedSuccess", message)
        print(message["message"])


if __name__ == "__main__":
    EMAIL = "salahsaad308@gmail.com"
    disable_email(EMAIL)
