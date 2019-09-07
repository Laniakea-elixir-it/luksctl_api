from flask import Flask, jsonify, request
import subprocess

import luksctl_run

app = Flask(__name__)

@app.route('/luksctl_api_wn/v1.0/status', methods=['GET'])
def get_status():

    return luksctl_run.status()

@app.route('/luksctl_api_wn/v1.0/nfs-restart', methods=['POST'])
def nfs_restart():

    return luksctl_run.nfs_restart()
