import requests

# Bad practice, change api_Gateway to something used prod.
API_GATEWAY_URL = 'http://127.0.0.1:5000'


def register_user_test(username, password):
    """Test for registering users. """
    url = f"{API_GATEWAY_URL}/register-user"
    data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        try:
            response_json = response.json()
            print(f"Register Response: {response_json}")

            # Assert specific conditions in the response
            assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
            assert "message" in response_json, "Response JSON does not contain 'message'"
            assert response_json[
                       "message"] == "User registered successfully", f"Unexpected message: {response_json['message']}"

            print("Registration test passed!")
        except requests.exceptions.JSONDecodeError:
            print("Failed to decode JSON response")
            assert False, "Response is not a valid JSON"

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        assert False, f"HTTP error: {http_err}"

    except Exception as err:
        print(f"An error occurred: {err}")
        assert False, f"General error: {err}"


def login_user_test(username, password):
    """Test for logging in"""
    url = f"{API_GATEWAY_URL}/login"
    data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        try:
            response_json = response.json()
            print(f"Login Response: {response_json}")

            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
            assert "message" in response_json, "Response JSON does not contain 'message'"
            assert response_json[
                       "message"] == "User logged in successfully", f"Unexpected message: {response_json['message']}"
            assert "token" in response_json, "Response JSON does not contain 'token'"

            print("Login User test passed!")

        except requests.exceptions.JSONDecodeError:
            print("Failed to decode JSON response")
            assert False, "Response is not a valid JSON"

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        assert False, f"HTTP error: {http_err}"

    except Exception as err:
        print(f"An error occurred: {err}")
        assert False, f"General error: {err}"


def create_entry_test(token, category, title, description):
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

    try:
        response_json = response.json()
        assert response.status_code == 202, f"Expected status code 202, got {response.status_code}"  # unsure if status code should be same or not
        assert "message" in response_json, "Response JSON does not contain 'message'"
        assert response_json[
                   "message"] == "Suggestion added successfully", f"Unexpected message: {response_json['message']}"
        print("Created entry test passed!")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        assert False, f"HTTP error: {http_err}"

    except Exception as err:
        print(f"An error occurred: {err}")
        assert False, f"General error: {err}"


def get_suggestion_test():
    url = f"{API_GATEWAY_URL}/get_suggestion"
    response = requests.get(url)

    try:
        response_json = response.json()
        assert 'category' in response_json and 'title' in response_json and 'description' in response_json
    except requests.exceptions.JSONDecodeError as decode_error:
        assert False, f"Json Decode error: {decode_error}"

    except Exception as err:
        print(f"An error occurred: {err}")
        assert False, f"General error: {err}"


# Run auth, logging, suggestion
if __name__ == "__main__":
    token = "your_valid_token_here"
    register_user_test("test_user", "test_password")
    login_user_test("test_user", "test_password")
    create_entry_test(token, "Movie", "Inception", "Test Description")
    get_suggestion_test()
