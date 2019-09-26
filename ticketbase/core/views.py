import json
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.images import ImageFile

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# from .models import Foo
# from .serializers import FooSerializer


def index(request):
    context = {}
    return render(request, 'core/index.html', context)



@api_view(['POST'])
def foo(request):
    """
    Create a new foo
    """
    serializer = FooSerializer(data=request.data)
    if serializer.is_valid():
        foo = serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
