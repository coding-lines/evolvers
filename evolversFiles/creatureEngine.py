import creatureNames,newWorldGenerator
from random import randint,choice
from math import ceil


maintainPopulation = 5 #Wenn die Bevölkerung niedriger als der eingegebene Wert ist, werden neue Kreaturen gespawnt


def avg(a,b):
    return (a+b)/2


def newCreature(worldSize=[100,100]):
    bt = randint(100,400)
    col = [randint(0,255),randint(0,255),randint(0,255)]
    bnds = [255,255,255] if int(sum(col)/3) < 128 else [0,0,0]
    return {"name":creatureNames.continueName(creatureNames.continueName(creatureNames.continueName(creatureNames.continueName(creatureNames.newName())))),"energy":100,"parent":"None","x":randint(0,worldSize[0]-1),"reproduceTime":10,"rotation":choice([0,45,90,135,180,225,270,315]),"y":randint(0,worldSize[1]-1),"generation":0,"color":col,"boundaries":bnds,"age":0,"attributes":{"birthTreshold":bt,"birthEnergy":bt // 2,"eatState":randint(1,1000),"fleeState":randint(1,2),"walkSpeed":randint(1,5),"eatSpeed":randint(1,5),"fleeSpeed":randint(5,10),"avoidsWater":not bool(randint(0,100))}}

def initWorld(worldSizeX,worldSizeY, worldGeneration="new",smooth=8):
    if worldGeneration == "new":
        return newWorldGenerator.makeWorld(worldSizeX,worldSizeY,smooth)
    land = True
    world:list = []
    worldFood:list = []
    for x in range(worldSizeX):
        worldFood += [[]]
        world += [[]]
        for y in range(worldSizeY):
            world[x] += [land]
            if land:
                if x == 0 or y == 0:
                    worldFood[x]+=[3]
                else:
                    worldFood[x] += [randint(1,2)]
            else:
                worldFood[x] += [0]
            if land:
                if bool(randint(0,1)) and not bool(randint(0,3)) and bool(randint(0,1)):
                    land = not land
            else:
                if bool(randint(0,1)) and bool(randint(0,1)):
                    land = not land
    return [world,worldFood]


def createChildOf(creature):
    newCreature = creature.copy()
    newCreature["attributes"]["avoidsWater"] = not newCreature["attributes"]["avoidsWater"] if not bool(randint(0,100)) else newCreature["attributes"]["avoidsWater"]
    newCreature["parent"] = newCreature["name"][:]
    newCreature["name"] = creatureNames.alterName(newCreature["name"])
    newCreature["age"] = 0
    newCreature["rotation"] = choice([0,45,90,135,180,225,270,315])
    newCreature["generation"] += 1
    newCreature["attributes"]["birthTreshold"] = randint(100,400)
    newCreature["attributes"]["eatState"] += randint(-10,10) if (newCreature["attributes"]["eatState"] < 1000 and newCreature["attributes"]["eatState"] > 10) else randint(-10,0) if newCreature["attributes"]["eatState"] > 1000 else randint(0,10)
    if newCreature["attributes"]["walkSpeed"] in range(2,5):
        newCreature["attributes"]["walkSpeed"] += randint(-1,1)
    elif newCreature["attributes"]["walkSpeed"] == 1:
        newCreature["attributes"]["walkSpeed"] += randint(0,1)
    else:
        newCreature["attributes"]["walkSpeed"] -= randint(0,1)
    if newCreature["attributes"]["eatSpeed"] in range(2,5):
        newCreature["attributes"]["eatSpeed"] += randint(-1,1)
    elif newCreature["attributes"]["eatSpeed"] == 1:
        newCreature["attributes"]["eatSpeed"] += randint(0,1)
    else:
        newCreature["attributes"]["eatSpeed"] -= randint(0,1)
    if newCreature["attributes"]["fleeSpeed"] in range(6,10):
        newCreature["attributes"]["fleeSpeed"] += randint(-1,1)
    elif newCreature["attributes"]["fleeSpeed"] == 5:
        newCreature["attributes"]["fleeSpeed"] += randint(0,1)
    else:
        newCreature["attributes"]["fleeSpeed"] -= randint(0,1)
    newCreature["energy"] = newCreature["attributes"]["birthEnergy"]
    newCreature["attributes"]["birthEnergy"] = newCreature["attributes"]["birthTreshold"] // 2
    return newCreature
    
    

def initCreatures(count,worldSize=[100,100]):
    creatures:list = []
    for i in range(count):
        creatures += [newCreature(worldSize)]
    return creatures

def runIteration(creatures,world):
    #KREATURITERATION
    for creature in range(len(creatures)):
        if not "realFleeSpeed" in creatures[creature]["attributes"]:
            creatures[creature]["attributes"]["realFleeSpeed"] = creatures[creature]["attributes"]["fleeSpeed"]/15
            creatures[creature]["attributes"]["realWalkSpeed"] = creatures[creature]["attributes"]["walkSpeed"]/15
            creatures[creature]["attributes"]["realEatSpeed"] = creatures[creature]["attributes"]["eatSpeed"]/15

            
            
        creatures[creature]["age"] += 1 #Alter in Iterationen erhöhen
        creatures[creature]["reproduceTime"] -= 1 if creatures[creature]["reproduceTime"] > 0 else 0
        if creatures[creature]["attributes"]["fleeState"] == 1 and not world[0][int(creatures[creature]["x"])][int(creatures[creature]["y"])]:
            try:
                if creatures[creature]["attributes"]["avoidsWater"]:
                    #Alle Rotationsrichtungen nach bewohnbarem Land absuchen
                    if world[0][int(creatures[creature]["x"])][int(creatures[creature]["y"]-1)]:
                        creatures[creature]["rotation"] = 0
                    elif world[0][int(creatures[creature]["x"]+1)][int(creatures[creature]["y"]-1)]:
                        creatures[creature]["rotation"] = 45
                    elif world[0][int(creatures[creature]["x"]+1)][int(creatures[creature]["y"])]:
                        creatures[creature]["rotation"] = 90
                    elif world[0][int(creatures[creature]["x"]+1)][int(creatures[creature]["y"]+1)]:
                        creatures[creature]["rotation"] = 135
                    elif world[0][int(creatures[creature]["x"])][int(creatures[creature]["y"]+1)]:
                        creatures[creature]["rotation"] = 180
                    elif world[0][int(creatures[creature]["x"]-1)][int(creatures[creature]["y"]+1)]:
                        creatures[creature]["rotation"] = 225
                    elif world[0][int(creatures[creature]["x"]-1)][int(creatures[creature]["y"])]:
                        creatures[creature]["rotation"] = 270
                    elif world[0][int(creatures[creature]["x"]-1)][int(creatures[creature]["y"]-1)]:
                        creatures[creature]["rotation"] = 315
                    else:
                        if randint(0,100) < 5:
                            if bool(randint(0,1)):
                                creatures[creature]["rotation"] += 45 #Zufällige Rotation
                            else:
                                creatures[creature]["rotation"] -= 45
                            if creatures[creature]["rotation"] < 0:
                                creatures[creature]["rotation"] = 0
                
            except:
                if randint(0,100) < 5:
                    if bool(randint(0,1)):
                        creatures[creature]["rotation"] += 45 #Zufällige Rotation
                    else:
                        creatures[creature]["rotation"] -= 45
                    if creatures[creature]["rotation"] < 0:
                        creatures[creature]["rotation"] = 0
            
            if creatures[creature]["rotation"] in range(0,45) or creatures[creature]["rotation"] in range(314,360):
                creatures[creature]["y"] -= creatures[creature]["attributes"]["realFleeSpeed"]
            if creatures[creature]["rotation"] in range(134,226):
                creatures[creature]["y"] += creatures[creature]["attributes"]["realFleeSpeed"]
            if creatures[creature]["rotation"] in range(44,136):
                creatures[creature]["x"] += creatures[creature]["attributes"]["realFleeSpeed"]
            if creatures[creature]["rotation"] in range(224,316):
                creatures[creature]["x"] -= creatures[creature]["attributes"]["realFleeSpeed"]
            creatures[creature]["energy"] -= ceil(creatures[creature]["attributes"]["fleeSpeed"]/3)
            #Bewegung nach Rotation und Geschwindigkeit
            #FleeStateReal
        elif creatures[creature]["attributes"]["fleeState"] == 2 and world[0][int(creatures[creature]["x"])][int(creatures[creature]["y"])]:
            if randint(0,100) < 5:
                if bool(randint(0,1)):
                    creatures[creature]["rotation"] += 45 #Zufällige Rotation
                else:
                    creatures[creature]["rotation"] -= 45
                if creatures[creature]["rotation"] < 0:
                    creatures[creature]["rotation"] = 0
            
            if creatures[creature]["rotation"] in range(0,45) or creatures[creature]["rotation"] in range(314,360):
                creatures[creature]["y"] -= creatures[creature]["attributes"]["realFleeSpeed"]
            if creatures[creature]["rotation"] in range(134,226):
                creatures[creature]["y"] += creatures[creature]["attributes"]["realFleeSpeed"]
            if creatures[creature]["rotation"] in range(44,136):
                creatures[creature]["x"] += creatures[creature]["attributes"]["realFleeSpeed"]
            if creatures[creature]["rotation"] in range(224,316):
                creatures[creature]["x"] -= creatures[creature]["attributes"]["realFleeSpeed"]
            creatures[creature]["energy"] -= ceil(creatures[creature]["attributes"]["fleeSpeed"]/2)
            #Bewegung nach Rotation und Geschwindigkeit
            #FleeStateFake
        elif creatures[creature]["energy"]-randint(-150,50) < creatures[creature]["attributes"]["eatState"]:
            if world[1][int(creatures[creature]["x"])][int(creatures[creature]["y"])] > 1:
                #Essen, wenn mindestens eine Energieeinheit im Boden verfügbar
                world[1][int(creatures[creature]["x"])][int(creatures[creature]["y"])] -= 1
                creatures[creature]["energy"] += 7 #Essen pro Energieeinheit
                if randint(0,1000) == 69:
                    creatures[creature]["energy"] += 10
                    if randint(0,1000) == 420:
                        creatures[creature]["energy"] += 100
                        print("Nice!")

            if randint(0,100) < 10:
                if bool(randint(0,1)):
                    creatures[creature]["rotation"] += 45 #Zufällige Rotation
                else:
                    creatures[creature]["rotation"] -= 45
                if creatures[creature]["rotation"] < 0:
                    creatures[creature]["rotation"] = 0
            if creatures[creature]["attributes"]["fleeState"] == 1:
                try:
                    if not world[0][creatures[creature]["x"]][creatures[creature]["y"]-1] and creatures[creature]["rotation"] == 180:
                        creatures[creature]["rotation"] += choice([-90,-45,0,45,90])
                    if not world[0][creatures[creature]["x"]][creatures[creature]["y"]+1] and creatures[creature]["rotation"] == 0:
                        creatures[creature]["rotation"] += choice([-90,-45,0,45,90])
                    if not world[0][creatures[creature]["x"]+1][creatures[creature]["y"]] and creatures[creature]["rotation"] == 90:
                        creatures[creature]["rotation"] += choice([-90,-45,0,45,90])
                    if not world[0][creatures[creature]["x"]-1][creatures[creature]["y"]] and creatures[creature]["rotation"] == 270:
                        creatures[creature]["rotation"] += choice([-90,-45,0,45,90]) #Zufällige Rotation
                except:
                    if randint(0,100) < 5:
                        if bool(randint(0,1)):
                            creatures[creature]["rotation"] += 45 #Zufällige Rotation
                        else:
                            creatures[creature]["rotation"] -= 45
                        if creatures[creature]["rotation"] < 0:
                            creatures[creature]["rotation"] = 0
            
            if creatures[creature]["rotation"] in range(0,45) or creatures[creature]["rotation"] in range(314,360):
                creatures[creature]["y"] -= creatures[creature]["attributes"]["realEatSpeed"]
            if creatures[creature]["rotation"] in range(134,226):
                creatures[creature]["y"] += creatures[creature]["attributes"]["realEatSpeed"]
            if creatures[creature]["rotation"] in range(44,136):
                creatures[creature]["x"] += creatures[creature]["attributes"]["realEatSpeed"]
            if creatures[creature]["rotation"] in range(224,316):
                creatures[creature]["x"] -= creatures[creature]["attributes"]["realEatSpeed"]
            #Bewegung nach Rotation und Geschwindigkeit

            creatures[creature]["energy"] -= ceil(creatures[creature]["attributes"]["eatSpeed"]/2)
            #EatState
        else:
            #WalkState
            if randint(0,100) < 10:
                if bool(randint(0,1)):
                    creatures[creature]["rotation"] += 45 #Zufällige Rotation
                else:
                    creatures[creature]["rotation"] -= 45
                if creatures[creature]["rotation"] < 0:
                    creatures[creature]["rotation"] = 0
            
            if creatures[creature]["attributes"]["fleeState"] == 1:
                try:
                    if not world[0][creatures[creature]["x"]][creatures[creature]["y"]-1] and creatures[creature]["rotation"] == 180:
                        creatures[creature]["rotation"] += choice([-90,-45,0,45,90])
                    if not world[0][creatures[creature]["x"]][creatures[creature]["y"]+1] and creatures[creature]["rotation"] == 0:
                        creatures[creature]["rotation"] += choice([-90,-45,0,45,90])
                    if not world[0][creatures[creature]["x"]+1][creatures[creature]["y"]] and creatures[creature]["rotation"] == 90:
                        creatures[creature]["rotation"] += choice([-90,-45,0,45,90])
                    if not world[0][creatures[creature]["x"]-1][creatures[creature]["y"]] and creatures[creature]["rotation"] == 270:
                        creatures[creature]["rotation"] += choice([-90,-45,0,45,90])
                except:
                    if randint(0,100) < 5:
                        if bool(randint(0,1)):
                            creatures[creature]["rotation"] += 45 #Zufällige Rotation
                        else:
                            creatures[creature]["rotation"] -= 45
                        if creatures[creature]["rotation"] < 0:
                            creatures[creature]["rotation"] = 0
            
            if creatures[creature]["rotation"] in range(0,45) or creatures[creature]["rotation"] in range(314,360):
                creatures[creature]["y"] -= creatures[creature]["attributes"]["realWalkSpeed"]
            if creatures[creature]["rotation"] in range(134,226):
                creatures[creature]["y"] += creatures[creature]["attributes"]["realWalkSpeed"]
            if creatures[creature]["rotation"] in range(44,136):
                creatures[creature]["x"] += creatures[creature]["attributes"]["realWalkSpeed"]
            if creatures[creature]["rotation"] in range(224,316):
                creatures[creature]["x"] -= creatures[creature]["attributes"]["realWalkSpeed"]

            creatures[creature]["energy"] -= ceil(creatures[creature]["attributes"]["walkSpeed"]/2)
            
            
            if creatures[creature]["energy"] > creatures[creature]["attributes"]["birthTreshold"] and creatures[creature]["reproduceTime"] <= 0:
                creatures[creature]["energy"] -= creatures[creature]["attributes"]["birthEnergy"]
                if bool(randint(0,1)):
                    creatures+=[createChildOf(creatures[creature])]
                    creatures[creature]["reproduceTime"] = 60
                    #print("Reproduction")
            
        if creatures[creature]["rotation"] not in range(0,316):
            creatures[creature]["rotation"] = choice([0,45,90,135,180,225,270,315])
            
        if creatures[creature]["x"]+1 > len(world[0]) or creatures[creature]["x"]-1 < 0:
            creatures[creature]["x"] = 1
            if bool(randint(0,1)):
                creatures[creature]["rotation"] += 45 #Zufällige Rotation
            else:
                creatures[creature]["rotation"] -= 45
            if creatures[creature]["rotation"] < 0:
                creatures[creature]["rotation"] = 0
        if creatures[creature]["y"]+1 > len(world[0][0]) or creatures[creature]["y"]-1 < 0:
            creatures[creature]["y"] = 1
            if bool(randint(0,1)):
                creatures[creature]["rotation"] += choice([-45,0,45])
            if creatures[creature]["rotation"] < 0:
                creatures[creature]["rotation"] = 0
        
        if not world[0][int(creatures[creature]["x"])][int(creatures[creature]["y"])]:
            creatures[creature]["energy"] -= ceil(creatures[creature]["energy"] / 100)
    creature = 0
    while creature < len(creatures):
        if creatures[creature]["energy"] < 0:
            del creatures[creature]
            creature -= 1
        creature += 1
    if maintainPopulation > len(creatures) or (randint(0,1000) == 420 and randint(0,100) == 69):
        creatures += [newCreature()]
    return [creatures,world]


def runWorldIteration(world):
                    
    #WELTITERATION
            
    for x in range(len(world[1])):
        for y in range(len(world[1][x])):
            if world[0][x][y] and x != 0 and y != 0 and world[1][x][y] < 10.1:
                world[1][x][y] += 0.2
                
    #print(time()-t)
    return world

