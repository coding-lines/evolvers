def assignClick(mousePos,cameraPos,creatures,sidebarOpen,scale):
    if not sidebarOpen or mousePos[0] < 1000:
        ingameCoords = [(mousePos[0] // scale) + cameraPos[0], (mousePos[1] // scale)+cameraPos[1]]
        for creature in range(len(creatures)):
            if int(creatures[creature]["x"]) in range(ingameCoords[0]-2,ingameCoords[0]+2) and int(creatures[creature]["y"]) in range(ingameCoords[1]-2,ingameCoords[1] +2):
                return creature
        
