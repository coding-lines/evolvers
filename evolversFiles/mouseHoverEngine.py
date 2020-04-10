def assignClick(mousePos,sidebarOpen,cameraPos,scale):
    if not sidebarOpen or mousePos[0] < 1000:
        return [(mousePos[0] // scale) + cameraPos[0], (mousePos[1] // scale)+cameraPos[1]]
