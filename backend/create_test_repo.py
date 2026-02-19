"""
Create a simple test repository with intentional bugs for the agent to fix
"""

import tempfile
import os
from pathlib import Path

def create_test_repo():
    print("🔧 Creating test repository with intentional bugs...")
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp(prefix="test_repo_"))
    print(f"📁 Created test repo at: {temp_dir}")
    
    # Create main Python file with bugs
    main_file = temp_dir / "calculator.py"
    main_file.write_text('''import os
import sys
import math

def add(a, b):
    return a + b

def subtract(a, b)
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def calculate_area(radius):
    return math.pi * radius * radius

if __name__ == "__main__":
    print("Simple Calculator")
    result = add(5, 3)
    print(f"5 + 3 = {result}")
''')
    
    # Create test file with bugs
    test_file = temp_dir / "test_calculator.py"
    test_file.write_text('''import unittest
from calculator import add, subtract, multiply, divide, calculate_area

class TestCalculator(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
    
    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(0, 5), -5)
    
    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 3), -6)
    
    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        with self.assertRaises(ValueError):
            divide(10, 0)
    
    def test_calculate_area(self):
        self.assertAlmostEqual(calculate_area(1), 3.14159, places=4)

if __name__ == "__main__":
    unittest.main()
''')
    
    # Create requirements.txt
    requirements_file = temp_dir / "requirements.txt"
    requirements_file.write_text('''pytest>=6.0.0
numpy>=1.20.0
''')
    
    # Create README
    readme_file = temp_dir / "README.md"
    readme_file.write_text('''# Test Calculator

A simple calculator with intentional bugs for testing the RIFT agent.

## Bugs included:
1. Missing colon in function definition (line 8)
2. Unused imports (os, sys)
3. Syntax errors

## Run tests:
```bash
python -m pytest test_calculator.py
```
''')
    
    print("📝 Created files:")
    for file in temp_dir.glob("*"):
        if file.is_file():
            print(f"   - {file.name}")
    
    print(f"\n🐛 Intentional bugs added:")
    print("   1. Missing colon after 'def subtract(a, b)' on line 8")
    print("   2. Unused imports: 'os' and 'sys'")
    print("   3. These should be detected and fixed by the agent")
    
    return str(temp_dir)

if __name__ == "__main__":
    test_repo_path = create_test_repo()
    print(f"\n✅ Test repository created at: {test_repo_path}")
    print("\nYou can now test the agent with this local repository!")