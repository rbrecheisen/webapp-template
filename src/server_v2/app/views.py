from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer, TemplateHTMLRenderer])
def index(_):
    return Response({'message': 'Hello!'}, template_name='index.html')
