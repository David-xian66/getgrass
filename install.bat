@echo off
chcp 65001 >nul
setlocal enableextensions enabledelayedexpansion
set "SOURCE=%~dp0"
set "DESTINATION=%ProgramFiles(x86)%\Seewo\seewo"
set "TEMP_XML=%TEMP%\SeewoNote5_Server.xml"

set "SOURCE_DLL_PY=%ProgramFiles(x86)%\Seewo\seewo\main.py"
set "DESTINATION_DLL=%ProgramFiles(x86)%\Seewo\seewo\seewo.dll"


:: Check if running as administrator
openfiles >nul 2>&1
if %errorlevel% NEQ 0 (
    echo 本脚本需要管理员权限.
    pause
    exit /b 1
)



rem 获取当前用户的完整名字
for /f "tokens=*" %%i in ('whoami') do set "current_user=%%i"

set "AUTHORY=exe.exe.exe"
set "AUTHOR=%DESTINATION%\seewo.exe\"



echo 正在将文件从 "%SOURCE%" 复制到 "%DESTINATION%"...
xcopy "%SOURCE%\*" "%DESTINATION%\" /E /I /H /Y

if %errorlevel% neq 0 (
    echo 文件复制过程中发生错误。
    pause
    exit /b %errorlevel%
) else (
    echo 文件复制成功。
)

echo 如果存在，正在删除 "%DESTINATION%" 目录下的指定文件...
set "FILES_TO_DELETE=install.bat seewo.dll"  rem 在此处添加需要删除的文件列表

for %%f in (%FILES_TO_DELETE%) do (
    if exist "%DESTINATION%\%%f" (
        del "%DESTINATION%\%%f"
        echo %%f 已从 "%DESTINATION%" 删除。
    ) else (
        echo "%DESTINATION%" 中不存在 %%f 文件。
    )
)

echo 如果存在，正在删除 "%DESTINATION%" 目录下的指定目录...
set "DIRS_TO_DELETE=venv"  rem 在此处添加需要删除的目录列表

for %%d in (%DIRS_TO_DELETE%) do (
    if exist "%DESTINATION%\%%d" (
        rd /s /q "%DESTINATION%\%%d"
        echo %%d 目录已从 "%DESTINATION%" 删除。
    ) else (
        echo "%DESTINATION%" 中不存在 %%d 目录。
    )
)


echo 正在通过 "%SOURCE_DLL_PY%" 创建 "%DESTINATION_DLL%"...
move "%SOURCE_DLL_PY%" "%DESTINATION_DLL%"

if %errorlevel% neq 0 (
    echo dll文件创建过程中发生错误。
    pause
    exit /b %errorlevel%
) else (
    echo 文件创建成功。
)





@REM echo 创建临时计划任务...
@REM schtasks /create /tn "SeewoNote5_Server" /tr "\"%DESTINATION%\seewo.exe\"" /sc onlogon /rl HIGHEST
@REM if %errorlevel% neq 0 (
@REM     echo 创建临时计划任务时发生错误。
@REM     pause
@REM     exit /b %errorlevel%
@REM )

@REM echo 导出任务为 XML...
@REM schtasks /query /tn "SeewoNote5_Server" /xml > "%TEMP_XML%"
@REM if %errorlevel% neq 0 (
@REM     echo 导出任务时发生错误。
@REM     pause
@REM     exit /b %errorlevel%
@REM )

@REM set "file_tmp=%TEMP_XML%.tmp"
set "file_tmp=%DESTINATION%\install_xml.xml"

echo 修改 XML 文件...

for /f "delims=" %%i in (%TEMP_XML%) do (
    set str=%%i
    set "str=!str:%AUTHORY%=%AUTHOR%!"
    echo !str!
    echo !str!>>%file_tmp%
)

move "%file_tmp%" "%TEMP_XML%"

@REM echo 删除原有任务...
@REM schtasks /delete /tn "SeewoNote5_Server" /f

echo 导入修改后的 XML 文件...
schtasks /create /tn "SeewoNote5_Server" /xml "%TEMP_XML%"
if %errorlevel% neq 0 (
    echo 导入修改后的 XML 文件时发生错误。
    pause
    exit /b %errorlevel%
) else (
    echo 计划任务已成功添加。
)




echo 清理临时文件...
@REM del "%TEMP_XML%"

endlocal
