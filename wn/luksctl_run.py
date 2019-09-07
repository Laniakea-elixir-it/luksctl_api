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
def check_status(nfs_mount_list):

  for mountpoint in nfs_mount_list:
    logging.debug(mountpoint + ': ' + str(os.path.ismount(mountpoint)))
    if not os.path.ismount(mountpoint):
      return False

  return True

#______________________________________
def get_status(nfs_mount_list):

  logging.debug(nfs_mount_list)

  if check_status(nfs_mount_list):
    return jsonify({'nfs_state': 'mounted' })
  else:
    return jsonify({'nfs_state': 'unmounted'})

#______________________________________
def nfs_mount(nfs_mount_list):

  if check_status(nfs_mount_list):
    return jsonify({'nfs_state': 'mounted' })

  command = which('sudo') + ' ' + which('mount') + ' -a -t nfs'

  logging.debug(command)

  status, stdout, stderr = exec_cmd(command)

  logging.debug( 'NFS mount subprocess call status: ' + str(status) )
  logging.debug( 'NFS mount subprocess call stdout: ' + str(stdout) )
  logging.debug( 'NFS mount subprocess call stderr: ' + str(stderr) )

  return get_status(nfs_mount_list)
