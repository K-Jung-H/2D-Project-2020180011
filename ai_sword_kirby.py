from pico2d import (get_time, load_image, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_q, draw_rectangle, load_font )
import World
import game_framework
import random
import math
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from SK_Sword_Attack import Sword_Kirby_Sword_Strike as Sword_Strike
from SK_Attack_Area import Sword_Kirby_Attack_Area
import one_player_mode

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
FAST_RUN_SPEED_PPS = RUN_SPEED_PPS * 1.8


TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10
FRAMES_PER_JUMP_ACTION = 15
FRAMES_PER_FALLING_ATTACK = 10

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 10  # 일반 공격 동작 속도
FRAMES_PER_FAST_ATTACK = 15  # 빠른 공격 동작 속도 더 빠르게
FRAMES_PER_CHARGE_ATTACK = 8
FRAMES_PER_UPPER_ATTACK = 15
FRAMES_PER_DROP_ATTACK = 20


# reforged
stand_focus = [[0, 27], [31, 27]]
walk_focus = [[0, 25], [29, 28], [61, 31], [96, 32], [133, 32], [169, 28], [201, 24], [229, 23], [256, 23], [283, 28], [315, 25]] # 11개
Run_focus = [[0, 31], [35, 29], [67, 26],  [97, 26], [127, 28], [159, 25], [188, 26], [218, 29]]
Jump_focus = [[0, 30], [34, 30], [68, 21], [93, 21], [118, 22], [144, 32], [180, 35], [219, 32], [255, 25], [284, 25]] # 10개
damaged_focus = [[0, 32], [33, 34], [69, 35]]
Normal_Attack_focus = [[0, 29], [32, 31], [71, 31], [127, 39], [177, 43], [224, 43], [271, 64], [339, 61]]
Speed_Attack_focus = [[0, 42], [46, 37], [87, 34], [136, 19], [197, 42], [260, 49], [335, 53], [421, 62], [516, 62], [608, 43], [685, 58], [781, 58]]
charge_focus = [[0, 43], [48, 42], [94, 36], [149, 22], [175, 41], [223, 43], [275, 43], [331, 48], [382, 43]]
charge_location = [0, -10, -10, 0, 20, 20, 20, 20, 0]
Upper_attack_focus = [[0, 29], [33, 32], [69, 40], [113, 46], [169, 47], [225, 47], [281, 47], [337, 47], [393, 47],
                      [452, 47], [505, 46]]
Drop_attack_focus = [[0, 41], [45, 41], [90, 43], [138, 42], [186, 36], [240, 41], [291, 43], [347, 48]]
Defense_focus = [[0,23], [29, 26], [61, 30], [98, 18], [122, 24], [152, 32], [189, 22], [218, 24], [250, 25], [282, 25]]
Falling_attack_focus = [[2, 54], [61, 54], [120, 54], [179, 54], [238, 54], [297, 54], [355, 54], [414, 54],
                        [2, 54], [61, 54], [120, 54], [179, 54], [238, 54], [297, 54], [355, 54], [414, 54],
                        [2, 54], [61, 54], [120, 54], [179, 54], [238, 54], [297, 54], [355, 54], [414, 54],[474, 54]]



class Attack_Area:
    def __init__(self, player):
        self.x, self.y = player.x, player.y
        self.p = player
        self.p_dir = player.dir
        self.x_range = 0
        self.y_range = 0
        self.power = 0
        self.Attacking = False
        self.charge_attack = True

    def draw(self):
        draw_rectangle(*self.get_bb())



    def update(self):
        self.x, self.y = self.p.x, self.p.y
        self.Attacking = self.p.Attacking
        self.p_dir = self.p.dir
        if not self.Attacking:
            self.x_range, self.y_range, self.power = 0, 0, 0

        elif self.Attacking:
            if self.p.state == 'Normal_attack':
                self.x_range, self.y_range = 50, 50
                self.power = 2
            elif self.p.state == 'Upper_attack':
                self.x_range, self.y_range = 40, 40
                self.power = 2
            elif self.p.state == 'Drop_attack':
                self.x_range, self.y_range = 40, 50
                self.power = 2
            elif self.p.state == 'Falling_attack':
                self.x_range, self.y_range = 50, 50
                self.power = 3

    def get_bb(self):
        p_L = self.x - self.x_range
        p_B = self.y - self.y_range
        p_R = self.x + self.x_range
        p_T = self.y + self.y_range

        if self.p.state =='Normal_attack':
            return p_L + self.p_dir * 50, p_B, p_R + self.p_dir * 50, p_T

        elif self.p.state =='Upper_attack':
            return p_L + self.p_dir * 30, p_B + 20, p_R + self.p_dir * 30, p_T

        elif self.p.state =='Drop_attack':
            return p_L, p_B, p_R, p_T - 50

        elif self.p.state == 'Falling_attack':
            return p_L, p_B - 5, p_R, p_T - 5

        else:
            return 0, 0, 0, 0






        return p_L, p_B, p_R, p_T

    def handle_collision(self, group, other):
        pass

class Sword_Kirby:

    def __init__(self, Player = "p1"):
        self.x, self.y = 400, 150
        self.Life = 10
        self.Picked_Player = Player
        if Player == "p1":
            self.dir = 1
            self.x = 100
        else:
            self.dir = -1
            self.x = 900
        self.frame = 0

        self.state = 'Idle'
        self.jump_value = 0 #점프 구현

        self.attack_area = Attack_Area(self)
        self.Attacking = False

        self.Attack_cool_time = 0
        self.Attack_called = False


        self.damaged_time = None # 맞은 시점
        self.damaged_motion = 1
        self.damaged_amount = 0
        self.Damage_called = False

        self.Jumping = False

        self.font = load_font('resource/ENCR10B.TTF', 16)
        self.stand_image = load_image('resource/Sword_Kirby/Sword_kirby_Stand.png')
        self.walk_image = load_image('resource/Sword_Kirby/Sword_kirby_Walk.png')
        self.run_image = load_image('resource/Sword_Kirby/Sword_kirby_Run.png')
        self.jump_image = load_image('resource/Sword_Kirby/Sword_kirby_Jump.png')
        self.damaged_image = load_image('resource/Sword_Kirby/sword_kirby_damaged.png')
        self.normal_attack_image = load_image('resource/Sword_Kirby/sword_kirby_normal_attack.png')
        self.speed_attack_image = load_image('resource/Sword_Kirby/sword_kirby_speed_attack.png')
        self.charge_attack_image = load_image('resource/Sword_Kirby/sword_kirby_charge_attack.png')
        self.upper_attack_image = load_image('resource/Sword_Kirby/sword_kirby_upper_attack.png')
        self.drop_attack_image = load_image('resource/Sword_Kirby/sword_kirby_drop_attack.png')
        self.falling_attack_image = load_image('resource/Sword_Kirby/sword_kirby_falling_attack.png')
        self.defense_image = load_image('resource/Sword_Kirby/Defense_Kirby.png')

        # ai
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.attack_area.update()

        if self.Life <= 0:
            self.state = 'Hurt'
            self.frame = 0
            self.damaged_motion += 1
        else:
            self.bt.run()
            print(self.state)
            print(self.state)
            print(self.state)
            print(self.state)
            print(self.state)
            print(self.state)

    def draw(self):
        self.font.draw(self.x - 10, self.y + 60, f'{self.Life:02d}', (255, 0, 0))
        if self.state == 'Walk':
            self.frame = self.frame % 7
            frame = int(self.frame)
            if self.dir == 1:
                self.walk_image.clip_draw(walk_focus[frame][0], 0, walk_focus[frame][1], 36, self.x, self.y, walk_focus[frame][1] * 2, 36 * 2)

            elif self.dir == -1:
                self.walk_image.clip_composite_draw(walk_focus[frame][0], 0, walk_focus[frame][1], 36, 0, 'h', self.x, self.y,
                                                    walk_focus[frame][1] * 2, 36 * 2)

        elif self.state == 'Run':
            self.frame = self.frame % 4
            frame = int(self.frame)
            if self.dir == 1:
                self.run_image.clip_draw(Run_focus[frame][0], 0, Run_focus[frame][1], 39,
                                         self.x, self.y, Run_focus[frame][1] * 2, 39 * 2)

            elif self.dir == -1:
                self.run_image.clip_composite_draw(Run_focus[frame][0], 0, Run_focus[frame][1], 39,
                                                   0, 'h', self.x, self.y, Run_focus[frame][1] * 2, 39 * 2)

        elif self.state == 'Normal_attack':
            self.frame = self.frame % 8     # 안해도 되지만 혹시 모를 방지
            frame = int(self.frame)
            if self.dir == 1:
                if frame < 4:
                    self.normal_attack_image.clip_draw(Normal_Attack_focus[frame][0], 0, Normal_Attack_focus[frame][1], 50,
                                                       self.x, self.y, Normal_Attack_focus[frame][1] * 2, 50 * 2)
                elif frame >= 4:
                    self.normal_attack_image.clip_draw(Normal_Attack_focus[frame][0], 0, Normal_Attack_focus[frame][1], 50,
                                                       self.x + 20, self.y, Normal_Attack_focus[frame][1] * 2, 50 * 2)

            elif self.dir == -1:
                if frame < 4:
                    self.normal_attack_image.clip_composite_draw(Normal_Attack_focus[frame][0], 0,  Normal_Attack_focus[frame][1],
                                                                 50, 0, 'h', self.x - 20, self.y,  Normal_Attack_focus[frame][1] * 2,
                                                                 50 * 2)
                elif frame >= 4:
                    self.normal_attack_image.clip_composite_draw(Normal_Attack_focus[frame][0], 0,  Normal_Attack_focus[frame][1],
                                                                 50, 0, 'h', self.x - 20, self.y,  Normal_Attack_focus[frame][1] * 2,
                                                                 50 * 2)

        elif self.state == 'Idle':
            frame = int(self.frame) % 2
            if self.dir == 1:
                self.stand_image.clip_draw(stand_focus[frame][0], 0, stand_focus[frame][1], 40,
                                           self.x, self.y + 10, stand_focus[frame][1] * 2, 40 * 2)

            if self.dir == -1:
                self.stand_image.clip_composite_draw(stand_focus[frame][0], 0, stand_focus[frame][1], 40,
                                                     0, 'h', self.x, self.y + 10, stand_focus[frame][1] * 2, 40 * 2)

        elif self.state == 'Hurt':

            frame = 1 if self.damaged_motion >= 50 else 0
            if self.damaged_motion % 2 == 0:
                if self.dir == -1:
                    self.damaged_image.clip_draw(damaged_focus[frame][0], 0, damaged_focus[frame][1], 42, self.x, self.y,
                                                 damaged_focus[frame][1] * 2, 42 * 2)
                elif self.dir == 1:
                    self.damaged_image.clip_composite_draw(damaged_focus[frame][0], 0, damaged_focus[frame][1], 42,
                                                           0, 'h', self.x, self.y, damaged_focus[frame][1] * 2, 42 * 2)

        elif self.state == 'Jump':
            frame = int(self.frame) % 10

            if self.dir == 1:
                self.jump_image.clip_draw(Jump_focus[frame][0], 0, Jump_focus[frame][1], 54, self.x, self.y + 10, Jump_focus[frame][1] * 2,
                                          54 * 2)

            elif self.dir == -1:
                self.jump_image.clip_composite_draw(Jump_focus[frame][0], 0, Jump_focus[frame][1], 54, 0, 'h', self.x, self.y + 10,
                                                    Jump_focus[frame][1] * 2, 54 * 2)


        elif self.state == 'Upper_attack':
            frame = int(self.frame) % 11
            self.y += 5
            if self.dir == 1:
                self.upper_attack_image.clip_draw(Upper_attack_focus[frame][0], 0, Upper_attack_focus[frame][1], 61, self.x, self.y,
                                                Upper_attack_focus[frame][1] * 2, 61 * 2)

            elif self.dir == -1:
                self.upper_attack_image.clip_composite_draw(Upper_attack_focus[frame][0], 0, Upper_attack_focus[frame][1], 61, 0, 'h',
                                                          self.x, self.y, Upper_attack_focus[frame][1] * 2, 61 * 2)


        elif self.state == 'Drop_attack':
            frame = int(self.frame) % 7
            self.y -= 5
            if self.dir == 1:
                self.drop_attack_image.clip_draw(Drop_attack_focus[frame][0], 0, Drop_attack_focus[frame][1], 48, self.x, self.y,
                                               Drop_attack_focus[frame][1] * 2, 48 * 2)

            elif self.dir == -1:
                self.drop_attack_image.clip_composite_draw(Drop_attack_focus[frame][0], 0, Drop_attack_focus[frame][1], 48, 0, 'h',
                                                         self.x, self.y, Drop_attack_focus[frame][1] * 2, 48 * 2)


        elif self.state == 'Falling_attack':
            frame = int(self.frame) % 27
            if self.dir == 1:
                self.falling_attack_image.clip_draw(Falling_attack_focus[frame][0], 0, Falling_attack_focus[frame][1], 54, self.x, self.y,
                                                    Falling_attack_focus[frame][1] * 2, 54 * 2)
            elif self.dir == -1:
                self.falling_attack_image.clip_composite_draw(Falling_attack_focus[frame][0], 0, Falling_attack_focus[frame][1], 54,
                                                            0,'h',self.x, self.y, Falling_attack_focus[frame][1] * 2, 54 * 2)

        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.attack_area.get_bb())


    def get_bb(self):
        if self.state == 'Idle':
            if self.dir == 1:
                return self.x - 10, self.y - 35, self.x + 30, self.y + 5
            elif self.dir == -1:
                return self.x - 30, self.y - 35, self.x + 10, self.y + 5

        elif self.state == 'Walk'or self.state == 'Run':
            if self.dir == 1:
                return self.x - 12, self.y - 35, self.x + 32, self.y + 5
            elif self.dir == -1:
                return self.x - 32, self.y - 35, self.x + 12, self.y + 5
            else:
                if self.Last_Input_Direction == 1:
                    return self.x - 12, self.y - 35, self.x + 32, self.y + 5
                elif self.Last_Input_Direction == -1:
                    return self.x - 32, self.y - 35, self.x + 12, self.y + 5


        elif self.state == 'Jump':
            if self.dir == 1:
                return self.x - 12, self.y - 35, self.x + 32, self.y + 5
            elif self.dir == -1:
                return self.x - 32, self.y - 35, self.x + 12, self.y + 5
            else:
                if self.Last_Input_Direction == 1:
                    return self.x - 12, self.y - 35, self.x + 32, self.y + 5
                elif self.Last_Input_Direction == -1:
                    return self.x - 32, self.y - 35, self.x + 12, self.y + 5


        elif self.state == 'Normal_attack':
            if self.dir == 1:
                return self.x - 35, self.y - 35, self.x + 35, self.y + 15
            elif self.dir == -1:
                return self.x - 45, self.y - 35, self.x + 25, self.y + 15

        elif self.state == 'Upper_attack':
            if self.dir == 1:
                return self.x - 45, self.y - 30, self.x, self.y + 10
            elif self.dir == -1:
                return self.x, self.y - 30, self.x + 45, self.y + 10

        elif self.state == 'Drop_attack':
            if self.dir == 1:
                return self.x - 40, self.y - 20, self.x, self.y + 20
            elif self.dir == -1:
                return self.x, self.y - 20, self.x + 40, self.y + 20

        elif self.state == 'Falling_attack':
            return self.x - 20, self.y - 20, self.x + 20, self.y + 20
        else:
            return 0, 0, 0, 0




    def handle_collision(self, group, other):
        if self.Picked_Player == "p1":
            if group == 'p1 : p2_attack_range' or group == 'p1 : p2_Sword_Skill':
                if other.Attacking:
                    print("com is damaged")
                    #ai damaged
                    if self.state != 'Hurt':
                        self.damaged_amount = max(1, other.power)
                        self.Life -= self.damaged_amount
                    self.state = 'Hurt'
                    self.dir = other.p_dir

        else:
            if group == 'p2 : p1_attack_range' or group == 'p2 : p1_Sword_Skill':
                if other.Attacking:
                    print("com is damaged by", group, other.x_range, other.y_range)
                    #ai damaged
                    if self.state != 'Hurt':
                        self.damaged_amount = max(1, other.power)
                        self.Life -= self.damaged_amount
                    self.state = 'Hurt'
                    self.dir = other.p_dir

    #===================================ai======================================================

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        speed = RUN_SPEED_PPS
        if self.x > tx:
            self.dir = -1
        elif self.x < tx:
            self.dir = 1
        if self.state == 'Walk':
            speed = RUN_SPEED_PPS
        elif self.state == 'Run':
            speed = RUN_SPEED_PPS * 1.5
        self.x += self.dir * speed * game_framework.frame_time


    def set_random_location(self):
        self.tx, self.ty = random.randint(100, 900), 150
        return BehaviorTree.SUCCESS

    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_player_nearby(self, distance):
        if self.distance_less_than(one_player_mode.Player.x, one_player_mode.Player.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            self.state = 'Idle'
            return BehaviorTree.FAIL


    def walk_to_player(self, r= 3):
        self.state = 'Walk'
        self.move_slightly_to(one_player_mode.Player.x, one_player_mode.Player.y)
        if self.distance_less_than(one_player_mode.Player.x, one_player_mode.Player.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING


    def run_to_player(self, r=3):
        self.state = 'Run'
        self.move_slightly_to(one_player_mode.Player.x, one_player_mode.Player.y)
        if self.distance_less_than(one_player_mode.Player.x, one_player_mode.Player.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING


    def is_attack_possible(self, t):
        if int(get_time() - self.Attack_cool_time) >= t:
            if self.x > one_player_mode.Player.x:
                self.dir = -1
            elif self.x < one_player_mode.Player.x:
                self.dir = 1
            return BehaviorTree.SUCCESS
        else:
            self.state = 'Idle'
            return BehaviorTree.FAIL


    def attack_to_player(self): # Normal_attack
        if not self.Attack_called:
            self.frame = 0
            self.Attack_called = True

        self.state = 'Normal_attack'

        if int(self.frame) == 6 or int(self.frame) == 7:
            self.Attacking = True

        if int(self.frame) == 8:
            self.Attack_cool_time = get_time()
            self.Attack_called = False
            self.Attacking = False
            self.state = 'Idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_hurt(self):
        if self.state == 'Hurt': # 다친 상태가 됬다면 반대 방향으로 이동
            if self.Damage_called == False:
                self.Damage_called = True
                self.damaged_time = get_time()
                self.jump_value = 5
                self.y += self.jump_value
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def get_hurt(self):
        if get_time() - self.damaged_time >= 0.2 * self.damaged_amount:
            if self.y == 150:
                self.state = 'Idle'
                self.Damage_called = False
                self.dir *= -1
                self.damaged_motion = 0
                return BehaviorTree.SUCCESS
            else:
                return BehaviorTree.RUNNING
        else:
            self.damaged_motion += 1
            self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time * (self.damaged_amount * 0.5)
            self.x = clamp(25, self.x, 1000 - 25)

            if self.y > 150:
                self.y += self.jump_value
                self.jump_value -= 1
            self.y = clamp(150, self.y, 1000 - 25)

            return BehaviorTree.RUNNING

    def check_player_y_for_attack(self, distance):
        if self.distance_less_than(0, one_player_mode.Player.y, 0, self.y, distance):
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS


    def check_player_x_for_attack(self, distance):
        if self.distance_less_than(one_player_mode.Player.x, 0, self.x, 0, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL



    def select_to_air_attack(self):
        if self.state in ['Jump', 'Upper_attack', 'Drop_attack', 'Falling_attack']:
            if self.distance_less_than(one_player_mode.Player.x, one_player_mode.Player.y, self.x, self.y, 10):
                if (self.distance_less_than(one_player_mode.Player.x, one_player_mode.Player.y, self.x, self.y, 5)
                        and self.state == 'Jump'):
                    self.state = 'Falling_attack'
                    return True
                elif self.state == 'Jump' and self.jump_value < 0:
                    self.state = 'Drop_attack'
                    return True

                elif self.state == 'Jump' and self.jump_value >= 5:
                    self.state = 'Upper_attack'
                    return True
        return False




    def check_last_action(self):
        if self.Jumping:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL


    def jump(self):
        if self.Jumping == False:
            self.jump_value = 20
            self.Jumping = True
            self.state = 'Jump'

        self.jump_value -= 1
        if self.state != 'Falling_attack':
            self.y += self.jump_value

        else:
            self.y += self.jump_value/5


        speed = RUN_SPEED_PPS * 1.5
        self.x += self.dir * speed * game_framework.frame_time

        self.x = clamp(25, self.x, 1000 - 25)

        if self.y <= 150:
            self.y = 150
            self.jump_value = 0
            self.state = 'Idle'
            self.Jumping = False
            return BehaviorTree.SUCCESS

        elif self.select_to_air_attack():
            self.frame = 0
            self.Attacking = True
            return BehaviorTree.SUCCESS

        else:
            return BehaviorTree.RUNNING



    def build_behavior_tree(self):
        a1 = Action('Set random location', self.set_random_location)
        a2 = Action('Move to', self.move_to)
        a3 = Action('move to player', self.walk_to_player)
        a4 = Action('run to player', self.run_to_player)
        a5 = Action('attack to player', self.attack_to_player) # 기본 공격
        a6 = Action('Damaged', self.get_hurt)

        a7 = Action('Jump',self.jump)



        c1 = Condition('근처에 플레이어가 있는가?', self.is_player_nearby, 10)
        c2 = Condition('멀리에 플레이어가 있는가?', self.is_player_nearby, 15)


        c3 = Condition('마지막으로 공격한지 3초가 지났는가?', self.is_attack_possible, 3)
        c4 = Condition('플레이어가 공격범위 내에 있는가?', self.is_player_nearby, 5)

        c5 = Condition('공격을 받은 상태인가?', self.is_hurt)

        c6 = Condition('상대가 공중에 있는가?', self.check_player_y_for_attack, 3)
        c7 = Condition('현재 공중 액션에 있는가?', self.check_last_action)


        SEQ_If_in_jumping = Sequence('if_in_jumping', c7, a7)
        SEQ_follow_jump = Sequence('jump_to_follow', c6, a7) # 상대에 따라 점프하기

        SEL_jump = Selector('JUMP', SEQ_follow_jump, SEQ_If_in_jumping)
        SEQ_jump = Sequence('Jump', SEL_jump)
        SEL_do_air_action = Selector('Air_Action', SEQ_jump)




        SEQ_near_chase = Sequence('Chase_Near_Player', c1, a3)
        SEQ_far_chase = Sequence('Chase_Far_Player', c2, a4)


        SEQ_ground_attack = Sequence('Ground_attack',c4, a5) #공격 범위 안이라면 공격


        SEQ_wander = Sequence('Wander', a1, a2)
        SEQ_hurt = Sequence('HURT', c5, a6)


        SEQ_Chase = Sequence("chase", c3, SEQ_far_chase, SEQ_near_chase)  # 마지막으로 공격한지 3초가 지났다면 추격
        SEQ_chase_attack = Sequence("chase_and_attack", SEQ_Chase, SEQ_ground_attack)

        root = SEQ_1stage = Selector("1 stage: move and normal_attack", SEQ_hurt,SEL_do_air_action, SEQ_chase_attack, SEQ_wander)

        self.bt = BehaviorTree(root)
        pass

