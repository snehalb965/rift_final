#!/usr/bin/env python3
"""
Example Issues and Fixes - Shows exactly what the agent detects and how it fixes them
"""

def show_example_fixes():
    """Show examples of issues the agent can detect and fix"""
    
    examples = [
        {
            "bug_type": "LINTING",
            "description": "Unused import detection and removal",
            "original_code": '''import os
import sys  # This is unused
import json

def get_data():
    return json.loads('{"key": "value"}')''',
            "fixed_code": '''import os
import json

def get_data():
    return json.loads('{"key": "value"}')''',
            "explanation": "Removed unused 'sys' import"
        },
        
        {
            "bug_type": "SYNTAX", 
            "description": "Missing colon in function definition",
            "original_code": '''def calculate_sum(a, b)  # Missing colon
    return a + b

def greet(name)  # Missing colon
    return f"Hello, {name}!"''',
            "fixed_code": '''def calculate_sum(a, b):  # Added colon
    return a + b

def greet(name):  # Added colon
    return f"Hello, {name}!"''',
            "explanation": "Added missing colons to function definitions"
        },
        
        {
            "bug_type": "LOGIC",
            "description": "Assignment vs comparison in if statement",
            "original_code": '''def check_admin(user):
    if user = "admin":  # Should be ==
        return True
    return False''',
            "fixed_code": '''def check_admin(user):
    if user == "admin":  # Fixed to comparison
        return True
    return False''',
            "explanation": "Changed assignment (=) to comparison (==)"
        },
        
        {
            "bug_type": "TYPE_ERROR",
            "description": "String and integer concatenation",
            "original_code": '''def create_message(name, age):
    return "Hello " + name + ", you are " + age + " years old"  # age is int''',
            "fixed_code": '''def create_message(name, age):
    return "Hello " + name + ", you are " + str(age) + " years old"  # Convert age to string''',
            "explanation": "Added str() conversion for integer concatenation"
        },
        
        {
            "bug_type": "IMPORT",
            "description": "Relative import converted to absolute",
            "original_code": '''from .utils import helper_function  # Relative import
from .config import settings''',
            "fixed_code": '''from utils import helper_function  # Absolute import
from config import settings''',
            "explanation": "Converted relative imports to absolute imports"
        },
        
        {
            "bug_type": "INDENTATION",
            "description": "Mixed tabs and spaces",
            "original_code": '''def mixed_indentation():
    if True:
        print("This uses spaces")
	print("This uses tabs")  # Tab character''',
            "fixed_code": '''def mixed_indentation():
    if True:
        print("This uses spaces")
        print("This uses spaces too")  # Converted to spaces''',
            "explanation": "Converted tabs to consistent spaces"
        }
    ]
    
    print("🔧 RIFT 2026 Agent - Issue Detection and Fixing Examples")
    print("="*60)
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['bug_type']} - {example['description']}")
        print("-" * 50)
        
        print("❌ ORIGINAL CODE (with issue):")
        print("```python")
        print(example['original_code'])
        print("```")
        
        print("\n✅ FIXED CODE:")
        print("```python")
        print(example['fixed_code'])
        print("```")
        
        print(f"\n💡 What was fixed: {example['explanation']}")
        
        # Show the exact format the agent reports
        print(f"\n📊 Agent Report Format:")
        print(f"   {example['bug_type']} error in example.py line X → Fix: {example['explanation'].lower()}")
        print(f"   Commit: [AI-AGENT] Fix {example['bug_type']}: {example['explanation']}")
    
    print("\n" + "="*60)
    print("🎯 TESTING INSTRUCTIONS")
    print("="*60)
    print("To see this in action with real repositories:")
    print("1. Run: python demo_fixes.py")
    print("2. Or test with real repos using the test data I provided")
    print("3. The agent will find similar issues in real Python projects")
    
    print("\n📊 Expected Results:")
    print("• Simple repos (Hello-World): 0-5 issues")
    print("• Medium repos (Flask/Requests): 10-30 issues") 
    print("• Large repos (Pandas): 20-50 issues")
    print("• All issues will be in the exact format shown above")

if __name__ == "__main__":
    show_example_fixes()