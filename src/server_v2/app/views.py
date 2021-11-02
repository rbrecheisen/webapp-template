from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

from .backend import get_dataset_models, get_dataset_model, create_dataset_model_from_files, \
    delete_dataset_model, rename_dataset_model, get_file_names, get_task_models, get_task_classes, create_task_model, \
    get_task_model, delete_task_model, start_task_in_background, get_task_form


@login_required
@require_http_methods(['GET'])
def index(request):
    return redirect('/datasets/')


# ----------------------------------------------------------------------------------------------------------------------
@login_required
@require_http_methods(['GET'])
def get_datasets(request):
    return render(request, 'datasets.html', context={'datasets': get_dataset_models(request.user)})


@login_required
@require_http_methods(['GET'])
def get_dataset(request, dataset_id):
    return render(request, 'dataset.html', context={
        'dataset': get_dataset_model(dataset_id),
        'task_classes': get_task_classes(),
        'tasks': get_task_models(dataset_id), 'file_names': get_file_names(dataset_id)})


@login_required
@require_http_methods(['POST'])
def create_dataset(request):
    files = request.FILES.getlist('files')
    dataset = create_dataset_model_from_files(files, request.user)
    return render(request, 'dataset.html', context={
        'dataset': get_dataset_model(dataset.id),
        'task_classes': get_task_classes(),
        'tasks': get_task_models(dataset.id), 'file_names': get_file_names(dataset.id)})


@login_required
@require_http_methods(['POST'])
def rename_dataset(request, dataset_id):
    dataset = rename_dataset_model(dataset_id, request.POST.get('new_name', None))
    return render(request, 'dataset.html', context={
        'dataset': get_dataset_model(dataset.id),
        'task_classes': get_task_classes(),
        'tasks': get_task_models(dataset.id), 'file_names': get_file_names(dataset.id), 'renamed': True})


@login_required
@require_http_methods(['GET'])
def delete_dataset(request, dataset_id):
    delete_dataset_model(dataset_id)
    return render(request, 'datasets.html', context={'datasets': get_dataset_models(request.user)})


# ----------------------------------------------------------------------------------------------------------------------
@login_required
@require_http_methods(['POST'])
def create_task(request, dataset_id):
    ds = get_dataset_model(dataset_id)
    task = create_task_model(ds, request.POST.get('task_class', None))
    return render(request, 'task.html', context={'task': task, 'task_form': get_task_form(task.id)})


@login_required
@require_http_methods(['GET'])
def get_task(request, task_id):
    return render(request, 'task.html', context={
        'task': get_task_model(task_id), 'task_form': get_task_form(task_id)})


@login_required
@require_http_methods(['GET'])
def delete_task(request, task_id):
    task = get_task_model(task_id)
    dataset_id = task.dataset.id
    delete_task_model(task_id)
    return render(request, 'dataset.html', context={
        'dataset': get_dataset_model(dataset_id),
        'task_classes': get_task_classes(),
        'tasks': get_task_models(dataset_id), 'file_names': get_file_names(dataset_id)})


@login_required
@require_http_methods(['POST'])
def start_task(request, task_id):
    task = get_task_model(task_id)
    task.parameters = dict(request.POST.items())
    # task.save()
    task = start_task_in_background(task)
    return render(request, 'dataset.html', context={
        'dataset': get_dataset_model(task.dataset.id),
        'task_classes': get_task_classes(),
        'tasks': get_task_models(task.dataset.id), 'file_names': get_file_names(task.dataset.id)})


# ----------------------------------------------------------------------------------------------------------------------
def handle_login(request):
    """ This view allows retrieval of a session ID for the purpose of calling views protected
    with the @login_required decorator using REST. You can then use Python requests to call HTML-based
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
    return HttpResponseForbidden('wrong method')
