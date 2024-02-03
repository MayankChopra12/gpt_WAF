# app.py

import os
import signal
from flask import Flask, render_template, jsonify
import threading
import subprocess
import time
import mitmapp as mt

chat_gpt_response = ""
mitm_process = None  # Global variable to store the mitmproxy process
response_file_path = "response_file.txt"
mitm_log_file_path = "mitm_log.txt"


app = Flask(__name__)

@app.route('/')
def hello():
    global response_file_path, mitm_log_file_path

    # Read the mitmproxy logs from the file
    with open(mitm_log_file_path, "r") as mitm_log_file:
        mitm_logs = mitm_log_file.read()

    # Read the response from the file
    with open(response_file_path, "r") as response_file:
        chat_gpt_response = response_file.read()

    data = {'chat_gpt_response': chat_gpt_response, 'mitm_logs': mitm_logs}
    return jsonify(data)

def run_flask_app():
    app.run(port=5000)

def start_mitmproxy():
    global mitm_process
    mitm_cmd = ['mitmdump', '-s', 'mitmapp.py', '--quiet']
    mitm_process = subprocess.Popen(mitm_cmd)

def stop_mitmproxy():
    global mitm_process
    if mitm_process:
        print("Stopping mitmproxy...")
        mitm_process.terminate()
        mitm_process.wait()
        print("mitmproxy stopped.")

if __name__ == "__main__":
    # Start mitmproxy in a separate process
    mitm_thread = threading.Thread(target=start_mitmproxy)
    mitm_thread.start()
    
    # Start Flask app
    run_flask_app()

    # Stop mitmproxy when the Flask app is terminated
    stop_mitmproxy()
