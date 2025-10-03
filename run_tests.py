#!/usr/bin/env python3
"""
Test runner script for ApplyBot.
Provides easy commands to run different types of tests.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Main test runner function."""
    # Ensure we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("🧪 ApplyBot Test Runner")
    print("=" * 50)
    
    # Check if pytest is installed
    try:
        subprocess.run(["pytest", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pytest not found. Please install dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
    else:
        test_type = "all"
    
    success = True
    
    if test_type in ["all", "integration"]:
        # Run integration tests
        cmd = [
            "pytest", 
            "test_integration_simple.py", 
            "-v", 
            "--tb=short",
            "--color=yes"
        ]
        success &= run_command(cmd, "Running integration tests")
    
    if test_type in ["all", "unit"]:
        # Run unit tests (if any exist)
        unit_test_files = list(Path(".").glob("test_unit_*.py"))
        if unit_test_files:
            cmd = [
                "pytest", 
                *[str(f) for f in unit_test_files],
                "-v", 
                "--tb=short",
                "--color=yes"
            ]
            success &= run_command(cmd, "Running unit tests")
        else:
            print("ℹ️  No unit test files found (test_unit_*.py)")
    
    if test_type == "coverage":
        # Run tests with coverage
        cmd = [
            "pytest", 
            "--cov=app",
            "--cov-report=html",
            "--cov-report=term-missing",
            "-v"
        ]
        success &= run_command(cmd, "Running tests with coverage")
        
        if success:
            print("\n📊 Coverage report generated in htmlcov/index.html")
    
    if test_type == "env":
        # Test environment variable loading
        cmd = [
            "pytest", 
            "test_integration_simple.py::TestEnvironmentVariables",
            "-v"
        ]
        success &= run_command(cmd, "Testing environment variable loading")
    
    # Summary
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests completed successfully!")
    else:
        print("❌ Some tests failed. Check the output above.")
        sys.exit(1)

def print_usage():
    """Print usage information."""
    print("""
Usage: python run_tests.py [test_type]

Test types:
  all         - Run all tests (default)
  integration - Run integration tests only
  unit        - Run unit tests only
  coverage    - Run tests with coverage report
  env         - Test environment variable loading only

Examples:
  python run_tests.py
  python run_tests.py integration
  python run_tests.py coverage
    """)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        print_usage()
    else:
        main()