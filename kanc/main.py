#!/usr/bin/env python
import os
import sys
import getopt
import getpass
import kanpyj
import json
import subprocess
import tempfile

def usage():
    sys.exit(2)

def print_row_with_border(row, col_size, row_type='data'):
    vline = ''
    if row_type == 'header' or row_type == 'footer':
        for i in range(0, len(row)):
            vline += '+'
            for j in range(col_size[i]+1):
                    vline += '-'
        vline += '+'
        print vline
    if row_type == 'header' or row_type == 'data':
        for i in range(0, len(row)):
            fmt = '|{:<' + str(col_size[i] + 1) + '}'
            sys.stdout.write(fmt.format(row[i]))
        sys.stdout.write('|\n')
    if row_type == 'header':
        print vline

def print_row_simple(row, col_size, row_type='data'):
    if row_type == 'header' or row_type == 'data':
        for i in range(0, len(row)):
            fmt = '{:<' + str(col_size[i] + 1) + '} '
            sys.stdout.write(fmt.format(row[i]))
        sys.stdout.write('\n')

def print_arr(arr, header = None, sort=True, border=False):
    if sort:
        arr = sorted(arr, key=lambda i: i[0])
    arr.insert(0, header)
    for i in range(len(arr[0])):
        arr[0][i] = arr[0][i].upper()
    max_len=[]
    for row in arr:
        for i in range(0, len(row)):
            if i >= len(max_len):
                max_len.append(0)
            if row[i] is not None and max_len[i] < len(row[i]):
                max_len[i] = len(row[i])

    print_row_func = print_row_with_border if border else print_row_simple
    # header
    for row in arr[:1]:
        print_row_func(row, max_len, 'header')
    # body
    for row in arr[1:]:
        print_row_func(row, max_len, 'data')
    print_row_func(arr[0], max_len, 'footer')

def list_items(items, fields, json_mode):
    if json_mode:
        print json.dumps(items, indent=2)
    else:
        arr = []
        for i in items:
            row = []
            for f in fields:
                row.append(i[f])
            arr.append(row)
        print_arr(arr, fields)

def show_attr(item, json_mode):
    if json_mode:
        print json.dumps(item, indent=2)
    else:
        arr = []
        for i in item:
            arr.append([i, item[i]])
        print_arr(arr, ['name', 'value'])

def show_board(board):
    header = []
    rows = []
    max_tasks = 0
    for col in board:
        header.append(col['title'])
        if max_tasks < len(col['tasks']):
            max_tasks = len(col['tasks'])
    for i in range(max_tasks):
        row = []
        for c in range(len(board)):
            if i < len(board[c]['tasks']):
                t = board[c]['tasks'][i]
                title ='{:>03}. {}'.format(t['id'], t['title'])
                if len(title) > 30:
                    title = title[:27] + '...'
                row.append(title)
            else:
                row.append('')
        rows.append(row)

    print_arr(rows, header, sort=False, border=True)

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
        rc = open(rcfile).read()
        rc_dict = json.loads(rc)
        host = rc_dict['host']
        apikey = rc_dict['apikey']

    if host is None:
        sys.stdout.write('input your host: ')
        host = sys.stdin.readline()
        apikey = getpass.getpass('input your api key: ')
    c = kanpyj.Client(host, apikey)
    if args[0] == 'project':
        if args[1] == 'list':
            list_items(c.get_all_projects(), ['id', 'name'], json_mode)
        elif args[1] == 'show':
            item = c.get_project_by_id(int(args[2]))
            show_attr(item, json_mode)
        elif args[1] == 'create':
            j = edit(json.dumps({'name':''}))
            if j is not None:
                c.create_project(j)
    elif args[0] == 'user':
        if args[1] == 'list':
            list_items(c.get_all_users(), ['id', 'username', 'name'], json_mode)
        elif args[1] == 'show':
            show_attr(c.get_user(int(args[2])), json_mode)
    elif args[0] == 'task':
        if args[1] == 'list':
            item = c.get_all_tasks(int(args[2]), 1)
            list_items(item)
        elif args[1] == 'show':
            show_attr(c.get_task(int(args[2])), json_mode)
    elif args[0] == 'board':
        if args[1] == 'show':
            show_board(c.get_board(int(args[2])))

if __name__ == '__main__':
    main()

