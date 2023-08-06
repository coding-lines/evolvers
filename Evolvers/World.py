import Chunk
import CreatureManager
import os
import time

from ast import literal_eval

class World:
    def __init__(self, size_limit=[0, 0], chunk_size = 12, regrowth_factor = 1, fertility_range_factor = 1, water_cover = 0.5, start_creatures = 50, maintain_population = 5, file_name = ""):

        if file_name != "":
            with open(os.path.join(file_name, "world.json"), "r") as f:
                json_repr = literal_eval(f.read())

            self.size_limit = json_repr["size_limit"]

            self.chunk_size = json_repr["chunk_size"]

            self.tile_limit = [self.chunk_size * self.size_limit[0], self.chunk_size * self.size_limit[1]]

            self.regrowth_factor = json_repr["regrowth_factor"]
            self.fertility_range_factor = json_repr["fertility_range_factor"]
            self.water_cover = json_repr["water_cover"]

            self.generated_chunks = json_repr["generated_chunks"]

            self.chunks = {}

            for chunk in self.generated_chunks:
                self.chunks[chunk] = Chunk.Chunk(size = self.chunk_size)
                self.chunks[chunk].load_from_file(os.path.join(file_name, chunk + ".json"))

            self.creature_manager = CreatureManager.CreatureManager(self.tile_limit, file_name = file_name)

        else:
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


    def full_creature_iteration(self, speed = 1, override_dt = 0):
        self = self.creature_manager.full_iteration(self, speed = speed, override_dt = override_dt)

    def save_world_to(self, path):
        metadata = {
        "size_limit": self.size_limit,
        "chunk_size": self.chunk_size,
        "regrowth_factor": self.regrowth_factor,
        "fertility_range_factor": self.fertility_range_factor,
        "water_cover": self.water_cover,
        "generated_chunks": self.generated_chunks
        }
        with open(os.path.join(path, "world.json"), "w") as f:
            f.write(str(metadata))

        for chunk_key in self.chunks.keys():
            self.chunks[chunk_key].save_to(path, chunk_key)

        self.creature_manager.save_to(path)
