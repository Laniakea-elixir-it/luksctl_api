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
logging.basicConfig(filename='/tmp/luksctl-api-wn.log', format='%(levelname)s %(asctime)s %(message)s', level='DEBUG')

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

  command = which('sudo') + ' ' + which('ls') + ' /home/galaxy/galaxy'

  status, stdout, stderr = exec_cmd(command)

  logging.debug( 'Volume status stdout: ' + str(stdout) )
  logging.debug( 'Volume status stderr: ' + str(stderr) )
  logging.debug( 'Volume status: ' + str(status) )

  logging.debug(os.path.isdir('/home/galaxy/galaxy'))

  if os.path.exists('/home/galaxy/galaxy'):
    return jsonify({'nfs_state': 'mounted' })
  else:
    return jsonify({'nfs_state': 'unmounted'})

#______________________________________
def nfs_restart():

  command = which('sudo') + ' ' + which('systemctl') + ' restart nfs-server'

  print os.name

  status, stdout, stderr = exec_cmd(command)

  logging.debug( 'Volume status stdout: ' + str(stdout) )
  logging.debug( 'Volume status stderr: ' + str(stderr) )
  logging.debug( 'Volume status: ' + str(status) )

  return status()
