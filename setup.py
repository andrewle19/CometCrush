import cx_Freeze
import os
os.environ['TCL_LIBRARY'] = "C:\\Program Files (x86)\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Program Files (x86)\\Python35-32\\tcl\\tk8.6"
executables = [cx_Freeze.Executable('shootem.py')]
cx_Freeze.setup(
    name = "Comet Crusher",
    options={"build_exe":{"packages":["pygame"],
            "include_files":["img","sound","high_score.txt"] }},
    executables = executables
)
