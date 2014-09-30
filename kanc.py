import os
import sys
import fileinput
import getopt
import getpass
import kanpyj
import json

def usage():
    sys.exit(2)

def print_arr(arr, header = None):
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
    for row in arr:
        for i in range(0, len(row)):
            fmt = '{:<' + str(max_len[i] + 1) + '}' 
            sys.stdout.write(fmt.format(row[i]))
        sys.stdout.write('\n')

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
        host = fileinput.input()
        apikey = getpass.getpass('input your api key: ')
    c = kanpyj.Client(host, apikey)
    if args[0] == 'project':
        if args[1] == 'list':
            list_items(c.get_all_projects(), ['id', 'name'], json_mode)
        elif args[1] == 'show':
            item = c.get_project_by_id(int(args[2]))
            show_attr(item, json_mode)
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

if __name__ == '__main__':
    main()

