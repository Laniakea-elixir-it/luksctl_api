#!/usr/bin/env python
"""
"""

# Imports
from flask import Flask, jsonify, request
import subprocess
import json, requests
import os, sys
from os.path import exists, pathsep
from string import split

# Create logging facility
import logging
logging.basicConfig(filename='/tmp/luksctl-api.log', format='%(levelname)s %(asctime)s %(message)s', level='DEBUG')

#______________________________________
def exec_cmd(cmd):

  proc = subprocess.Popen( args=cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
  communicateRes = proc.communicate()
  stdOutValue, stdErrValue = communicateRes
  status = proc.wait()

  return status, stdOutValue, stdErrValue


#______________________________________
def which(name):

  PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

  for path in PATH.split(os.path.pathsep):
    full_path = path + os.sep + name
    if os.path.exists(full_path):
      return str(full_path)


#______________________________________
def status():

  command = which('sudo') + ' ' + which('luksctl') + ' status'

  status, stdout, stderr = exec_cmd(command)

  logging.debug( 'Volume status stdout: ' + str(stdout) )
  logging.debug( 'Volume status stderr: ' + str(stderr) )
  logging.debug( 'Volume status: ' + str(status) )

  if str(status) == '0':
    return jsonify({'volume_state': 'mounted' })
  elif str(status)  == '1':
    return jsonify({'volume_state': 'unmounted' })
  else:
    return jsonify({'volume_state': 'unavailable', 'output': stdout, 'stderr': stderr })


#______________________________________
def open(vault_url, vault_token, secret_root, secret_path, secret_key):

  status_command = which('sudo') + ' ' + which('luksctl') + ' status'

  current_stat, current_stodut, current_stderr = exec_cmd(status_command)

  if str(current_stat) == '0':
    return jsonify({'volume_state': 'mounted'})

  else:

    read_token = unwrap_vault_token(vault_url, vault_token)

    secret = read_secret( vault_url, secret_root, secret_path, read_token, secret_key)

    # open volume
    command = 'printf "'+secret+'\n" | ' + which('sudo') + ' ' + which('luksctl') + ' open'

    status, stdout, stderr = exec_cmd(command)

    logging.debug( 'Volume status stdout: ' + str(stdout) )
    logging.debug( 'Volume status stderr: ' + str(stderr) )
    logging.debug( 'Volume status: ' + str(status) )

    if str(status) == '0':
      return jsonify({'volume_state': 'mounted' })
    elif str(status)  == '1':
      return jsonify({'volume_state': 'unmounted' })
    else:
      return jsonify({'volume_state': 'unavailable', 'output': stdout, 'stderr': stderr })


#______________________________________
def unwrap_vault_token(url, wrapping_token):

  url = url + '/v1/sys/wrapping/unwrap'

  headers = { "X-Vault-Token": wrapping_token }

  response = requests.post(url, headers=headers, verify=False)

  response.raise_for_status()

  deserialized_response = json.loads(response.text)

  try:
    deserialized_response["auth"]["client_token"]
  except KeyError:
    raise Exception("[FATAL] Unable to unwrap vault token.")

  return deserialized_response["auth"]["client_token"]


#______________________________________
def read_secret(url, secret_root, secret_path, token, key):

  url = url + '/v1/'+ secret_root +'/data/' + secret_path

  headers = { "X-Vault-Token": token }

  response = requests.get( url, headers=headers, verify=False )

  deserialized_response = json.loads(response.text)

  try:
    deserialized_response["data"]
  except KeyError:
    raise Exception("[FATAL] Unable to write vault path.")

  return deserialized_response["data"]["data"][key]


#______________________________________
def revoke_token(url, token):

  url = url + '/v1/auth/token/revoke-self'

  headers = { "X-Vault-Token": token }

  response = requests.post( url, headers=headers, verify=False )
