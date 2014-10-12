#!/usr/bin/env python
from tabulate import tabulate
import os
import sys
import getopt
import getpass
import kanpyj
import json
import subprocess
import tempfile
from .command import factory

def usage():
    sys.exit(2)

def edit(data):
    editor = os.environ.get('EDITOR')
    if editor is None or editor == '':
        sys.stdout.write('Error: No editor is specified EDITOR')
    tmp_file = tempfile.mkstemp()
    f = file(tmp_file[1], 'w')
    f.write(data)
    f.close()
    subprocess.call([editor, tmp_file[1]])
    f = file(tmp_file[1])
    updated_data = f.read()
    f.close()
    os.remove(tmp_file[1])

    if data == updated_data:
        sys.stderr.write('Abort: The data is not updated')
        return None
    return updated_data

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hjp')
    except getopt.GetoptError as err:
        usage()

    json_mode = ('-j', '') in opts
    host = None
    apikey = None

    rcfile = os.path.expanduser('~/.kancrc')
    if os.path.exists(rcfile):
        with open(rcfile) as f:
            rc = f.read()
        rc_dict = json.loads(rc)
        host = rc_dict['host']
        apikey = rc_dict['apikey']

    if host is None:
        sys.stdout.write('input your host: ')
        host = sys.stdin.readline()
        apikey = getpass.getpass('input your api key: ')
    c = kanpyj.PatchedClient(host, apikey)
    
    cmd = factory.create(args[0], c)
    if cmd is None:
        usage()
    cmd.action(args[1:])

if __name__ == '__main__':
    main()

