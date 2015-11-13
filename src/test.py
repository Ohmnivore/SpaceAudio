import os

os.system('pandoc ../README.md -o ../README.html')

# root_dir = '.'
# for dir_name, subdir_list, file_list in os.walk(root_dir):
#     for fname in file_list:
#         full_path = os.path.join(dir_name, fname)
#         filename, file_extension = os.path.splitext(full_path)
#         par_path = os.path.abspath(os.path.join(full_path, os.pardir))
#         base_name = os.path.basename(filename)
#         if (file_extension == '.ui'):
#             print('Processing: ' + full_path)
#             os.system('C:\Python34\Lib\site-packages\PyQt5\pyuic5.bat ' +
#             full_path + ' -o ' + os.path.join(par_path, 'ui_' + base_name + '.py'))
#         elif (file_extension == '.qrc'):
#             print('Processing: ' + full_path)
#             os.system('C:\Python34\Lib\site-packages\PyQt5\pyrrc5.exe ' +
#             full_path + ' -o ' + os.path.join(par_path, 'rc_' + base_name + '.py'))

print()
os.system('python main.py')
