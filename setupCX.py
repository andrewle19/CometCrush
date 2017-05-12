from cx_Freeze import setup, Executable

exe=Executable(
     script="main.py",
     base="Win32Gui",
     icon="app.ico"
     )
includefiles=["img","sound","high_score.txt"]
includes=[]
excludes=[]
packages=["pygame","random"]
setup(

     version = "0.0",
     description = "No Description",
     author = "Anndrew Le",
     name = "Comet Crush",
     options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
     executables = [exe]
     )
