#!/usr/bin/env python3
import json
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

def copy_to_clipboard(text):
    # Try Windows (clip.exe)
    if sys.platform == 'win32':
        try:
            subprocess.run(['clip.exe'], input=text.encode('utf-8'), check=True, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            pass

    # Try macOS (pbcopy)
    if sys.platform == 'darwin':
        try:
            subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=True, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            pass

    # Try wl-clipboard (Wayland Linux)
    try:
        subprocess.run(['wl-copy'], input=text.encode('utf-8'), check=True, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        pass
    
    # Try xclip (X11)
    try:
        subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode('utf-8'), check=True, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        pass

    # Try xsel (X11)
    try:
        subprocess.run(['xsel', '--clipboard', '--input'], input=text.encode('utf-8'), check=True, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        pass

    return False

class CharmHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == '/copy-charm':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                x = float(data.get("kc_x2", 0))
                y = float(data.get("kc_y2", 0))
                z = float(data.get("kc_z2", 0))
                
                formatted_cmd = f"!charm_set {x:.2f} {y:.2f} {z:.2f}"
                
                success = copy_to_clipboard(formatted_cmd)
                
                if success:
                    print(f"\n✅ [SUCCESS] Extracted and copied to clipboard: {formatted_cmd}")
                else:
                    print(f"\n❌ [ERROR] Could not copy to clipboard.")
                    print(f"   Make sure wl-clipboard or xclip is installed.")
                    print(f"   Command was: {formatted_cmd}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "command": formatted_cmd}).encode('utf-8'))
                
            except Exception as e:
                print(f"\n[ERROR] Failed to process data: {e}")
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress default HTTP logging to keep the terminal clean
        pass

def run(server_class=HTTPServer, handler_class=CharmHandler, port=5000):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print(f"🚀 Starting CS2 Charm Extractor server on port {port}...")
    print("⏳ Waiting for data from browser... (Press Ctrl+C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        httpd.server_close()

if __name__ == "__main__":
    run()
