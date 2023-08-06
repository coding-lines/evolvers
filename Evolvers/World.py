import Chunk
import CreatureManager
import time

class World:
    def __init__(self, size_limit=[0, 0], chunk_size = 12, regrowth_factor = 1, fertility_range_factor = 1, water_cover = 0.5, start_creatures=50, maintain_population=5):

        #[0, 0] = unlimited
        self.size_limit = size_limit

        self.chunk_size = chunk_size

        self.tile_limit = [chunk_size * size_limit[0], chunk_size * size_limit[1]]

        #List of ALL generated chunk keys
        self.generated_chunks = []

        #Loaded Chunk objects (key = x_y)
        self.chunks = {}

        #Food regrowth rate (0 = food does not regrow, 1 = normal growth rate, 2 = 2x growth, ...)
        self.regrowth_factor = regrowth_factor

        #Radius around water where the ground is fertile (-1 = ground is always fertile, 0 = no fertile ground, 1 = standard range, 2 = 2x range, ...)
        self.fertility_range_factor = fertility_range_factor

        #Percentage of water in the world (-1 = automatic (random), 0 = no water, 1 = only water)
        self.water_cover = water_cover

        self.creature_manager = CreatureManager.CreatureManager(self.tile_limit, start_creatures, maintain_population)

    def is_chunk_loaded(self, chunk):
        if chunk not in self.generated_chunks:
            return False

        if not chunk in self.chunks.keys():
            return False

        return self.chunks[chunk].loaded

    def chunk_exists(self, chunk):
        return chunk in self.generated_chunks

    def chunk_in_bounds(self, chunk):
        if self.size_limit == [0, 0]:
            return True

        chunk = chunk.split("_")
        chunk = [int(chunk[0]), int(chunk[1])]

        #Negative chunks are only valid for infinite worlds
        if chunk[0] < 0 or chunk[1] < 0:
            return False

        in_x_bounds = chunk[0] < self.size_limit[0]
        in_y_bounds = chunk[1] < self.size_limit[1]

        return (in_x_bounds and in_y_bounds)

    def get_chunk(self, chunk):
        if not self.chunk_in_bounds(chunk):
            raise IndexError("Referenced chunk outside of world border")

        if self.chunk_exists(chunk):
            if not self.is_chunk_loaded(chunk):
                pass

        else:
            self.chunks[chunk] = Chunk.Chunk(size = self.chunk_size)
            self.generated_chunks += [chunk]
            self.chunks[chunk].generate(water_cover = self.water_cover)

        return self.chunks[chunk]

    def full_world_iteration(self, speed = 1):
        for chunk in self.chunks.keys():
            self.chunks[chunk].run_iteration(regrowth_factor = self.regrowth_factor, speed = speed)

    def visible_only_world_iteration(self, renderer, camera, speed = 1):
        visible = renderer.get_chunks_in_view(camera, self)

        count = 0

        for chunk in visible:
            if self.is_chunk_loaded(chunk):
                self.chunks[chunk].run_iteration(regrowth_factor = self.regrowth_factor, speed = speed)
                count += 1


    def full_creature_iteration(self, speed = 1):
        self = self.creature_manager.full_iteration(self, speed = speed)
