import sys
import os
sys.path.append('.')

def run_tests():
    try:
        from tests.test_model_manager import test_model_compatibility_check
        test_model_compatibility_check()
        print("✅ test_model_compatibility_check passed")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)