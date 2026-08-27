"""
Automated Test Runner Script
"""

import subprocess
import sys

def main():
    print("Running GracefulOS Multi-Tier Test Suite...")
    res = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"])
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
