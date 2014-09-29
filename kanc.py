import os
import sys
import fileinput
import getopt
import getpass
import kanpyj
import json

def usage():
    sys.exit(2)

def project_to_str(item):
    return '{}\t{}'.format(item['id'], item['name'])

def user_to_str(item):
    return '{}\t{}\t{}'.format(item['id'], item['username'], item['name'])

def list_items(items, func):
    for i in items:
        print func(i)

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
            list_items(c.get_all_projects(), project_to_str)
        elif args[1] == 'show':
            item = c.get_project_by_id(int(args[2]))
            show_attr(item)
    elif args[0] == 'user':
        if args[1] == 'list':
            list_items(c.get_all_users(), user_to_str)
        elif args[1] == 'show':
            show_attr(c.get_user(int(args[2])))

if __name__ == '__main__':
    main()

