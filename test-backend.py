import requests
import json

def test_backend():
    try:
        # Test health endpoint
        print("Testing backend health...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test run-agent endpoint
        print("\nTesting run-agent endpoint...")
        data = {
            "repo_url": "https://github.com/octocat/Hello-World",
            "team_name": "Test Team",
            "leader_name": "Test Leader"
        }
        response = requests.post("http://localhost:8000/api/run-agent", 
                               json=data, 
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        print(f"Run agent: {response.status_code}")
        if response.status_code == 200:
            print(f"Success: {response.json()}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running on http://localhost:8000")
        print("Please start the backend with: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_backend()