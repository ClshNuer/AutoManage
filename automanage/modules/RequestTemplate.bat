@echo off

REM 用于cmd 后台启动运行 RequestTemplate


REM 设置Java路径和jar文件路径
set JAVA_PATH=G:\AllInOne\00_OfficeApps\DevKit\jdk1.8.0_221\jdk1.8.0_221\bin\java.exe
set JAR_PATH=G:\AllInOne\04_DatabaseAssessment\RequestTemplate\RequestTemplate.jar

REM 启动jar文件并最小化窗口
start /min cmd /c %JAVA_PATH% -jar %JAR_PATH%

