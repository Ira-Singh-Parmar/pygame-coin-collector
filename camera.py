class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.width = width
        self.height = height

    def update(self, target_rect):
        #Center camera on player
        self.offset_x = target_rect.centerx - self.width // 2