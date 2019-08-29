from http.server import BaseHTTPRequestHandler, HTTPServer
import os


PORT = 8080


class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'

        try:
            print(f'recv req for: {self.path}')
            sendReply = False
            if self.path.endswith('.html'):
                mimetype = 'text/html'
                sendReply = True
            elif self.path.endswith('.csv'):
                mimetype = 'text/csv'
                sendReply = True

            if sendReply:
                with open(os.curdir + os.sep + self.path, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(f.read())
        except IOError:
            self.send_error(404, f'File not found: {self.path}')


try:
    server = HTTPServer(('', PORT), WebHandler)
    print("serving at port", PORT)
    server.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down web server')
    server.socket.close()
