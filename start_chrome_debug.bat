@echo off
echo Starting Chrome with Remote Debugging Port 9222...
echo You can log into Examly / NeoColab in this browser window.
echo Once logged in, run: python gemini_autocode.py your_question.png --attach

if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\Google\Chrome\ExamlyDebugProfile"
) else (
    if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
        start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\Google\Chrome\ExamlyDebugProfile"
    ) else (
        start chrome --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\Google\Chrome\ExamlyDebugProfile"
    )
)
