#!/usr/bin/env python3
"""
Simple test to verify the API service fixes
"""

# Check the API service file for the correct changes
api_service_path = "./frontend/src/lib/services/api.ts"

try:
    with open(api_service_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Validating API service fixes...")

    # Check 1: Base URL should not include /api
    base_url_line = ""
    for line in content.split('\n'):
        if 'this.baseUrl =' in line:
            base_url_line = line
            break

    if 'http://127.0.0.1:8000' in base_url_line and '/api' not in base_url_line:
        print("✓ Base URL correctly configured (does not include /api)")
    else:
        print(f"✗ Base URL incorrectly configured: {base_url_line}")

    # Check 2: sendMessage endpoint should include /api prefix to match backend route structure
    if '/api/${userId}/chat' in content:
        print("✓ sendMessage endpoint correctly configured (constructs /api/{userId}/chat)")
    else:
        print("✗ sendMessage endpoint does not include /api prefix")
        # Look for the actual endpoint
        in_send_message = False
        for i, line in enumerate(content.split('\n')):
            if 'async sendMessage(' in line:
                in_send_message = True
                print(f"  sendMessage method found at line {i+1}")
            elif in_send_message and 'return this.request' in line:
                print(f"  Endpoint found: {line.strip()}")
                in_send_message = False

    # Check 3: Task endpoints should include /api prefix
    task_endpoints_found = []
    for line in content.split('\n'):
        if 'return this.request' in line and ('/tasks/' in line or '/chat' in line):
            task_endpoints_found.append(line.strip())

    print(f"Found {len([t for t in task_endpoints_found if '/api' in t])}/{len(task_endpoints_found)} endpoints with /api prefix")
    for endpoint in task_endpoints_found:
        prefix = "✓" if '/api' in endpoint else "✗"
        print(f"  {prefix} {endpoint}")

    print("\nValidation complete!")

except FileNotFoundError:
    print(f"Error: Could not find file {api_service_path}")
except Exception as e:
    print(f"Error validating API service: {e}")
    import traceback
    traceback.print_exc()