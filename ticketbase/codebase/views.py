import json
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.images import ImageFile
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Ticket


def index(request):
    context = {}
    return render(request, 'codebase/index.html', context)


def search(request):
    q = request.GET.get('q', '')
    keywords = q.split()
    filters = [Q(summary__icontains=kw) | Q(ticketnote__content__icontains=kw) for kw in keywords]
    tickets = Ticket.objects.filter(*filters).distinct().order_by('-ticket_id')
    context = {
        'results': tickets[:100],
        'q': q,
    }
    return render(request, 'codebase/search.html', context)


def ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    context = {
        'ticket': ticket,
    }
    return render(request, 'codebase/ticket.html', context)


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
