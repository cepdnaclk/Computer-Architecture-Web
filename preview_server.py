#!/usr/bin/env python3
"""
Simple local web server to preview the Lectures on Computer Architecture website before deployment.
Run this script and open http://localhost:8000 in your browser.
"""

import http.server
import socketserver
import webbrowser
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add headers to prevent caching during development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    # Change to the project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("=" * 60)
    print("Lectures on Computer Architecture — Local Preview Server")
    print("=" * 60)
    print(f"\n🌐 Starting server at http://localhost:{PORT}")
    print("\n📱 Preview your website:")
    print(f"   • Main page: http://localhost:{PORT}/")
    print(f"   • Lecture 1: http://localhost:{PORT}/lectures/lecture-01.html")
    print("\n💡 Press Ctrl+C to stop the server\n")
    print("=" * 60)
    
    # Open browser automatically
    webbrowser.open(f'http://localhost:{PORT}/')
    
    # Start server
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()
