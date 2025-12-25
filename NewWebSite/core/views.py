from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings


ORG = {
    'name': 'Apt Computing Labs',
    'founder': 'Kamal',
    'email': 'kamal@aptcomputinglabs.com',
    'phone': '9739858111',
    'linkedin': 'https://www.linkedin.com/groups/11816027/',
    'github': 'https://github.com/kamallearner123',
    'founder_profile': 'https://www.linkedin.com/in/kamalkumarmukiri/',
}


def home(request):
    news = [
        {'title': 'Upcoming Rust Bootcamp', 'date': '2025-10-01'},
        {'title': 'Embedded Systems Workshop', 'date': '2025-11-12'},
    ]
    from .models import SessionPhoto
    session_photos = SessionPhoto.objects.all()
    return render(request, 'core/home.html', {'org': ORG, 'news': news, 'session_photos': session_photos})


def courses(request):
    courses = [
        'C/C++ Programming',
        'Rust Programming',
        'Python & SDLC',
        'Cyber Security Basics',
        'ML/AI Basics',
        'IoT with Raspberry Pi and ESP32',
        'Embedded Systems & Automotive Diagnostics',
    ]
    return render(request, 'core/courses.html', {'org': ORG, 'courses': courses})


def services(request):
    services = {
        'online': 'Live online trainings across all topics',
        'in_class': 'On-premise trainings for colleges and offices. We can travel.',
    }
    return render(request, 'core/services.html', {'org': ORG, 'services': services})


def contact(request):
    sent = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # For now just log or send via console backend. Make sure settings configured for real email.
        subject = f'Contact form: {name}'
        body = f'From: {name} <{email}>\n\n{message}'
        try:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [ORG['email']])
            sent = True
        except Exception:
            sent = False
    return render(request, 'core/contact.html', {'org': ORG, 'sent': sent})


def news(request):
    materials = [
        {'title': 'Intro to Secure Coding', 'type': 'pdf'},
        {'title': 'ML Basics — slides', 'type': 'video'},
    ]
    return render(request, 'core/news.html', {'org': ORG, 'materials': materials})
