from pico2d import (get_time, load_image, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_q, draw_rectangle, load_font )
import World
import game_framework
import random
import math
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from SK_Sword_Attack import Sword_Kirby_Sword_Strike as Sword_Strike
from SK_Attack_Area import Sword_Kirby_Attack_Area
import one_player_mode

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
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
FRAMES_PER_ATTACK = 10      # 일반 공격 동작 속도
FRAMES_PER_FAST_ATTACK = 15 # 빠른 공격 동작 속도 더 빠르게
FRAMES_PER_CHARGE_ATTACK = 8
FRAMES_PER_UPPER_ATTACK = 15
FRAMES_PER_DROP_ATTACK = 20



#reforged
stand_focus = [[0, 32], [44, 33], [92, 30], [139, 31]]
walk_focus = [[0, 22], [39, 27], [80, 30], [120, 37], [167, 37], [214, 32], [259, 29], [299, 20]]
Run_focus = [[0, 34], [41, 30], [83, 29], [122, 34], [165, 30], [210, 34]]
Jump_focus = [[0, 32], [47, 35], [97, 30], [138, 21], [177, 22], [218, 20], [253, 21], [290, 20], [318, 22], [352, 24], [386, 33], [437, 39], [500, 34], [564, 30], [614, 30], [666, 30], [717, 28]]
damaged_focus = [[0, 34], [42, 39]]
Upper_attack_focus = [[0, 24], [42, 24], [92, 24], [144, 28], [210, 50], [299, 56], [387, 76], [489, 80], [606, 92], [739, 20], [804, 26], [867, 28]]
Drop_attack_focus = [[0, 39], [66, 44], [141, 56], [249, 76], [354, 28]] #jump 2,3,4,5,6 이미지 후 연결
Falling_attack_focus = [[0, 53], [54, 53], [110, 53], [116, 53], [218, 53], [277, 53], [331, 53], [386, 53] , [0, 53], [54, 53], [110, 53], [116, 53], [218, 53], [277, 53], [331, 53], [386, 53], [0, 53], [54, 53], [110, 53], [116, 53], [218, 53], [277, 53], [331, 53], [386, 53]] #점프의 12, 13, 14번째 이미지를 쓰고 하기
charge_focus = [[0, 56], [68, 58], [139, 65], [215, 41], [267, 41], [320, 40], [370, 40], [440, 62], [528, 70], [629, 70], [733, 92]]
charge_location = [[-33, -9], [- 35, -9], [-42, -9], [- 18, -9], [ -18, -9], [-17, -9], [-17, -9], [- 16, -9], [- 17 ,-9], [-21, -9], [-21,-9]]
Normal_Attack_focus = [[45, 800, 45, 50],[97,800, 60, 50],[160, 800, 60, 50],[227, 800, 45, 50], [290, 800, 55, 50], [362, 785, 90, 50], [455, 785, 95, 50],[555, 785, 70, 50] ]
Speed_Attack_focus = [[40, 700, 55, 50], [105, 700, 55, 50], [165, 700, 55, 50], [230, 700, 75, 50], [310, 695, 65, 50],  [390, 690, 85, 50], [570,616,85,50], [670,616,70,50], ]
Defense_focus = [[0,23], [29, 26], [61, 30], [98, 18], [122, 24], [152, 32], [189, 22], [218, 24], [250, 25], [282, 25]]



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


    def handle_collision(self, group, other):
        pass

class Master_Kirby:

    def __init__(self, Player = "p1"):
        self.x, self.y = 400, 150
        self.Life = 20
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

        self.falling = False
        self.damaged_time = None # 맞은 시점
        self.damaged_motion = 1
        self.damaged_amount = 0
        self.Damage_called = False
        self.Get_Damage = False

        self.Jumping = False

        self.font = load_font('resource/ENCR10B.TTF', 16)
        self.image = load_image('resource/Master_Kirby.png')
        self.stand_image = load_image('resource/Kirby_Stand.png')
        self.walk_image = load_image('resource/Kirby_Walk.png')
        self.run_image = load_image('resource/Kirby_Run.png')
        self.jump_image = load_image('resource/Kirby_Jump.png')
        self.damaged_image = load_image('resource/Kirby_Damaged.png')
        self.defense_image = load_image('resource/Sword_Kirby/Defense_Kirby.png')
        self.charge_attack_image = load_image('resource/Kirby_Charge_Attack.png')
        self.upper_attack_image = load_image('resource/Kirby_Upper_Attack.png')
        self.drop_attack_image = load_image('resource/Kirby_Drop_Attack.png')
        self.falling_attack_image = load_image('resource/Kirby_Falling_Attack.png')


        # ai
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        if self.state == 'Normal_attack':
            if 3 <= int(self.frame) <= 8:
                self.Attacking = True
        elif self.state == 'Upper_attack':
            if 3 <= int(self.frame) <= 10:
                self.Attacking = True
            else:
                self.Attacking = False
        elif self.state == 'Drop_attack':
            if 4 <= int(self.frame) <= 7:
                self.Attacking = True
            else:
                self.Attacking = False
        elif self.state == 'Falling_attack':
            if 3 <= int(self.frame) <= 25:
                self.Attacking = True
            else:
                self.Attacking = False

        if self.state == 'Jump' or self.state == 'Idle':
            self.Attacking = False

        self.attack_area.update()

        if self.Life <= 0:
            self.state = 'Hurt'
            self.frame = 0
            self.damaged_motion += 1
        else:
            self.bt.run()

    def draw(self):
        self.font.draw(self.x - 10, self.y + 60, f'{self.Life:02d}', (255, 0, 0))
        if self.state == 'Walk':
            frame = int(self.frame) % 7
            p_size_x = walk_focus[frame][1]
            if self.dir == 1:
                self.walk_image.clip_draw(walk_focus[frame][0], 0, p_size_x, 49, self.x, self.y + 10, p_size_x * 2,
                                        49 * 2)
            elif self.dir == -1:
                self.walk_image.clip_composite_draw(walk_focus[frame][0], 0, p_size_x, 49,
                                                  0, 'h', self.x, self.y + 10, p_size_x * 2, 49 * 2)

        elif self.state == 'Run':
            frame = int(self.frame) % 6
            p_size_x = Run_focus[frame][1]
            if self.dir == 1:
                self.run_image.clip_composite_draw(Run_focus[frame][0], 0, p_size_x, 44, 0, 'h', self.x, self.y + 10,
                                                 p_size_x * 2, 44 * 2)
            elif self.dir == -1:
                self.run_image.clip_draw(Run_focus[frame][0], 0, p_size_x, 44, self.x, self.y + 10, p_size_x * 2,
                                       44 * 2)

        elif self.state == 'Idle':
            frame = int(self.frame) % 4
            p_size_x = stand_focus[frame][1]
            if self.dir == 1:
                self.stand_image.clip_draw(stand_focus[frame][0], 0, p_size_x, 45,
                                         self.x, self.y + 10, p_size_x * 2, 45 * 2)

            if self.dir == -1:
                self.stand_image.clip_composite_draw(stand_focus[frame][0], 0, p_size_x, 45,
                                                   0, 'h', self.x, self.y + 10, p_size_x * 2, 45 * 2)


        elif self.state == 'Jump':
            frame = int(self.frame) % 17
            p_start_x = Jump_focus[frame][0]
            p_width = Jump_focus[frame][1]
            if self.dir == 1:
                self.jump_image.clip_draw(p_start_x, 0, p_width, 54, self.x, self.y + 10, p_width * 2,
                                        54 * 2)

            elif self.dir == -1:
                self.jump_image.clip_composite_draw(p_start_x, 0, p_width, 54, 0, 'h', self.x, self.y + 10,
                                                  p_width * 2, 54 * 2)


        elif self.state == 'Normal_attack':
            frame = int(self.frame) % 9
            p_size_x = Normal_Attack_focus[frame][2]
            p_size_y = Normal_Attack_focus[frame][3]
            if self.dir == 1:
                if frame <= 4:
                    self.image.clip_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x, p_size_y,
                                       self.x, self.y + 10, p_size_x * 2, p_size_y * 2)
                elif frame > 4:
                    self.image.clip_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x, p_size_y,
                                       self.x + 5 * frame, self.y - 5, p_size_x * 2, p_size_y * 2)

            elif self.dir == -1:
                if frame <= 4:
                    self.image.clip_composite_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x,
                                                 p_size_y,
                                                 0, 'h', self.x, self.y + 10, p_size_x * 2, p_size_y * 2)
                elif frame > 4:
                    self.image.clip_composite_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x,
                                                 p_size_y,
                                                 0, 'h', self.x - 5 * frame, self.y - 5, p_size_x * 2, p_size_y * 2)



        elif self.state == 'Hurt':

            frame = 1 if self.damaged_motion >= 50 else 0
            if self.damaged_motion % 2 == 0:
                if self.dir == -1:
                    self.damaged_image.clip_draw(damaged_focus[frame][0], 0, damaged_focus[frame][1], 42, self.x, self.y,
                                                 damaged_focus[frame][1] * 2, 42 * 2)
                elif self.dir == 1:
                    self.damaged_image.clip_composite_draw(damaged_focus[frame][0], 0, damaged_focus[frame][1], 42,
                                                           0, 'h', self.x, self.y, damaged_focus[frame][1] * 2, 42 * 2)




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

        elif self.state == 'Hurt':
            if self.dir == 1:
                return self.x - 10, self.y - 35, self.x + 30, self.y + 5
            elif self.dir == -1:
                return self.x - 30, self.y - 35, self.x + 10, self.y + 5




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

        if group == 'p : Falling_area':
            if self.state == 'Hurt':
                self.falling = True
            if self.falling:
                self.y -=10



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

        if 5 <= int(self.frame) == 8:
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
        if get_time() - self.damaged_time >= 0.2 * self.damaged_amount and self.y == 150:
            self.state = 'Idle'
            self.Get_Damage = False
            self.Damage_called = False
            self.dir *= -1
            self.damaged_motion = 0
            return BehaviorTree.SUCCESS
        else:
            self.Get_Damage = True
            self.damaged_motion += 1
            self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time * (self.damaged_amount * 0.5)
            self.y += self.jump_value
            self.jump_value -= 1

            if self.falling == False:
                self.y = max(self.y, 150)
            return BehaviorTree.RUNNING


    def check_player_y_for_attack(self, distance):
        if one_player_mode.Player.y > self.y + 50:
            if one_player_mode.Player.y > 100:
                return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL


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

        if self.y <= 150:
            self.y = 150
            self.jump_value = 0
            self.state = 'Idle'
            self.Jumping = False
            return BehaviorTree.SUCCESS

        elif self.select_to_air_attack():
            self.frame = 0
            self.Attacking = True
            return BehaviorTree.RUNNING

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

