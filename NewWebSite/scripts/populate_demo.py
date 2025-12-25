"""Run this script to populate demo problems and events.

Usage: python scripts/populate_demo.py
"""
import os
import django

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apt_site.settings')
django.setup()

from judge.models import Problem
from core.models import Event

def main():
    problems = [
        ('FizzBuzz', 'Print FizzBuzz for numbers 1..N'),
        ('Two Sum', 'Find two numbers that add to target'),
        ('Matrix Rotate', 'Rotate matrix by 90 degrees'),
        ('Palindrome Check', 'Check if string is palindrome'),
        ('Prime Sieve', 'List primes up to N'),
        ('UART Echo', 'Embedded: echo input back over UART')
    ]
    for t,d in problems:
        Problem.objects.get_or_create(title=t, description=d)

    Event.objects.get_or_create(title='Rust Bootcamp', description='Intro to Rust for systems', start_date='2025-10-01')
    Event.objects.get_or_create(title='Embedded Workshop', description='Hands-on IoT labs', start_date='2025-11-12')

    print('Demo data created')

if __name__ == '__main__':
    main()
