import os
from PIL import Image,ImageDraw,ImageFont
import creatureEngine

class options:
    useGame = "new" #new/load
    worldSize = [192,108]
    worldGenerator = "new"
    startCreatures = 50
    gameFiles = "notFinished"
    playBackSpeed = 4

    scaling = 10 #Größe eines Blocks in Pixeln
    frames = 900

class storage:
    if options.useGame == "new":
        creatures = creatureEngine.initCreatures(options.startCreatures,options.worldSize)
        world = creatureEngine.initWorld(options.worldSize[0],options.worldSize[1], options.worldGenerator,8)
        font = ImageFont.truetype("font.ttf",16)

#os.chdir("renders")

for frameNumber in range(options.frames):
    print("Rendere Frame",frameNumber+1)
    for i in range(options.playBackSpeed):
        storage.creatures,storage.world = creatureEngine.runIteration(storage.creatures,storage.world)
    if not bool(frameNumber % (60//options.playBackSpeed)):
        storage.world = creatureEngine.runWorldIteration(storage.world)
    im = Image.new("RGB",(options.worldSize[0]*options.scaling, options.worldSize[1]*options.scaling))
    draw = ImageDraw.Draw(im)
    for x in range(options.worldSize[0]):
        for y in range(options.worldSize[1]):
            if storage.world[0][x][y]:
                blue = 0
                green = int(storage.world[1][x][y] / 12 *100) + 50
                red = 50
            else:
                blue = 150
                green = 100
                red = 0
            p1 = [x*options.scaling,y*options.scaling]
            draw.rectangle([p1[0],p1[1],p1[0]+options.scaling,p1[1]+options.scaling],fill=(red,green,blue),outline=(0,0,0))

    for c in range(len(storage.creatures)):
                    pos = [storage.creatures[c]["x"]*options.scaling,storage.creatures[c]["y"]*options.scaling]
                    size = int((storage.creatures[c]["energy"]/8+88)/5)
                    draw.ellipse([pos[0],pos[1],pos[0]+size,pos[1]+size],fill=tuple(storage.creatures[c]["color"]),outline=tuple(storage.creatures[c]["boundaries"]))
                    draw.text((pos[0]-5,pos[1]+size), storage.creatures[c]["name"], font=storage.font, fill=(255,255,255))
    im.save("renders/"+str(frameNumber)+".png")

#os.system("ffmpeg -y -r 30 -i renders/%01d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p renders/evolversVideo.mp4")
#os.system("rm renders/*.png")



