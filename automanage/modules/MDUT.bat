@echo off

REM 用于cmd 后台启动运行 Multiple.Database.Utilization.Tools


REM 设置Java路径和jar文件路径
set JAVA_PATH=G:\AllInOne\00_OfficeApps\DevKit\jdk1.8.0_221\jdk1.8.0_221\bin\java.exe
set JAVA_CLASSPATH=G:\AllInOne\00_OfficeApps\DevKit\jdk1.8.0_221\jdk1.8.0_221\lib\tools.jar
set JAR_PATH=G:\AllInOne\04_DatabaseAssessment\MDUT\Multiple.Database.Utilization.Tools-2.1.1-jar-with-dependencies.jar

REM 启动jar文件并最小化窗口
start /min cmd /c %JAVA_PATH% -jar %JAR_PATH%

