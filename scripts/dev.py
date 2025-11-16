#!/usr/bin/env python3
"""Development utility scripts."""

import sys
import subprocess

COMMANDS = {
    'install': ['pip', 'install', '-r', 'requirements.txt'],
    'install-dev': ['pip', 'install', '-r', 'requirements.txt', '-r', 'requirements-dev.txt'],
    'test': ['pytest', 'tests/', '-v'],
    'test-cov': ['pytest', 'tests/', '--cov=src', '--cov-report=html'],
    'demo': ['python', 'demo/demo_report.py'],
}

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Usage: python scripts/dev.py [command]")
        print("\nAvailable commands:")
        for cmd in COMMANDS:
            print(f"  {cmd}")
        sys.exit(1)
    
    cmd = COMMANDS[sys.argv[1]]
    subprocess.run(cmd)