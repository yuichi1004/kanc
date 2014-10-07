from base import BaseCommand

class ProjectCommand(BaseCommand):
    name = 'project'

    def __init__(self, client):
        super(ProjectCommand, self).__init__(client)
    
    def action(self, args):
        if args[0] == 'list':
            self.print_items(self.client.get_all_projects(), ['id', 'name'])
        elif args[0] == 'show':
            project_id = int(args[1])
            self.print_attr(self.client.get_project_by_id(project_id))

