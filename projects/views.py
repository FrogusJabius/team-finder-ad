from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project

@login_required
def toggle_favorite(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': '/users/login/'}, status=401)

    project = get_object_or_404(Project, pk=pk)
    
    if project.favorited_by.filter(id=request.user.id).exists():
        project.favorited_by.remove(request.user)
        status = 'removed'
    else:
        project.favorited_by.add(request.user)
        status = 'added'
        
    return JsonResponse({'status': status, 'is_favorited': status == 'added'})
