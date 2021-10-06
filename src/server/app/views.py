from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.core.files import File
from django.shortcuts import render

from .backend import *
from .tasks.BaseTask import TaskUnknownError


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
        return render(request, 'datasets.html', context={'datasets': get_dataset_models()})
    elif request.method == 'POST':
        files = request.FILES.getlist('files')
        create_dataset_model_from_files(files, request.user)
        return render(request, 'datasets.html', context={'datasets': get_dataset_models()})
    else:
        return HttpResponseForbidden('Wrong method')


@login_required
def dataset(request, dataset_id):
    ds = get_dataset_model(dataset_id)
    if request.method == 'GET':
        action = request.GET.get('action', None)
        if action == 'delete':
            delete_dataset_model(ds)
            return render(request, 'datasets.html', context={'datasets': get_dataset_models()})
    elif request.method == 'POST':
        new_name = request.POST.get('new_name', None)
        if new_name:
            rename_dataset_model(ds, new_name)
            return render(request, 'datasets.html', context={'datasets': get_dataset_models()})
    else:
        return HttpResponseForbidden('Wrong method')
    return render(request, 'dataset.html', context={
        'dataset': ds,
        'tasks': get_task_models_for_dataset(ds),
        'task_types': get_task_types(),
        'file_names': get_file_path_models_names(ds)
    })


@login_required
def tasks(request, dataset_id):
    if request.method == 'POST':
        ds = get_dataset_model(dataset_id)
        task_type = request.POST.get('task_type', None)
        try:
            create_task(task_type, ds)
            return render(request, 'dataset.html', context={
                'dataset': ds,
                'tasks': get_task_models_for_dataset(ds),
                'task_types': get_task_types(),
                'file_names': get_file_path_models_names(ds)
            })
        except TaskUnknownError:
            return HttpResponseForbidden('Unknown task')
    else:
        return HttpResponseForbidden('Wrong method')


@login_required
def task(request, dataset_id, task_id):
    if request.method == 'GET':
        ds = get_dataset_model(dataset_id)
        t = get_task_model(task_id)
        action = request.GET.get('action', None)
        if action == 'delete':
            cancel_and_delete_task(t)
        return render(request, 'dataset.html', context={
            'dataset': ds,
            'tasks': get_task_models_for_dataset(ds),
            'task_types': get_task_types(),
            'file_names': get_file_path_models_names(ds)
        })
    else:
        return HttpResponseForbidden('Wrong method')


@login_required
def download(request, dataset_id):
    if request.method == 'GET':
        ds = get_dataset_model(dataset_id)
        file_path = get_zipped_download(ds)
        with open(file_path, 'rb') as f:
            response = HttpResponse(File(f), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(ds.name)
            return response
    else:
        return HttpResponseForbidden('Wrong method')
