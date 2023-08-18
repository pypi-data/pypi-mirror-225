import socket
import threading
from contextlib import closing
from time import sleep
from flask import Flask, request, send_from_directory
from pyngrok import ngrok
from pysingleton import PySingleton

app = Flask(__name__)


@app.route("/callback", methods=["POST"])
def webhook_handler():
    result = request.json
    state = result["state"]
    uid = result["uid"]
    cb_queue, tmp_dir = WebhookServer.QUEUES.get(uid)
    if state == "done":
        txt_file = tmp_dir / f"{uid}.txt"
        speeches = result["speeches"]
        with txt_file.open("a") as fout:
            for speech in speeches:
                fout.write(speech["formattedText"] + "\n")
    cb_queue.get()
    cb_queue.task_done()
    return "OK"


@app.route("/files/<path:filename>", methods=["GET"])
def getfile(filename):
    return send_from_directory("/tmp", filename)


@app.route("/shutdown", methods=['GET'])
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return "Shutting down..."


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class WebhookServer(metaclass=PySingleton):
    QUEUES = {}

    def __init__(self, host="localhost", port=None):
        if port is None:
            port = find_free_port()
        self.port = port
        self.host = host
        threading.Thread(
            target=lambda: app.run(
                host=self.host, port=self.port, debug=True, use_reloader=False
            )
        ).start()
        sleep(5)
        self.tunnel = ngrok.connect(str(self.port), bind_tls=True)

    def stop(self):
        import requests
        requests.get(f"http://{self.host}:{self.port}/shutdown")

    @property
    def public_url(self):
        return self.tunnel.public_url
