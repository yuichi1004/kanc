import sys
import getopt
import kanpyj

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

    c = kanpyj.Client('http://localhost:8080',
            'a8ae71fc7f1b507389f5254eb0b53afce810ecc127b49c59fed61a2a9c74')
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

