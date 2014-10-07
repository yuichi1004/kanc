from board import BoardCommand
from user import UserCommand
from project import ProjectCommand
from task import TaskCommand
import inspect
import sys

def create(name, client):
    commands = [BoardCommand, UserCommand, ProjectCommand, TaskCommand]
    for c in commands:
        if c.name == name:
            return c(client)
    return None

