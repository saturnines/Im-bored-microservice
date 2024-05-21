# Microservices Project

## Overview

Currently, this project has 3 microservices:
1. **User Authentication Service**: Manages user registration and login.
2. **Suggestion Service**: Manages CRUD operations for suggestions.
3. **API Gateway**: Routes requests to the appropriate microservice.

## Communication Contract

### Register a New User

**Example Call:**
```python
import requests

API_GATEWAY_URL = 'http://127.0.0.1:5000'
data = {
    "username": "newuser",
    "password": "newpassword",
    "rank": 1  # Optional, default is 1
}
response = requests.post(f"{API_GATEWAY_URL}/register-user", json=data)
print(response.json())
```

### Logging In
```python
import requests

API_GATEWAY_URL = 'http://127.0.0.1:5000'
data = {
    "username": "newuser",
    "password": "newpassword"
}
response = requests.post(f"{API_GATEWAY_URL}/login", json=data)
print(response.json())
```

### Creating Suggestions

```python
import requests

API_GATEWAY_URL = 'http://127.0.0.1:5000'
token = "your_jwt_token"
headers = {
    "Authorization": f"Bearer {token}"
}
data = {
    "category": "Test Category",
    "title": "Test Title",
    "description": "Test Description"
}
response = requests.put(f"{API_GATEWAY_URL}/create_entry", json=data, headers=headers)
print(response.json())
```

### Deleting Suggestion
```python
import requests

API_GATEWAY_URL = 'http://127.0.0.1:5000'
token = "your_jwt_token"
headers = {
    "Authorization": f"Bearer {token}"
}
data = {
    "category": "Test Category",
    "title": "Test Title",
    "description": "Test Description"
}
response = requests.delete(f"{API_GATEWAY_URL}/delete_entry", json=data, headers=headers)
print(response.json())
```

###Getting Random Suggestion
```python
import requests

API_GATEWAY_URL = 'http://127.0.0.1:5000'
response = requests.get(f"{API_GATEWAY_URL}/get_suggestion")
print(response.json())
```

