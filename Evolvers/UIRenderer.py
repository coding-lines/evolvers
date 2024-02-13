class UIRenderer:
    def __init__(self, dimensions, font):
        self.width = dimensions[0]
        self.height = dimensions[1]

        self.font = font

    def is_on_ui_object(self, obj, pos):
        x_collision = pos[0] > obj.x and pos[0] < obj.x + obj.width
        y_collision = pos[1] > obj.y and pos[1] < obj.y + obj.height
        return x_collision and y_collision

    def render_menu(self, screen):
        screen.fill([0,0,0])
