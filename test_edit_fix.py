#!/usr/bin/env python3
"""
Test script to verify that the edit task functionality fixes are working properly.
"""

import ast
import sys
from pathlib import Path

def check_frontend_fix():
    """Check if the frontend edit task page has the correct implementation."""
    frontend_file = Path("frontend/src/app/tasks/[id]/edit/page.tsx")

    if not frontend_file.exists():
        print("❌ Frontend edit page does not exist!")
        return False

    content = frontend_file.read_text()

    # Check that the handleSubmit function calls updateTask instead of getTaskById
    if "await apiService.updateTask(taskId.toString(), data)" in content:
        print("✅ Frontend edit page correctly calls updateTask")
    else:
        print("❌ Frontend edit page does not call updateTask properly")
        return False

    # Check that taskId is handled as a string (for UUID support)
    if "params.id as string" in content:
        print("✅ Frontend edit page correctly handles taskId as string")
    else:
        print("❌ Frontend edit page does not handle taskId as string")
        return False

    # Check that it doesn't call getTaskById in handleSubmit
    lines = content.split('\n')
    in_handle_submit = False
    for line in lines:
        if "const handleSubmit" in line and "async" in line:
            in_handle_submit = True
        elif in_handle_submit and line.strip().startswith('}'):
            in_handle_submit = False
        elif in_handle_submit and "getTaskById" in line and "apiService" in line:
            print("❌ Frontend edit page still calls getTaskById in handleSubmit")
            return False

    print("✅ Frontend edit page does not incorrectly call getTaskById in handleSubmit")
    return True

def check_backend_fix():
    """Check if the backend task service has the correct implementation."""
    backend_file = Path("backend/src/services/task_service.py")

    if not backend_file.exists():
        print("❌ Backend task service does not exist!")
        return False

    content = backend_file.read_text()

    # Check that datetime import is at the top
    lines = content.split('\n')
    import_datetime_found = False
    for line in lines[:20]:  # Check first 20 lines for imports
        if "import datetime" in line and not line.strip().startswith('#'):
            import_datetime_found = True
            break

    if import_datetime_found:
        print("✅ Backend task service has datetime import at top")
    else:
        print("❌ Backend task service does not have datetime import at top")
        return False

    # Count how many times "import datetime" appears in the file
    import_count = content.count("import datetime")
    if import_count == 1:
        print("✅ Backend task service has only one datetime import (at top)")
    else:
        print(f"❌ Backend task service has {import_count} datetime imports (should be 1 at top only)")
        return False

    # Check that there are no inline "import datetime" inside methods
    lines_with_inline_import = []
    for i, line in enumerate(lines):
        if "import datetime" in line and not line.strip().startswith("#"):
            # Check if this line is inside a function/method (not in the imports section)
            if i > 20:  # After the import section
                lines_with_inline_import.append(i + 1)

    if not lines_with_inline_import:
        print("✅ Backend task service has no inline datetime imports in methods")
    else:
        print(f"❌ Backend task service has inline datetime imports at lines: {lines_with_inline_import}")
        return False

    return True

def main():
    print("🔍 Testing fixes for the 422 error when editing tasks...")
    print()

    frontend_ok = check_frontend_fix()
    print()
    backend_ok = check_backend_fix()
    print()

    if frontend_ok and backend_ok:
        print("🎉 All fixes verified successfully!")
        print("✅ The 422 error when editing tasks should now be resolved")
        return True
    else:
        print("❌ Some issues remain with the fixes")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)