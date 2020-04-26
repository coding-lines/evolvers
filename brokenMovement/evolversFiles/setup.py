import cx_Freeze

executables = [cx_Freeze.Executable("runGame_GUI.py",icon="icon.ico",base="Win32GUI")]

<<<<<<< HEAD
cx_Freeze.setup(name="Evolvers",options={"build_exe":{"packages":["pygame","random"],"include_files":["worldImage.jpg","pygame_textinput.py","left.png","right.png","menuBackground.jpg","true.png","false.png","icon.png","logoSmall.png","creatureEngine.py","newWorldGenerator.py","mouseHoverEngine.py","cameraEngine.py","creatureClickEngine.py","creatureNames.py","font_pt-sans.ttf"]}},executables=executables)
=======
cx_Freeze.setup(name="Evolvers",options={"build_exe":{"packages":["pygame","random"],"include_files":["worldImage.jpg","pygame_textinput.py","left.png","right.png","menuBackground.jpg","true.png","false.png","icon.png","logoSmall.png","creatureEngine.py","newWorldGenerator.py","mouseHoverEngine.py","cameraEngine.py","creatureClickEngine.py","creatureNames.py","font_pt-sans.ttf"]}},executables=executables)
>>>>>>> a0430bd1503802ace66224afa42cfdacb1dea960
