import re
import fnmatch

class Selector:
    """ Selector for target task/project/user """
    def __init__(self, client):
        self.client = client

    def get_tasks(self, project_id, states):
        """
        Get tasks based on project and states
        """
        tasks = []
        for state in states:
            query_result = self.client.get_all_tasks(project_id, state)
            if len(tasks) == 0:
                tasks = query_result
            else:
                for t in query_result:
                    tasks.append(t)
        return tasks

    def filter_tasks_by_name(self, tasks, exp):
        r = re.compile(fnmatch.translate(exp))
        tasks = [t for t in tasks if r.match(t['title'])]
        return tasks
    
    def filter_tasks_by_column(self, tasks, column):
        if len(tasks) == 0:
            return tasks
        project_id = tasks[0]['project_id']
        column_id = None
        for c in self.client.get_columns(project_id):
            if c['title'] == column:
                column_id = c['id']
        if column_id is None:
            raise RuntimeError('No column named {0} found'.format(column))
        tasks = [t for t in tasks if t['column_id'] == column_id]
        return tasks

    def select_tasks(self, exp, project_id, states):
        """
        Select users by id, or name
        """
        tasks = []
        if isinstance(exp, int) or exp.isdigit():
            tasks.append(self.client.get_task(int(exp)))
        else :
            # Get tasks based on states
            tasks = self.get_tasks(project_id, states)
            # Filter tasks based on expression
            tasks = self.filter_tasks_by_name(tasks, exp)
        return tasks

