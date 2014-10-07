from base import BaseCommand

class UserCommand(BaseCommand):
    name = 'user'

    def __init__(self, client):
        super(UserCommand, self).__init__(client)
    
    def action(self, args):
        if args[0] == 'list':
            self.print_items(self.client.get_all_users(), 
                    ['id', 'username', 'name'])
        elif args[0] == 'show':
            user_id = int(args[1])
            self.print_attr(self.client.get_user(user_id))

