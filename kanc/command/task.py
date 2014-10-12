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
            self.print_attr(task, ['id','title'])
        elif args[0] == 'create':
            task = self.client.create_empty_params('createTask')
            task = self.edit_attr(task, ['title', 'project_id'])
            if task is not None:
                self.client.create_task(**task)
        elif args[0] == 'edit':
            task_id = int(args[1])
            task = self.client.get_task(task_id)
            task = self.client.remove_unused_params('updateTask', task)
            update = self.edit_attr(task, ['id','title'])
            if update is not None:
                self.client.update_task(**update)

