import cx_Freeze

executables = [cx_Freeze.Executable("runGame_GUI.py",icon="icon.ico",base="Win32GUI")]

cx_Freeze.setup(name="Evolvers",options={"build_exe":{"worldImage.jpg","pygame_textinput.py","left.png","right.png","packages":["pygame","random"],"include_files":["menuBackground.jpg","true.png","false.png","icon.png","logoSmall.png","creatureEngine.py","newWorldGenerator.py","mouseHoverEngine.py","cameraEngine.py","creatureClickEngine.py","creatureNames.py","font_pt-sans.ttf"]}},executables=executables)