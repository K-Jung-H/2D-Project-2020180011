from pico2d import *
import game_world
import game_framework


class Meta_Knight_Sword_Strike:
    image = None

    def __init__(self, x, y, velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('resource/Meta_Knight_Skill.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.clip_draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.velocity * 100 * game_framework.frame_time

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)


    def get_bb(self, state):
        if state == Normal_Attack:
            pass
        elif state == Speed_Attack:
            pass
        elif state == Charge_Attack:
            pass
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10


    def handle_collision(self, group, other):
        game_world.remove_object(self)
        pass