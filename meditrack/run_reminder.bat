@echo off
cd /d "C:\meditrack\meditrack\meditrack"
call C:\meditrack\env\Scripts\activate.bat
python manage.py check_reminders >> output.txt 2>&1