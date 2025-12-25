from django.contrib import admin
from .models import Problem, Submission


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('problem', 'user', 'language', 'created_at', 'verdict')
    readonly_fields = ('created_at',)
