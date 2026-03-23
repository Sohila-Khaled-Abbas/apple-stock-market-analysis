@echo off
echo =======================================================
echo Starting Apple Stock Market Analysis Automated Update
echo =======================================================

:: Navigate to the directory where the script is located
cd /d "%~dp0"

:: Activate Anaconda Environment (Uncomment and edit the path below if needed)
:: For example, if your Conda is installed in C:\Users\[YOUR_USER]\anaconda3:
:: call "C:\Users\%USERNAME%\anaconda3\Scripts\activate.bat" myenvironment

:: Execute the python script
echo Running yf_update.py...
python yf_update.py

echo.
echo Process Complete.
:: Pause prevents the command prompt window from closing immediately so you can read the output.
:: If you schedule this purely in the background via Task Scheduler, you can remove the pause.
pause
