#!/usr/bin/env python3
"""
Validate that all modules import correctly after the fixes
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    print("Testing module imports...")

    try:
        from backend.src.main import app
        print("✓ Main app imported successfully")
    except Exception as e:
        print(f"✗ Main app import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    try:
        from backend.src.api.routes import tasks
        print("✓ Tasks route imported successfully")
    except Exception as e:
        print(f"✗ Tasks route import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    try:
        from backend.src.services import task_service
        print("✓ Task service imported successfully")
    except Exception as e:
        print(f"✗ Task service import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\nAll imports successful! 🎉")
    return True

if __name__ == "__main__":
    test_imports()