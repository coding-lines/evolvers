import Creature

class CreatureManager:
    def __init__(self, tile_limit = [0, 0], start_creatures = 50, maintain_population = 5):
        self.tile_limit = tile_limit
        self.maintain_population = maintain_population
        self.creatures = []

        for i in range(start_creatures):
            self.creatures += [Creature.Creature(new = True, spawn_range = min(self.tile_limit) - 1)]


    def full_iteration(self, world, speed = 1):
        reproducing = []
        death = []
        for n_creature, creature in enumerate(self.creatures):
            world, reproduce = creature.run_iteration(world, speed = speed)

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
