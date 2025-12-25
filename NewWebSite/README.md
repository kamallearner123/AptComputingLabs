# Apt Computing Labs — Website

This is a minimal Django site skeleton for Apt Computing Labs. It includes:

- Public pages: Home, Courses, Services, Contact, News/Materials.
- A `judge` app where users can view problems and submit solutions (submissions are stored; there is no remote code execution for safety).
- Simple auth (Django built-in login/logout), admin to manage problems and events.

Quick start

1. Create a virtualenv and install dependencies from `requirements.txt`.
2. Run `python manage.py migrate` then `python manage.py createsuperuser`.
3. Run `python manage.py runserver` and open http://127.0.0.1:8000/

Notes

- Replace `SECRET_KEY` in `apt_site/settings.py` for production.
- Configure email backend in settings to enable contact form email sending.
- For safety, this project does NOT execute submitted code. To add judging, integrate a sandboxed runner or external judge service.
