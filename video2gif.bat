@echo off
setlocal

set video=%1
set fps=%2

echo Turning video %video% into frames
call :v2i %video% %fps%

echo Turning frames into pixelated frames
call :i2p %video%

echo Turning pixelated frames into gif
call :p2g %video%

goto :eof

:v2i
python src/v2i.py %1 --fps %2
goto :eof

:i2p
python src/i2p.py %1
goto :eof

:p2g
python src/p2g.py %1
goto :eof

endlocal