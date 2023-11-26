from pico2d import (get_time, load_image, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_q, draw_rectangle, load_font )
import World
import game_framework
import random
import math
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from M_Sword_Attack import Meta_Knight_Sword_Strike as Sword_Strike
from M_Attack_Area import Meta_Attack_Area
import one_player_mode

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
FAST_RUN_SPEED_PPS = RUN_SPEED_PPS * 1.8

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 8      # 일반 공격 동작 속도
FRAMES_PER_FAST_ATTACK = 10 # 빠른 공격 동작 속도 더 빠르게
FRAMES_PER_CHARGE_ATTACK = 10
FRAMES_PER_DROP_ATTACK = 12
FRAMES_PER_FALLING_ATTACK = 5


#walking_focus = [[3, 58], [3, 66], [10, 66], [15, 50], [6, 50], [3, 66], [5, 66]]
Normal_Attack_focus = [[110, 50], [220, 60], [325, 75], [425, 110], [649, 91]]
Speed_Attack_focus = [[2, 50, 485], [2, 50, 485], [755, 110, 480], [2, 100, 405],[110,100,400]]
Charge_Attack_focus = [[2, 50],[110, 50],[220,60],[325, 75],[425,110], [425,110],[540, 100],[540, 100],[540, 100],[645,110]]

#reforged_frame
#start_x, width
Walk_focus = [[2,39], [51,36], [100, 34], [149, 37], [203, 36], [258, 40], [316, 41], [377, 38] ]
Run_focus = [[7,25], [59,23], [100, 34], [147, 23], [189, 23] ]
Fly_focus = [[3, 58], [3, 66], [10, 66], [15, 50], [6, 50], [3, 66], [5, 66]]
Jump_focus = [[9, 32],[57, 27], [101, 28], [143, 26], [187, 26], [230, 26], [274, 27], [315, 27], [357, 28], [401, 32]]
Upper_attack_focus = [[130, 29], [178, 48], [240, 33], [291, 25], [337, 29]]
damaged_focus = [[0, 29], [56, 52]]
Drop_attack_focus = [[0, 28], [48, 26], [96, 26], [136, 28], [188, 27], [242, 30], [290, 37],[355, 27], [405, 27]]
Falling_attack_focus = [[0, 33], [55,32], [112, 34], [166, 37], [227, 33], [284, 33], [339, 32], [396, 34], [451, 32], [509, 32]]
Faf_player_location = [[0,0], [-15, -15], [-25, 0], [0, -5], [-25, -15], [0,0], [-15, -15], [-25, 0], [0,0], [0,0]]



class Attack_Area:
    def __init__(self, player):
        self.x, self.y = player.x, player.y
        self.p = player
        self.p_dir = player.dir
        self.x_range = 0
        self.y_range = 0
        self.power = 0
        self.Attacking = False

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

    def get_bb(self):
        p_L = self.x - self.x_range
        p_B = self.y - self.y_range
        p_R = self.x + self.x_range
        p_T = self.y + self.y_range

        if self.p.state =='Normal_attack':
            return p_L + self.p_dir * 50, p_B, p_R + self.p_dir * 50, p_T

        return p_L, p_B, p_R, p_T

    def handle_collision(self, group, other):
        pass

class MetaKnight:

    def __init__(self, Player = "p1"):
        self.x, self.y = 400, 150
        self.Life = 1
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

        self.font = load_font('resource/ENCR10B.TTF', 16)
        self.image = load_image('resource/Meta_Knight_3.png')
        self.walk_image = load_image('resource/Meta_Knight_Walk.png')
        self.run_image = load_image('resource/Meta_Knight_Run.png')
        self.jump_image = load_image('resource/Meta_Knight_Jump.png')
        self.upper_attack_image = load_image('resource/Meta_Knight_Upper_Attack.png')
        self.drop_attack_image = load_image('resource/Meta_Knight_Air_Attack.png')
        self.falling_attack_image = load_image('resource/Meta_Knight_Air_Hard_Attack.png')
        self.damaged_image = load_image('resource/Meta_Knight_Damaged.png')


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

    def draw(self):
        self.font.draw(self.x - 10, self.y + 60, f'{self.Life:02d}', (255, 0, 0))
        if self.state == 'Walk':
            self.frame = self.frame % 7
            frame = int(self.frame)
            if self.dir == 1:
                self.walk_image.clip_draw(Walk_focus[frame][0], 0, Walk_focus[frame][1], 36, self.x, self.y, Walk_focus[frame][1] * 2, 36 * 2)

            elif self.dir == -1:
                self.walk_image.clip_composite_draw(Walk_focus[frame][0], 0, Walk_focus[frame][1], 36, 0, 'h', self.x, self.y,
                                                  Walk_focus[frame][1] * 2, 36 * 2)

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
            self.frame = self.frame % 6     # 안해도 되지만 혹시 모를 방지
            frame = int(self.frame)
            if self.dir == 1:
                self.image.clip_draw(Normal_Attack_focus[frame][0], 480, Normal_Attack_focus[frame][1], 60, self.x + 30, self.y,
                                   Normal_Attack_focus[frame][1] * 2, 60 * 2)

            elif self.dir == -1:
                self.image.clip_composite_draw(Normal_Attack_focus[frame][0], 480, Normal_Attack_focus[frame][1], 60,
                                               0, 'h', self.x - 30, self.y, Normal_Attack_focus[frame][1] * 2, 60 * 2)
        elif self.state == 'Idle':
            frame = 0
            if self.dir == 1:
                self.walk_image.clip_draw(44 * frame, 0, 44, 36, self.x, self.y, 44 * 2, 36 * 2)

            elif self.dir == -1:
                self.walk_image.clip_composite_draw(44 * frame, 0, 44, 36, 0, 'h', self.x, self.y, 44 * 2, 36 * 2)

        elif self.state == 'Hurt':

            frame = 1 if self.damaged_motion >= 50 else 0
            if self.damaged_motion % 2 == 0:
                if self.dir == -1:
                    self.damaged_image.clip_draw(damaged_focus[frame][0], 0, damaged_focus[frame][1], 42, self.x, self.y,
                                               damaged_focus[frame][1] * 2, 42 * 2)
                elif self.dir == 1:
                    self.damaged_image.clip_composite_draw(damaged_focus[frame][0], 0, damaged_focus[frame][1], 42,
                                                         0, 'h', self.x, self.y, damaged_focus[frame][1] * 2, 42 * 2)
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.attack_area.get_bb())


    def get_bb(self):
        if self.dir == 1:
            return self.x - 40, self.y - 35, self.x + 20, self.y + 5
        elif self.dir == -1:
            return self.x - 20, self.y - 35, self.x + 40, self.y + 5
        else:
            return self.x - 40, self.y - 35, self.x + 20, self.y + 5



    def handle_collision(self, group, other):
        if self.Picked_Player == "p1":
            if group == 'p1 : p2_attack_range' or group == 'p1 : p2_Sword_Skill':
                if other.Attacking:
                    print("p1 is damaged")
                    #ai damaged
                    if self.state != 'Hurt':
                        self.damaged_amount = max(1, other.power)
                        self.Life -= self.damaged_amount
                    self.state = 'Hurt'
                    self.dir = other.p_dir

        else:
            if group == 'p2 : p1_attack_range' or group == 'p2 : p1_Sword_Skill':
                if other.Attacking:
                    print("p2 is damaged by", group, other.x_range, other.y_range)
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


    def attack_to_player(self):
        if not self.Attack_called:
            self.frame = 0
            self.Attack_called = True

        self.state = 'Normal_attack'

        if int(self.frame) == 3 or int(self.frame) == 4:
            self.Attacking = True

        if int(self.frame) == 4:
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


    def build_behavior_tree(self):
        a1 = Action('Set random location', self.set_random_location)
        a2 = Action('Move to', self.move_to)
        a3 = Action('move to player', self.walk_to_player)
        a4 = Action('run to player', self.run_to_player)
        a5 = Action('attack to player', self.attack_to_player) # 기본 공격
        a6 = Action('Damaged', self.get_hurt)


        c1 = Condition('근처에 플레이어가 있는가?', self.is_player_nearby, 10)
        c2 = Condition('멀리에 플레이어가 있는가?', self.is_player_nearby, 15)


        c3 = Condition('마지막으로 공격한지 3초가 지났는가?', self.is_attack_possible, 3)
        c4 = Condition('플레이어가 공격범위 내에 있는가?', self.is_player_nearby, 5)
        c5 = Condition('공격을 받은 상태인가?', self.is_hurt)


        SEQ_near_chase = Sequence('Chase_Near_Player', c1, a3)
        SEQ_far_chase = Sequence('Chase_Far_Player', c2, a4)
        SEQ_normal_attack = Sequence('Normal_attack_to_Player', c4, a5)

        SEQ_wander = Sequence('Wander', a1, a2)
        SEQ_hurt = Sequence('HURT', c5, a6)

        SEQ_Chase_and_Normal_attack = Sequence("chase_and_attack", c3, SEQ_far_chase, SEQ_near_chase, SEQ_normal_attack)
        root = SEQ_1stage = Selector("1 stage: move and normal_attack",SEQ_hurt, SEQ_Chase_and_Normal_attack, SEQ_wander)

        self.bt = BehaviorTree(root)
        pass

