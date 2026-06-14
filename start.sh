#!/bin/bash
cd ~/Desktop/student_system
source venv/bin/activate
export ANTHROPIC_API_KEY=$(cat ~/Desktop/student_system/.env | grep ANTHROPIC_API_KEY | cut -d '=' -f2)