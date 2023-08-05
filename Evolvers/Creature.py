import creatureNames
import math
import random
import GeneticNN

class CreatureProperties:
    def get_random_color():
        return [random.randint(0, 255), random.randint(0, 255), random.randint(0,255)]

    def alter_color(color):
        value_to_change = random.randint(0,2)

        color[value_to_change] += random.randint(-3, 3)

        if color[value_to_change] > 255:
            color[value_to_change] = 255
        elif color[value_to_change] < 0:
            color[value_to_change] = 0

        return color

    def get_background_color(color):
        brightness = sum(color)
        return [255, 255, 255] if brightness < 384 else [0, 0, 0]

    def get_random_name():
        return creatureNames.createNameOfLength(7)

    def alter_name(name):
        return creatureNames.alterName(name)

class Creature:
    def __init__(self, new = True):
        if not new:
            self.populated = False
        else:
            self.populated = True

            self.name = CreatureProperties.get_random_name()

            self.color = CreatureProperties.get_random_color()
            self.background_color = CreatureProperties.get_background_color(self.color)

            self.x = 0
            self.y = 0
            self.rotation = random.randint(0, 359)

            self.v_x = 0
            self.v_y = 0

            self.energy = 100

            self.generation = 0
            self.age = 0 #in seconds
            self.ancestors = []
            self.children = []
            #Ancestors and children only stored as names. For children, only store direct children

            self.last_iteration = time.time()

            self.brain_type = "neural_network" #Type of logic to execute on iteration

            ################
            #NEURAL NETWORK#
            ################
            #Inputs: Energy, Ground type, Ground food content, rotation, constant 1, memory?
            ###
            #Outputs: Rotation change, speed, eat, reproduce, memory
            ###

            self.brain_storage = GeneticNN.Network([6, 6, 5])
            self.memory = 0

    def create_mutation_of(self, other):
        self.name = CreatureProperties.alter_name(other.name)

        self.color = CreatureProperties.alter_color(other.color)
        self.background_color = CreatureProperties.get_background_color(self.color)

        self.x = other.x
        self.y = other.y
        self.rotation = random.randint(0, 359)

        self.v_x = 0
        self.v_y = 0

        self.generation = other.generation + 1
        self.age = 0
        self.ancestors = other.ancestors[:19] + [other.name]

        self.brain_type = other.brain_type[:]
        if other.brain_type == "neural_network":
            self.brain_storage = other.brain_storage.mutate()

        self.memory = 0

        self.energy = 100

    def run_iteration(self, world):
        if self.populated:
            chunk_id = str(math.floor(self.x / world.chunk_size)) + "_" + str(math.floor(self.y / world.chunk_size))

            if world.is_chunk_loaded(chunk_id):

                chunk = world.get_chunk(chunk_id)

                chunk_coords = [round(self.x % world.chunk_size), round(self.y % world.chunk_size)]

                ground_type = chunk.terrain[chunk_coords[0]][chunk_coords[1]]
                ground_is_water = 1 if ground_type == -1 else 0

                ground_food = chunk.food[chunk_coords[0]][chunk_coords[1]]

                if self.brain_type == "neural_network":
                    changes = self.brain_storage.predict([self.energy, ground_is_water, ground_food, self.rotation, 1, self.memory])

                    self.memory = changes[-1]

                else:
                    print("Could not complete creature iteration: No valid brain logic type.")

            self.rotation
