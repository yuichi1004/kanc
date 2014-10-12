from base import BaseCommand
import json

class UserCommand(BaseCommand):
    name = 'user'

    def __init__(self, client):
        super(UserCommand, self).__init__(client)
        self.param_order = ['id', 'user_id', 'username', 'name']
    
    def action(self, args):
        if args[0] == 'list':
            self.print_items(self.client.get_all_users(), 
                    ['id', 'username', 'name'])
        elif args[0] == 'show':
            user_id = int(args[1])
            user = self.client.get_user(user_id)
            primary_fields = ['id', 'username', 'name']
            self.print_attr(user, primary_fields)
        elif args[0] == 'create':
            user = self.client.create_empty_params('createUser')
            user = self.edit_attr(user)
            if user is not None:
                self.client.create_user(**user)
        elif args[0] == 'edit':
            user_id = int(args[1])
            user = self.client.get_user(user_id)
            user = self.client.remove_unused_params('updateUser', user)
            update = self.edit_attr(user, ['id', 'username'])
            if update is not None:
                self.client.update_user(**update)


