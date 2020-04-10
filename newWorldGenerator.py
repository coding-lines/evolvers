from random import randint

def makeWorld(worldSizeX,worldSizeY,smoothIters=8):
    world = []
    for x in range(worldSizeX):
        world += [[]]
        for y in range(worldSizeY):
            world[x]+=[True if randint(0,100) > 45 else False]
    #for x in range(worldSizeX):
        #world[x].sort()
        #for i in range(randint(int(worldSizeX/5),int(worldSizeX/3))):
        #    world[x].append(world[x].pop(0))
    worldNew = []
    for x in range(worldSizeX):
        worldNew += [[]]
        for y in range(worldSizeY):
            addedBools = 0
            if x % worldSizeX != 0:
                addedBools += int(world[x-1][y])
                if x <= worldSizeX-2:
                    addedBools += int(world[x+1][y])
                    addedBools+= int(world[x+1][y-1])
                if y % worldSizeY != 0:
                    addedBools += int(world[x-1][y-1])
                    if x <= worldSizeX-2 and y <= worldSizeY-2:
                        addedBools+= int(world[x+1][y+1])
            if y % worldSizeY != 0:
                addedBools += int(world[x][y-1])
                if y <= worldSizeY-2:
                    addedBools += int(world[x][y+1])
                    addedBools+= int(world[x-1][y+1])
            if addedBools >= 4:
                worldNew[x] += [True]
            else:
                worldNew[x] += [False]

    for iter in range(smoothIters):
        world = worldNew.copy()
        worldNew = []
        for x in range(worldSizeX):
            worldNew += [[]]
            for y in range(worldSizeY):
                addedBools = 0
                if x % worldSizeX != 0:
                    addedBools += int(world[x-1][y])
                    if x <= worldSizeX-2:
                        addedBools += int(world[x+1][y])
                        addedBools+= int(world[x+1][y-1])
                    if y % worldSizeY != 0:
                        addedBools += int(world[x-1][y-1])
                        if x <= worldSizeX-2 and y <= worldSizeY-2:
                            addedBools+= int(world[x+1][y+1])
                if y % worldSizeY != 0:
                    addedBools += int(world[x][y-1])
                    if y <= worldSizeY-2:
                        addedBools += int(world[x][y+1])
                        addedBools+= int(world[x-1][y+1])
                if addedBools >= 5:
                    worldNew[x] += [True]
                else:
                    worldNew[x] += [False]
    
    
    worldFood = []
    for x in range(worldSizeX):
        worldFood +=[[]]
        for y in range(worldSizeY):
            if worldNew[x][y]:
                worldFood[x] += [randint(1,2)]
            else:
                worldFood[x] += [0]
    
    return [worldNew,worldFood]
