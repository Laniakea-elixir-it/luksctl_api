from flask import Flask, jsonify, request
import subprocess

import luksctl_run

app = Flask(__name__)
app.config.from_json('config.json')

# Create logging facility
import logging
logging.basicConfig(filename='/tmp/luksctl-api-wn.log', format='%(levelname)s %(asctime)s %(message)s', level='DEBUG')

nfs_mountpoint_list = app.config.get('NFS_MOUNTPOINT_LIST')

@app.route('/luksctl_api_wn/v1.0/status', methods=['GET'])
def get_status():

    return luksctl_run.get_status(nfs_mountpoint_list)

@app.route('/luksctl_api_wn/v1.0/nfs-mount', methods=['POST'])
def nfs_mount():

    return luksctl_run.nfs_mount(nfs_mountpoint_list)
