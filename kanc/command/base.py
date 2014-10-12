from tabulate import tabulate
import tempfile
import json
import subprocess
import os
import sys

class BaseCommand(object):
    def __init__(self, client):
        self.client = client

    def print_attr(self, item, primary_fields=[]):
        arr = []
        for f in primary_fields:
            arr.append([f, item[f]])
        for f in item:
            if f not in primary_fields:
                arr.append([f, item[f]])
        print tabulate(arr, headers=['name', 'value'], tablefmt='simple')

    def print_items(self, items, fields):
        arr = []
        for i in items:
            row = []
            for f in fields:
                row.append(i[f])
            arr.append(row)
        print tabulate(arr, headers=fields, tablefmt='simple')

    def edit_attr(self, item, required_fields = []):
        editor = os.environ.get('EDITOR')
        if editor is None or editor == '':
            sys.stdout.write('Error: No editor is specified EDITOR')
 
        # create pretty json
        data = "{\n"
        for f in required_fields:
            data += '    "{}":{},\n'.format(f, json.dumps(item[f]))
            del item[f]
        data += "\n"
        for f in item:
            data += '    "{}":{},\n'.format(f, json.dumps(item[f]))
        data = data[0:len(data)-2]
        data = data + "\n}\n"

        tmp_file = tempfile.mkstemp()
        f = file(tmp_file[1], 'w')
        f.write(data)
        f.close()
        subprocess.call([editor, tmp_file[1]])
        f = file(tmp_file[1])
        modified = f.read()
        f.close()
        os.remove(tmp_file[1])

        if data == modified:
            sys.stderr.write('Abort: The data is not updated')
            return None
        
        return json.loads(modified)

