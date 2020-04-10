import pygame
import time
import creatureEngine,creatureNames,cameraEngine
import math

class game():
    class options():
        dimensions = [1280,720]
        frame_rate = 60
        gameTitle = "Evolvers_SMALLFOV_EXTREMELOWPOWER"
        pixel_size = 1
        cursorVisible = True
        #Generelle Informationen über das Spiel
    class timers():
        frame = 0
        seconds = 0
        #In dieser Klasse kann direkt auf die GameTimer zugegriffen werden.
    class state():
        done = False
        #Status des Spiels
    class storage():
        showSidebar = True
        simulationRunning = True
        startCreatures = 100
        worldSize = [200,200]
        cameraPos = [1,1,18,12,1]
        textureStorage: dict = {}
        x = time.time()
        print("Generiere Kreaturen... Das kann einige Zeit dauern...")
        gameEntities = creatureEngine.initCreatures(startCreatures)
        print(str(startCreatures)+" Kreaturen in "+str(time.time()-x) + " Sekunden generiert.")
        x = time.time()
        print("Generiere Welt... Das kann einige Zeit dauern...")
        gameWorld = creatureEngine.initWorld(worldSize[0],worldSize[1])
        print("Welt von der Größe",str(worldSize[0]),"x",str(worldSize[1]), "in",str(time.time()-x),"Sekunden generiert.")
        saturationMax = max(max(gameWorld[1]))
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
            #game.storage.textureStorage["testTexture"] = Image.open("testtexture.png")
            #Funktion, um Texturen zu laden. (Texturen können auch in der DrawFunction geladen werden, das spart zwar RAM, aber führt zu Rucklern!)
        def gameInit():
            pass
            #Funktion, die beim Spielstart ausgeführt wird.
    class draw():
        def onDrawFunction():
            if game.storage.simulationRunning:
                game.storage.gameEntities,game.storage.gameWorld = creatureEngine.runIteration(game.storage.gameEntities,game.storage.gameWorld)
            for x in range(int(game.storage.cameraPos[0]),int(game.storage.cameraPos[2])):
                for y in range(int(game.storage.cameraPos[1]),int(game.storage.cameraPos[3])):
                    if game.storage.gameWorld[0][x][y]:
                        blue = 0
                        green = int(game.storage.gameWorld[1][x][y] / game.storage.saturationMax *100) + 50
                        red = 50
                    else:
                        blue = 150
                        green = 100
                        red = 0
                    p1 = [(x-game.storage.cameraPos[0])*80,(y-game.storage.cameraPos[1])*80]
                    pygame.draw.line(screen,[0,0,0],[p1[0],0],[p1[0],game.options.dimensions[1]])
                    pygame.draw.line(screen,[0,0,0],[0,p1[1]],[game.options.dimensions[0],p1[1]])
                    pygame.draw.rect(screen, [red,green,blue], [p1[0],p1[1],80,80])
            for c in range(0,len(game.storage.gameEntities)):
                pos = [int((game.storage.gameEntities[c]["x"] - game.storage.cameraPos[0])*80),int((game.storage.gameEntities[c]["y"] - game.storage.cameraPos[1])*80)]
                pygame.draw.circle(screen,game.storage.gameEntities[c]["boundaries"],pos,34)
                pygame.draw.circle(screen,game.storage.gameEntities[c]["color"],pos,30)
                text = game.storage.font.render(game.storage.gameEntities[c]["name"], True, [255,255,255])
                screen.blit(text,(pos[0]-80, pos[1]+30))

            #SIDEBAR
            if game.storage.showSidebar:
                screen.blit(s, (1000,0))   
                
            #Code, der jeden Frame ausgeführt wird. (auch Draw-Befehle)
    class timedExecute():
        def onSecondFunction():
            #print(len(game.storage.gameEntities))
            game.storage.saturationMax = max(max(game.storage.gameWorld[1]))
            game.storage.gameWorld = creatureEngine.runWorldIteration(game.storage.gameWorld)
            #Code, der jede Sekunde ausgeführt wird.
            


execute.init.texLoader()
execute.init.gameInit()
pygame.init()

screen = pygame.display.set_mode(game.options.dimensions)

clock = pygame.time.Clock()


pygame.display.set_caption(game.options.gameTitle)

pygame.key.set_repeat(500, 10)

game.storage.font = pygame.font.Font("font_pt-sans.ttf",48)
s = pygame.Surface((280,720))  # the size of your rect
s.set_alpha(180)                # alpha level
s.fill((0,0,0))   
while not game.state.done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.state.done = True
        if event.type == pygame.MOUSEBUTTONUP:
            if not event.button == 4:
                if not event.button == 5:
                    pos = list(pygame.mouse.get_pos())
                    print(pos)
        if event.type == pygame.KEYDOWN:
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
            if event.key == pygame.K_e:
                game.storage.showSidebar = not game.storage.showSidebar
        #if event.type == pygame.MOUSEBUTTONDOWN:
         #   if event.button == 4:
          #      game.storage.cameraPos = cameraEngine.zoomIn(game.storage.cameraPos)
           # if event.button == 5:
            #    game.storage.cameraPos = cameraEngine.zoomOut(game.storage.cameraPos)
        
    #code
    screen.fill([255, 0, 255])
    execute.draw.onDrawFunction()
    pygame.mouse.set_visible(game.options.cursorVisible)
    pygame.display.flip()
    
    clock.tick(game.options.frame_rate)
    
    game.timers.frame+=1
    if game.timers.frame == game.options.frame_rate:
        game.timers.frame = 0
        game.timers.seconds+=1
        execute.timedExecute.onSecondFunction()
    
    
    
pygame.quit()
