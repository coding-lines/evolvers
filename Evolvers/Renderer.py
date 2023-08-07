import pygame
import math
import time
import random

class Renderer:
    def __init__(self, dimensions, font, pixels_per_tile = 40):
        self.scaling = pixels_per_tile
        self.width = dimensions[0]
        self.height = dimensions[1]

        self.font = font

        self.water_color = [0, 100, 150]
        self.infertile = [100, 100, 100]
        self.ungrown = [50, 50, 0]
        self.grown = [50, 200, 0]

    def mix_color(self, color1, color2, factor = 0.5):
        r = color1[0] * factor +  color2[0] * (1 - factor)
        g = color1[1] * factor +  color2[1] * (1 - factor)
        b = color1[2] * factor +  color2[2] * (1 - factor)

        return [r, g, b]

    def get_chunks_in_view(self, camera, world):
        tiles_x = math.ceil(self.width / (camera.z * self.scaling * world.chunk_size)) + 1
        tiles_y = math.ceil(self.height / (camera.z * self.scaling * world.chunk_size)) + 1

        chunks_x = list(range(math.floor(camera.x / world.chunk_size), math.ceil(camera.x / world.chunk_size + tiles_x)))
        chunks_y = list(range(math.floor(camera.y / world.chunk_size), math.ceil(camera.y / world.chunk_size + tiles_y)))

        chunks_in_view = []
        for cx in chunks_x:
            for cy in chunks_y:
                chunks_in_view += [str(cx) + "_" + str(cy)]

        return chunks_in_view

    def render_world(self, screen, camera, world, water_background=True):
        if water_background:
            screen.fill(self.water_color)

        chunks_in_view = self.get_chunks_in_view(camera, world)

        tile_size = self.scaling * camera.z
        chunk_pixel_size = tile_size * world.chunk_size

        for chunk_id in chunks_in_view:
            if world.chunk_in_bounds(chunk_id):
                chunk = world.get_chunk(chunk_id)
                chunk_coords = chunk_id.split("_")
                chunk_coords = [int(chunk_coords[0]), int(chunk_coords[1])]

                for x in range(chunk.size):
                    for y in range(chunk.size):
                        if chunk.terrain[x][y] == -1 and water_background:
                            continue

                        draw_x = (chunk_coords[0]) * chunk_pixel_size - camera.x * tile_size + x * tile_size
                        draw_y = (chunk_coords[1]) * chunk_pixel_size - camera.y * tile_size + y * tile_size

                        #If tile is visible
                        if draw_x + tile_size > 0 and draw_x < self.width and draw_y + tile_size > 0 and draw_y < self.height:
                            color = self.water_color if chunk.terrain[x][y] == -1 else self.mix_color(self.mix_color(self.grown, self.ungrown, chunk.food[x][y] / 10), self.infertile, chunk.terrain[x][y])

                            pygame.draw.rect(screen, color, [draw_x, draw_y, tile_size, tile_size])

        for n in range(math.ceil(self.height / tile_size)):
            pygame.draw.line(screen, [0, 0, 0], [0, (-camera.y % 1) * tile_size + n * tile_size], [self.width, (-camera.y % 1) * tile_size + n * tile_size])

        for n in range(math.ceil(self.width / tile_size)):
            pygame.draw.line(screen, [0, 0, 0], [(-camera.x % 1) * tile_size + n * tile_size, 0], [(-camera.x % 1) * tile_size + n * tile_size, self.height])

    def render_creatures(self, screen, camera, creatures):

        font = pygame.font.Font(self.font, round(camera.z * 40))

        for creature in creatures:
            size = round(((creature.energy + 50) * camera.z * self.scaling) // 250)
            pos = [round((creature.x - camera.x) * self.scaling * camera.z), round((creature.y - camera.y) * self.scaling * camera.z)]

            if pos[0] - size < self.width and pos[0] + size > 0 and pos[1] - size < self.height and pos[1] + size > 0:

                pygame.draw.circle(screen, creature.background_color, pos, size + 2)
                pygame.draw.circle(screen, creature.color, pos, size)

                name_label = font.render(creature.name, True, [255, 255, 255])
                screen.blit(name_label, [pos[0] - (name_label.get_width() // 2), pos[1] + size])
