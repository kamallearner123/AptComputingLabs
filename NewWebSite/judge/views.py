from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Problem, Submission


def problems_list(request):
    problems = Problem.objects.all()
    return render(request, 'judge/problems.html', {'problems': problems})


def problem_detail(request, pk):
    prob = get_object_or_404(Problem, pk=pk)
    created = False
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('/accounts/login/?next=' + request.path)
        lang = request.POST.get('language')
        code = request.POST.get('code')
        sub = Submission.objects.create(problem=prob, user=request.user, language=lang, code=code)
        created = True
    return render(request, 'judge/problem_detail.html', {'problem': prob, 'created': created})


@login_required
def my_submissions(request):
    subs = Submission.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'judge/submissions.html', {'subs': subs})
