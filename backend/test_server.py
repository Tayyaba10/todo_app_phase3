#!/usr/bin/env python3
"""Simple test server script"""

try:
    from src.main import app
    print("✓ Successfully imported app")

    import uvicorn
    print("✓ Successfully imported uvicorn")

    print("Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()