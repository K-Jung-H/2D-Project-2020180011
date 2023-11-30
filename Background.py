from pico2d import load_image


class BackGround:
    def __init__(self,x = 500, y = 300, stage = 1):
        self.x, self.y, = x, y
        self.stage = stage
        self.back1 = load_image('resource/Stage_Background.png')
        self.back2 = load_image('resource/Background_Valley.png')
        self.back3 = load_image('resource/boss_map.png')

    def draw(self):
        if self.stage == 1:
            self.back1.clip_draw(0, 100, 1000, 1000, self.x, self.y, 1000, 690)
        elif self.stage == 2:
            self.back2.clip_draw(0, 0, 736, 465, self.x, self.y , 1000, 640)
        elif self.stage == 3:
            self.back3.clip_draw(0, 0, 240, 396, self.x, self.y + 30, 1000, 660)


    def update(self):
        pass

