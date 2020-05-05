import pygame, pygame_textinput
import time, os
from math import floor
import creatureEngine,cameraEngine,creatureClickEngine,mouseHoverEngine,evolversRenderer

def readfile(name):
    with open(name,"r") as f:
        return(f.read())


class const:
    WHITE = [255,255,255]
    BLACK = [0,0,0]
    LIGHT_GREY = [200,200,200]
    GREY = [100,100,100]
    DARK_GREY = [50,50,50]
    RED = [255,0,0]
    GREEN = [0,200,0]




class builtin:
    builtinLanguage = {"title":"English (Built in)",
                       "general":{"back":"back","results":"results","points":"points","wait":"please wait","save":"save","load":"load","menu":"menu"},
                       "menu":{"start":"start","benchmark":"benchmark","setting":"settings","new":"new simulation","load":"Load simulation","simBench":"Simulation benchmark","worldsize":"World size","startcreatures":"Start creatures"},
                       "benchmarks":{"suggestion":"Suggestion","low":"Low settings","medium":"Medium settings","high":"High settings","simulating":"Simulate scenario","benchmarkRunning":"Benchmark is running"},
                       "settings":{"view_distance":"View distance","relative_scale":"Size in relation to energy","low":"low","medium":"medium","high":"high"}
                       ,"sidebar":{"years":"Years","year":"Year","population":"Population","mode":"Gamemode","name":"Name","age":"Age","generation":"Generation","parent":"Parent","energy":"Energy","fps":"FPS","simulation_speed":"Simulation speed"},
                       "controls": ["WASD: Move creature","Spacebar: Pause simulation","Arrows: Move camera","O / P: Faster / slower","E: Show / hide side menu","M: Display mouse-hover","J: spawn / delete player","Q: eat (as player)","X: reproduce (200 energy)","F12: render field","scroll: camera speed"]
                       ,"gameModes":{"spectator":"Spectator","player":"Creature"}}


class game:
    class options:
        #Erstellen von Dateien, falls sie fehlen.
        

        
        if not os.path.isfile("settings.json"):
            with open("settings.json","w") as f:
                f.write("{'viewDistance':32,'sizeAffect':False,'languagePack':'STD'}")
                f.close()
        if not os.path.isdir("save"):
            os.mkdir("save")
        if not os.path.isdir("renders"):
            os.mkdir("renders")
        if not os.path.isfile("data"):
            with open("data","w") as f:
                f.write("")
                f.close()
        try:
            optionsFile = eval(readfile("settings.json"))
            if not (type(optionsFile) == type({"template":"dict"})):
                raise EOFError("Settings File corrupted")
        except:
            raise EOFError("Settings File corrupted")
        #Spieloptionen
        if 'languagePack' in optionsFile:
            language = optionsFile["languagePack"]
        else:
            language = "STD"
        if os.path.isfile(optionsFile["languagePack"]+".lang"):
            try:
                with open(optionsFile["languagePack"]+".lang","r") as f:
                    langData = eval(f.read())
                    f.close()
            except:
                language = "STD"
        else:
            language = "STD"
        if language == "STD":
            langData = builtin.builtinLanguage
        dimensions = [1280,720]
        frame_rate = 60
        gameTitle = "Evolvers"
        pixel_size = 1
        currentScreen = "menu"
        cursorVisible = True
        sizeAffect = optionsFile["sizeAffect"]
        del optionsFile
        #Generelle Informationen über das Spiel
    class timers:
        frame = 0
        seconds = 0
        #In dieser Klasse kann direkt auf die GameTimer zugegriffen werden.
    class state:
        done = False
        #Status des Spiels
    class storage:
        camMaxSpeed = 1 #Maximale Kamerageschwindigkeit in Blocks per Frame
        
        cameraSpeed = [0,0] #Aktuelle Kamerabewegungsrichtung
        
        
        cameraMoved = False #Kamera im letzten Frame bewegt?
        
        toastDuration = 0 #Länge eines Toasts in Frames
        
        #TODO: Cleanup der Variablen
        
        worldSizeSlider = 0 #Slider bei Erstellung einer neuen Welt
        
        entityCountSlider = 0 #Slider bei der Erstellung der Kreaturen
        
        worldNumber = 0 #Nummer der ausgewählten Welt auf dem LoadScreen
        noCommaFrames = 0 #Framezeit der Komma-Fehlermeldung beim Speichern
        textinput = pygame_textinput.TextInput(font_family="font_pt-sans.ttf", text_color=(255,255,255),font_size=40, max_string_length=16) #Texteingabefeld
        benchmarkFrame = 0 #Fortschritt eines Benchmarks
        try:
            optionsFile = eval(readfile("settings.json")) #Lesen aus der Einstellungsdatei
            if not (str(type(optionsFile))  == "<class 'dict'>"):
                raise EOFError("Settings File corrupted")
        except:
            raise EOFError("Settings File corrupted")
        viewDistance = optionsFile["viewDistance"]
        fieldSize = 40 if viewDistance == 32 else 20 if viewDistance == 64 else 80
        worldGeneration = "new"
        playerHasMoved = 0
        playerInGame = False
        runMouseHover = True
        playBackSpeed = 1
        sideBarInformation: dict = {"name":"None","energy":0,"parent":"None","age":0,"generation":0}
        showSidebar = True
        simulationRunning = False
        startCreatures = 200
        worldSmooth = 6
        worldSize = [101,101]
        cameraPos = [1,1,34,22,1] if viewDistance == 32 else [1,1,68,44,1] if viewDistance == 64 else [1,1,18,12,1]
        trueFPS = 60
        textureStorage: dict = {}
        guiTexts: dict = {}
        fonts: dict = {}
        #Speicherort von Spieldaten oder Texturen

class engine:
    def refreshGameInformation():
        #Funktion um den Titel und die Auflösung zu ändern
        global screen
        screen = pygame.display.set_mode(game.options.dimensions)
        pygame.display.set_caption(game.options.gameTitle)
        game.options.pixel_count = [game.options.dimensions[0] // game.options.pixel_size, game.options.dimensions[1] // game.options.pixel_size]


class execute:
    class init:
        def texLoader():
            game.storage.textureStorage["backgroundimage"] = pygame.image.load("menuBackground.jpg")
            game.storage.textureStorage["logoSmall"] = pygame.image.load("logoSmall.png")
            game.storage.textureStorage["false"] = pygame.image.load("false.png")
            game.storage.textureStorage["true"] = pygame.image.load("true.png")
            game.storage.textureStorage["left"] = pygame.image.load("left.png")
            game.storage.textureStorage["right"] = pygame.image.load("right.png")
            game.storage.textureStorage["worldImage"] = pygame.image.load("worldImage.jpg")
            #Funktion, um Texturen zu laden. (Texturen können auch in der DrawFunction geladen werden, das spart zwar RAM, aber führt zu Rucklern!)
        def gameInit():
            pass
            # Funktion, die beim Spielstart ausgeführt wird.
    class draw:
        def onDrawFunction():
            game.storage.trueFPS = clock.get_fps()
            if game.options.currentScreen == "game":
                mPos = list(pygame.mouse.get_pos())
                if not game.storage.cameraMoved:
                    game.storage.cameraSpeed = [0,0]
                else:
                    game.storage.cameraMoved = False
                game.storage.playerHasMoved -= 1 if game.storage.playerHasMoved > 0 else 0
                if game.storage.simulationRunning:
                    game.storage.gameEntities,game.storage.gameWorld = creatureEngine.runIteration(game.storage.gameEntities,game.storage.gameWorld)
                    for i in range(game.storage.playBackSpeed-1):
                        game.storage.gameEntities,game.storage.gameWorld = creatureEngine.runIteration(game.storage.gameEntities,game.storage.gameWorld)
                        game.timers.frame += 1
                for x in range(int(game.storage.cameraPos[0]),int(game.storage.cameraPos[2])):
                    for y in range(int(game.storage.cameraPos[1]),int(game.storage.cameraPos[3])):
                        if game.storage.gameWorld[0][x][y]:
                            blue = 0
                            green = int(game.storage.gameWorld[1][x][y] / 12 *100) + 50
                            red = 50
                        else:
                            blue = 150
                            green = 100
                            red = 0
                        p1 = [(x-game.storage.cameraPos[0])*game.storage.fieldSize,(y-game.storage.cameraPos[1])*game.storage.fieldSize]
                        pygame.draw.rect(screen, [red,green,blue], [p1[0],p1[1],game.storage.fieldSize,game.storage.fieldSize])
                        pygame.draw.line(screen,const.BLACK,[p1[0],0],[p1[0],game.options.dimensions[1] + game.storage.fieldSize])
                        pygame.draw.line(screen,const.BLACK,[0,p1[1]],[game.options.dimensions[0],p1[1]])
                        
                #MOUSEHOVER
                if game.storage.runMouseHover:
                    pos = list(pygame.mouse.get_pos())
                    pos[0]+=int(game.storage.cameraPos[0]%1*game.storage.fieldSize)
                    pos[1]+=int(game.storage.cameraPos[1]%1*game.storage.fieldSize)
                    posNew = mouseHoverEngine.assignClick(pos,game.storage.showSidebar,game.storage.cameraPos,game.storage.fieldSize)
                    if not posNew == None:
                        saturationText = game.storage.fonts[24].render(str(round(game.storage.gameWorld[1][floor(posNew[0])][floor(posNew[1])],1)), True, const.WHITE)
                        screen.blit(saturationText,(mPos[0], mPos[1]+20))
                #KREATUREN
                for c in range(0,len(game.storage.gameEntities)):
                    if game.storage.gameEntities[c]["x"] >= game.storage.cameraPos[0]-1 and game.storage.gameEntities[c]["y"] >= game.storage.cameraPos[1]-1:
                        if game.storage.gameEntities[c]["x"] <= game.storage.cameraPos[2]+1 and game.storage.gameEntities[c]["y"] <= game.storage.cameraPos[3]+1:
                            pos = [int((game.storage.gameEntities[c]["x"] - game.storage.cameraPos[0])*game.storage.fieldSize),int((game.storage.gameEntities[c]["y"] - game.storage.cameraPos[1])*game.storage.fieldSize)]
                            size = int((game.storage.gameEntities[c]["energy"]/8+88)/5) if game.options.sizeAffect else 40 if game.storage.viewDistance == 16 else 20
                            pygame.draw.circle(screen,game.storage.gameEntities[c]["boundaries"],pos,size+2)
                            pygame.draw.circle(screen,game.storage.gameEntities[c]["color"],pos,size)
                            text = game.storage.fonts[24].render(game.storage.gameEntities[c]["name"], True, const.WHITE)
                            screen.blit(text,(pos[0]-50, pos[1]+size))

                #SPIELER
                if game.storage.playerInGame:
                    game.storage.playerInformation["age"] += 1
                    game.storage.playerInformation["energy"] -= 1 if not(bool(game.timers.frame%3)) and not(game.storage.gameWorld[0][int(game.storage.playerInformation["x"])][int(game.storage.playerInformation["y"])]) else 0
                    if game.storage.playerInformation["energy"] < 1:
                        execute.evolvers.respawnPlayer()

                    pos = [int((game.storage.playerInformation["x"] - game.storage.cameraPos[0])*game.storage.fieldSize),int((game.storage.playerInformation["y"] - game.storage.cameraPos[1])*game.storage.fieldSize)]
                    if game.storage.viewDistance != 16:
                        if pos[0] < 600:
                            game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[-1,0],game.storage.worldSize)
                        if pos[0] > 600:
                            game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[1,0],game.storage.worldSize)
                        if pos[1] < 320:
                            game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[0,-1],game.storage.worldSize)
                        if pos[1] > 320:
                            game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[0,1],game.storage.worldSize)
                    else:
                        if pos[0] < 640:
                            game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[-1,0],game.storage.worldSize)
                        if pos[0] > 640:
                            game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[1,0],game.storage.worldSize)
                        if pos[1] < 320:
                            game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[0,-1],game.storage.worldSize)
                        if pos[1] > 320:
                            game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[0,1],game.storage.worldSize)



                    size = int((game.storage.playerInformation["energy"]/8+88)/5) if game.options.sizeAffect else 40 if game.storage.viewDistance == 16 else 20
                    pos = [int((game.storage.playerInformation["x"] - game.storage.cameraPos[0])*game.storage.fieldSize),int((game.storage.playerInformation["y"] - game.storage.cameraPos[1])*game.storage.fieldSize)]
                    pygame.draw.circle(screen,game.storage.playerInformation["boundaries"],pos,size+2)
                    pygame.draw.circle(screen,game.storage.playerInformation["color"],pos,size)
                    text = game.storage.fonts[24].render(game.storage.playerInformation["name"], True, const.WHITE)
                    screen.blit(text,(pos[0]-50, pos[1]+size))




                #SIDEBAR
                if game.storage.showSidebar:
                    screen.blit(s, (1000,0))

                    timeText = game.storage.fonts[28].render(game.options.langData["sidebar"]["year"]+": "+str(round((game.timers.frame + (game.timers.seconds*60))/4800,3)), True, const.WHITE)
                    screen.blit(timeText,(1010,20))
                    popText = game.storage.fonts[28].render(game.options.langData["sidebar"]["population"]+": "+str(len(game.storage.gameEntities)), True, const.WHITE)
                    screen.blit(popText,(1010,60))
                    modeText = game.storage.fonts[24].render(game.options.langData["sidebar"]["mode"]+": "+game.options.langData["gameModes"]["player"] if game.storage.playerInGame else game.options.langData["sidebar"]["mode"]+": "+game.options.langData["gameModes"]["spectator"], True, const.WHITE)
                    screen.blit(modeText,(1010,100))

                    if not game.storage.playerInGame:
                        nameText = game.storage.fonts[24].render(game.options.langData["sidebar"]["name"]+": "+game.storage.sideBarInformation["name"], True, const.WHITE)

                        ageText = game.storage.fonts[24].render(game.options.langData["sidebar"]["age"]+": "+str(round(game.storage.sideBarInformation["age"]/4800,3))+" "+game.options.langData["sidebar"]["years"], True, const.WHITE)

                        genText = game.storage.fonts[24].render(game.options.langData["sidebar"]["generation"]+": "+str(game.storage.sideBarInformation["generation"]), True, const.WHITE)

                        parentText = game.storage.fonts[24].render(game.options.langData["sidebar"]["parent"]+": "+str(game.storage.sideBarInformation["parent"]), True, const.WHITE)


                        energyText = game.storage.fonts[24].render(game.options.langData["sidebar"]["energy"]+": "+str(game.storage.sideBarInformation["energy"]), True, const.WHITE)

                    else:
                        nameText = game.storage.fonts[24].render(game.options.langData["sidebar"]["name"]+": "+ game.storage.playerInformation["name"], True, const.WHITE)
                        ageText = game.storage.fonts[24].render(game.options.langData["sidebar"]["age"]+": "+str(round(game.storage.playerInformation["age"]/4800,3))+" Jahre", True, const.WHITE)
                        genText = game.storage.fonts[24].render(game.options.langData["sidebar"]["generation"]+": 0", True, const.WHITE)
                        parentText = game.storage.fonts[24].render(game.options.langData["sidebar"]["parent"]+": None", True, const.WHITE)
                        energyText = game.storage.fonts[24].render(game.options.langData["sidebar"]["energy"]+": "+str(game.storage.playerInformation["energy"]), True, const.WHITE if (game.storage.gameWorld[0][int(game.storage.playerInformation["x"])][int(game.storage.playerInformation["y"])]) and game.storage.playerInformation["energy"] > 50 else [255,0,0] if game.timers.frame % 30 <= 10 else const.WHITE)

                    FPS = game.storage.fonts[24].render(game.options.langData["sidebar"]["fps"]+": "+str(int(game.storage.trueFPS)), True, const.WHITE)
                    screen.blit(FPS,(1010,360))

                    screen.blit(nameText,(1010,140))
                    screen.blit(ageText,(1010,180))
                    screen.blit(genText,(1010,220))
                    screen.blit(parentText,(1010,260))
                    screen.blit(energyText,(1010,300))

                    for i,n in enumerate(game.storage.ctrlTexts):
                        screen.blit(n,(1010,430+(i*20)))

                    s_speedText = game.storage.fonts[18].render(game.options.langData["sidebar"]["simulation_speed"]+": "+str(game.storage.playBackSpeed), True, const.WHITE)
                    screen.blit(s_speedText,(1010,670))
            elif game.options.currentScreen == "menu":
                screen.blit(game.storage.textureStorage["backgroundimage"],(0,0))
                screen.blit(game.storage.textureStorage["logoSmall"],(515,28))
                screen.blit(startText,((game.options.dimensions[0]//2)-(startText.get_rect().width//2),20))
                screen.blit(menuTextA if not (mousePos[0] in range((game.options.dimensions[0]//2)-(menuTextA.get_rect().width//2),(game.options.dimensions[0]//2)+(menuTextA.get_rect().width//2)) and mousePos[1] in range(220,290)) else menuTextA_HOVER,((game.options.dimensions[0]//2)-(menuTextA.get_rect().width//2),220))
                screen.blit(menuTextB if not (mousePos[0] in range((game.options.dimensions[0]//2)-(menuTextB.get_rect().width//2),(game.options.dimensions[0]//2)+(menuTextB.get_rect().width//2)) and mousePos[1] in range(320,390)) else menuTextB_HOVER,((game.options.dimensions[0]//2)-(menuTextB.get_rect().width//2),320))
                screen.blit(game.storage.guiTexts["settings"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["settings"].get_rect().width//2),(game.options.dimensions[0]//2)+(menuTextB.get_rect().width//2)) and mousePos[1] in range(420,490)) else game.storage.guiTexts["settingsHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["settings"].get_rect().width//2),420))
            elif game.options.currentScreen == "benchmarkMenu":
                screen.blit(game.storage.textureStorage["backgroundimage"],(0,0))
                screen.blit(game.storage.textureStorage["logoSmall"],(515,28))
                screen.blit(startText,((game.options.dimensions[0]//2)-(startText.get_rect().width//2),20))
                screen.blit(game.storage.guiTexts["simulationBenchmark"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["simulationBenchmark"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["simulationBenchmark"].get_rect().width//2)) and mousePos[1] in range(220,290)) else game.storage.guiTexts["simulationBenchmarkHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["simulationBenchmark"].get_rect().width//2),220))
                screen.blit(game.storage.guiTexts["back"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["back"].get_rect().width//2)) and mousePos[1] in range(420,490)) else game.storage.guiTexts["backHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),420))
            elif game.options.currentScreen == "settings":
                viewdistance = game.storage.fonts[48].render(game.options.langData["settings"]["view_distance"]+": "+(game.options.langData["settings"]["low"] if game.storage.viewDistance == 16 else game.options.langData["settings"]["medium"] if game.storage.viewDistance == 32 else game.options.langData["settings"]["high"]), True, const.WHITE)
                screen.blit(game.storage.textureStorage["backgroundimage"],(0,0))
                screen.blit(game.storage.textureStorage["logoSmall"],(515,28))
                screen.blit(startText,((game.options.dimensions[0]//2)-(startText.get_rect().width//2),20))
                screen.blit(game.storage.guiTexts["back"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["back"].get_rect().width//2)) and mousePos[1] in range(620,690)) else game.storage.guiTexts["backHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),620))
                screen.blit(viewdistance,(450 if game.storage.viewDistance == 16 else 465 if game.storage.viewDistance == 32 else 480,180))
                pygame.draw.rect(screen,const.WHITE,[300,260,680,5])
                pygame.draw.rect(screen,[200,200,200],[300 if game.storage.viewDistance == 16 else 640 if game.storage.viewDistance == 32 else 980,242,20,40])
                screen.blit(game.storage.textureStorage["true" if game.options.sizeAffect else "false"],(280,320))
                screen.blit(relsize,(360,330))
            elif game.options.currentScreen == "benchmark_nogui":
                screen.blit(game.storage.textureStorage["backgroundimage"],(0,0))
                screen.blit(benchmarkRunning,(30,30))
                if game.storage.benchmarkFrame == 0:
                    screen.blit(lowend,(30,120))
                if game.storage.benchmarkFrame == 1:
                    screen.blit(midend,(30,120))
                    game.storage.benchmarkTime = [time.time()]
                    game.storage.benchmarkWorld = creatureEngine.initWorld(101,101,"new",2)
                    game.storage.benchmarkCreatures = creatureEngine.initCreatures(100)
                    for m in range(21):
                        for i in range(60):
                            game.storage.benchmarkCreatures,game.storage.benchmarkWorld = creatureEngine.runIteration(game.storage.benchmarkCreatures,game.storage.benchmarkWorld)
                        game.storage.benchmarkWorld = creatureEngine.runWorldIteration(game.storage.benchmarkWorld)
                    game.storage.benchmarkTime += [time.time()]
                if game.storage.benchmarkFrame == 2:
                    screen.blit(highend,(30,120))
                    game.storage.benchmarkTime += [time.time()]
                    game.storage.benchmarkWorld = creatureEngine.initWorld(200,200,"new",2)
                    game.storage.benchmarkCreatures = creatureEngine.initCreatures(250)
                    for m in range(21):
                        for i in range(60):
                            game.storage.benchmarkCreatures,game.storage.benchmarkWorld = creatureEngine.runIteration(game.storage.benchmarkCreatures,game.storage.benchmarkWorld)
                        game.storage.benchmarkWorld = creatureEngine.runWorldIteration(game.storage.benchmarkWorld)
                    game.storage.benchmarkTime += [time.time()]
                if game.storage.benchmarkFrame == 3:
                    game.storage.benchmarkTime += [time.time()]
                    game.storage.benchmarkWorld = creatureEngine.initWorld(500,500,"new",2)
                    game.storage.benchmarkCreatures = creatureEngine.initCreatures(750)
                    for m in range(21):
                        for i in range(60):
                            game.storage.benchmarkCreatures,game.storage.benchmarkWorld = creatureEngine.runIteration(game.storage.benchmarkCreatures,game.storage.benchmarkWorld)
                        game.storage.benchmarkWorld = creatureEngine.runWorldIteration(game.storage.benchmarkWorld)
                    game.storage.benchmarkTime += [time.time()]
                    game.storage.benchmarkResults = [game.storage.benchmarkTime[1]-game.storage.benchmarkTime[0],game.storage.benchmarkTime[3]-game.storage.benchmarkTime[2],game.storage.benchmarkTime[5]-game.storage.benchmarkTime[4]]
                    game.options.currentScreen = "benchmark_nogui_results"
                game.storage.benchmarkFrame += 1
            elif game.options.currentScreen == "benchmark_nogui_results":
                screen.blit(game.storage.textureStorage["backgroundimage"],(0,0))
                screen.blit(results,(520,10))
                resultPoints1 = game.storage.fonts[48].render(game.options.langData["benchmarks"]["low"]+": "+str(int((1/(game.storage.benchmarkResults[0]/20))*1000))+" "+game.options.langData["general"]["points"], True, const.WHITE)
                screen.blit(resultPoints1,(10,120))
                resultPoints2 = game.storage.fonts[48].render(game.options.langData["benchmarks"]["medium"]+": "+str(int((1/(game.storage.benchmarkResults[1]/20))*1000))+" "+game.options.langData["general"]["points"], True, const.WHITE)
                screen.blit(resultPoints2,(10,170))
                resultPoints1 = game.storage.fonts[48].render(game.options.langData["benchmarks"]["high"]+": "+str(int((1/(game.storage.benchmarkResults[2]/20))*1000))+" "+game.options.langData["general"]["points"], True, const.WHITE)
                screen.blit(resultPoints1,(10,220))
                if int((1/(game.storage.benchmarkResults[2]/20))*1000) > 4000:
                    suggestion = game.storage.fonts[48].render(game.options.langData["benchmarks"]["suggestion"]+": "+game.options.langData["benchmarks"]["high"], True, const.WHITE)
                elif int((1/(game.storage.benchmarkResults[1]/20))*1000) > 4000:
                    suggestion = game.storage.fonts[48].render(game.options.langData["benchmarks"]["suggestion"]+": "+game.options.langData["benchmarks"]["medium"], True, const.WHITE)
                else:
                    suggestion = game.storage.fonts[48].render(game.options.langData["benchmarks"]["suggestion"]+": "+game.options.langData["benchmarks"]["low"], True, const.WHITE)
                screen.blit(suggestion,(10,320))
                screen.blit(game.storage.guiTexts["back"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["back"].get_rect().width//2)) and mousePos[1] in range(420,490)) else game.storage.guiTexts["backHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),420))
            elif game.options.currentScreen == "escapeMenu":
                screen.blit(game.storage.textureStorage["backgroundimage"],(0,0))
                screen.blit(backToGame if not (mousePos[0] in range((game.options.dimensions[0]//2)-(backToGame.get_rect().width//2),(game.options.dimensions[0]//2)+(backToGame.get_rect().width//2)) and mousePos[1] in range(190,260)) else backToGame_HOVER,((game.options.dimensions[0]//2)-(backToGame.get_rect().width//2),200))
                screen.blit(saveGame if not (mousePos[0] in range((game.options.dimensions[0]//2)-(saveGame.get_rect().width//2),(game.options.dimensions[0]//2)+(saveGame.get_rect().width//2)) and mousePos[1] in range(290,360)) else saveGame_HOVER,((game.options.dimensions[0]//2)-(saveGame.get_rect().width//2),300))
                screen.blit(game.storage.guiTexts["quitGame"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["quitGame"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["quitGame"].get_rect().width//2)) and mousePos[1] in range(390,460)) else game.storage.guiTexts["quitGameHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["quitGame"].get_rect().width//2),400))
            elif game.options.currentScreen == "gamemodeSelect":
                screen.blit(game.storage.textureStorage["backgroundimage"],(0,0))
                screen.blit(startText,((game.options.dimensions[0]//2)-(startText.get_rect().width//2),20))
                screen.blit(game.storage.textureStorage["logoSmall"],(515,28))
                screen.blit(game.storage.guiTexts["back"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["back"].get_rect().width//2)) and mousePos[1] in range(620,690)) else game.storage.guiTexts["backHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),620))
                screen.blit(game.storage.guiTexts["newGame"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["newGame"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["newGame"].get_rect().width//2)) and mousePos[1] in range(200,270)) else game.storage.guiTexts["newGameHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["newGame"].get_rect().width//2),200))
                screen.blit(game.storage.guiTexts["loadGame"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["loadGame"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["loadGame"].get_rect().width//2)) and mousePos[1] in range(290,360)) else game.storage.guiTexts["loadGameHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["loadGame"].get_rect().width//2),300))



            elif game.options.currentScreen == "saveAs":
                screen.blit(game.storage.textureStorage["backgroundimage"],(0,0))
                screen.blit(saveAsText,((game.options.dimensions[0]//2)-(saveAsText.get_rect().width//2),10))
                screen.blit(game.storage.guiTexts["back"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["back"].get_rect().width//2)) and mousePos[1] in range(420,490)) else game.storage.guiTexts["backHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),420))
                game.storage.textinput.update(events)
                screen.blit(game.storage.textinput.get_surface(), ((game.options.dimensions[0]//2)-(game.storage.textinput.get_surface().get_rect().width//2), 150))
                screen.blit(saveGame if not (mousePos[0] in range((game.options.dimensions[0]//2)-(saveGame.get_rect().width//2),(game.options.dimensions[0]//2)+(saveGame.get_rect().width//2)) and mousePos[1] in range(330,390)) else saveGame_HOVER,((game.options.dimensions[0]//2)-(saveGame.get_rect().width//2),330))
                if game.storage.noCommaFrames > 0:
                    game.storage.noCommaFrames -= 1
                    screen.blit(noComma, ((game.options.dimensions[0]//2)-(noComma.get_rect().width//2),550))

            elif game.options.currentScreen == "newGame":
                sizeSliderText = game.storage.fonts[28].render("Weltgröße: "+str(game.storage.worldSizeSlider+100)+"x"+str(game.storage.worldSizeSlider+100), True, const.WHITE)
                entitySliderText = game.storage.fonts[28].render("Startkreaturen: "+str(game.storage.entityCountSlider+10), True, const.WHITE)
                screen.blit(game.storage.textureStorage["backgroundimage"],(0,0))
                screen.blit(game.storage.guiTexts["back"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["back"].get_rect().width//2)) and mousePos[1] in range(620,690)) else game.storage.guiTexts["backHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),620))
                pygame.draw.rect(screen,const.WHITE,[165,250,950,5])
                pygame.draw.rect(screen,[150,150,150],[165 + game.storage.worldSizeSlider,230,15,45])
                screen.blit(sizeSliderText, ((game.options.dimensions[0]//2)-(sizeSliderText.get_rect().width//2),180))
                pygame.draw.rect(screen,const.WHITE,[165,400,950,5])
                pygame.draw.rect(screen,[150,150,150],[165 + game.storage.entityCountSlider,380,15,45])
                screen.blit(entitySliderText,((game.options.dimensions[0]//2)-(entitySliderText.get_rect().width//2),330))
                screen.blit(game.storage.guiTexts["startGame"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["startGame"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["startGame"].get_rect().width//2)) and mousePos[1] in range(540,610)) else game.storage.guiTexts["startGameHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["startGame"].get_rect().width//2),540))


            elif game.options.currentScreen == "loadGame":
                screen.blit(game.storage.textureStorage["backgroundimage"],(0,0))
                screen.blit(game.storage.guiTexts["back"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["back"].get_rect().width//2)) and mousePos[1] in range(620,690)) else game.storage.guiTexts["backHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),620))
                screen.blit(game.storage.textureStorage["left"],(20, 328))
                screen.blit(game.storage.textureStorage["right"],(1196, 328))
                worldNameToLoad = game.storage.fonts[48].render(game.storage.savedWorldsList[game.storage.worldNumber],True,const.WHITE)
                screen.blit(worldNameToLoad,[(game.options.dimensions[0]//2)-(worldNameToLoad.get_rect().width//2) + 120,330])
                screen.blit(game.storage.textureStorage["worldImage"],[100,180])
                screen.blit(game.storage.guiTexts["startGame"] if not (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["startGame"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["startGame"].get_rect().width//2)) and mousePos[1] in range(540,610)) else game.storage.guiTexts["startGameHover"],((game.options.dimensions[0]//2)-(game.storage.guiTexts["startGame"].get_rect().width//2),540))
            if game.storage.toastDuration > 0:
                game.storage.toastDuration -= 1
                screen.blit(toast,[(game.options.dimensions[0]//2)-(toast.get_rect().width//2),600])
                screen.blit(game.storage.toastMessage,[(game.options.dimensions[0]//2)-(game.storage.toastMessage.get_rect().width//2),635])


            
            #Code, der jeden Frame ausgeführt wird. (auch Draw-Befehle)
    class timedExecute:
        def onSecondFunction():
            if game.storage.playerInGame:
                game.storage.playerInformation["energy"] -= 1
            #print(len(game.storage.gameEntities))
            if game.options.currentScreen == "game" and game.storage.simulationRunning:
                game.storage.gameWorld = creatureEngine.runWorldIteration(game.storage.gameWorld)
            #Code, der jede Sekunde ausgeführt wird.
    
    class evolvers:
        def respawnPlayer():
            game.storage.playerInformation = creatureEngine.newCreature()
            game.storage.playerInformation["name"] = "PLAYER"
            game.storage.playerInformation["x"] = 16
            game.storage.playerInformation["y"] = 9
            game.storage.playerInformation["attributes"]["birthEnergy"] = 50
            game.storage.playerInformation["attributes"]["birthTreshold"] = 100
            del game.storage.playerInformation["attributes"]["fleeState"],game.storage.playerInformation["attributes"]["eatState"],game.storage.playerInformation["attributes"]["eatSpeed"],game.storage.playerInformation["attributes"]["fleeSpeed"],game.storage.playerInformation["attributes"]["walkSpeed"]
            game.storage.playerInformation["attributes"]["speed"] = 10
        def reloadSettings():
            try:
                game.options.optionsFile = eval(readfile("settings.json"))
                if not (str(type(game.options.optionsFile))  == "<class 'dict'>"):
                    raise EOFError("Settings File corrupted")
            except:
                raise EOFError("Settings File corrupted")
            #Neuladen der Sprachpakete
            if 'languagePack' in game.options.optionsFile:
                game.options.language = game.options.optionsFile["languagePack"]
            else:
                game.options.language = "STD"
            if os.path.isfile(game.options.optionsFile["languagePack"]+".lang"):
                try:
                    game.options.langData = eval(readfile(game.options.optionsFile["languagePack"]+".lang"))
                except:
                    game.options.language = "STD"
            else:
                game.options.language = "STD"
            if game.options.language == "STD":
                game.options.langData = builtin.builtinLanguage
            #Neuladen der Spieleinstellungen und Lesen in die Storage Class
            game.options.sizeAffect = game.options.optionsFile["sizeAffect"]
            try:
                game.storage.optionsFile = eval(readfile("settings.json"))
                if not (str(type(game.storage.optionsFile))  == "<class 'dict'>"):
                    raise EOFError("Settings File corrupted")
            except:
                raise EOFError("Settings File corrupted")
            game.storage.viewDistance = game.storage.optionsFile["viewDistance"]
            game.storage.fieldSize = 40 if game.storage.viewDistance == 32 else 20 if game.storage.viewDistance == 64 else 80
        def toastMessage(message,duration):
            game.storage.toastDuration = duration
            game.storage.toastMessage = game.storage.fonts[24].render(message,True,const.WHITE)

execute.init.texLoader()
execute.init.gameInit()
pygame.init()
programIcon = pygame.image.load('icon.png')



with open("data","r") as f:
    game.storage.savedWorldsList = f.read().split(",")
    f.close()



pygame.display.set_icon(programIcon)
screen = pygame.display.set_mode(game.options.dimensions)
clock = pygame.time.Clock()
pygame.display.set_caption(game.options.gameTitle)

pygame.key.set_repeat(100, 10)

for i in [96,64,48,28,24,18]: #Alle zu ladenden Schriftgrößen
    game.storage.fonts[i] = pygame.font.Font("font_pt-sans.ttf",i) #Fonts laden


s = pygame.Surface((280,720))
toast = pygame.Surface((1024,100))

game.storage.ctrlTexts:list = []

for control in game.options.langData["controls"]:
    game.storage.ctrlTexts += [game.storage.fonts[18].render(control, True, const.WHITE)] # Steuerungsmethoden rendern



s.set_alpha(180)
toast.set_alpha(180)
s.fill((0,0,0))
toast.fill((0,0,0))


#Render Template
if not (os.path.isfile("render_template")):
    raise EOFError("No render template found!")
else:
    try:
        with open("render_template","r") as f:
            render_template = eval(f.read())
            f.close()
        if type(render_template) != type([1,]):
            raise EOFError("Render template incomplete")
    except:
        raise EOFError("Render template incomplete")


for render_job in render_template: #Render every text in the render template
    game.storage.guiTexts[render_job["name"]] = game.storage.fonts[render_job["font_size"]].render(render_job["text"],True,render_job["color"])
    if render_job["createHover"]:
        game.storage.guiTexts[render_job["name"]+"Hover"] = game.storage.fonts[render_job["font_size"]].render(render_job["text"],True,const.GREY)




benchmarkRunning = game.storage.fonts[48].render("Benchmark läuft... Bitte warten...", True, const.WHITE)
lowend = game.storage.fonts[48].render("Simuliere Szenario 1/3", True, const.WHITE)
midend = game.storage.fonts[48].render("Simuliere Szenario 2/3", True, const.WHITE)
highend = game.storage.fonts[48].render("Simuliere Szenario 3/3", True, const.WHITE)
results = game.storage.fonts[64].render("Ergebnisse", True, const.WHITE)

backToGame = game.storage.fonts[64].render("Zurück zum Spiel", True, const.WHITE)
backToGame_HOVER = game.storage.fonts[64].render("Zurück zum Spiel", True, const.GREY)

saveGame = game.storage.fonts[64].render("Speichern", True, const.WHITE)
saveGame_HOVER = game.storage.fonts[64].render("Speichern", True, const.GREY)

noComma = game.storage.fonts[48].render("Im Namen darf kein Komma vorkommen!", True, [255,0,0])

saveAsText = game.storage.fonts[48].render("Gib einen Namen für den Spielstand ein", True, const.WHITE)

menuTextA = game.storage.fonts[64].render("START", True, const.WHITE)
menuTextA_HOVER = game.storage.fonts[64].render("START", True, const.GREY)
menuTextB = game.storage.fonts[64].render("BENCHMARK", True, const.WHITE)
menuTextB_HOVER = game.storage.fonts[64].render("BENCHMARK", True, const.GREY)
startText = game.storage.fonts[96].render("EV   LVERS", True, const.WHITE)
relsize = game.storage.fonts[48].render("Größe im Verhältnis zur Energie", True, const.WHITE)



while not game.state.done:
    events = pygame.event.get()
    for event in events:
        if game.options.currentScreen != "game":
            mousePos = list(pygame.mouse.get_pos())
        if event.type == pygame.QUIT:
            game.state.done = True
        if pygame.mouse.get_pressed()[0]:
            try:
                if game.options.currentScreen == "newGame":
                    if (mousePos[0] in range(165,1115) and mousePos[1] in range(230,270)):
                        game.storage.worldSizeSlider = mousePos[0] - 165
                    if (mousePos[0] in range(165,1115) and mousePos[1] in range(380,430)):
                        game.storage.entityCountSlider = mousePos[0] - 165
                        
            except AttributeError:
                pass
                            

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4 and game.options.currentScreen == "game":
                game.storage.camMaxSpeed *= 2 if game.storage.camMaxSpeed < 3 else 1
            if event.button == 5 and game.options.currentScreen == "game":
                game.storage.camMaxSpeed /= 2 if game.storage.camMaxSpeed > 0.2 else 1
            if event.button < 4:
                if game.options.currentScreen == "game":
                    pos = list(pygame.mouse.get_pos())
                    pos[0]+=int(game.storage.cameraPos[0]%1*game.storage.fieldSize)
                    pos[1]+=int(game.storage.cameraPos[1]%1*game.storage.fieldSize)
                    flooredCameraPos = [int(game.storage.cameraPos[0]),int(game.storage.cameraPos[1]),int(game.storage.cameraPos[2]),int(game.storage.cameraPos[3])]
                    crt = creatureClickEngine.assignClick(pos,flooredCameraPos,game.storage.gameEntities,game.storage.showSidebar,game.storage.fieldSize)
                    if not crt == None:
                        game.storage.showSidebar = True
                        game.storage.sideBarInformation["name"] = game.storage.gameEntities[crt]["name"]
                        game.storage.sideBarInformation["age"] = game.storage.gameEntities[crt]["age"]
                        game.storage.sideBarInformation["energy"] = game.storage.gameEntities[crt]["energy"]
                        game.storage.sideBarInformation["parent"] = game.storage.gameEntities[crt]["parent"]
                        game.storage.sideBarInformation["generation"] = game.storage.gameEntities[crt]["generation"]
                else:
                    if game.options.currentScreen == "menu":
                        if mousePos[0] in range(580,780) and mousePos[1] in range(220,290):
                            game.options.currentScreen = "gamemodeSelect"
                            game.timers.frame = 0
                            game.timers.seconds = 0
                            game.storage.simulationRunning = True
                        elif mousePos[0] in range(480,850) and mousePos[1] in range(320,390):
                            game.options.currentScreen = "benchmarkMenu"
                            game.timers.frame = 0
                            game.timers.seconds = 0
                            game.storage.simulationRunning = False
                        elif mousePos[0] in range(450,920) and mousePos[1] in range(420,490):
                            game.options.currentScreen = "settings"
                    elif game.options.currentScreen == "benchmarkMenu":
                        if mousePos[0] in range(300,960) and mousePos[1] in range(220,290):
                            game.storage.benchmarkFrame = 0
                            game.options.currentScreen = "benchmark_nogui"
                        if mousePos[0] in range(520,720) and mousePos[1] in range(420,490):
                            game.options.currentScreen = "menu"
                    elif game.options.currentScreen == "settings":
                        if mousePos[0] in range(520,720) and mousePos[1] in range(620,690):
                            with open("settings.json","w") as f:
                                f.write(str(game.storage.optionsFile))
                                f.close()
                            game.storage.fieldSize = 40 if game.storage.viewDistance == 32 else 20 if game.storage.viewDistance == 64 else 80
                            game.storage.cameraPos = [1,1,34,22,1] if game.storage.viewDistance == 32 else [1,1,68,44,1] if game.storage.viewDistance == 64 else [1,1,18,12,1]
                            execute.evolvers.reloadSettings()
                            game.options.currentScreen = "menu"
                        if mousePos[0] in range(280,340) and mousePos[1] in range(230,290):
                            game.storage.viewDistance = 16
                            game.storage.optionsFile["viewDistance"] = 16
                        if mousePos[0] in range(630,670) and mousePos[1] in range(230,290):
                            game.storage.viewDistance = 32
                            game.storage.optionsFile["viewDistance"] = 32
                        if mousePos[0] in range(970,1010) and mousePos[1] in range(230,290):
                            game.storage.viewDistance = 64
                            game.storage.optionsFile["viewDistance"] = 64
                        if mousePos[0] in range(270,355) and mousePos[1] in range(320,395):
                            game.options.sizeAffect = not game.options.sizeAffect
                            game.storage.optionsFile["sizeAffect"] = not game.storage.optionsFile["sizeAffect"]
                    elif game.options.currentScreen == "benchmark_nogui_results":
                        if mousePos[0] in range(520,720) and mousePos[1] in range(420,490):
                            game.options.currentScreen = "menu"
                    elif game.options.currentScreen == "escapeMenu":
                        if mousePos[0] in range(420,920) and mousePos[1] in range(190,260):
                            game.options.currentScreen = "game"
                            game.storage.simulationRunning = True
                        if (mousePos[0] in range(520,810) and mousePos[1] in range(290,360)):
                            game.options.currentScreen = "saveAs"
                            game.storage.noCommaFrames = 0
                            game.storage.textinput.clear_text()
                        if (mousePos[0] in range(590,760) and mousePos[1] in range(390,460)):
                            game.options.currentScreen = "menu"
                    elif game.options.currentScreen == "saveAs":
                        if mousePos[0] in range(520,720) and mousePos[1] in range(420,490):
                            game.options.currentScreen = "escapeMenu"
                        if (mousePos[0] in range((game.options.dimensions[0]//2)-(saveGame.get_rect().width//2),(game.options.dimensions[0]//2)+(saveGame.get_rect().width//2)) and mousePos[1] in range(330,390)):
                            if "," in game.storage.textinput.get_text():
                                game.storage.noCommaFrames = 70
                                screen.blit(noComma, ((game.options.dimensions[0]//2)-(noComma.get_rect().width//2),550))
                            else:
                                with open("data","r") as f:
                                    data = f.read()
                                    f.close()
                                if not game.storage.textinput.get_text() in data.split(","):
                                    with open("data","w") as f:
                                        data += "" if len(data) == 0 else ","
                                        data += game.storage.textinput.get_text()
                                        f.write(data)
                                        f.close()
                                with open("save/"+game.storage.textinput.get_text()+"_world.json","w") as f:
                                    f.write(str(game.storage.gameWorld))
                                    f.close()
                                with open("save/"+game.storage.textinput.get_text()+"_creatures.json","w") as f:
                                    f.write(str(game.storage.gameEntities))
                                    f.close()
                                with open("save/"+game.storage.textinput.get_text()+"_players.json","w") as f:
                                    f.write(str(game.storage.playerInformation))
                                    f.close()
                                with open("save/"+game.storage.textinput.get_text()+"_options.json","w") as f:
                                    f.write("{'seconds':"+str(game.timers.seconds)+",'frame':"+str(game.timers.frame)+"}")
                                    f.close()
                                with open("data","r") as f:
                                    game.storage.savedWorldsList = f.read().split(",")
                                    f.close()
                                game.options.currentScreen = "escapeMenu"
                    elif game.options.currentScreen == "gamemodeSelect":
                        if (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["back"].get_rect().width//2)) and mousePos[1] in range(620,690)):
                            game.options.currentScreen = "menu"
                        if (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["newGame"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["newGame"].get_rect().width//2)) and mousePos[1] in range(200,270)):
                            game.options.currentScreen = "newGame"
                        if (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["loadGame"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["loadGame"].get_rect().width//2)) and mousePos[1] in range(290,360)):
                            game.options.currentScreen = "loadGame" if game.storage.savedWorldsList != [""] else "gamemodeSelect"
                    elif game.options.currentScreen == "loadGame":
                        if (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["back"].get_rect().width//2)) and mousePos[1] in range(620,690)):
                            game.options.currentScreen = "gamemodeSelect"
                        if mousePos[0] in range(20, 84) and mousePos[1] in range(328, 392):
                            game.storage.worldNumber -= 1 if game.storage.worldNumber > 0 else 0
                        if mousePos[0] in range(1196, 1260) and mousePos[1] in range(328, 392):
                            game.storage.worldNumber += 1 if game.storage.worldNumber+1 < len(game.storage.savedWorldsList) else 0
                        if (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["startGame"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["startGame"].get_rect().width//2)) and mousePos[1] in range(540,610)):
                            with open("save/"+game.storage.savedWorldsList[game.storage.worldNumber]+"_world.json","r") as f:
                                game.storage.gameWorld = eval(f.read())
                                f.close()
                            with open("save/"+game.storage.savedWorldsList[game.storage.worldNumber]+"_players.json","r") as f:
                                game.storage.playerInformation = eval(f.read())
                                f.close()
                            with open("save/"+game.storage.savedWorldsList[game.storage.worldNumber]+"_creatures.json","r") as f:
                                game.storage.gameEntities = eval(f.read())
                                f.close()
                            with open("save/"+game.storage.savedWorldsList[game.storage.worldNumber]+"_options.json","r") as f:
                                worldOptionsFile:dict = eval(f.read())
                                f.close()
                            game.timers.frame = worldOptionsFile["frame"]
                            game.storage.camSpeedMax = 1
                            game.timers.seconds = worldOptionsFile["seconds"]
                            game.storage.gameWorld = creatureEngine.runWorldIteration(game.storage.gameWorld)
                            game.storage.cameraPos = [1,1,34,22,1] if game.storage.viewDistance == 32 else [1,1,68,44,1] if game.storage.viewDistance == 64 else [1,1,18,12,1]
                            game.options.currentScreen = "game"
                    elif game.options.currentScreen == "newGame":
                        if (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["back"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["back"].get_rect().width//2)) and mousePos[1] in range(620,690)):
                            game.options.currentScreen = "gamemodeSelect"
                        if (mousePos[0] in range((game.options.dimensions[0]//2)-(game.storage.guiTexts["startGame"].get_rect().width//2),(game.options.dimensions[0]//2)+(game.storage.guiTexts["startGame"].get_rect().width//2)) and mousePos[1] in range(540,610)):
                            game.storage.gameEntities = creatureEngine.initCreatures(game.storage.entityCountSlider+10)
                            game.storage.worldSize = [game.storage.worldSizeSlider+100,game.storage.worldSizeSlider+100]
                            game.storage.gameWorld = creatureEngine.initWorld(game.storage.worldSizeSlider+100,game.storage.worldSizeSlider+100,game.storage.worldGeneration,game.storage.worldSmooth)
                            game.timers.frame = 0
                            game.timers.seconds = 0
                            game.storage.camSpeedMax = 1
                            execute.evolvers.respawnPlayer()
                            game.storage.gameWorld = creatureEngine.runWorldIteration(game.storage.gameWorld)
                            game.storage.cameraPos = [1,1,34,22,1] if game.storage.viewDistance == 32 else [1,1,68,44,1] if game.storage.viewDistance == 64 else [1,1,18,12,1]
                            game.options.currentScreen = "game"


        if event.type == pygame.KEYDOWN:
            #CONTROLS
            if game.options.currentScreen == "game":
                if event.key == pygame.K_F12:
                    evolversRenderer.render_frame(game.storage.gameWorld,game.storage.gameEntities,10)
                if event.key == pygame.K_ESCAPE:
                    game.options.currentScreen = "escapeMenu"
                    game.storage.simulationRunning = False
                if event.key == pygame.K_LEFT:
                    if not game.storage.playerInGame:
                        game.storage.cameraMoved = True
                        game.storage.cameraSpeed[0] = (-(game.storage.camMaxSpeed)+game.storage.cameraSpeed[0]*7)/8
                        game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[game.storage.cameraSpeed[0],0],game.storage.worldSize)
                if event.key == pygame.K_RIGHT:
                    if not game.storage.playerInGame:
                        game.storage.cameraSpeed[0] = ((game.storage.camMaxSpeed)+game.storage.cameraSpeed[0]*7)/8
                        game.storage.cameraMoved = True
                        game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[game.storage.cameraSpeed[0],0],game.storage.worldSize)
                if event.key == pygame.K_UP:
                    if not game.storage.playerInGame:
                        game.storage.cameraSpeed[1] = (-(game.storage.camMaxSpeed)+game.storage.cameraSpeed[1]*7)/8
                        game.storage.cameraMoved = True
                        game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[0,game.storage.cameraSpeed[1]],game.storage.worldSize)
                if event.key == pygame.K_DOWN:
                    if not game.storage.playerInGame:
                        game.storage.cameraSpeed[1] = ((game.storage.camMaxSpeed)+game.storage.cameraSpeed[1]*7)/8
                        game.storage.cameraMoved = True
                        game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[0,game.storage.cameraSpeed[1]],game.storage.worldSize)
                if event.key == pygame.K_SPACE:
                    game.storage.simulationRunning = not game.storage.simulationRunning
                    execute.evolvers.toastMessage("Simulation gestartet." if game.storage.simulationRunning else "Simulation gestoppt.",60)
                if event.key == pygame.K_d:
                    if bool(game.timers.frame % 2) or game.storage.playerHasMoved == 0:
                        if int(game.storage.playerInformation["energy"]) > 0:
                            if not int(game.storage.playerInformation["x"]+1) >= game.storage.worldSize[0]:
                                game.storage.playerHasMoved = 2
                                game.storage.playerInformation["energy"] -= 1
                                game.storage.playerInformation["x"] += (game.storage.playerInformation["attributes"]["speed"] / 10) if game.storage.playerInformation["x"] < game.storage.worldSize[0] else 0
                        else:
                            execute.evolvers.respawnPlayer()
                if event.key == pygame.K_a:
                    if bool(game.timers.frame % 2) or game.storage.playerHasMoved == 0:
                        if int(game.storage.playerInformation["energy"]) > 0:
                            game.storage.playerHasMoved = 2
                            game.storage.playerInformation["energy"] -= 1
                            game.storage.playerInformation["x"] -= (game.storage.playerInformation["attributes"]["speed"] / 10) if game.storage.playerInformation["x"] > 1 else 0
                        else:
                            execute.evolvers.respawnPlayer()
                if event.key == pygame.K_s:
                    if bool(game.timers.frame % 2) or game.storage.playerHasMoved == 0:
                        if int(game.storage.playerInformation["energy"]) > 0:
                            if not int(game.storage.playerInformation["y"]+1) >= game.storage.worldSize[1]:
                                game.storage.playerHasMoved = 2
                                game.storage.playerInformation["energy"] -= 1
                                game.storage.playerInformation["y"] += (game.storage.playerInformation["attributes"]["speed"] / 10) if game.storage.playerInformation["y"] < game.storage.worldSize[1] else 0
                        else:
                            execute.evolvers.respawnPlayer()
                if event.key == pygame.K_w:
                    if bool(game.timers.frame % 2) or game.storage.playerHasMoved == 0:
                        if int(game.storage.playerInformation["energy"]) > 0:
                            game.storage.playerHasMoved = 2
                            game.storage.playerInformation["energy"] -= 1
                            game.storage.playerInformation["y"] -= (game.storage.playerInformation["attributes"]["speed"] / 10) if game.storage.playerInformation["y"] > 1 else 0
                        else:
                            execute.evolvers.respawnPlayer()
                if event.key == pygame.K_m:
                    game.storage.runMouseHover = not game.storage.runMouseHover
                if event.key == pygame.K_e:
                    game.storage.showSidebar = not game.storage.showSidebar
                if event.key == pygame.K_p:
                    game.storage.playBackSpeed *= 2 if game.storage.playBackSpeed < 15 else 1
                if event.key == pygame.K_j:
                    game.storage.playerInGame = not game.storage.playerInGame
                    game.storage.playerCameraMovement = [0,0]
                    game.storage.cameraPos = [1,1,34,22,1] if game.storage.viewDistance == 32 else [1,1,68,44,1] if game.storage.viewDistance == 64 else [1,1,18,11,1]
                    if game.storage.playerInGame:
                        game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[game.storage.playerInformation["x"]%1,game.storage.playerInformation["y"]%1], game.storage.worldSize)
                if event.key == pygame.K_o:
                    game.storage.playBackSpeed /= 2 if game.storage.playBackSpeed >= 2 else 1
                    game.storage.playBackSpeed = int(game.storage.playBackSpeed)
                if event.key == pygame.K_q:
                    if game.storage.gameWorld[1][int(game.storage.playerInformation["x"])][int(game.storage.playerInformation["y"])] >= 1 and game.storage.playerInformation["energy"] < 1000:
                        game.storage.gameWorld[1][int(game.storage.playerInformation["x"])][int(game.storage.playerInformation["y"])] -= 1
                        game.storage.playerInformation["energy"] += 7
                if event.key == pygame.K_x:
                    if game.storage.playerInformation["energy"] > 100 and game.storage.playerInGame:
                        game.storage.playerInformation["energy"] -= 100
                        childcrt = creatureEngine.newCreature()
                        childcrt["x"] = game.storage.playerInformation["x"]
                        childcrt["y"] = game.storage.playerInformation["y"]
                        childcrt["color"] = game.storage.playerInformation["color"].copy()
                        game.storage.gameEntities += [childcrt]

    #code
    execute.draw.onDrawFunction()
    pygame.mouse.set_visible(game.options.cursorVisible)
    pygame.display.flip()

    clock.tick(game.options.frame_rate)

    game.timers.frame+=1
    if game.timers.frame >= game.options.frame_rate:
        game.timers.frame = 0
        game.timers.seconds+=1
        execute.timedExecute.onSecondFunction()



pygame.quit()
