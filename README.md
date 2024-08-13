# Microservices Project

## Overview
This is a project I made to see how Microservices work for a future project. This is a proof of concept for myself.

This is a model to see how to "build" microservices, and use this as sort of an idea for future projects. 

Currently, this project has 3 microservices:
1. **User Authentication Service**: Manages user registration and login.
2. **Suggestion Service**: Manages CRUD operations for suggestions.
3. **API Gateway**: Routes requests to the appropriate microservice. (RBAC Enabled.)
4. **Logging Service**: Handles logging for each of the microservices. 

## Example Usages

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


### Example Responses 
```python
Registering a new user...
Raw Register Response: {
  "message": "User registered successfully"
}

Register Response: {'message': 'User registered successfully'}
Logging in with the registered user...
Raw Login Response: {
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdHVzZXIiLCJyYW5rIjoxLCJleHAiOjE3MTYzMTc1NjJ9.8Nrl34tED0Y2LUoEmUCp4N8teyMqnR5pEgLn4z53TZ0"
}

Login Response: {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdHVzZXIiLCJyYW5rIjoxLCJleHAiOjE3MTYzMTc1NjJ9.8Nrl34tED0Y2LUoEmUCp4N8teyMqnR5pEgLn4z53TZ0'}
Creating a new suggestion...
Raw Create Suggestion Response: {
  "message": "Suggestion added successfully"
}

Create Suggestion Response: {'message': 'Suggestion added successfully'}
Getting a random suggestion...
Raw Get Suggestion Response: {
  "category": "Test Category",
  "description": "Test Description",
  "title": "Test Title"
}

Get Suggestion Response: {'category': 'Test Category', 'description': 'Test Description', 'title': 'Test Title'}
Deleting the created suggestion...
Raw Delete Suggestion Response: {
  "error": "Access denied!"
}

Delete Suggestion Response: {'error': 'Access denied!'}
```

