from pico2d import *
import World
import game_framework
import player_MetaKnight

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_SKILL_EFFECT = 10

#스킬 영역은 캐릭터를 따라다니며 적용되게 할 것, 스킬 한 사용하고 영역 만들고 지우고는 힘듦

class Attack_Area:
    def __init__(self, player):
        self.x, self.y = player.x, player.y
        self.x_range = 0
        self.y_range = 0
        self.power = 0


    def draw(self):
        draw_rectangle(*self.get_bb(),(0, 0, 255))

    def update(self, player):
        self.x, self.y = player.x, player.y
        if not Attacking:
            self.x_range, self.y_range, self.power = 0, 0, 0
        else:
            if player.state == Normal_Attack:
                self.x_range, self.y_range = 50, 50
            pass #상태에 따라서 데미지 변경


    def get_bb(self, player):
        if player.state == Normal_Attack:
            return self.x - x_range, self.y - y_range, self.x + x_range, self.y + y_range
            pass
        elif player.state == Normal_Attack:
            return self.x - x_range, self.y - y_range, self.x + x_range, self.y + y_range
            pass
        elif player.state == Normal_Attack:
            return self.x - x_range, self.y - y_range, self.x + x_range, self.y + y_range
            pass
        else:
            return 0, 0, 0, 0


    def handle_collision(self, group, other):
        pass


    # Normal_Attack:
    #
    # Speed_Attack:
    #
    # Charge_Attack:
    #
    # Upper_Attack:
    #
    # Drop_Attack:
    #
    # Falling_Attack:
    #
    # Defense: