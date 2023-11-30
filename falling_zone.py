from pico2d import *



stage3 = [None]


class Falling_area:
    def __init__(self, stage = 1):
        self.stage = stage
        self.area_num = 0

    def get_bb(self):
        if self.stage == 1:
            if self.area_num == 0:
                return 0, 0, 50, 150
            else:
                return  970, 0, 1000, 150
        if self.stage == 2:
            return 400, 0, 600, 150

        return 0, 0, 0, 0

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        if self.stage == 1:
            self.area_num = (self.area_num + 1) % 2
        else:
            self.area_num = 0

    def handle_collision(self, group, other):
        pass

