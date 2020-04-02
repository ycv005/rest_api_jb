from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics, permissions, renderers, viewsets
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]
    def get(self,request,*args,**kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

@api_view(['GET'])
def api_root(request,format=None):
    return Response({
    "users": reverse('user-list',request=request,format=format),
    "snippets": reverse("snippet-list",request=request,format=format)
    })

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    # does both job, ie., list and detail actions, #https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#refactoring-to-use-viewsets
    queryset = User.objects.all()
    serializer_class = UserSerializer
