kanc
====
Kanboard remote CUI client

Installation
----
`pip install kanc` to install.

Usage
----
`kanc init` to create `~/.kanrc` file first. Then you can type `kanc 'command'`

Show Board
-----
Use `kanc board` to display your kanban board.

```
$ kanc board
| Backlog                        | Ready              | Work in progress               | Done                       |
|--------------------------------+--------------------+--------------------------------+----------------------------|
| 005. Support UTF-8             | 004. Update README | 003. User Friendly Help Mes... | 002. Publish v0.1.0 to pip |
| 007. Support Category          |                    |                                | 006. Tag on github         |
| 008. Support Project Permis... |                    |                                |                            |
```

Commands
----
The following commands are available.

* kanc board - show board of current project

* kanc user list - list all users
* kanc user show {user_id} - show user
* kanc user create - create new user
* kanc user edit {user_id} - edit a user
* kanc user remove {user_id_1} {user_id_2} ... - remove users

* kanc project list - list all projects
* kanc project current - show current project
* kanc project swtich {project_id} - switch project
* kanc project show {project_id} - show a proejct
* kanc project create - create new project
* kanc project edit {project_id} - edit a project
* kanc project remove {project_id} {project_id} - remove projects

* kanc task list - list all tasks in current project
* kanc task show {task_id} - show a task
* kanc task create - create new task
* kanc task edit {task_id} - edit a task
* kanc task remove {task_id} {task_id} - remove tasks
* kanc task move {task_id} up - move a task up on the board
* kanc task move {task_id} down - move a task down on the board
* kanc task move {task_id} {column} - move a task to other column
* kanc task open {task_id} - open a task
* kanc task close {task_id} - close a task


Patch Mode
---
Current release of kanboard has several bugs on API. `patched` option will fix
the issue. 

Those bugs are already fixed on master branch. If you want to use non-patched
version of the client, make `patched` option to be false.

License
----
MIT License

