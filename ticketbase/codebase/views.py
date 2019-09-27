import json
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.images import ImageFile
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Ticket, User


def index(request):
    context = {}
    return render(request, 'codebase/dashboard.html', context)


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

def dashboard(request, user_id):
    try:
        user = User.objects.get(codebase_id=user_id)
    except User.DoesNotExist:
        return render(request, 'codebase/dashboard.html')

    projects = user.projects.all()

    projects_context = []

    for project in projects:
        filter = [Q(assignee__codebase_id=user_id) & Q(project__project_id=project.project_id)]
        context = {
            'project': project,
            'tickets': Ticket.objects.filter(*filter).distinct().order_by('-ticket_id')[0:5]
        }

        projects_context.append(context)

    context = {
        'projects': projects_context
    }

    return render(request, 'codebase/dashboard.html', context)

def ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    ticket_notes = ticket.ticketnote_set.all()

    context = {
        'ticket': ticket,
        'first_note': ticket_notes.first,
        'ticket_notes': ticket_notes[1:len(ticket_notes)],
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
