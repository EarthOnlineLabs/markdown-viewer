#!/usr/bin/env python3
"""
mdview — 本地 Markdown 美化阅读器
Usage:
  mdview              # 启动服务，打开浏览器
  mdview file.md      # 启动服务并直接打开指定文件
"""
import sys, os, http.server, urllib.parse, webbrowser, socket

VIEWER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'md-viewer.html')
PORT = 9274

class Handler(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

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

        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not found')

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

    server = http.server.HTTPServer(('127.0.0.1', PORT), Handler)
    print(f'Markdown Viewer 已启动: http://127.0.0.1:{PORT}/')
    if file_arg:
        print(f'打开文件: {path}')
    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n已停止')
