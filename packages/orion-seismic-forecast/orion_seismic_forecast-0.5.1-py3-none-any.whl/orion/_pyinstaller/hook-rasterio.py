from PyInstaller.utils.hooks import collect_data_files

hiddenimports = ['rasterio.sample']

datas = collect_data_files('rasterio', excludes=['_pyinstaller'])
