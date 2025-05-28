@echo off
cd /d "C:\Users\Acer\meditrack_new\integ_final_project\meditrack\"
call C:\Users\Acer\meditrack_new\env\Scripts\activate.bat
python manage.py check_reminders >> output.txt 2>&1