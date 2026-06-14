#!/usr/bin/env python3
"""
mdview — 本地 Markdown 美化阅读器
Usage:
  mdview              # 启动服务，打开浏览器
  mdview file.md      # 启动服务并直接打开指定文件
"""
import sys, os, http.server, urllib.parse, webbrowser, socket, threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIEWER = os.path.join(BASE_DIR, 'md-viewer.html')
PORT = 9274

# Static assets served locally so the PWA (manifest / service worker / icons)
# behaves the same as the deployed site.
STATIC_TYPES = {
    '.webmanifest': 'application/manifest+json',
    '.js': 'text/javascript; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
}

class Handler(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Private-Network', 'true')

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path in ('/', '/index.html', '/md-viewer.html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(VIEWER, 'rb') as f:
                self.wfile.write(f.read())

        elif parsed.path == '/api/read':
            params = urllib.parse.parse_qs(parsed.query)
            path = params.get('path', [''])[0]
            if not path or not os.path.isabs(path) or not os.path.isfile(path):
                self.send_response(404)
                self.send_header('Content-Type', 'text/plain')
                self._cors()
                self.end_headers()
                self.wfile.write(b'File not found')
                return
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self._cors()
            self.end_headers()
            with open(path, 'rb') as f:
                self.wfile.write(f.read())

        elif parsed.path in ('/manifest.webmanifest', '/sw.js', '/favicon.svg') or \
                (parsed.path.startswith('/icons/') and parsed.path.endswith('.png')):
            self._serve_static(parsed.path)

        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not found')

    def _serve_static(self, req_path):
        rel = req_path.lstrip('/')
        full = os.path.normpath(os.path.join(BASE_DIR, rel))
        # path-traversal guard: must stay within BASE_DIR
        if not full.startswith(BASE_DIR + os.sep) or not os.path.isfile(full):
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not found')
            return
        ctype = STATIC_TYPES.get(os.path.splitext(full)[1], 'application/octet-stream')
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self._cors()
        self.end_headers()
        with open(full, 'rb') as f:
            self.wfile.write(f.read())

    def log_message(self, *args):
        pass

def port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

if __name__ == '__main__':
    file_arg = sys.argv[1] if len(sys.argv) > 1 else None

    url = f'http://127.0.0.1:{PORT}/'
    if file_arg:
        path = os.path.abspath(file_arg)
        url += f'?file={urllib.parse.quote(path)}'

    if port_in_use(PORT):
        print(f'服务已在运行，打开: {url}')
        webbrowser.open(url)
        sys.exit(0)

    class ThreadedServer(http.server.HTTPServer):
        daemon_threads = True
        def process_request(self, request, client_address):
            t = threading.Thread(target=self.process_request_thread, args=(request, client_address))
            t.daemon = True
            t.start()
        def process_request_thread(self, request, client_address):
            try:
                self.finish_request(request, client_address)
            except Exception:
                pass
            self.shutdown_request(request)

    server = ThreadedServer(('127.0.0.1', PORT), Handler)
    print(f'Markdown Viewer 已启动: http://127.0.0.1:{PORT}/')
    if file_arg:
        print(f'打开文件: {path}')
    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n已停止')
