#!/usr/bin/env python3
import http.server
import socketserver
import os
import subprocess
import json
from urllib.parse import urlparse, parse_qs
from pathlib import Path

PORT = 6767

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # Handle sensor test endpoint
        if parsed_path.path == '/api/test-sensors':
            query_params = parse_qs(parsed_path.query)
            passcode = query_params.get('passcode', [''])[0]
            
            if passcode != Path("/main/secrets/sp.txt").read_text().strip():
                self.send_response(401)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid passcode', 'success': False}).encode())
                return
            
            try:
                result = subprocess.run(
                    ['python3', os.path.expanduser('~/Soil/main/test/sensorstest.py')],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                output = result.stdout + result.stderr
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'output': output}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e), 'success': False}).encode())
            return
        
        # Serve static files normally
        super().do_GET()

os.chdir(os.path.expanduser('~/Soil'))
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    httpd.serve_forever()