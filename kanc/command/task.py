from base import BaseCommand

class TaskCommand(BaseCommand):
    name = 'task'

    def __init__(self, client):
        super(TaskCommand, self).__init__(client)
    
    def action(self, args):
        if args[0] == 'list':
            project_id = 1
            tasks = self.client.get_all_tasks(project_id, 1)
            self.print_items(tasks, ['id', 'name'])
        elif args[0] == 'show':
            task_id = int(args[1])
            task = self.client.get_task(task_id)
            self.print_attr(task)

