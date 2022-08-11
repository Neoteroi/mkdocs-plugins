import os
from multiprocessing import Process
from time import sleep

import pytest
from flask import Flask

SERVER_PORT = 44777
BASE_URL = f"http://127.0.0.1:{SERVER_PORT}"


app = Flask(__name__, static_url_path="", static_folder="res")


def start_server():
    app.run(host="127.0.0.1", port=44777)


def get_sleep_time():
    # when starting a server process,
    # a longer sleep time is necessary on Windows
    if os.name == "nt":
        return 1.5
    return 0.5


def _start_server_process(target):
    server_process = Process(target=target)
    server_process.start()
    sleep(get_sleep_time())

    if not server_process.is_alive():
        raise TypeError("The server process did not start!")

    yield 1

    sleep(1.2)
    server_process.terminate()


@pytest.fixture(scope="module", autouse=True)
def test_server():
    yield from _start_server_process(start_server)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=44778, debug=True)
