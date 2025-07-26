#!/usr/bin/env python3
"""
Simple CORS test script to verify Railway deployment
"""
import requests

def test_cors():
    """Test CORS configuration for Vercel frontend"""
    url = "https://web-production-9bb32.up.railway.app/health"
    headers = {
        "Origin": "https://notice-board-frontend-phi.vercel.app",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "Content-Type"
    }
    
    try:
        # Test preflight request
        response = requests.options(url, headers=headers)
        print(f"Preflight Response Status: {response.status_code}")
        print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT FOUND')}")
        print(f"Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'NOT FOUND')}")
        print(f"Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers', 'NOT FOUND')}")
        
        # Test actual request
        response = requests.get(url, headers={"Origin": "https://notice-board-frontend-phi.vercel.app"})
        print(f"\nActual Request Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_cors() 