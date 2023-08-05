import Creature

class CreatureManager:
    def __init__(self, tile_limit = [0, 0]):
        self.tile_limit = tile_limit
        self.creatures = []

    def full_iteration(self, world):
        reproducing = []
        death = []
        for n_creature, creature in enumerate(self.creatures):
            world, reproduce = creature.run_iteration(world)

            if creature.energy <= 0:
                death += [n_creature]

            if reproduce:
                reproducing += [n_creature]

        new_creatures = []

        for i in reproducing:
            new_creatures += [Creature.Creature(new=False)]
            new_creatures[-1].create_mutation_of(self.creatures[i])

        death.reverse()

        for i in death:
            del self.creatures[i]

        self.creatures += new_creatures

        if len(self.creatures) < 5:
            self.creatures += [Creature.Creature(new=True)]

        return world
