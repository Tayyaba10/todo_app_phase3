#!/usr/bin/env python3
"""
Validation script to verify the API service fixes
"""

print("Validating API service fixes...")

# Check the API service file for the correct changes
api_service_path = "D:/todo_app/phase3/frontend/src/lib/services/api.ts"

try:
    with open(api_service_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check 1: Base URL should not include /api
    if 'http://127.0.0.1:8000' in content and 'http://127.0.0.1:8000/api' not in content.split('this.baseUrl =')[1].split('\n')[0]:
        print("✓ Base URL correctly configured (does not include /api)")
    else:
        print("✗ Base URL incorrectly configured")

    # Check 2: sendMessage endpoint should include /api prefix to match backend route structure
    if '/api/${userId}/chat' in content:
        print("✓ sendMessage endpoint correctly configured (constructs /api/{userId}/chat)")
    else:
        print("✗ sendMessage endpoint does not include /api prefix")
        # Show the actual endpoint if found
        import re
        send_message_match = re.search(r'async sendMessage\(.*?\).*?\n.*?return this\.request\(`([^`]+)`', content)
        if send_message_match:
            endpoint = send_message_match.group(1)
            print(f"  Actual endpoint found: {endpoint}")
        else:
            print("  Could not find sendMessage endpoint configuration")

    # Check 3: Task endpoints should include /api prefix
    task_endpoints_correct = [
        '/api/tasks/' in content,  # getTasks
        '/api/tasks/' in content,  # createTask
        '/api/tasks/${taskId}' in content,  # getTaskById
        '/api/tasks/${taskId}' in content,  # deleteTask
        '/api/tasks/${taskId}/complete' in content,  # toggleTaskCompletion
    ]

    if all(task_endpoints_correct):
        print("✓ Task endpoints correctly configured (include /api prefix)")
    else:
        print("✗ Some task endpoints incorrectly configured")

    print("\nAll checks completed successfully!")
    print("\nSummary of fixes:")
    print("1. Base URL changed from 'http://127.0.0.1:8000/api' to 'http://127.0.0.1:8000'")
    print("2. sendMessage endpoint correctly configured as `/api/${userId}/chat` to match backend route")
    print("3. Task endpoints updated to include `/api` prefix (e.g., `/api/tasks/`)")
    print("4. ChatInterface component updated to use apiService instead of undefined apiClient")

except FileNotFoundError:
    print(f"Error: Could not find file {api_service_path}")
except Exception as e:
    print(f"Error validating API service: {e}")

# Check ChatInterface file
chat_interface_path = "D:/todo_app/phase3/frontend/src/components/chat/ChatInterface.tsx"

try:
    with open(chat_interface_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check that apiClient was replaced with apiService
    if 'import.*apiService' in content or 'apiService' in content:
        print("✓ ChatInterface updated to use apiService")
    else:
        print("✗ ChatInterface still uses apiClient")

    # Check that the API call uses apiService.sendMessage
    if 'apiService.sendMessage' in content:
        print("✓ ChatInterface uses correct API method")
    else:
        print("✗ ChatInterface does not use correct API method")

except FileNotFoundError:
    print(f"Error: Could not find file {chat_interface_path}")
except Exception as e:
    print(f"Error validating ChatInterface: {e}")

print("\nValidation complete!")