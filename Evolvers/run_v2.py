import pygame, pygame_textinput
import time, os

from ast import literal_eval

import Camera, World, SimulationRenderer, UIRenderer

def readfile(name):
    with open(name,"rb") as f:
        return f.read().decode("utf-8")

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

test_world = World.World(size_limit=[10, 10], water_cover=0.4, start_creatures=200, maintain_population=30)
#test_world = World.World(file_name = "save/world_test")
cam = Camera.Camera()
renderer = SimulationRenderer.Renderer(dimensions, "font/PTSans-Regular.ttf")
ui_renderer = UIRenderer.UIRenderer(dimensions, "font/PTSans-Regular.ttf")

dt = 0
global_speed = 1
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
            elif current_screen == "simulation":
                pos = list(pygame.mouse.get_pos())
                renderer.get_clicked(pos, cam, test_world.creature_manager.creatures)

        elif event.type == pygame.KEYDOWN:
            if current_screen == "simulation":
                if event.key == pygame.K_p:
                    global_speed += 1 if global_speed < 50 else 0
                elif event.key == pygame.K_o:
                    global_speed -= 1 if global_speed > 1 else 0
                elif event.key == pygame.K_F12:
                    if not os.path.exists("save/world_test"):
                        if not os.path.exists("save"):
                            os.mkdir("save")
                        os.mkdir("save/world_test")
                    test_world.save_world_to("save/world_test")
                elif event.key == pygame.K_F11:
                    if os.path.exists("save/world_test"):
                        test_world = World.World(file_name = "save/world_test")
                elif event.key == pygame.K_ESCAPE:
                    if renderer.clicked_creature:
                        renderer.clicked_creature = False
                        test_world.creature_manager.deselect_all()
                    else:
                        current_screen = "escape_menu"

            elif current_screen == "escape_menu":
                if event.key == pygame.K_ESCAPE:
                    current_screen = "simulation"

    if current_screen == "simulation":
        cam.update(pygame.key.get_pressed(), dt)

        test_world.full_world_iteration(override_dt = dt if global_speed == 1 else global_speed * (1 / target_fps))
        #test_world.visible_only_world_iteration(renderer, cam, global_speed)
        #sped up iterations while converving accuracy
        for i in range(global_speed):
            test_world.full_creature_iteration(override_dt = dt if global_speed == 1 else 1 / target_fps)

        renderer.render_world(screen, cam, test_world, water_background=True)
        renderer.render_creatures(screen, cam, test_world.creature_manager.creatures)

    else:
        ui_renderer.render_menu(screen)

    pygame.display.flip()

    clock.tick(target_fps)

    dt = time.time() - t
    t = time.time()

pygame.quit()
