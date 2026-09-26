from django import forms
from projects.models import Project

from team_finder.mixins import GitHubUrlMixin


class ProjectForm(GitHubUrlMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        widgets = {
            'status': forms.Select(choices=Project.STATUS_CHOICES),
        }
