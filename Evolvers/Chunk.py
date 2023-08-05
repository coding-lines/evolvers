import random
import time

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
        pass

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

        #TODO: fertility

        for x in range(self.size):
            for y in range(self.size):
                if self.terrain[x][y] <= 0:
                    self.food[x] += [0]
                else:
                    self.food[x] += [2 * self.terrain[x][y]]

        self.loaded = True
        self.last_iteration = time.time()

    def run_iteration(self, regrowth_factor = 1):
        for x in range(self.size):
            for y in range(self.size):
                if self.terrain[x][y] > 0:
                    self.food[x][y] += 0.5 * self.terrain[x][y] * (time.time() - self.last_iteration) * regrowth_factor
                    if self.food[x][y] > 10:
                        self.food[x][y] = 10

        self.last_iteration = time.time()
