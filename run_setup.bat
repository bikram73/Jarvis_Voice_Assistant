@echo off
echo ========================================
echo JARVIS VOICE ASSISTANT SETUP
echo ========================================
echo.
echo Installing dependencies...
python setup.py
echo.
echo Testing installation...
python test_assistant.py
echo.
echo Setup complete! Press any key to exit.
pause