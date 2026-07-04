from django.shortcuts import render
from django.core.paginator import Paginator
from .models import User, Project
from django.contrib.auth.decorators import login_required

def users_list_view(request):
    users_list = User.objects.all().order_by('-date_joined')
    filter_type = request.GET.get('filter')

    if request.user.is_authenticated and filter_type:
        if filter_type == 'fav_authors':
            fav_authors_ids = Project.objects.filter(favorited_by=request.user).values_list('author_id', flat=True)
            users_list = users_list.filter(id__in=fav_authors_ids)
            
        elif filter_type == 'my_projects_authors':
            joined_projects_authors = Project.objects.filter(members=request.user).values_list('author_id', flat=True)
            users_list = users_list.filter(id__in=joined_projects_authors)
            
        elif filter_type == 'likers':
            likers_ids = User.objects.filter(favorite_projects__author=request.user).values_list('id', flat=True)
            users_list = users_list.filter(id__in=likers_ids)
            
        elif filter_type == 'my_members':
            members_ids = User.objects.filter(joined_projects__author=request.user).values_list('id', flat=True)
            users_list = users_list.filter(id__in=members_ids)

    paginator = Paginator(users_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'users/users_list.html', {'page_obj': page_obj})
