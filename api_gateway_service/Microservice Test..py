import requests

API_GATEWAY_URL = 'http://127.0.0.1:5000'


def create_suggestion(token, category, title, description):
    url = f"{API_GATEWAY_URL}/create_entry"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "category": category,
        "title": title,
        "description": description
    }
    response = requests.put(url, json=data, headers=headers)
    print(f"Raw Create Suggestion Response: {response.text}")  # Print raw response
    try:
        response_json = response.json()
        print(f"Create Suggestion Response: {response_json}")
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")

def get_suggestion():
    url = f"{API_GATEWAY_URL}/get_suggestion"
    response = requests.get(url)
    print(f"Raw Get Suggestion Response: {response.text}")
    try:
        response_json = response.json()
        print(f"Get Suggestion Response: {response_json}")
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")

def delete_suggestion(token, category, title, description):
    url = f"{API_GATEWAY_URL}/delete_entry"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "category": category,
        "title": title,
        "description": description
    }
    response = requests.delete(url, json=data, headers=headers)
    print(f"Raw Delete Suggestion Response: {response.text}")
    try:
        response_json = response.json()
        print(f"Delete Suggestion Response: {response_json}")
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")

