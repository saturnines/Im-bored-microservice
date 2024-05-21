import requests

API_GATEWAY_URL = 'http://127.0.0.1:5000'

def register_user(username, password):
    url = f"{API_GATEWAY_URL}/register-user"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=data)
    print(f"Raw Register Response: {response.text}")
    try:
        response_json = response.json()
        print(f"Register Response: {response_json}")
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")

def login_user(username, password):
    url = f"{API_GATEWAY_URL}/login"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=data)
    print(f"Raw Login Response: {response.text}")
    try:
        response_json = response.json()
        print(f"Login Response: {response_json}")
        return response_json.get('token')
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")
        return None

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

if __name__ == "__main__":
    print("Registering a new user...")
    register_user("testuser", "testpassword")

    print("Logging in with the registered user...")
    token = login_user("testuser", "testpassword")

    if token:
        # Create new suggestion
        print("Creating a new suggestion...")
        create_suggestion(token, "Test Category", "Test Title", "Test Description")

        # Get random suggestion
        print("Getting a random suggestion...")
        get_suggestion()

        # Delete created suggestion
        print("Deleting the created suggestion...")
        delete_suggestion(token, "Test Category", "Test Title", "Test Description")
