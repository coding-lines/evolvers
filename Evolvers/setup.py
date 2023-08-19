import cx_Freeze

executables = [cx_Freeze.Executable("run_v2.py",icon="images/icon.ico",base="Win32GUI")]

included_files = ["images/", "font/", "pygame_textinput.py", "Camera.py", "Chunk.py", "Creature.py", "CreatureManager.py", "CreatureNames.py", "GeneticNN.py", "NeuralNetworkRenderer.py", "NewWorldGenerator.py", "Renderer.py", "World.py", "LICENSE Pygame Textinput.txt"]

cx_Freeze.setup(name="Evolvers", options={"build_exe":{"packages":["pygame", "PIL"], "include_files":included_files}}, executables=executables)
