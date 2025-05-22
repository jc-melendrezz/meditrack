@echo off
cd /d "C:\Users\Acer\meditrack_new\integ_final_project\meditrack"
call C:\Users\Acer\meditrack_new\env\Scripts\activate.bat
python manage.py reset_reminders >> rest_reminders_log.txt 2>&1