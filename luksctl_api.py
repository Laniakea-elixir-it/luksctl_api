from flask import Flask, jsonify, request
import subprocess
import os.path

import luksctl_run

# Create logging facility
import logging
logging.basicConfig(filename='/tmp/luksctl-api.log', format='%(levelname)s %(asctime)s %(message)s', level='DEBUG')

app = Flask(__name__)
if os.path.exists('config.json'):
    app.config.from_json('config.json')
else:
    app.config.from_json('config.json.sample')

infra_config = app.config.get('INFRASTRUCTURE_CONFIGURATION')
virtualization_type = app.config.get('VIRTUALIZATION_TYPE')

@app.route('/luksctl_api/v1.0/status', methods=['GET'])
def get_status():

    return luksctl_run.status()

@app.route('/luksctl_api/v1.0/open', methods=['POST'])
def luksopen():

    if not request.json or \
       not 'vault_url' in request.json or \
       not 'vault_token' in request.json or \
       not 'secret_root' in request.json or \
       not 'secret_path' in request.json or \
       not 'secret_key' in request.json:
       abort(400)

    node_list = None
    if infra_config == 'cluster':
        node_list = app.config.get("WN_IPS")
        logging.debug(node_list)

    return luksctl_run.open(request.json['vault_url'],
                            request.json['vault_token'],
                            request.json['secret_root'],
                            request.json['secret_path'],
                            request.json['secret_key'],
                            infra_config,
                            virtualization_type,
                            node_list)
