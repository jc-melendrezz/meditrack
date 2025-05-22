@echo off
cd /d "C:\Users\Acer\meditrack\integ_final_project\meditrack"
call C:\Users\Acer\meditrack\env\Scripts\activate.bat
python manage.py check_reminders >> output.txt 2>&1