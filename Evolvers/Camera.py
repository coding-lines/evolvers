import pygame

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 1
        self.rotation = 0
        self.movement_speed = 50

    def update(self, keys_pressed, delta_time):
        if keys_pressed[pygame.K_DOWN]:
            self.y += delta_time * self.movement_speed
        if keys_pressed[pygame.K_UP]:
            self.y -= delta_time * self.movement_speed
        if keys_pressed[pygame.K_LEFT]:
            self.x -= delta_time * self.movement_speed
        if keys_pressed[pygame.K_RIGHT]:
            self.x += delta_time * self.movement_speed
