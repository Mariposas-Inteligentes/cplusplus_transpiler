import os
import subprocess
import sys

test_files_dir = 'tests/parser_test_files'
test_file_ext = '.py'
expected_output = """Error count for lexer: 0
Error count for parsing: 0"""

def run_parser(file_path):
    python_ver = 'python'
    if (len(sys.argv) == 2 and sys.argv[1] == '1'):
        python_ver = 'python3'
    result = subprocess.run([python_ver, 'main.py', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()

def check_test_files():
    failed_tests = 0
    passed_tests = 0

    for file_name in os.listdir(test_files_dir):
        if file_name.endswith(test_file_ext):
            test_file_path = os.path.join(test_files_dir, file_name)
            actual_output = run_parser(test_file_path)

            if file_name.startswith('test_valid'):
                if  expected_output not in actual_output:
                    print(f"Test failed for {file_name} (Expected valid):")
                    print(f"Expected output:\n{expected_output}")
                    print(f"Actual output:\n{actual_output}")
                    failed_tests += 1
                else:
                    passed_tests += 1

            elif file_name.startswith('test_invalid'):
                if  expected_output in actual_output:
                    print(f"Test failed for {file_name} (Expected invalid):")
                    print(f"Expected output to be different from:\n{expected_output}")
                    print(f"Actual output:\n{actual_output}")
                    failed_tests += 1
                else:
                    passed_tests += 1
    
    print(f"\nTotal tests passed: {passed_tests}")
    print(f"Total tests failed: {failed_tests}")

if __name__ == "__main__":
    check_test_files()
