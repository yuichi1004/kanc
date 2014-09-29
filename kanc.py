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
            if max_len[i] < len(row[i]):
                max_len[i] = len(row[i])
    for row in arr:
        for i in range(0, len(row)):
            fmt = '{:<' + str(max_len[i] + 1) + '}' 
            sys.stdout.write(fmt.format(row[i]))
        sys.stdout.write('\n')

def list_items(items, fields):
    arr = []
    for i in items:
        row = []
        for f in fields:
            row.append(i[f])
        arr.append(row)
    print_arr(arr, fields)

def show_attr(item):
    max_len = 0
    for k in item:
        if len(k) > max_len:
            max_len = len(k)
    for k in item:
        fmt = '{:<' + str(max_len + 2) +  '}{}'
        print fmt.format(k, item[k])

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hj:p')
    except getopt.GetoptError as err:
        usage()

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
            list_items(c.get_all_projects(), ['id', 'name'])
        elif args[1] == 'show':
            item = c.get_project_by_id(int(args[2]))
            show_attr(item)
    elif args[0] == 'user':
        if args[1] == 'list':
            list_items(c.get_all_users(), ['id', 'username', 'name'])
        elif args[1] == 'show':
            show_attr(c.get_user(int(args[2])))

if __name__ == '__main__':
    main()

