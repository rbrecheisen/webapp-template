from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

from .backend import get_dataset_models, get_dataset_model, create_dataset_model_from_files, \
    delete_dataset_model, rename_dataset_model


@login_required
@require_http_methods(['GET'])
def index(request):
    return render(request, 'index.html', context={'message': 'Hello!'})


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


@login_required
@require_http_methods(['GET'])
def get_datasets(request):
    return render(request, 'get_datasets.html', context={'datasets': get_dataset_models(request.user)})


@login_required
@require_http_methods(['GET'])
def get_dataset(request, dataset_id):
    return render(request, 'get_dataset.html', context={'dataset': get_dataset_model(dataset_id)})


@login_required
@require_http_methods(['POST'])
def create_dataset(request):
    files = request.FILES.getlist('files')
    dataset = create_dataset_model_from_files(files, request.user)
    return render(request, 'get_dataset.html', context={'dataset': dataset})


@login_required
@require_http_methods(['PUT'])
def rename_dataset(request, dataset_id):
    rename_dataset_model(dataset_id, request.PUT.get('new_name', None))
    return render(request, 'get_dataset.html', context={'dataset': get_dataset_model(dataset_id)})


@login_required
@require_http_methods(['DELETE'])
def delete_dataset(request, dataset_id):
    delete_dataset_model(dataset_id)
    return render(request, 'get_datasets.html', context={'datasets': get_dataset_models(request.user)})
