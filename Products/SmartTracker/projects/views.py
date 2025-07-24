from django.shortcuts import render
from .models import ProjectModel, WorkTaskModel
from accounts.models import EmployeeModel
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect


class ProjectsDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        projects = ProjectModel.objects.all()
        return render(request, 'projects/projects_dashboard.html', {'projects': projects})
    

# Create your views here.
class CreateProjectView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'projects/create_project.html')

    def post(self, request):
        title = request.POST.get('title')
        phase = request.POST.get('phase')
        risk = request.POST.get('risk')
        notes = request.POST.get('notes')
        hours = request.POST.get('hours')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        project = ProjectModel.objects.create(
            title=title,
            phase=phase,
            risk=risk,
            notes=notes,
            hours=hours,
            start_date=start_date,
            end_date=end_date
        )
        project.working_people.set(request.POST.getlist('working_people'))
        project.save()
        return render(request, 'projects/project_created.html', {'project': project})


# class CreateWorkTaskView(LoginRequiredMixin, View):
#     def get(self, request):
#         projects = ProjectModel.objects.all()
#         employees = EmployeeModel.objects.all()
#         return render(request, 'projects/create_work_task.html', {'projects': projects, 'employees': employees})

#     def post(self, request):
#         projects = ProjectModel.objects.all()
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         assigned_to_id = request.POST.get('assigned_to')
#         status = request.POST.get('status')
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         project_id = request.POST.get('project_id')
        

#         assigned_to = None
#         if assigned_to_id:
#             try:
#                 assigned_to = EmployeeModel.objects.get(pk=assigned_to_id)
#             except EmployeeModel.DoesNotExist:
#                 assigned_to = None

#         project = None
#         if project_id:
#             try:
#                 project = ProjectModel.objects.get(pk=project_id)
#             except ProjectModel.DoesNotExist:
#                 project = None

#         if project is None:
#             print(f"Project with ID {project_id} does not exist.")
#             return render(request, 'projects/create_work_task.html', {'projects': projects, 'error': 'Invalid project selected.'})

#         work_task = WorkTaskModel.objects.create(
#             title=title,
#             description=description,
#             assigned_to=assigned_to,
#             status=status,
#             start_date=start_date,
#             end_date=end_date,
#             project=project
#         )
#         print(f"Work task created: {work_task.title}, Assigned to: {work_task.assigned_to.get_full_name() if work_task.assigned_to else 'Unassigned'}" )
#         work_task.save()
#         return render(request, 'projects/work_task_created.html', {'work_task': work_task})

class CreateWorkTaskView(LoginRequiredMixin, View):
    def get(self, request):
        projects = ProjectModel.objects.all()
        employees = EmployeeModel.objects.filter(is_active=True)
        return render(request, 'projects/create_work_task.html', {'projects': projects, 'employees': employees})

    def post(self, request):
        projects = ProjectModel.objects.all()
        employees = EmployeeModel.objects.filter(is_active=True)
        
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        status = request.POST.get('status')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        project_id = request.POST.get('project_id')

        # Validate required fields
        if not title or not project_id or not status:
            return render(request, 'projects/create_work_task.html', {
                'projects': projects,
                'employees': employees,
                'error': 'Title, project, and status are required.'
            })

        # Validate project
        project = None
        try:
            project = ProjectModel.objects.get(pk=project_id)
        except (ProjectModel.DoesNotExist, ValueError):
            return render(request, 'projects/create_work_task.html', {
                'projects': projects,
                'employees': employees,
                'error': 'Invalid project selected.'
            })

        # Validate assigned_to
        assigned_to = None
        if assigned_to_id:
            try:
                assigned_to = EmployeeModel.objects.get(pk=assigned_to_id)
            except (EmployeeModel.DoesNotExist, ValueError):
                return render(request, 'projects/create_work_task.html', {
                    'projects': projects,
                    'employees': employees,
                    'error': 'Invalid employee selected.'
                })

        # Validate status
        valid_statuses = [choice[0] for choice in WorkTaskModel._meta.get_field('status').choices]
        if status not in valid_statuses:
            return render(request, 'projects/create_work_task.html', {
                'projects': projects,
                'employees': employees,
                'error': 'Invalid status selected.'
            })

        # Validate dates
        start_date_obj = parse_date(start_date) if start_date else None
        end_date_obj = parse_date(end_date) if end_date else None
        if start_date and not start_date_obj:
            return render(request, 'projects/create_work_task.html', {
                'projects': projects,
                'employees': employees,
                'error': 'Invalid start date format.'
            })
        if end_date and not end_date_obj:
            return render(request, 'projects/create_work_task.html', {
                'projects': projects,
                'employees': employees,
                'error': 'Invalid end date format.'
            })

        # Create the task
        try:
            work_task = WorkTaskModel.objects.create(
                title=title,
                description=description or '',
                assigned_to=assigned_to,
                status=status,
                start_date=start_date_obj,
                end_date=end_date_obj,
                project=project
            )
            return render(request, 'projects/work_task_created.html', {'work_task': work_task})
        except Exception as e:
            return render(request, 'projects/create_work_task.html', {
                'projects': projects,
                'employees': employees,
                'error': f'Error creating task: {str(e)}'
            })
class DisplayProjectsView(LoginRequiredMixin, View):
    def get(self, request):
        projects = ProjectModel.objects.all()
        return render(request, 'projects/display_projects.html', {'projects': projects})


class DisplayWorkTasksView(LoginRequiredMixin, View):
    def get(self, request):
        print("Fetching work tasks...")
        work_tasks = WorkTaskModel.objects.all()
        print("Work tasks fetched:", work_tasks.count())
        for work_task in work_tasks:
            print(f"Work Task: {work_task.title}, Assigned To: {work_task.assigned_to}" if work_task.assigned_to else "Unassigned")
            if work_task.assigned_to:
                work_task.assigned_to = work_task.assigned_to.get_full_name()
            else:
                work_task.assigned_to = "Unassigned"
        if not work_tasks:
            return render(request, 'projects/display_work_tasks.html', {'work_tasks': []})
        else:
            work_tasks = work_tasks.order_by('start_date')
        return render(request, 'projects/display_work_tasks.html', {'work_tasks': work_tasks})
