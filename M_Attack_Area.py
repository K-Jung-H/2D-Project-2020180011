from pico2d import *
import World
import game_framework
import player_MetaKnight

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_SKILL_EFFECT = 10

#스킬 영역은 캐릭터를 따라다니며 적용되게 할 것, 스킬 한 사용하고 영역 만들고 지우고는 힘듦




class Meta_Attack_Area:
    def __init__(self, player):
        self.x, self.y = player.x, player.y
        self.p = player
        self.player_cur_state = None
        self.p_dir = player.dir
        self.x_range = 0
        self.y_range = 0
        self.power = 0


    def draw(self):
        draw_rectangle(*self.get_bb())



    def update(self, state_machine_cur_state, player_dir, player_power):
        self.x, self.y = self.p.x, self.p.y
        self.player_cur_state = state_machine_cur_state
        self.p_dir = player_dir
        if not self.p.Attacking:
            self.x_range, self.y_range, self.power = 0, 0, 0

        else:
            if self.player_cur_state == player_MetaKnight.Normal_Attack:
                self.x_range, self.y_range = 50, 50
                self.power = 2
            elif self.player_cur_state == player_MetaKnight.Speed_Attack:
                self.x_range, self.y_range = 50, 50
                self.power = 1
            elif self.player_cur_state == player_MetaKnight.Charge_Attack:
                self.x_range, self.y_range = 50, 50
                self.power = player_power
            elif self.player_cur_state == player_MetaKnight.Upper_Attack:
                self.x_range, self.y_range = 40, 60
                self.power = 2
            elif self.player_cur_state == player_MetaKnight.Drop_Attack:
                self.x_range, self.y_range = 40, 60
                self.power = 2
            elif self.player_cur_state == player_MetaKnight.Falling_Attack:
                self.x_range, self.y_range = 50, 50
                self.power = 3

            pass #상태에 따라서 데미지 변경


    def get_bb(self):
        p_L = self.x - self.x_range
        p_B = self.y - self.y_range
        p_R = self.x + self.x_range
        p_T = self.y + self.y_range

        if self.player_cur_state == player_MetaKnight.Normal_Attack:
            return p_L + self.p_dir * 50, p_B, p_R + self.p_dir * 50, p_T

        elif self.player_cur_state == player_MetaKnight.Speed_Attack:
            return p_L + self.p_dir * 50, p_B - 10, p_R + 50 * self.p_dir, p_T - 10

        elif self.player_cur_state == player_MetaKnight.Charge_Attack:
            return p_L + self.p_dir * 50, p_B, p_R + self.p_dir * 50, p_T

        elif self.player_cur_state == player_MetaKnight.Upper_Attack:
            return p_L, p_B + 30, p_R, p_T + 10

        elif self.player_cur_state == player_MetaKnight.Drop_Attack:
            return p_L, p_B - 30, p_R, p_T - 80

        elif self.player_cur_state == player_MetaKnight.Falling_Attack:
            return p_L - self.p_dir * 10, p_B - 5, p_R - self.p_dir * 10, p_T - 5
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