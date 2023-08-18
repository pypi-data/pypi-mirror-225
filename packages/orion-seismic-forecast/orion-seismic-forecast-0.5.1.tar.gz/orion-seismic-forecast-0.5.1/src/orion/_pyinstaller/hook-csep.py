from PyInstaller.utils.hooks import collect_data_files

hiddenimports = []

datas = collect_data_files('csep', excludes=['_pyinstaller'])
