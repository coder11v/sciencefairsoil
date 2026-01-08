#!/bin/bash

# Get passcode from query string
PASSCODE=$(echo "$QUERY_STRING" | grep -oP 'passcode=\K[^&]*' | sed 's/%2B/+/g')

echo "Content-Type: application/json"
echo ""

if [ "$PASSCODE" != "MusselGrowth" ]; then
    echo '{"error":"Invalid passcode","success":false}'
    exit 1
fi

# Run the Python sensor test
cd /main/test
OUTPUT=$(python3 sensorstest.py 2>&1)
EXITCODE=$?

if [ $EXITCODE -eq 0 ]; then
    # Use Python to safely escape the output as JSON
    python3 << 'EOF'
import sys
import json
output = sys.stdin.read()
print(json.dumps({"success": True, "output": output}))
EOF
else
    python3 << 'EOF'
import sys
import json
output = sys.stdin.read()
print(json.dumps({"success": False, "error": "Script failed", "output": output}))
EOF
fi