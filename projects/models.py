from django.db import models
from django.conf import settings
from django.urls import reverse

class Project(models.Model):
    STATUS_CHOICES = [('open', 'Открыт'), ('closed', 'Закрыт')]
    
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ProjectMember', related_name='joined_projects', blank=True)
    
    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_projects', blank=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.pk})

class ProjectMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
