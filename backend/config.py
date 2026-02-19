"""
Configuration file for RIFT 2026 Agent
Contains API keys and settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or ""

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or ""

# Server Configuration
BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 5))

# Agent Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.1))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 1500))

print(f"✅ Configuration loaded:")
print(f"   - OpenAI API Key: {'✅ Set' if OPENAI_API_KEY else '❌ Missing'}")
print(f"   - GitHub Token: {'✅ Set' if GITHUB_TOKEN else '❌ Missing'}")
print(f"   - Backend Port: {BACKEND_PORT}")
print(f"   - LLM Model: {LLM_MODEL}")
