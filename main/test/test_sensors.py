#!/usr/bin/env python3
"""
TO be used by index.html in main proj dir.
"""
import sys
import subprocess
import json
import os
from urllib.parse import parse_qs

# Set headers for JSON
print("Content-Type: application/json")
print()

# Get the query string
query_string = os.environ.get('QUERY_STRING', '')
params = parse_qs(query_string)
passcode = params.get('passcode', [''])[0]

if passcode != 'MusselGrowth':
    print(json.dumps({'error': 'Invalid passcode', 'success': False}))
    sys.exit(1)

try:
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sensorstest_path = os.path.join(script_dir, 'sensorstest.py')
    
    # Run the sensor test
    result = subprocess.run(
        ['python3', sensorstest_path],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=script_dir  # Run from the test directory
    )
    
    output = result.stdout + result.stderr
    
    print(json.dumps({
        'success': True,
        'output': output
    }))
except subprocess.TimeoutExpired:
    print(json.dumps({
        'error': 'Test timed out after 30 seconds',
        'success': False
    }))
except Exception as e:
    print(json.dumps({
        'error': str(e),
        'success': False
    }))
