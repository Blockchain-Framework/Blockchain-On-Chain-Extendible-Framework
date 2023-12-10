# http_utils.py
import requests

def send_request(url, method='GET', headers=None, data=None):
    try:
        response = requests.request(method, url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None
