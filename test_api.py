#!/usr/bin/env python3
"""
Simple test script to verify API endpoints are working
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return False

def test_db_check():
    """Test database connection"""
    try:
        response = requests.get(f"{BASE_URL}/db-check")
        print(f"DB Check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"DB Check Failed: {e}")
        return False

def test_swagger_docs():
    """Test Swagger documentation"""
    try:
        response = requests.get(f"{BASE_URL}/api/docs/")
        print(f"Swagger Docs: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Swagger Docs Failed: {e}")
        return False

def test_signup():
    """Test user signup"""
    try:
        data = {
            "fullName": "Test User",
            "email": "test@example.com",
            "password": "TestPass123!",
            "role": "collector"
        }
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=data)
        print(f"Signup: {response.status_code} - {response.json()}")
        return response.status_code in [201, 409]  # 409 if user already exists
    except Exception as e:
        print(f"Signup Failed: {e}")
        return False

def test_login():
    """Test user login"""
    try:
        data = {
            "email": "test@example.com",
            "password": "TestPass123!"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        print(f"Login: {response.status_code} - {response.json()}")
        if response.status_code == 200:
            return response.json().get('access_token')
        return None
    except Exception as e:
        print(f"Login Failed: {e}")
        return None

def test_gallery():
    """Test gallery endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/artworks/")
        print(f"Gallery: {response.status_code} - Items: {len(response.json().get('items', []))}")
        return response.status_code == 200
    except Exception as e:
        print(f"Gallery Failed: {e}")
        return False

def main():
    print("Testing ArtMarket API...")
    print("=" * 50)
    
    # Basic health checks
    if not test_health_check():
        print("❌ Health check failed - server may not be running")
        return
    
    if not test_db_check():
        print("❌ Database connection failed")
        return
    
    # Test API documentation
    test_swagger_docs()
    
    # Test authentication
    test_signup()
    token = test_login()
    
    # Test gallery
    test_gallery()
    
    print("=" * 50)
    print("✅ Basic API tests completed")
    
    if token:
        print(f"🔑 Authentication token: {token[:20]}...")
    else:
        print("⚠️  Authentication may have issues")

if __name__ == "__main__":
    main()