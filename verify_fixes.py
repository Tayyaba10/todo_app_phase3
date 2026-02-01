#!/usr/bin/env python3
"""
Verification script to confirm that the fixes for the 422 error when editing tasks have been applied.
"""

import json
from pathlib import Path

def verify_fixes():
    print("🔍 Verifying fixes for 422 error when editing tasks...\n")

    # Check frontend fix
    print("1. Checking frontend edit page fix:")
    frontend_file = Path("frontend/src/app/tasks/[id]/edit/page.tsx")

    if frontend_file.exists():
        content = frontend_file.read_text()

        # Check that updateTask is called instead of getTaskById in handleSubmit
        if "apiService.updateTask(taskId.toString(), data)" in content:
            print("   ✅ Frontend correctly calls updateTask API")
        else:
            print("   ❌ Frontend does not call updateTask API properly")
            print(f"   Looking for: apiService.updateTask(taskId.toString(), data)")
            actual_lines = [line.strip() for line in content.split('\n') if 'apiService' in line and ('updateTask' in line or 'getTaskById' in line)]
            print(f"   Found: {actual_lines}")
            return False

        # Check that taskId is handled as string (for UUID support)
        if "params.id as string" in content:
            print("   ✅ Frontend correctly handles taskId as string for UUIDs")
        else:
            print("   ❌ Frontend does not handle taskId as string")
            print(f"   Looking for: params.id as string")
            actual_lines = [line.strip() for line in content.split('\n') if 'taskId =' in line]
            print(f"   Found: {actual_lines}")
            return False

        # Verify handleSubmit function structure
        lines = content.split('\n')
        in_handle_submit = False
        found_correct_call = False

        for line_num, line in enumerate(lines):
            if "const handleSubmit" in line and "async" in line:
                in_handle_submit = True
            elif in_handle_submit and line.strip().endswith('};') and "try" not in line:
                # End of function body
                break
            elif in_handle_submit and "apiService.updateTask" in line:
                found_correct_call = True
            elif in_handle_submit and "apiService.getTaskById" in line and "handleSubmit" in content[:content.find(line)]:
                # Found getTaskById inside handleSubmit (wrong)
                print(f"   ❌ Frontend still calls getTaskById in handleSubmit at line {line_num + 1}: {line.strip()}")
                return False

        if found_correct_call:
            print("   ✅ Frontend handleSubmit contains correct updateTask call")
        else:
            print("   ❌ Frontend handleSubmit does not contain updateTask call")
            return False

        print("   ✅ Frontend edit page fix verified\n")
    else:
        print("   ❌ Frontend file does not exist")
        return False

    # Check backend fix
    print("2. Checking backend task service fix:")
    backend_file = Path("backend/src/services/task_service.py")

    if backend_file.exists():
        content = backend_file.read_text()

        # Check that datetime import is at the top
        header_content = '\n'.join(content.split('\n')[:15])  # First 15 lines
        if "import datetime" in header_content:
            print("   ✅ Backend has datetime import at top of file")
        else:
            print("   ❌ Backend does not have datetime import at top")
            print(f"   Header content: {header_content}")
            return False

        # Count total datetime imports in the file
        total_imports = content.count("import datetime")
        if total_imports == 1:
            print("   ✅ Backend has exactly one datetime import (at the top)")
        else:
            print(f"   ❌ Backend has {total_imports} datetime imports (should be 1 at top only)")
            import_lines = [(i+1, line.strip()) for i, line in enumerate(content.split('\n')) if "import datetime" in line]
            print(f"   Import lines found: {import_lines}")
            return False

        # Check that the methods use the imported datetime module
        if "datetime.datetime.utcnow()" in content:
            print("   ✅ Backend methods use imported datetime module")
        else:
            print("   ❌ Backend methods don't use imported datetime module")
            print(f"   Looking for: datetime.datetime.utcnow()")
            utcnow_lines = [line.strip() for line in content.split('\n') if "utcnow" in line]
            print(f"   Found: {utcnow_lines}")
            return False

        print("   ✅ Backend task service fix verified\n")
    else:
        print("   ❌ Backend file does not exist")
        return False

    # Summary
    print("🎉 All fixes have been successfully verified!")
    print("\n📋 Summary of fixes applied:")
    print("   • Frontend edit page now calls apiService.updateTask() instead of apiService.getTaskById()")
    print("   • Frontend properly handles task IDs as strings (for UUID support)")
    print("   • Backend has datetime import at the top of the file")
    print("   • Backend methods use the imported datetime module properly")
    print("\n✅ The 422 error when editing tasks should now be resolved")

    return True

if __name__ == "__main__":
    success = verify_fixes()
    exit(0 if success else 1)