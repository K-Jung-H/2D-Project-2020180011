from pico2d import *
import World
import game_framework
import player_Kirby

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_SKILL_EFFECT = 10





class Kirby_Attack_Area:
    def __init__(self, player):
        self.x, self.y = player.x, player.y
        self.p = player
        self.player_cur_state = None
        self.p_dir = player.dir
        self.x_range = 0
        self.y_range = 0
        self.power = 0
        self.Attacking = False


    def draw(self):
        draw_rectangle(*self.get_bb())



    def update(self, state_machine_cur_state):
        self.x, self.y = self.p.x, self.p.y
        self.player_cur_state = state_machine_cur_state
        self.p_dir = self.p.dir
        self.Attacking = self.p.Attacking

        if not self.p.Attacking:
            self.x_range, self.y_range, self.power = 0, 0, 0

        else: # 공격 상태일 때
            if self.player_cur_state == player_Kirby.Normal_Attack:

                self.x_range, self.y_range = 50, 50
                self.power = 2
            elif self.player_cur_state == player_Kirby.Speed_Attack:
                self.x_range, self.y_range = 60, 50
                self.power = 1
            elif self.player_cur_state == player_Kirby.Charge_Attack:
                self.x_range, self.y_range = 30, 50
                self.power = self.p.Charging_Point
            elif self.player_cur_state == player_Kirby.Upper_Attack:
                self.x_range, self.y_range = 30, 40
                self.power = 2
            elif self.player_cur_state == player_Kirby.Drop_Attack:
                self.x_range, self.y_range = 40, 70
                self.power = 2
            elif self.player_cur_state == player_Kirby.Falling_Attack:
                self.x_range, self.y_range = 50, 50
                self.power = 3



    def get_bb(self):
        p_L = self.x - self.x_range
        p_B = self.y - self.y_range
        p_R = self.x + self.x_range
        p_T = self.y + self.y_range

        if self.player_cur_state == player_Kirby.Normal_Attack:
            return p_L + self.p_dir * 50, p_B, p_R + self.p_dir * 50, p_T

        elif self.player_cur_state == player_Kirby.Speed_Attack:
            return p_L + self.p_dir * 50, p_B - 10, p_R + 50 * self.p_dir, p_T - 10

        elif self.player_cur_state == player_Kirby.Charge_Attack:
            return p_L + self.p_dir * 50, p_B, p_R + self.p_dir * 50, p_T

        elif self.player_cur_state == player_Kirby.Upper_Attack:
            return p_L, p_B + 30, p_R, p_T + 10

        elif self.player_cur_state == player_Kirby.Drop_Attack:
            return p_L, p_B - 30, p_R, p_T - 80

        elif self.player_cur_state == player_Kirby.Falling_Attack:
            return p_L, p_B - 5, p_R, p_T - 5

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