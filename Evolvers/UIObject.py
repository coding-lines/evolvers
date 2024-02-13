class UIObject:
    def __init__(self, object, coords):
        self.object = object

        self.x = coords[0]
        self.y = coords[1]

        self.width = object.get_width()
        self.height = object.get_height()

    def blit(self, screen):
        screen.blit(self.object, [self.x, self.y])
