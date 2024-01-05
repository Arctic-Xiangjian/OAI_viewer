import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=slice_reviewer',
    '--onefile',
    '--windowed',
    '--add-data=/Volumes/arctic4T00/OAI_viewer/data/*:data',
    '/Volumes/arctic4T00/OAI_viewer/slice_reviewer.py'
])