import cx_Freeze

executables = [cx_Freeze.Executable("run.py",icon="images/icon.ico",base="Win32GUI")]

included_files = ["images/", "font/", "pygame_textinput.py", "creatureEngine.py", "newWorldGenerator.py", "mouseHoverEngine.py", "cameraEngine.py", "creatureClickEngine.py", "creatureNames.py", "evolversRenderer.py", "DE.lang", "ENG.lang"]

cx_Freeze.setup(name="Evolvers", options={"build_exe":{"packages":["pygame", "PIL"], "include_files":included_files}}, executables=executables)
