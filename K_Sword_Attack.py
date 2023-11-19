from pico2d import *
import World
import game_framework

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_SKILL_EFFECT = 10


class Master_Kirby_Sword_Strike:
    image = None

    def __init__(self, x, y, velocity = 1):
        if Master_Kirby_Sword_Strike.image == None:
            Master_Kirby_Sword_Strike.image = load_image('resource/Master_Kirby_Skill.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.x_size = abs(velocity) * 25 # 이미지 프래임 크기 50, 70 으로 되어 있음
        self.y_size = abs(velocity) * 25
        self.frame = 0
        self.Attacking = True


    def draw(self):
        self.image.clip_draw(int(self.frame) * 50, 0, 50, 70, self.x, self.y, self.x_size, self.y_size)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.velocity * 100 * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_SKILL_EFFECT * ATTACK_PER_TIME * game_framework.frame_time) % 5

        if self.x < 25 or self.x > 1600 - 25:
            World.remove_object(self)


    def get_bb(self):
        x_range = self.x_size//2
        y_range = self.y_size//2
        return self.x - x_range, self.y - y_range, self.x + x_range, self.y + y_range


    def handle_collision(self, group, other):
        World.remove_object(self)
        pass