import dotenv
import requests
import os

dotenv.load_dotenv(override=True)


def send_ha_notification(title: str, message: str) -> tuple[int, dict]:
    """Send a notification tool.
    Args:
        title (str): The title of the notification.
        message (str): The message content of the notification.
    Returns:
        tuple[int, dict]: The status code and response from the notification service."""
    url = os.getenv("HA_NOTIFICATION_URL")
    headers = {
        "Authorization": f"Bearer {os.getenv('HA_NOTIFICATION_TOKEN')}",
        "Content-Type": "application/json"
    }
    data = {
        "state": message,
        "attributes":
        {
            "from_number": title,
        }}

    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.json()


if __name__ == "__main__":
    status_code, response = send_ha_notification(
        "Test Title", "This is a test message.")
    print(f"Status Code: {status_code}")
    print(f"Response: {response}")
