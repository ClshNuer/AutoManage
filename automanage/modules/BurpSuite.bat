@echo off

REM 用于cmd 后台启动运行 BurpSuite
REM jdk11

REM 设置Java路径和jar文件路径
set JAVA_PATH=D:\Softwares\scoop\apps\openjdk11\current\bin\java.exe
set BurpSuite_PATH=G:\AllInOne\03_WebApplicationAnalysis\0301_WebApplicationProxies\Burpsuite\
set JAVA_AGENT_PATH=%BurpSuite_PATH%BurpLoaderKeygen.jar
set JAR_PATH=%BurpSuite_PATH%202001\burpsuite_pro_v2020.1.jar

REM 启动jar文件并最小化窗口
start /min cmd /c %JAVA_PATH% -javaagent:%JAVA_AGENT_PATH% -noverify -jar %JAR_PATH%

