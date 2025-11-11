@echo off
setlocal enabledelayedexpansion

rem
set "folder=output_easy_shot0_gemini-pro"

rem
for %%i in ("%folder%\*.lp") do (
    rem
    set "tempfile=%%~ni_temp.lp"
    type nul > "!tempfile!"

    rem
    for /f "usebackq delims=" %%a in ("%%i") do (
        rem
        set "line=%%a"
        set "line=!line:```=!"

        rem
        echo(!line!>> "!tempfile!"
    )

    rem
    move /y "!tempfile!" "%%i" >nul
)

echo All triple backticks have been removed from lp files.
endlocal


