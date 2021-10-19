from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(_):
    return Response({'message': 'Hello!'}, template_name='index.html')


@api_view(['GET', 'POST'])
def datasets(request):
    pass


@api_view(['GET', 'DELETE'])
def dataset(request):
    pass


@api_view(['GET', 'POST'])
def tasks(request):
    pass


@api_view(['GET', 'DELETE'])
def task(request):
    pass
