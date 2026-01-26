#!/usr/bin/env python3
"""
Test runner script for RecruitifyAI API tests
Provides convenient commands for running different test suites
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd):
    """Run a shell command and return exit code"""
    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Run API tests for RecruitifyAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --all              # Run all tests
  python run_tests.py --pdf              # Run PDF extraction tests
  python run_tests.py --gemini           # Run Gemini API tests
  python run_tests.py --rapidapi         # Run RapidAPI tests
  python run_tests.py --integration      # Run integration tests
  python run_tests.py --coverage         # Run with coverage report
  python run_tests.py --verbose          # Run with verbose output
        """
    )
    
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--pdf', action='store_true', help='Run PDF extraction tests')
    parser.add_argument('--gemini', action='store_true', help='Run Gemini API tests')
    parser.add_argument('--rapidapi', action='store_true', help='Run RapidAPI tests')
    parser.add_argument('--integration', action='store_true', help='Run integration tests')
    parser.add_argument('--coverage', action='store_true', help='Run with coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--quick', '-q', action='store_true', help='Quick test run (minimal output)')
    
    args = parser.parse_args()
    
    test_file = "test_apis.py"
    base_cmd = ["pytest", test_file]
    
    if args.verbose:
        base_cmd.append("-vv")
    elif not args.quick:
        base_cmd.append("-v")
    
    if args.quick:
        base_cmd.append("-q")
    
    base_cmd.append("--tb=short")
    
    if args.coverage:
        base_cmd.extend(["--cov=main", "--cov-report=html", "--cov-report=term"])
    
    if args.all or (not any([args.pdf, args.gemini, args.rapidapi, args.integration])):
        exit_code = run_command(base_cmd)
    else:
        if args.pdf:
            cmd = base_cmd + ["::TestPDFExtraction"]
            exit_code = run_command(cmd)
        
        if args.gemini:
            cmd = base_cmd + ["::TestGeminiAPI"]
            exit_code = run_command(cmd)
        
        if args.rapidapi:
            cmd = base_cmd + ["::TestRapidAPIJSearch"]
            exit_code = run_command(cmd)
        
        if args.integration:
            cmd = base_cmd + ["::TestIntegration"]
            exit_code = run_command(cmd)
    
    if exit_code == 0:
        print(f"\n{'='*60}")
        print("✅ All tests passed!")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}")
        print("❌ Some tests failed!")
        print(f"{'='*60}\n")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
