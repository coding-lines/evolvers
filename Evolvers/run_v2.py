import pygame, pygame_textinput
import time, os

from ast import literal_eval

import Camera, World, Renderer

def readfile(name):
    with open(name,"rb") as f:
        return f.read().decode("utf-8")


class const:
    WHITE = [255,255,255]
    BLACK = [0,0,0]
    LIGHT_GREY = [200,200,200]
    GREY = [100,100,100]
    DARK_GREY = [50,50,50]
    RED = [255,0,0]
    GREEN = [0,200,0]

dimensions = [1280,720]
target_fps = 60
current_screen = "simulation"
open = True

pygame.init()
screen = pygame.display.set_mode(dimensions)

icon = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
pygame.display.set_caption("Evolvers")

test_world = World.World(size_limit=[5,5], water_cover=0.7)
cam = Camera.Camera()
renderer = Renderer.Renderer(dimensions, "font/PTSans-Regular.ttf")

dt = 0
t = time.time()

while open:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            open = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4:
                cam.z += 0.1 if cam.z < 10 else 0
            elif event.button == 5:
                cam.z -= 0.1 if cam.z >= 0.2 else 0

    if pygame.key.get_pressed()[pygame.K_DOWN]:
        cam.y += dt * cam.movement_speed
    if pygame.key.get_pressed()[pygame.K_UP]:
        cam.y -= dt * cam.movement_speed
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        cam.x -= dt * cam.movement_speed
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        cam.x += dt * cam.movement_speed

    test_world.visible_only_world_iteration(renderer, cam)
    test_world.full_creature_iteration()


    screen.fill([0,0,0])
    renderer.render_world(screen, cam, test_world)
    renderer.render_creatures(screen, cam, test_world.creature_manager.creatures)

    pygame.display.flip()

    clock.tick(target_fps)

    dt = time.time() - t
    t = time.time()

pygame.quit()
