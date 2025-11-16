"""
Test script to check if all routes are working
"""
import sys
import requests
import json

BASE_URL = "http://localhost:5000"

def test_endpoint(method, endpoint, data=None, headers=None):
    """Test an endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=5)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=5)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=5)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=5)
        
        print(f"[{response.status_code}] {method} {endpoint}")
        if response.status_code < 400:
            try:
                result = response.json()
                print(f"  Response: {json.dumps(result, indent=2, ensure_ascii=False)[:200]}...")
            except:
                print(f"  Response: {response.text[:200]}")
        else:
            print(f"  Error: {response.text[:200]}")
        return response.status_code < 500
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Cannot connect to {url}")
        print("  Make sure server is running: python app.py")
        return False
    except Exception as e:
        print(f"[ERROR] {method} {endpoint}: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("Testing Backend Routes")
    print("=" * 60)
    print()
    
    # Test health check
    print("1. Health Check")
    test_endpoint('GET', '/api/health')
    print()
    
    # Test auth routes
    print("2. Auth Routes")
    test_endpoint('POST', '/api/auth/register', {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'test123',
        'role': 'student'
    })
    test_endpoint('POST', '/api/auth/login', {
        'email': 'test@example.com',
        'password': 'test123'
    })
    print()
    
    # Test journal routes (without auth - should fail gracefully)
    print("3. Journal Routes")
    test_endpoint('GET', '/api/journal?user_id=1')
    test_endpoint('GET', '/api/journal/stats?user_id=1')
    print()
    
    # Test AI analysis
    print("4. AI Analysis")
    test_endpoint('POST', '/api/ai/analyze', {
        'text': 'Hôm nay tôi cảm thấy rất vui',
        'mood': 'happy'
    })
    print()
    
    # Test activities
    print("5. Activities")
    test_endpoint('GET', '/api/activities/message/today')
    print()
    
    # Test family routes
    print("6. Family Routes")
    test_endpoint('GET', '/api/family/children?parent_id=1')
    print()
    
    print("=" * 60)
    print("Testing complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()

