import creatureNames
import math
import random
import time
import GeneticNN

class CreatureProperties:
    def get_random_color():
        return [random.randint(0, 255), random.randint(0, 255), random.randint(0,255)]

    def alter_color(color):
        value_to_change = random.randint(0,2)

        color[value_to_change] += random.choice([-20, -10, -1, 1, 10, 20])

        if color[value_to_change] > 255:
            color[value_to_change] = int(random.random() * 50) + 200
        elif color[value_to_change] < 0:
            color[value_to_change] = int(random.random() * 50)

        return color

    def get_background_color(color):
        brightness = sum(color)
        return [255, 255, 255] if brightness < 384 else [0, 0, 0]

    def get_random_name():
        return creatureNames.createNameOfLength(7)

    def alter_name(name):
        change_type = random.random()
        if change_type < 0.2:
            if len(name) > 3 and random.random() < 0.5:
                return name[:-1] #Cut off one letter
            elif len(name) < 9:
                return creatureNames.continueName(name)
        return creatureNames.alterName(name)

class Creature:
    def __init__(self, new = True, spawn_range=20, json_repr = ""):
        if not new:
            if json_repr != "":
                self.populated = json_repr["populated"]

                self.name = json_repr["name"]

                self.color = json_repr["color"]
                self.background_color = CreatureProperties.get_background_color(self.color)

                self.x = json_repr["x"]
                self.y = json_repr["y"]
                self.rotation = json_repr["rotation"]

                self.v_x = 0
                self.v_y = 0

                self.energy = json_repr["energy"]

                self.generation = json_repr["generation"]
                self.age = json_repr["age"]
                self.ancestors = json_repr["ancestors"]
                self.children = json_repr["children"]

                self.last_iteration = time.time()

                self.brain_type = json_repr["brain_type"]

                if self.brain_type == "neural_network":
                    self.brain_storage = GeneticNN.Network(json_repr = json_repr["brain_storage"])

                self.memory = json_repr["memory"]

            else:
                self.populated = False
        else:
            self.populated = True

            self.name = CreatureProperties.get_random_name()

            self.color = CreatureProperties.get_random_color()
            self.background_color = CreatureProperties.get_background_color(self.color)

            spawn_range = spawn_range if spawn_range > 0 else 100

            self.x = random.randint(0, spawn_range)
            self.y = random.randint(0, spawn_range)
            self.rotation = random.random()

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
            #Inputs: Energy, Ground type, Ground food content, rotation, constant 1, memory?, -x border, +x border, -y border, +y border
            ###
            #Outputs: Rotation change, speed, eat, reproduce, memory
            ###

            self.brain_storage = GeneticNN.Network([10, 5])
            self.memory = 0

    def create_mutation_of(self, other):
        self.populated = True
        self.name = CreatureProperties.alter_name(other.name)

        self.color = CreatureProperties.alter_color(other.color.copy())
        self.background_color = CreatureProperties.get_background_color(self.color)

        self.x = other.x
        self.y = other.y
        self.rotation = random.random()

        self.v_x = 0
        self.v_y = 0

        self.generation = other.generation + 1
        self.age = 0
        self.ancestors = other.ancestors[:19] + [other.name]
        self.children = []

        self.last_iteration = time.time()

        self.brain_type = other.brain_type[:]
        if other.brain_type == "neural_network":
            self.brain_storage = other.brain_storage.mutate()

        self.memory = 0

        self.energy = 100

        other.children = other.children[:19] + [self.name]
        return other

    def get_json_repr(self):
        brain_json = {}
        if self.brain_type == "neural_network":
            brain_json = self.brain_storage.get_json_repr()

        return {
        "populated": self.populated,
        "name": self.name,
        "color": self.color,
        "x": self.x,
        "y": self.y,
        "rotation": self.rotation,
        "energy": self.energy,
        "generation": self.generation,
        "age": self.age,
        "ancestors": self.ancestors,
        "children": self.children,
        "brain_type": self.brain_type,
        "brain_storage": brain_json,
        "memory": self.memory
        }

    def run_iteration(self, world, speed = 1, override_dt = 0):
        reproduce = False
        if override_dt != 0:
            delta_time = override_dt
        else:
            delta_time = speed * (time.time() - self.last_iteration)
        if self.populated:
            self.age += delta_time

            chunk_id = str(math.floor(self.x / world.chunk_size)) + "_" + str(math.floor(self.y / world.chunk_size))

            if world.is_chunk_loaded(chunk_id):

                chunk = world.get_chunk(chunk_id)

                chunk_coords = [math.floor(self.x % world.chunk_size), math.floor(self.y % world.chunk_size)]

                ground_type = chunk.terrain[chunk_coords[0]][chunk_coords[1]]
                ground_is_water = 1 if ground_type == -1 else 0

                ground_food = chunk.food[chunk_coords[0]][chunk_coords[1]]

                if self.brain_type == "neural_network":

                    borderless_world = world.size_limit == [0, 0]

                    brain_inputs = [
                    self.energy / 100,
                    ground_is_water,
                    ground_food,
                    self.rotation,
                    int(math.floor(self.x - 2) < 0) if not borderless_world else 0,
                    int(math.ceil(self.x + 2) >= world.size_limit[0] * world.chunk_size) if not borderless_world else 0,
                    int(math.floor(self.y - 2) < 0) if not borderless_world else 0,
                    int(math.ceil(self.y + 2) >= world.size_limit[1] * world.chunk_size) if not borderless_world else 0,
                    self.memory,
                    1
                    ]

                    changes = self.brain_storage.predict(brain_inputs)

                    #Limit memory
                    if changes[4] > 255:
                        changes[4] = 255
                    elif changes[4] < -255:
                        changes[4] = -255

                    self.memory = changes[4]

                else:
                    print("Could not complete creature iteration: No valid brain logic type.")

                #Rotation change
                self.rotation += changes[0] * delta_time
                if self.rotation > 1 or self.rotation < 0:
                    self.rotation = self.rotation % 1

                #Speed change
                #Limit maximum speed
                if changes[1] > 5:
                    changes[1] = 5
                elif changes[1] < 0:
                    changes[1] = 0


                self.energy -= 0.25 * delta_time #Preventing creatures from doing nothing

                if ground_is_water:
                    self.energy -= 10 * delta_time #Water hurts the creature

                self.energy -= changes[1] * delta_time

                #Eating
                if changes[2] > 0.5:
                    self.energy -= delta_time #Discourage constant eating

                    if ground_is_water:
                        self.energy -= 15 * delta_time #Trying to eat water hurts the creature
                    else:
                        self.energy += min(10 * delta_time, ground_food)
                        world.chunks[chunk_id].food[chunk_coords[0]][chunk_coords[1]] -= min(10 * delta_time, ground_food)

                #Reproduction
                if changes[3] > 0.5:
                    if self.energy >= 200:
                        self.energy -= 100
                        reproduce = True


                #PHYSICS
                rotation_rad = self.rotation * 2 * math.pi

                acceleration_x = math.cos(rotation_rad)
                acceleration_y = math.sin(rotation_rad)

                vector_length = math.sqrt((acceleration_x ** 2) + (acceleration_y ** 2))

                acceleration_x /= vector_length
                acceleration_y /= vector_length

                acceleration_x *= changes[1]
                acceleration_y *= changes[1]

                if delta_time < 1:
                    self.v_x = (1 - delta_time) * self.v_x + acceleration_x * delta_time
                    self.v_y = (1 - delta_time) * self.v_y + acceleration_y * delta_time

                else:
                    self.v_x = acceleration_x
                    self.v_y = acceleration_y

                self.x += acceleration_x * delta_time
                self.y += acceleration_y * delta_time

                #'laziness' penalty
                if abs(self.v_x) + abs(self.v_y) < 0.2:
                    self.energy -= 50 * (0.2 - (abs(self.v_x) + abs(self.v_y))) * delta_time

                #Limit movement across world borders and penalize it
                if world.size_limit != [0, 0]:
                    if self.x < 0:
                        self.x = 1
                        self.energy -= 5
                    elif self.x > world.size_limit[0] * world.chunk_size:
                        self.x = world.size_limit[0] * world.chunk_size - 1
                        self.energy -= 5

                    if self.y < 0:
                        self.y = 1
                        self.energy -= 5
                    elif self.y > world.size_limit[1] * world.chunk_size:
                        self.y = world.size_limit[1] * world.chunk_size - 1
                        self.energy -= 5

                #Force reproduction when creature is hoarding energy
                if self.energy > 1000 and not reproduce:
                    reproduce = True
                    self.energy -= 100

        self.last_iteration = time.time()
        return world, reproduce
