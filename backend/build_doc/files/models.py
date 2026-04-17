from django.db import models
from django.contrib.auth.models import User


class UserFile(models.Model):
    STAGE_CHOICES = [
        ('preproject', 'Предпроектная подготовка'),
        ('design', 'Проектирование'),
        ('expertise', 'Экспертиза и согласование'),
        ('preconstruction', 'Подготовка к строительству'),
        ('construction', 'Строительно-монтажные работы'),
        ('commissioning', 'Пусконаладочные работы'),
        ('handover', 'Сдача объекта'),
        ('operation', 'Эксплуатация'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userfiles')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='userfiles/')
    stage = models.CharField(max_length=32, choices=STAGE_CHOICES, default='construction')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    version = models.PositiveIntegerField(default=1)
    last_edited_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_files'
    )
    last_edited_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class FileComment(models.Model):
    file = models.ForeignKey(UserFile, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.author.email} к файлу {self.file.title}'


class FavoriteFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_files')
    file = models.ForeignKey(UserFile, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'file')


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_files')
    file = models.ForeignKey(UserFile, on_delete=models.CASCADE, related_name='file_projects')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'file')
