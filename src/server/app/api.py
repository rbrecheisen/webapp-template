from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .backend import get_dataset_models, get_dataset_model, create_dataset_model_from_files, \
    delete_dataset_model, rename_dataset_model
from .backend import get_task_models, get_task_model, create_task_model, delete_task_model
from .serializers import DataSetModelSerializer, TaskModelSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(request):
    return Response({'message': 'Hello!'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_datasets(request):
    serializer = DataSetModelSerializer(get_dataset_models(request.user), many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset(request, dataset_id):
    serializer = DataSetModelSerializer(get_dataset_model(dataset_id))
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_dataset(request):
    files = request.FILES.getlist('files')
    ds = create_dataset_model_from_files(files, request.user)
    serializer = DataSetModelSerializer(ds)
    return Response(serializer.data, status=201)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def rename_dataset(request, dataset_id):
    dataset = rename_dataset_model(dataset_id, request.PUT.get('new_name', None))
    serializer = DataSetModelSerializer(dataset)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dataset(request, dataset_id):
    delete_dataset_model(dataset_id)
    return Response({'message': 'Dataset {} deleted'.format(dataset_id)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request, dataset_id):
    serializer = TaskModelSerializer(get_task_models(dataset_id))
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request, dataset_id):
    task = create_task_model(dataset_id, dict(request.POST.items()))
    serializer = TaskModelSerializer(task)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task(request, task_id):
    serializer = TaskModelSerializer(get_task_model(task_id))
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    delete_task_model(task_id)
    return Response({'message': 'Task {} deleted'.format(task_id)})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_task(request, task_id):
    # TODO: get parameters as dict and pass to task
    pass
