from tabulate import tabulate

class BaseCommand(object):
    def __init__(self, client):
        self.client = client

    def print_attr(self, item):
        arr = []
        for i in item:
            arr.append([i, item[i]])
        print tabulate(arr, headers=['name', 'value'], tablefmt='simple')

    def print_items(self, items, fields):
        arr = []
        for i in items:
            row = []
            for f in fields:
                row.append(i[f])
            arr.append(row)
        print tabulate(arr, headers=fields, tablefmt='simple')
        
