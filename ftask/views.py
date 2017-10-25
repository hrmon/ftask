import datetime
from mongoengine.queryset.visitor import Q
from flask import Blueprint, request, redirect, url_for, flash
from models import Task, db

taskapp = Blueprint('taskapp', __name__, url_prefix='/taskapp')

@taskapp.route("/", methods=['GET'])
def index():
    """display submited jobs, can get filtered by time, tags and project"""
    data = request.get_json()
    if data['project'] is not None and data['tag'] is not None:
        return Task.objects(Q(start__gte=data['start']) &
                            Q(start__lte=data['finish']) &
                            Q(project=data['project']) &
                            Q(tags=data['tag']))
    elif data['project'] is not None:
        return Task.objects(Q(start__gte=data['start']) &
                            Q(start__lte=data['finish']) &
                            Q(project=data['project']))
    elif data['tag'] is not None:
        return Task.objects(Q(start__gte=data['start']) &
                            Q(start__lte=data['finish']) &
                            Q(tags=data['tag']))
    return Task.objects()

@taskapp.route("/", methods=['POST'], strict_slashes=False) # accessing without trailing slash makes error on POST method
def create_task():
    """create new task"""
    data = request.get_json()
    if data is not None:
        new = Task(title=data['title']) # set task properties
        new.tags = data['tags']
        new.project = data.get('project', 'default')
        new.description = data.get('description', None)
        new.ID = Task.object().count()+1
        if data['start'] is None:   # if it is a new running task
            if Task.objects(running=True).count() == 0:
                new.start = datetime.datetime.now()
                new.save()
            else:
                pass
        elif is_valid_time(data['start'], data['finish']):
            new.start = data['start']
            new.finish = data['finish']
            new.save()
        else:
            pass
    else:
        pass
    return redirect(url_for('taskapp.index'))

@taskapp.route('/<int:task_id>', methods=['POST'])
def update(task_id):
    '''update a task properties or terminate a running task'''
    data = request.get_json()
    task = Task.objects(ID=task_id)
    if data['action'] == 'modify':
        task.tags = data['tags']
        task.project = data['project']
        task.description = data['description']
        task.start = data.get('start', task.start)
        task.finish = data.get('finish', task.finish)
        if is_valid_time(task.start,task.finish):
            task.save()
        else:
            pass
    elif data['action'] == 'terminate':
        if task.running == True:
            task.finish = datetime.datetime.now()
            task.running = False
        else:
            pass

#@taskapp.route('/<int:task_id>', methods=['delete'])

def is_valid_time(start, finish):
    '''test if duration is positive and it doesn't end in future'''
    if finish < start or finish > datetime.datetime.now():
        return False
    else:
        return True


# TODO raise and handle exceptions
# TODO use jsl to validate json inputs
# TODO create a task based on a previous one
