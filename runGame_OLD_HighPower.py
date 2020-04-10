import pygame
import time
import creatureEngine,creatureNames,cameraEngine,creatureClickEngine,mouseHoverEngine
import math

class game():
    class options():
        dimensions = [1280,720]
        frame_rate = 60
        gameTitle = "Evolvers"
        pixel_size = 1
        cursorVisible = True
        sizeAffect = False
        #Generelle Informationen über das Spiel
    class timers():
        frame = 0
        seconds = 0
        #In dieser Klasse kann direkt auf die GameTimer zugegriffen werden.
    class state():
        done = False
        #Status des Spiels
    class storage():
        worldGeneration = "new"
        playerHasMoved = 0
        playerInGame = False
        playerCameraMovement = [0,0]
        playerInformation = creatureEngine.newCreature()
        playerInformation["name"] = "PLAYER"
        playerInformation["x"] = 32
        playerInformation["y"] = 18
        playerInformation["attributes"]["birthEnergy"] = 50
        playerInformation["attributes"]["birthTreshold"] = 100
        del playerInformation["attributes"]["fleeState"],playerInformation["attributes"]["eatState"],playerInformation["attributes"]["eatSpeed"],playerInformation["attributes"]["fleeSpeed"],playerInformation["attributes"]["walkSpeed"]
        playerInformation["attributes"]["speed"] = 10
        runMouseHover = True
        playBackSpeed = 1
        sideBarInformation: dict = {"name":"None","energy":0,"parent":"None","age":0,"generation":0}
        showSidebar = True
        simulationRunning = True
        startCreatures = 100
        worldSize = [200,200]
        cameraPos = [1,1,68,44,1]
        trueFPS = 60
        textureStorage: dict = {}
        x = time.time()
        print("Generiere Kreaturen... Das kann einige Zeit dauern...")
        gameEntities = creatureEngine.initCreatures(startCreatures)
        print(str(startCreatures)+" Kreaturen in "+str(time.time()-x) + " Sekunden generiert.")
        x = time.time()
        print("Generiere Welt... Das kann einige Zeit dauern...")
        gameWorld = creatureEngine.initWorld(worldSize[0],worldSize[1],worldGeneration)
        print("Welt von der Größe",str(worldSize[0]),"x",str(worldSize[1]), "in",str(time.time()-x),"Sekunden generiert.")
        saturationMax = 11
        #Speicherort von Spieldaten oder Texturen

class engine():
    class draw():
        def absoluteRect(posList,color):
            pygame.draw.rect(screen, color, [posList[0],posList[1],posList[2]-posList[0],posList[3]-posList[1]])
        def pixel(posX,posY,color):
            pygame.draw.rect(screen, color, [posX*game.options.pixel_size,posY*game.options.pixel_size,game.options.pixel_size,game.options.pixel_size])
        def pixelRect(posList,color):
            engine.draw.absoluteRect([posList[0]*game.options.pixel_size,posList[1]*game.options.pixel_size,posList[2]*game.options.pixel_size,posList[3]*game.options.pixel_size],color)
        def textureDraw(posX,posY,textureObject):
            for x in range(textureObject.width):
                for y in range(textureObject.height):
                    if textureObject.getpixel((x,y))[3] == 255:
                        engine.draw.pixel(x+posX,y+posY,list(textureObject.getpixel((x,y))))
        def refreshGameInformations():
            global screen
            screen = pygame.display.set_mode(game.options.dimensions)
            pygame.display.set_caption(game.options.gameTitle)
            game.options.pixel_count = [game.options.dimensions[0] // game.options.pixel_size, game.options.dimensions[1] // game.options.pixel_size]


class execute():
    class init():
        def texLoader():
            pass
            #Funktion, um Texturen zu laden. (Texturen können auch in der DrawFunction geladen werden, das spart zwar RAM, aber führt zu Rucklern!)
        def gameInit():
            pass
            #Funktion, die beim Spielstart ausgeführt wird.
    class draw():
        def onDrawFunction():
            game.storage.trueFPS = clock.get_fps() if bool(game.timers.frame % 2) else game.storage.trueFPS
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
                        green = int(game.storage.gameWorld[1][x][y] / (game.storage.saturationMax+1) *100) + 50
                        red = 50
                    else:
                        blue = 150
                        green = 100
                        red = 0
                    p1 = [(x-game.storage.cameraPos[0])*20,(y-game.storage.cameraPos[1])*20]
                    pygame.draw.line(screen,[0,0,0],[p1[0],0],[p1[0],game.options.dimensions[1]])
                    pygame.draw.line(screen,[0,0,0],[0,p1[1]],[game.options.dimensions[0],p1[1]])
                    pygame.draw.rect(screen, [red,green,blue], [p1[0],p1[1],40,40])
            #MOUSEHOVER
            if game.storage.runMouseHover:
                pos = list(pygame.mouse.get_pos())
                posNew = mouseHoverEngine.assignClick(pos,game.storage.showSidebar,game.storage.cameraPos,20)
                if not posNew == None:
                    saturationText = game.storage.font.render(str(round(game.storage.gameWorld[1][posNew[0]][posNew[1]],1)), True, [255,255,255])
                    screen.blit(saturationText,(pos[0], pos[1]+20))
            #KREATUREN
            for c in range(0,len(game.storage.gameEntities)):
                pos = [int((game.storage.gameEntities[c]["x"] - game.storage.cameraPos[0])*20),int((game.storage.gameEntities[c]["y"] - game.storage.cameraPos[1])*20)]
                size = int((game.storage.gameEntities[c]["energy"]/8+60)/5) if game.options.sizeAffect else 15
                pygame.draw.circle(screen,game.storage.gameEntities[c]["boundaries"],pos,size+2)
                pygame.draw.circle(screen,game.storage.gameEntities[c]["color"],pos,size)
                text = game.storage.font.render(game.storage.gameEntities[c]["name"], True, [255,255,255])
                screen.blit(text,(pos[0]-40, pos[1]+size))

            #SPIELER
            if game.storage.playerInGame:
                game.storage.playerInformation["age"] += 1
                for i in range(10):
                    game.storage.camposBackup = game.storage.cameraPos[:]
                    if game.storage.playerCameraMovement[0] <= -1:
                        game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[-1,0],game.storage.worldSize)
                        if game.storage.camposBackup != game.storage.cameraPos:
                            game.storage.playerCameraMovement[0] += 1
                    elif game.storage.playerCameraMovement[0] >= 1:
                        game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[1,0],game.storage.worldSize)
                        if game.storage.camposBackup != game.storage.cameraPos:
                            game.storage.playerCameraMovement[0] -= 1
                    elif game.storage.playerCameraMovement[1] <= -1:
                        game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[0,-1],game.storage.worldSize)
                        if game.storage.camposBackup != game.storage.cameraPos:
                            game.storage.playerCameraMovement[1] += 1
                    elif game.storage.playerCameraMovement[1] >= 1:
                        game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[0,1],game.storage.worldSize)
                        if game.storage.camposBackup != game.storage.cameraPos:
                            game.storage.playerCameraMovement[1] -= 1
                    else:
                        break
                pos = [int((game.storage.playerInformation["x"] - game.storage.cameraPos[0])*20),int((game.storage.playerInformation["y"] - game.storage.cameraPos[1])*20)]
                if pos[0] < 600:
                    game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[-1,0],game.storage.worldSize)
                if pos[0] > 600:
                    game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[1,0],game.storage.worldSize)
                if pos[1] < 320:
                    game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[0,-1],game.storage.worldSize)
                if pos[1] > 320:
                    game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[0,1],game.storage.worldSize)
                
                size = int((game.storage.gameEntities[c]["energy"]/8+60)/5) if game.options.sizeAffect else 15
                pos = [int((game.storage.playerInformation["x"] - game.storage.cameraPos[0])*20),int((game.storage.playerInformation["y"] - game.storage.cameraPos[1])*20)]
                pygame.draw.circle(screen,game.storage.playerInformation["boundaries"],pos,size+2)
                pygame.draw.circle(screen,game.storage.playerInformation["color"],pos,size)
                text = game.storage.font.render("PLAYER", True, [255,255,255])
                screen.blit(text,(pos[0]-50, pos[1]+size))

            
            
            #SIDEBAR
            if game.storage.showSidebar:
                screen.blit(s, (1000,0))
                
                timeText = game.storage.fontBig.render("Jahr: "+str(round((game.timers.frame + (game.timers.seconds*60))/4800,3)), True, [255,255,255])
                screen.blit(timeText,(1010,20))
                popText = game.storage.fontBig.render("Bevölkerung: "+str(len(game.storage.gameEntities)), True, [255,255,255])
                screen.blit(popText,(1010,60))
                modeText = game.storage.font.render("Spielmodus: Kreatur" if game.storage.playerInGame else "Spielmodus: Zuschauer", True, [255,255,255])
                screen.blit(modeText,(1010,100))
                
                if not game.storage.playerInGame:
                    nameText = game.storage.font.render("Name: "+game.storage.sideBarInformation["name"], True, [255,255,255])
                
                    ageText = game.storage.font.render("Alter: "+str(round(game.storage.sideBarInformation["age"]/4800,3))+" Jahre", True, [255,255,255])
                
                    genText = game.storage.font.render("Generation: "+str(game.storage.sideBarInformation["generation"]), True, [255,255,255])
                
                    parentText = game.storage.font.render("Elternteil: "+str(game.storage.sideBarInformation["parent"]), True, [255,255,255])
                
                
                    energyText = game.storage.font.render("Energie: "+str(game.storage.sideBarInformation["energy"]), True, [255,255,255])
                
                else:
                    nameText = game.storage.font.render("Name: PLAYER", True, [255,255,255])
                    ageText = game.storage.font.render("Alter: "+str(round(game.storage.playerInformation["age"]/4800,3))+" Jahre", True, [255,255,255])
                    genText = game.storage.font.render("Generation: 0", True, [255,255,255])
                    parentText = game.storage.font.render("Elternteil: None", True, [255,255,255])
                    energyText = game.storage.font.render("Energie: "+str(game.storage.playerInformation["energy"]), True, [255,255,255])

                FPS = game.storage.font.render("FPS: "+str(int(game.storage.trueFPS)), True, [255,255,255])
                screen.blit(FPS,(1010,400))
                
                
                
                
                screen.blit(nameText,(1010,140))
                screen.blit(ageText,(1010,180))
                screen.blit(genText,(1010,220))
                screen.blit(parentText,(1010,260))
                screen.blit(energyText,(1010,300))
                
                for i,n in enumerate(game.storage.ctrlTexts):
                    screen.blit(n,(1010,470+(i*20)))
                
                
                
                s_speedText = game.storage.fontSmall.render("Simulationsgeschwindigkeit: "+str(game.storage.playBackSpeed), True, [255,255,255])
                screen.blit(s_speedText,(1010,670))


            #Code, der jeden Frame ausgeführt wird. (auch Draw-Befehle)
    class timedExecute():
        def onSecondFunction():
            game.storage.trueFPS = clock.get_fps()
            #print(len(game.storage.gameEntities))
            game.storage.saturationMax = 11
            game.storage.gameWorld = creatureEngine.runWorldIteration(game.storage.gameWorld)
            #Code, der jede Sekunde ausgeführt wird.
            


execute.init.texLoader()
execute.init.gameInit()
pygame.init()

screen = pygame.display.set_mode(game.options.dimensions)

clock = pygame.time.Clock()


pygame.display.set_caption(game.options.gameTitle)

pygame.key.set_repeat(100, 10)

game.storage.fontBig = pygame.font.Font("font_pt-sans.ttf",28)
game.storage.font = pygame.font.Font("font_pt-sans.ttf",24)
game.storage.fontSmall = pygame.font.Font("font_pt-sans.ttf",18)
s = pygame.Surface((280,720))
game.storage.ctrlTexts = [game.storage.fontSmall.render("WASD : Kreatur bewegen", True, [255,255,255]),
                          game.storage.fontSmall.render("Leertaste: Simulation pausieren", True, [255,255,255])
                          ,game.storage.fontSmall.render("Pfeile: Kamera bewegen", True, [255,255,255])
                          ,game.storage.fontSmall.render("O / P: Schneller/Langsamer", True, [255,255,255])
                          ,game.storage.fontSmall.render("E: Seitenmenü ein/ausblenden", True, [255,255,255])
                          ,game.storage.fontSmall.render("M: Mousehover umschalten", True, [255,255,255])
                          ,game.storage.fontSmall.render("J: Spieler spawnen/löschen", True, [255,255,255])
                          ,game.storage.fontSmall.render("Q: Essen (als Spieler)", True, [255,255,255])
                          ,game.storage.fontSmall.render("X: Reproduzieren (200 Energie)", True, [255,255,255])]
s.set_alpha(180)
game.storage.gameWorld = creatureEngine.runWorldIteration(game.storage.gameWorld)
s.fill((0,0,0))   
while not game.state.done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.state.done = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button < 4:
                pos = list(pygame.mouse.get_pos())
                crt = creatureClickEngine.assignClick(pos,game.storage.cameraPos,game.storage.gameEntities,game.storage.showSidebar,20)
                if not crt == None:
                    game.storage.showSidebar = True
                    game.storage.sideBarInformation["name"] = game.storage.gameEntities[crt]["name"]
                    game.storage.sideBarInformation["age"] = game.storage.gameEntities[crt]["age"]
                    game.storage.sideBarInformation["energy"] = game.storage.gameEntities[crt]["energy"]
                    game.storage.sideBarInformation["parent"] = game.storage.gameEntities[crt]["parent"]
                    game.storage.sideBarInformation["generation"] = game.storage.gameEntities[crt]["generation"]
                    
        if event.type == pygame.KEYDOWN:
            #CONTROLS
            if event.key == pygame.K_LEFT:
                game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[-1,0],game.storage.worldSize)
            if event.key == pygame.K_RIGHT:
                game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[1,0],game.storage.worldSize)
            if event.key == pygame.K_UP:
                game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[0,-1],game.storage.worldSize)
            if event.key == pygame.K_DOWN:
                game.storage.cameraPos = cameraEngine.moveCamera(game.storage.cameraPos,[0,1],game.storage.worldSize)
            if event.key == pygame.K_SPACE:
                game.storage.simulationRunning = not game.storage.simulationRunning
                if game.storage.simulationRunning:
                    print("Simulation gestartet.")
                else:
                    print("Simulation gestoppt.")
            if event.key == pygame.K_d:
                if bool(game.timers.frame % 2) or game.storage.playerHasMoved == 0:
                    if bool(int(game.storage.playerInformation["energy"])):
                        game.storage.playerHasMoved = 2
                        game.storage.playerInformation["energy"] -= 1
                        game.storage.playerInformation["x"] += (game.storage.playerInformation["attributes"]["speed"] / 10) if game.storage.playerInformation["x"] < game.storage.worldSize[0] else 0
                        game.storage.playerCameraMovement[0] += (game.storage.playerInformation["attributes"]["speed"] / 10) if game.storage.playerInformation["x"] < game.storage.worldSize[0] else 0
                    else:
                        game.storage.playerInformation = creatureEngine.newCreature()
                        game.storage.playerInformation["name"] = "PLAYER"
                        game.storage.playerInformation["x"] = 16
                        game.storage.playerInformation["y"] = 9
                        game.storage.playerInformation["attributes"]["birthEnergy"] = 50
                        game.storage.playerInformation["attributes"]["birthTreshold"] = 100
                        del game.storage.playerInformation["attributes"]["fleeState"],game.storage.playerInformation["attributes"]["eatState"],game.storage.playerInformation["attributes"]["eatSpeed"],game.storage.playerInformation["attributes"]["fleeSpeed"],game.storage.playerInformation["attributes"]["walkSpeed"]
                        game.storage.playerInformation["attributes"]["speed"] = 10
            if event.key == pygame.K_a:
                if bool(game.timers.frame % 2) or game.storage.playerHasMoved == 0:
                    if bool(int(game.storage.playerInformation["energy"])):
                        game.storage.playerHasMoved = 2
                        game.storage.playerInformation["energy"] -= 1
                        game.storage.playerInformation["x"] -= (game.storage.playerInformation["attributes"]["speed"] / 10) if game.storage.playerInformation["x"] > 1 else 0
                        game.storage.playerCameraMovement[0] -= (game.storage.playerInformation["attributes"]["speed"] / 10) if game.storage.playerInformation["x"] > 1 else 0
                    else:
                        game.storage.playerInformation = creatureEngine.newCreature()
                        game.storage.playerInformation["name"] = "PLAYER"
                        game.storage.playerInformation["x"] = 16
                        game.storage.playerInformation["y"] = 9
                        game.storage.playerInformation["attributes"]["birthEnergy"] = 50
                        game.storage.playerInformation["attributes"]["birthTreshold"] = 100
                        del game.storage.playerInformation["attributes"]["fleeState"],game.storage.playerInformation["attributes"]["eatState"],game.storage.playerInformation["attributes"]["eatSpeed"],game.storage.playerInformation["attributes"]["fleeSpeed"],game.storage.playerInformation["attributes"]["walkSpeed"]
                        game.storage.playerInformation["attributes"]["speed"] = 10
            if event.key == pygame.K_s:
                if bool(game.timers.frame % 2) or game.storage.playerHasMoved == 0:
                    if bool(int(game.storage.playerInformation["energy"])):
                        game.storage.playerHasMoved = 2
                        game.storage.playerInformation["energy"] -= 1
                        game.storage.playerCameraMovement[1] += (game.storage.playerInformation["attributes"]["speed"] / 10) if game.storage.playerInformation["y"] < game.storage.worldSize[1] else 0
                        game.storage.playerInformation["y"] += (game.storage.playerInformation["attributes"]["speed"] / 10) if game.storage.playerInformation["y"] < game.storage.worldSize[1] else 0
                    else:
                        game.storage.playerInformation = creatureEngine.newCreature()
                        game.storage.playerInformation["name"] = "PLAYER"
                        game.storage.playerInformation["x"] = 16
                        game.storage.playerInformation["y"] = 9
                        game.storage.playerInformation["attributes"]["birthEnergy"] = 50
                        game.storage.playerInformation["attributes"]["birthTreshold"] = 100
                        del game.storage.playerInformation["attributes"]["fleeState"],game.storage.playerInformation["attributes"]["eatState"],game.storage.playerInformation["attributes"]["eatSpeed"],game.storage.playerInformation["attributes"]["fleeSpeed"],game.storage.playerInformation["attributes"]["walkSpeed"]
                        game.storage.playerInformation["attributes"]["speed"] = 10
            if event.key == pygame.K_w:
                if bool(game.timers.frame % 2) or game.storage.playerHasMoved == 0:
                    if bool(int(game.storage.playerInformation["energy"])):
                        game.storage.playerHasMoved = 2
                        game.storage.playerInformation["energy"] -= 1
                        game.storage.playerInformation["y"] -= (game.storage.playerInformation["attributes"]["speed"] / 10) if game.storage.playerInformation["y"] > 1 else 0
                        game.storage.playerCameraMovement[1] -= (game.storage.playerInformation["attributes"]["speed"] / 10) if game.storage.playerInformation["y"] > 1 else 0
                    else:
                        game.storage.playerInformation = creatureEngine.newCreature()
                        game.storage.playerInformation["name"] = "PLAYER"
                        game.storage.playerInformation["x"] = 16
                        game.storage.playerInformation["y"] = 9
                        game.storage.playerInformation["attributes"]["birthEnergy"] = 50
                        game.storage.playerInformation["attributes"]["birthTreshold"] = 100
                        del game.storage.playerInformation["attributes"]["fleeState"],game.storage.playerInformation["attributes"]["eatState"],game.storage.playerInformation["attributes"]["eatSpeed"],game.storage.playerInformation["attributes"]["fleeSpeed"],game.storage.playerInformation["attributes"]["walkSpeed"]
                        game.storage.playerInformation["attributes"]["speed"] = 10
            if event.key == pygame.K_m:
                game.storage.runMouseHover = not game.storage.runMouseHover
            if event.key == pygame.K_e:
                game.storage.showSidebar = not game.storage.showSidebar
            if event.key == pygame.K_p:
                game.storage.playBackSpeed *= 2 if game.storage.playBackSpeed < 15 else 1
            if event.key == pygame.K_j:
                game.storage.playerInGame = not game.storage.playerInGame
                game.storage.playerCameraMovement = [0,0]
                game.storage.cameraPos = [1,1,68,44,1]
            if event.key == pygame.K_o:
                game.storage.playBackSpeed /= 2 if game.storage.playBackSpeed >= 2 else 1
                game.storage.playBackSpeed = int(game.storage.playBackSpeed)
            if event.key == pygame.K_q:
                if game.storage.gameWorld[1][int(game.storage.playerInformation["x"])][int(game.storage.playerInformation["y"])] >= 1:
                    game.storage.gameWorld[1][int(game.storage.playerInformation["x"])][int(game.storage.playerInformation["y"])] -= 1
                    game.storage.playerInformation["energy"] += 7
            if event.key == pygame.K_x:
                if game.storage.playerInformation["energy"] >= 100 and game.storage.playerInGame:
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

