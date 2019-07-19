from flask import Flask, jsonify, request
import subprocess

import luksctl_run


app = Flask(__name__)

@app.route('/api/v1.0/status', methods=['GET'])
def get_status():

    return luksctl_run.status()

@app.route('/api/v1.0/open', methods=['POST'])
def lusopen():

    if not request.json or \
       not 'vault_url' in request.json or \
       not 'vault_token' in request.json or \
       not 'secret_root' in request.json or \
       not 'secret_path' in request.json or \
       not 'secret_key' in request.json:
       abort(400)

    return luksctl_run.open(request.json['vault_url'],
                            request.json['vault_token'],
                            request.json['secret_root'],
                            request.json['secret_path'],
                            request.json['secret_key'])
