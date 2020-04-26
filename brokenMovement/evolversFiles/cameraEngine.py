#cameraCoords syntax: [x1 (oben links),y1,x2 (unten rechts),y2,zoomLevel]

def roundCoords(cameraCoords):
    cameraCoords[0] = round(cameraCoords[0],3)
    cameraCoords[1] = round(cameraCoords[1],3)
    cameraCoords[2] = round(cameraCoords[2],3)
    cameraCoords[3] = round(cameraCoords[3],3)
    return cameraCoords


def moveCamera(cameraCoords, move,worldSize):
    if cameraCoords[0]+move[0] <= 1 and move[0] < 0:
        cameraCoords[0] -= cameraCoords[0]%1
        cameraCoords[2] -= cameraCoords[2]%1
        while cameraCoords[0] > 1:
            cameraCoords[0] -= 1 #Wenn Kamera x-Koordinaten unter 0 gesetzt werden, werden die Koordinaten proportional angeglichen
            cameraCoords[2] -= 1
    elif cameraCoords[2]+move[0]+1 >= worldSize[0]:
        return roundCoords(cameraCoords)
    else:
        cameraCoords[0] += move[0]
        cameraCoords[2] += move[0]#Bewegen (x)

    if cameraCoords[1]+move[1] <= 1 and move[1] < 0:
        cameraCoords[1] -= cameraCoords[1]%1
        cameraCoords[3] -= cameraCoords[3]%1
        while cameraCoords[1] > 1:
            cameraCoords[1] -= 1#Wenn Kamera y-Koordinaten unter 0 gesetzt werden, werden die Koordinaten proportional angeglichen
            cameraCoords[3] -= 1
    elif cameraCoords[3]+move[1]+1 >= worldSize[1]:
        return roundCoords(cameraCoords)
    else:
        cameraCoords[1] += move[1]
        cameraCoords[3] += move[1]#Bewegen (y)
    
    return roundCoords(cameraCoords)
