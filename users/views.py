from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from users.forms import (CustomPasswordChangeForm, EditProfileForm, LoginForm,
                         RegisterForm)
from users.models import User

from team_finder.constants import USERS_PER_PAGE
from team_finder.services import paginate


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('users:login')
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            return redirect('projects:list')
        form.add_error(None, 'Неверный email или пароль')
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('projects:list')


def user_profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/user-details.html', {'profile_user': profile_user})


@login_required
def edit_profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    if profile_user != request.user:
        return redirect('users:profile', user_id=user_id)
    form = EditProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile_user,
        current_user=request.user
    )
    if form.is_valid():
        form.save()
        return redirect('users:profile', user_id=user_id)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    if profile_user != request.user:
        return redirect('users:profile', user_id=user_id)
    form = CustomPasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('users:profile', user_id=user_id)
    return render(request, 'users/change_password.html', {'form': form})


def users_list(request):
    users = User.objects.all().order_by('-date_joined')

    active_filter = None
    if request.user.is_authenticated:
        active_filter = request.GET.get('filter')
        if active_filter == 'favorite_authors':
            fav_projects = request.user.favorites.all()
            users = User.objects.filter(
                owned_projects__in=fav_projects).distinct()
        elif active_filter == 'participated_authors':
            users = User.objects.filter(
                owned_projects__in=request.user.participated_projects.all()
            ).distinct()
        elif active_filter == 'fans':
            users = User.objects.filter(
                favorites__in=request.user.owned_projects.all()
            ).distinct()
        elif active_filter == 'my_participants':
            users = User.objects.filter(
                participated_projects__in=request.user.owned_projects.all()
            ).distinct()

    participants = paginate(users, request, USERS_PER_PAGE)
    return render(request, 'users/participants.html', {
        'participants': participants,
        'active_filter': active_filter,
    })
