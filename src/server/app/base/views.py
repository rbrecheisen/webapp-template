from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render

from .backend import *


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
    """ This view shows a list of datasets and allows upload of files that define a new dataset. Files
    can be of any type and there can be files of mixing types in a single dataset. Only later processing
    will determine whether file types are allowed.
    """
    if request.method == 'GET':
        return render(request, 'base/datasets.html', context={'datasets': get_datasets()})
    elif request.method == 'POST':
        files = request.FILES.getlist('files')
        create_dataset(files, request.user)
        return render(request, 'base/datasets.html', context={'datasets': get_datasets(), 'errors': []})
    else:
        return HttpResponseForbidden('Wrong method')


@login_required
def dataset(request, dataset_id):
    """ This view shows details about a single dataset and its files. You can also delete a dataset
    by providing the 'action' query parameter in the URL. If the dataset is associated with tasks,
    a list of these tasks is displayed.
    """
    ds = get_dataset(dataset_id)
    action = request.GET.get('action', None)
    if action == 'delete':
        delete_dataset(ds)
        return render(request, 'base/datasets.html', context={'datasets': get_datasets()})
    return render(request, 'base/dataset.html', context={
        'dataset': ds, 'tasks': get_tasks_for_dataset(ds), 'files': get_files(ds)})


@login_required
def tasks(request):
    if request.method == 'GET':
        return render(request, 'base/tasks.html', context={
            'tasks': get_tasks(), 'task_types': get_task_types()})
    elif request.method == 'POST':
        pass
    else:
        return HttpResponseForbidden('Wrong method')


@login_required
def task(request, task_id):
    pass
