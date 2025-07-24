from django.urls import path
from .views import CreateProjectView, CreateWorkTaskView, DisplayWorkTasksView, DisplayProjectsView, ProjectsDashboardView

urlpatterns = [
    path('', ProjectsDashboardView.as_view(), name='display_projects'),
    path('list_projects/', DisplayProjectsView.as_view(), name='display_projects'),
    path('list_tasks/', DisplayWorkTasksView.as_view(), name='list_tasks'),
    path('create_project/', CreateProjectView.as_view(), name='create_project'),
    path('create_work_task/', CreateWorkTaskView.as_view(), name='create_work_task'),
]
