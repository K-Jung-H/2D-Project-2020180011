from pico2d import load_image


class BackGround:
    def __init__(self,x = 500, y = 300):
        self.x, self.y, = x, y
        self.image = load_image('resource/Stage_Background.png')

    def draw(self):
        self.image.clip_draw(0, 100, 1000, 1000, self.x, self.y, 1000, 600)

    def update(self):
        pass
