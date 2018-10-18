@if "%DEBUG%" == "" @echo off
@rem ##########################################################################
@rem
@rem  trashbot startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%..

@rem Add default JVM options here. You can also use JAVA_OPTS and TRASHBOT_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS=

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto init

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto init

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:init
@rem Get command-line arguments, handling Windows variants

if not "%OS%" == "Windows_NT" goto win9xME_args

:win9xME_args
@rem Slurp the command line arguments.
set CMD_LINE_ARGS=
set _SKIP=2

:win9xME_args_slurp
if "x%~1" == "x" goto execute

set CMD_LINE_ARGS=%*

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\lib\trashbot.jar;%APP_HOME%\lib\emojisReactionData.dat;%APP_HOME%\lib\helpList.dat;%APP_HOME%\lib\instantHumorContainsPhrases.dat;%APP_HOME%\lib\instantHumorEqualsPhrases.dat;%APP_HOME%\lib\lyrics.dat;%APP_HOME%\lib\permissions.dat;%APP_HOME%\lib\recordUptime.dat;%APP_HOME%\lib\speakList.dat;%APP_HOME%\lib\todoList.dat;%APP_HOME%\lib\data;%APP_HOME%\lib\logback-classic-1.0.9.jar;%APP_HOME%\lib\slf4j-api-1.7.2.jar;%APP_HOME%\lib\logback-core-1.0.9.jar;%APP_HOME%\lib\javacord-core-3.0.0.jar;%APP_HOME%\lib\javacord-api-3.0.0.jar;%APP_HOME%\lib\logging-interceptor-3.9.1.jar;%APP_HOME%\lib\okhttp-3.9.1.jar;%APP_HOME%\lib\jackson-databind-2.9.3.jar;%APP_HOME%\lib\nv-websocket-client-1.31.jar;%APP_HOME%\lib\log4j-api-2.11.0.jar;%APP_HOME%\lib\okio-1.13.0.jar;%APP_HOME%\lib\jackson-annotations-2.9.0.jar;%APP_HOME%\lib\jackson-core-2.9.3.jar

@rem Execute trashbot
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %TRASHBOT_OPTS%  -classpath "%CLASSPATH%" trashbotBoot %CMD_LINE_ARGS%

:end
@rem End local scope for the variables with windows NT shell
if "%ERRORLEVEL%"=="0" goto mainEnd

:fail
rem Set variable TRASHBOT_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
if  not "" == "%TRASHBOT_EXIT_CONSOLE%" exit 1
exit /b 1

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
