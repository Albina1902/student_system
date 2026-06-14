#!/bin/bash
cd ~/Desktop/student_system
source venv/bin/activate
ANTHROPIC_API_KEY='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' python3 manage.py runserver 8000
