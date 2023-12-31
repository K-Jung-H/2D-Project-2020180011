from pico2d import *
import World
import game_framework

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_SKILL_EFFECT = 10

skill_focus = [[0, 30], [33, 32], [68, 27]]


class Sword_Kirby_Sword_Strike:
    image = None
    effect = None

    def __init__(self, x, y, velocity = 1):
        if Sword_Kirby_Sword_Strike.image == None:
            Sword_Kirby_Sword_Strike.image = load_image('resource/Sword_Kirby/sword_kirby_sword_skill.png')
            Sword_Kirby_Sword_Strike.effect = load_wav('resource/sound/SK_SS.wav')
        self.x, self.y, self.velocity = x, y, velocity
        self.x_size = abs(velocity)
        self.y_size = abs(velocity)
        self.x_range, self.y_range = 0, 0
        self.frame = 0
        self.power = abs(velocity)
        self.p_dir = velocity / abs(velocity)
        self.Attacking = True
        self.charge_attack = False
        self.effect.set_volume(128)
        self.effect.play()


    def draw(self):
        frame = int(self.frame)
        p_size_x = skill_focus[frame][1] * self.x_size
        p_size_y = 28 * self.y_size
        if self.p_dir == 1:
            self.image.clip_draw(skill_focus[frame][0], 0, skill_focus[frame][1], 62, self.x, self.y, p_size_x, p_size_y)
        elif self.p_dir == -1:
            self.image.clip_composite_draw(skill_focus[frame][0], 0, skill_focus[frame][1], 62,  0, 'h',self.x, self.y,
                                           p_size_x, p_size_y)
        #draw_rectangle(*self.get_bb())



    def update(self):
        self.x += self.velocity * 100 * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_SKILL_EFFECT * ATTACK_PER_TIME * game_framework.frame_time) % 3
        self.x_size = self.power
        self.y_size = self.power
        if self.x < 25 or self.x > 1600 - 25:
            self.effect.set_volume(0)
            World.remove_object(self)


    def get_bb(self):
        x_range = self.x_size * 30 // 2
        y_range = self.y_size * 28 // 2
        return self.x - x_range, self.y - y_range, self.x + x_range, self.y + y_range


    def handle_collision(self, group, other):
        if group == 'p1_Sword_Skill : p2_Sword_Skill':
            if self.power > other.power:
                self.power -= other.power
            else:
                World.remove_object(self)
        elif group == 'p1 : p2_Sword_Skill' or group == 'p2 : p1_Sword_Skill':
            self.effect.set_volume(0)
            World.remove_object(self)

