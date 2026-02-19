"""
Test the simple agent with a small repository
"""
from simple_agent import simple_healing_agent
import json

def test_with_small_repo():
    """Test with a small, fast repository"""
    print("Testing with a small repository...")
    
    # Use a small Python repository for testing
    result = simple_healing_agent(
        "https://github.com/kennethreitz/requests",  # Popular Python library
        "TestTeam",
        "TestUser"
    )
    
    print("\n" + "="*60)
    print("TEST RESULTS:")
    print("="*60)
    print(json.dumps(result, indent=2))
    print("="*60)
    
    return result

if __name__ == "__main__":
    test_with_small_repo()