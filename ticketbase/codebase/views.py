import json
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.images import ImageFile
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Ticket, User, Project


def index(request):
    project_options = request.user.projects.all()

    context = {"projects": project_options}
    return render(request, 'codebase/dashboard.html', context)


@login_required
def search(request):
    project_options = request.user.projects.all()
    q = request.GET.get('q', '')
    assignee_id = request.GET.get('assignee_id', '')
    assignee = request.GET.get('assignee', '')
    project_name = request.GET.get('project', 'all').lower()
    is_closed = request.GET.get('is_closed', False)

    if project_name == 'all':
        assignee_options = User.objects.all()
    else:
        projects = Project.objects.filter(slug=project_name)
        assignee_options = User.objects.filter(projects__in=projects)
    keywords = q.split()
    filters = [Q(summary__icontains=kw) | Q(ticketnote__content__icontains=kw) for kw in keywords]

    if is_closed == 'true':
        filters.append(Q(is_closed=True))
    elif is_closed == 'false':
        filters.append(Q(is_closed=False))

    if project_name != 'all':
        filters.append(Q(project__name=project_name))

    if assignee_id:
        filters.append(Q(assignee__codebase_id=assignee_id))

    if assignee:
        filters.append(Q(assignee__username=assignee))

    tickets = Ticket.objects.filter(*filters).distinct().order_by('-ticket_id')
    context = {
        'results': tickets[:10],
        'q': q,
        'assignee_options': assignee_options,
        'projects': project_options,
    }
    return render(request, 'codebase/search.html', context)


@login_required
def dashboard(request):
    user = request.user
    projects = user.projects.all()
    projects_context = []

    for project in projects:
        filter = [Q(assignee=user) & Q(project__project_id=project.project_id)]
        context = {
            'project': project,
            'tickets': Ticket.objects.filter(*filter).distinct().order_by('-ticket_id')[0:5]
        }

        projects_context.append(context)

    context = {
        'projects': projects_context
    }

    return render(request, 'codebase/dashboard.html', context)


@login_required
def ticket(request, project_name, ticket_id):
    project_options = request.user.projects.all()
    ticket = Ticket.objects.get(ticket_id=ticket_id, project__slug=project_name)
    ticket_notes = ticket.ticketnote_set.all()

    context = {
        'ticket': ticket,
        'first_note': ticket_notes.first,
        'ticket_notes': ticket_notes[1:len(ticket_notes)],
        "projects": project_options,
    }
    return render(request, 'codebase/ticket.html', context)


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
