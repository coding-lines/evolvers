import Creature
import os

from ast import literal_eval

class CreatureManager:
    def __init__(self, tile_limit = [0, 0], start_creatures = 50, maintain_population = 5, file_name = ""):
        if file_name != "":
            with open(os.path.join(file_name, "creatures.json"), "r") as f:
                json_repr = literal_eval(f.read())

            self.tile_limit = json_repr["tile_limit"]
            self.maintain_population = json_repr["maintain_population"]

            self.creatures = []

            for creature in json_repr["creatures"]:
                self.creatures += [Creature.Creature(new = False, json_repr = creature)]
        else:
            self.tile_limit = tile_limit
            self.maintain_population = maintain_population
            self.creatures = []

            for i in range(start_creatures):
                self.creatures += [Creature.Creature(new = True, spawn_range = min(self.tile_limit) - 1)]


    def save_to(self, path):
        creatures_json = []
        for creature in self.creatures:
            creatures_json += [creature.get_json_repr()]

        with open(os.path.join(path, "creatures.json"), "w") as f:
            f.write(str({"tile_limit": self.tile_limit, "maintain_population": self.maintain_population, "creatures": creatures_json}))

    def full_iteration(self, world, speed = 1, override_dt = 0):
        reproducing = []
        death = []
        for n_creature, creature in enumerate(self.creatures):
            world, reproduce = creature.run_iteration(world, speed = speed, override_dt = override_dt)

            if creature.energy <= 0:
                death += [n_creature]

            if reproduce:
                reproducing += [n_creature]

        new_creatures = []

        for i in reproducing:
            new_creatures += [Creature.Creature(new=False, spawn_range = min(self.tile_limit) - 1)]
            new_creatures[-1].create_mutation_of(self.creatures[i])

        death.reverse()

        for i in death:
            del self.creatures[i]

        self.creatures += new_creatures

        if len(self.creatures) < self.maintain_population:
            self.creatures += [Creature.Creature(new=True, spawn_range = self.tile_limit[0] - 1)]

        return world
