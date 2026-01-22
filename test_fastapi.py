#!/usr/bin/env python3
"""Test FastAPI endpoints"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing /health ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_chat(query):
    """Test chat endpoint"""
    print(f"\n=== Testing /chat with: '{query}' ===")
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"query": query}
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Answer: {data.get('answer')}")
    print(f"Sources: {data.get('sources')}")
    print(f"Confidence: {data.get('confidence')}")
    print(f"Mode: {data.get('mode')}")
    return response.status_code == 200

if __name__ == "__main__":
    print("="*70)
    print("TESTING FASTAPI CHATBOT")
    print("="*70)
    
    # Run tests
    tests = [
        ("Health Check", lambda: test_health()),
        ("Empty query", lambda: test_chat("")),
        ("General query", lambda: test_chat("Hello team")),
        ("Process query", lambda: test_chat("Quy trình tuyển dụng?")),
        ("Policy query", lambda: test_chat("Chính sách remote work?")),
    ]
    
    passed = sum(1 for name, test in tests if test())
    
    print("\n" + "="*70)
    print(f"SUMMARY: {passed}/{len(tests)} tests passed")
    print("="*70)