@echo off
REM pyinstaller -F -n SpaceAudio -i assets/icon.ico --noconsole src/main.py
pyinstaller -n SpaceAudio -i assets/icon.ico --noconsole src/main.py
REM -robocopy assets dist\assets /E /NFL /NDL /NJH /NJS /nc /ns /np
REM -robocopy ffmpeg dist\ffmpeg /E /NFL /NDL /NJH /NJS /nc /ns /np
REM -robocopy . dist gnu_gpl_two /E /NFL /NDL /NJH /NJS /nc /ns /np
REM -robocopy . dist gnu_lgpl_two_point_one /E /NFL /NDL /NJH /NJS /nc /ns /np
REM -robocopy . dist LICENSE.md /E /NFL /NDL /NJH /NJS /nc /ns /np
REM -robocopy . dist README.html /E /NFL /NDL /NJH /NJS /nc /ns /np
REM -robocopy . dist README.md /NFL /NDL /NJH /NJS /nc /ns /np
