from pico2d import *
import World
import game_framework

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_SKILL_EFFECT = 10


class Meta_Knight_Sword_Strike:
    image = None
    effect = None

    def __init__(self, x, y, velocity = 1):
        if Meta_Knight_Sword_Strike.image == None:
            Meta_Knight_Sword_Strike.image = load_image('resource/Meta_Knight_Skill.png')
            Meta_Knight_Sword_Strike.effect = load_wav('resource/sound/Meta_SS.wav')
        self.x, self.y, self.velocity = x, y, velocity
        self.x_size = abs(velocity) * 25
        self.y_size = abs(velocity) * 25
        self.frame = 0
        self.power = abs(velocity)
        self.p_dir = velocity / abs(velocity)
        self.Attacking = True
        self.charge_attack = False
        self.effect.set_volume(128)
        self.effect.play()


    def draw(self):
        self.image.clip_draw(int(self.frame) * 49, 0, 49, 49, self.x, self.y, self.x_size, self.y_size)
        #draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.velocity * 100 * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_SKILL_EFFECT * ATTACK_PER_TIME * game_framework.frame_time) % 5
        self.x_size = self.power * 25
        self.y_size = self.power * 25
        if self.x < 25 or self.x > 1600 - 25:
            self.effect.set_volume(0)
            World.remove_object(self)


    def get_bb(self):
        return self.x - self.x_size // 2, self.y - self.y_size // 2, self.x + self.x_size // 2, self.y + self.y_size // 2


    def handle_collision(self, group, other):
        if group == 'p1_Sword_Skill : p2_Sword_Skill':
            if self.power > other.power:
                self.power -= other.power
            else:
                World.remove_object(self)
        elif group == 'p1 : p2_Sword_Skill' or group == 'p2 : p1_Sword_Skill':
            self.effect.set_volume(0)
            World.remove_object(self)