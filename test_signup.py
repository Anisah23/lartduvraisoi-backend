import requests
import json

# Test valid email
data = {
    'fullName': 'Test User',
    'email': 'test@example.com',
    'password': 'Password123',
    'role': 'collector'
}
response = requests.post('http://localhost:5000/api/auth/signup', json=data)
print('Valid email test:')
print(f'Status: {response.status_code}')
print(f'Response: {response.json()}')
print()

# Test invalid email
data_invalid = data.copy()
data_invalid['email'] = 'invalid-email'
response_invalid = requests.post('http://localhost:5000/api/auth/signup', json=data_invalid)
print('Invalid email test:')
print(f'Status: {response_invalid.status_code}')
print(f'Response: {response_invalid.json()}')
print()

# Test another invalid email
data_invalid2 = data.copy()
data_invalid2['email'] = 'test@'
response_invalid2 = requests.post('http://localhost:5000/api/auth/signup', json=data_invalid2)
print('Another invalid email test:')
print(f'Status: {response_invalid2.status_code}')
print(f'Response: {response_invalid2.json()}')
print()
