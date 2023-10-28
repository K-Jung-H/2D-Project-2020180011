from pico2d import load_image


class Grass:
    def __init__(self,x = 400, y = 30):
        self.x, self.y, = x, y
        self.image = load_image('resource/Stage_Background.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass
