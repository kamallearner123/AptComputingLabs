from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    LANG_CHOICES = [
        ('c', 'C'),
        ('cpp', 'C++'),
        ('py', 'Python'),
        ('rs', 'Rust'),
    ]
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=LANG_CHOICES)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    verdict = models.CharField(max_length=50, default='Stored')

    def __str__(self):
        return f'{self.user} - {self.problem} ({self.language})'
