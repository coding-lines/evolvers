import math
import os
import random
import time

from ast import literal_eval

class ChunkConverters:
    def boolean_to_tile_type(tile):
        if tile:
            return 1
        else:
            return -1

    def terrain_value_to_tile_type(tile):
        if tile >= 0:
            return 1
        return tile

class Chunk:
    def __init__(self, size=12):

        self.size = size

        self.last_iteration = time.time()

        #Terrain value: -1 = Water, positive numbers = land, value indicated fertility (0 = infertile, 1 = 100% fertile)
        self.terrain = []

        #Food values: same as in Evolvers v1
        self.food = []

        self.loaded = False

    def load_from_file(self, file_name):
        with open(file_name, "r") as f:
            json_repr = literal_eval(f.read())

        self.terrain = json_repr["terrain"]
        self.food = json_repr["food"]

        self.loaded = True

    def generate(self, borders = {}, water_cover = 0.5):
        self.terrain = []
        self.food = []

        for i in range(self.size):
            self.terrain += [[]]
            self.food += [[]]

        #Calculate water / land spread
        for x in range(self.size):
            for y in range(self.size):
                #Get the nearest generated tile on the x-axis
                if x == 0 and "-x" in borders.keys():
                    last_x = ChunkConverters.terrain_value_to_tile_type(border["-x"][y])
                elif x == self.size - 1 and "+x" in borders.keys():
                    last_x = ChunkConverters.terrain_value_to_tile_type(border["+x"][y])
                elif x != 0 and x != self.size -1 and y != 0:
                    last_x = self.terrain[x][y-1]
                else:
                    #If no directly attached generated tile exists, randomize the tile
                    last_x = ChunkConverters.boolean_to_tile_type(random.random() > water_cover)

                #Get the nearest generated tile on the y-axis
                if y == 0 and "-y" in borders.keys():
                    last_y = ChunkConverters.terrain_value_to_tile_type(border["-y"][y])
                elif y == self.size - 1 and "+y" in borders.keys():
                    last_y = ChunkConverters.terrain_value_to_tile_type(border["+y"][y])
                elif y != 0 and y != self.size -1 and x != 0:
                    last_y = self.terrain[x-1][y]
                else:
                    #If no directly attached generated tile exists, randomize the tile
                    last_y = ChunkConverters.boolean_to_tile_type(random.random() > water_cover)

                random_tile = ChunkConverters.boolean_to_tile_type(random.random() > water_cover)

                self.terrain[x] += [random.choice([last_x, last_y, random_tile])]

        #Basic world smoothing (needs rework for chunk border cases)
        for smoothing_step in range(3):
            for x in range(self.size):
                for y in range(self.size):
                    neighbor_terrain = []

                    for x_neighbor in range(x-1, x+2):
                        for y_neighbor in range(y-1, y+2):
                            if x == x_neighbor and y == y_neighbor:
                                continue

                            if x_neighbor >= len(self.terrain) or y_neighbor >= len(self.terrain):
                                continue

                            if x_neighbor < 0 or y_neighbor < 0:
                                continue

                            neighbor_terrain += [self.terrain[x_neighbor][y_neighbor]]

                    if neighbor_terrain.count(self.terrain[x][y]) < math.floor(len(neighbor_terrain) / 2):
                        if self.terrain[x][y] == -1:
                            self.terrain[x][y] = 1
                        else:
                            self.terrain[x][y] = -1

        #TODO: fertility

        for x in range(self.size):
            for y in range(self.size):
                if self.terrain[x][y] <= 0:
                    self.food[x] += [0]
                else:
                    self.food[x] += [5 * self.terrain[x][y] * random.random()]

        self.loaded = True
        self.last_iteration = time.time()

    def run_iteration(self, regrowth_factor = 1, speed = 1):
        for x in range(self.size):
            for y in range(self.size):
                if self.terrain[x][y] > 0:
                    self.food[x][y] += 0.25 * self.terrain[x][y] * (time.time() - self.last_iteration) * regrowth_factor * speed
                    if self.food[x][y] > 10:
                        self.food[x][y] = 10

        self.last_iteration = time.time()

    def compress(self, food_map):
        for x in range(len(food_map)):
            for y in range(len(food_map[0])):
                food_map[x][y] = round(food_map[x][y], 2)

        return food_map

    def save_to(self, path, key):

        chunk_data = {
        "terrain": self.terrain,
        "food": self.compress(self.food)
        }

        with open(os.path.join(path, key + ".json"), "w") as f:
            f.write(str(chunk_data))
