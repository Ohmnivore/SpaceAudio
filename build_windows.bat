@echo off
pyinstaller -F -n SpaceAudio -i assets/icon.ico --noconsole main.py
robocopy assets dist\assets /E /NFL /NDL /NJH /NJS /nc /ns /np
robocopy ffmpeg dist\ffmpeg /E /NFL /NDL /NJH /NJS /nc /ns /np
robocopy . dist gnu_gpl_two /E /NFL /NDL /NJH /NJS /nc /ns /np
robocopy . dist gnu_lgpl_two_point_one /E /NFL /NDL /NJH /NJS /nc /ns /np
robocopy . dist LICENSE.md /E /NFL /NDL /NJH /NJS /nc /ns /np
robocopy . dist README.html /E /NFL /NDL /NJH /NJS /nc /ns /np
robocopy . dist README.md /NFL /NDL /NJH /NJS /nc /ns /np
