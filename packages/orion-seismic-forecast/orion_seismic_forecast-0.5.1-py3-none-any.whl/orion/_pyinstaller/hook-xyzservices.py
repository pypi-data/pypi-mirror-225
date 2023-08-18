from PyInstaller.utils.hooks import collect_data_files

hiddenimports = []

datas = collect_data_files('xyzservices', excludes=['_pyinstaller'])
