import requests

API_GATEWAY_URL = 'http://127.0.0.1:5000'


def register_user(username, password):
    url = f"{API_GATEWAY_URL}/register-user"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=data)
    print(f"Register Response: {response.json()}")


def login_user(username, password):
    url = f"{API_GATEWAY_URL}/login"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=data)
    print(f"Login Response: {response.json()}")
    return response.json().get('token')


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
    print(f"Create Suggestion Response: {response.json()}")


def get_suggestion():
    url = f"{API_GATEWAY_URL}/get_suggestion"
    response = requests.get(url)
    print(f"Get Suggestion Response: {response.json()}")


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
    print(f"Delete Suggestion Response: {response.json()}")


if __name__ == "__main__":
    # Register a new user
    register_user("testuser", "testpassword")

    # Login with the registered user to get a token
    token = login_user("testuser", "testpassword")

    if token:
        # Create a new suggestion
        create_suggestion(token, "Test Category", "Test Title", "Test Description")

        # Get a random suggestion
        get_suggestion()

        # Delete the created suggestion
        delete_suggestion(token, "Test Category", "Test Title", "Test Description")
