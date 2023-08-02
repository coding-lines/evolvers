from PIL import Image,ImageDraw,ImageFont
import creatureEngine,os

class options:
    useGame = "load" #new/load
    worldSize = [192,108]
    worldGenerator = "new"
    startCreatures = 50
    playBackSpeed = 1

    scaling = 10 #Größe eines Blocks in Pixeln
    frames = 1

class storage:
    if options.useGame == "new":
        creatures = creatureEngine.initCreatures(options.startCreatures,options.worldSize)
        world = creatureEngine.initWorld(options.worldSize[0],options.worldSize[1], options.worldGenerator,8)
    font = ImageFont.truetype("font/PTSans-Regular.ttf",16)


def render_frame(world,creatures,scaling=10):
    storage.world = world
    storage.creatures = creatures
    options.scaling = scaling
    options.worldSize = [len(world[0]),len(world[0][0])]
    runRenderer()

def runRenderer():
    for frameNumber in range(options.frames):
        print("Render wird angefertigt...")
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
        filename = 0
        while os.path.isfile("renders/"+str(filename)+".png"):
            filename += 1
        im.save("renders/"+str(filename)+".png")
