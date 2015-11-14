REM @echo off
rmdir /s SpaceAudioWin32
pyinstaller -n SpaceAudio -i assets/icon.ico --noconsole --distpath=SpaceAudioWin32 --workpath=build --specpath=build src/main.py
robocopy assets SpaceAudioWin32\assets /E
robocopy src SpaceAudioWin32\SpaceAudio avbin.dll
robocopy . SpaceAudioWin32 gnu_gpl_two
robocopy . SpaceAudioWin32 gnu_lgpl_two_point_one
robocopy . SpaceAudioWin32 LICENSE.md
robocopy . SpaceAudioWin32 README.html
robocopy . SpaceAudioWin32 README.md
