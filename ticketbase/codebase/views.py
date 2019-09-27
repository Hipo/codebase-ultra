import json
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.images import ImageFile
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Ticket


def index(request):
    context = {}
    return render(request, 'codebase/index.html', context)


def search(request):
    q = request.GET.get('q', '')
    assignee_id = request.GET.get('assignee_id', '')
    assignee = request.GET.get('assignee', '')
    keywords = q.split()
    keyword_filter = [Q(summary__icontains=kw) | Q(ticketnote__content__icontains=kw) for kw in keywords]

    if assignee_id:
        keyword_filter.append(Q(assignee__codebase_id=assignee_id))

    if assignee:
        keyword_filter.extend([Q(assignee__username__icontains=assignee) |
                               Q(assignee__first_name__icontains=assignee) |
                               Q(assignee__last_name__icontains=assignee) |
                               Q(assignee__email__icontains=assignee)])

    tickets = Ticket.objects.filter(*keyword_filter).distinct().order_by('-ticket_id')
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


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'codebase/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
