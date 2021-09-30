from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render

from .backend import *
from .tasks import TaskUnknownError


def handle_login(request):
    """ This view allows retrieval of a session ID for the purpose of calling views protected
    with the @login_required decorator. You can then use Python Requests to call HTML-based
    views instead of REST API endpoints.
    """
    if request.method == 'GET':
        username = request.GET['username']
        password = request.GET['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # This response contains the CSRF token as well as the Session ID
            # that you need in subsequent requests to @login_required decorated views
            return HttpResponse('authenticated')
        return HttpResponseForbidden('wrong username or password')
    return HttpResponseForbidden('Wrong method')


@login_required
def datasets(request):
    if request.method == 'GET':
        return render(request, 'datasets.html', context={'datasets': get_datasets()})
    elif request.method == 'POST':
        files = request.FILES.getlist('files')
        create_dataset(files, request.user)
        return render(request, 'datasets.html', context={'datasets': get_datasets()})
    else:
        return HttpResponseForbidden('Wrong method')


@login_required
def dataset(request, dataset_id):
    ds = get_dataset(dataset_id)
    action = request.GET.get('action', None)
    if action == 'delete':
        delete_dataset(ds)
        return render(request, 'datasets.html', context={'datasets': get_datasets()})
    return render(request, 'dataset.html', context={
        'dataset': ds,
        'tasks': get_tasks_for_dataset(ds),
        'task_types': get_task_types(),
        'files': get_files(ds)
    })


@login_required
def tasks(request, dataset_id):
    if request.method == 'POST':
        ds = get_dataset(dataset_id)
        task_type = request.POST.get('task_type', None)
        try:
            create_task(task_type, ds)
            return render(request, 'dataset.html', context={
                'dataset': ds,
                'tasks': get_tasks_for_dataset(ds),
                'task_types': get_task_types(),
                'files': get_files(ds)
            })
        except TaskUnknownError:
            return HttpResponseForbidden('Unknown task')
    else:
        return HttpResponseForbidden('Wrong method')


@login_required
def task(request, dataset_id, task_id):
    """ This view is only used for deleting tasks. """
    if request.method == 'GET':
        ds = get_dataset(dataset_id)
        t = get_task(task_id)
        action = request.GET.get('action', None)
        if action == 'delete':
            cancel_and_delete_task(t)
        return render(request, 'dataset.html', context={
            'dataset': ds,
            'tasks': get_tasks_for_dataset(ds),
            'task_types': get_task_types(),
            'files': get_files(ds)
        })
    else:
        return HttpResponseForbidden('Wrong method')
