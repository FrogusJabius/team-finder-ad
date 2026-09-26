from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from projects.forms import ProjectForm
from projects.models import Project

from team_finder.constants import PROJECTS_PER_PAGE, STATUS_CLOSED
from team_finder.services import paginate


def project_list(request):
    projects = Project.objects.select_related(
        'owner').prefetch_related('participants')
    projects_page = paginate(projects, request, PROJECTS_PER_PAGE)
    return render(request, 'projects/project_list.html', {'projects': projects_page})


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related(
            'owner').prefetch_related('participants'),
        pk=project_id
    )
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect('projects:detail', project_id=project.pk)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner != request.user:
        return redirect('projects:detail', project_id=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('projects:detail', project_id=project_id)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})


@login_required
@require_POST
def join_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.participants.add(request.user)
    return redirect('projects:detail', project_id=project_id)


@login_required
@require_POST
def close_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner == request.user:
        project.status = STATUS_CLOSED
        project.save()
    return redirect('projects:detail', project_id=project_id)


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if favorited := user.favorites.filter(pk=project_id).exists():
        user.favorites.remove(project)
    else:
        user.favorites.add(project)
    return JsonResponse({'status': 'ok', 'favorited': not favorited})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if participating := project.participants.filter(pk=user.pk).exists():
        project.participants.remove(user)
    else:
        project.participants.add(user)
    return JsonResponse({'status': 'ok', 'participant': not participating})


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner == request.user:
        project.status = STATUS_CLOSED
        project.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=HTTPStatus.FORBIDDEN)


@login_required
def favorites_list(request):
    projects = request.user.favorites.select_related(
        'owner').prefetch_related('participants')
    projects_page = paginate(projects, request, PROJECTS_PER_PAGE)
    return render(request, 'projects/favorite_projects.html', {'projects': projects_page})
