import http.server
import os
import threading

from tpds.helper import log


class UnoServer:
    def __init__(self, port=None):
        self.port = 1304 if port is None else port

    def start_uno(self, path="."):
        # Start the server in a new thread
        daemon = threading.Thread(
            name="daemon_server", target=self.__start_server, args=(path, self.port)
        )

        # Set as a daemon so it will be killed once the main thread is dead.
        daemon.setDaemon(True)
        daemon.start()

    def __start_server(self, path, port):
        """Start a simple webserver serving path on port"""
        current_dir = os.getcwd()
        try:
            if os.path.isdir(path):
                os.chdir(path)
                httpd = http.server.HTTPServer(("", port), quietServer)
                httpd.serve_forever()
            else:
                log("Uno server launching path is invaid.")
        finally:
            os.chdir(current_dir)


class quietServer(http.server.CGIHTTPRequestHandler):
    def log_message(self, format, *args):
        log(args)
