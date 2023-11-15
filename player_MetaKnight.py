from pico2d import (get_time, load_image, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE,
                    SDLK_LEFT, SDLK_RIGHT, SDLK_DOWN, SDLK_COMMA, SDLK_PERIOD, SDLK_SLASH,
                    SDLK_a, SDLK_s, SDLK_d, SDLK_f, SDLK_e, SDLK_q, draw_rectangle, load_font )
import World
import game_framework
from M_Sword_Attack import Meta_Knight_Sword_Strike as Sword_Strike

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 8      # 일반 공격 동작 속도
FRAMES_PER_FAST_ATTACK = 10 # 빠른 공격 동작 속도 더 빠르게
FRAMES_PER_CHARGE_ATTACK = 8


walking_focus = [[3, 58], [3, 66], [10, 66], [15, 50], [6, 50], [3, 66], [5, 66]]
Normal_Attack_focus = [[110, 50],[220,60],[325, 75],[425,110], [425,110]]
Speed_Attack_focus = [[2, 50, 485], [2, 50, 485], [755, 110, 480], [2, 100, 405],[110,100,400]]
Charge_Attack_focus = [[2, 50],[110, 50],[220,60],[325, 75],[425,110], [425,110],[540, 100],[540, 100],[540, 100],[645,110]]
Defense_focus = [[445, 30, 340],[498, 35, 340], [540, 35, 340], [592, 42, 330], [636, 42, 340], [0, 50, 210], [50, 50, 210], [113, 50, 210], [163, 50, 210]]




def Right_Move_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_RIGHT or e[1].key == SDLK_d)


def Right_Move_Up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and (e[1].key == SDLK_RIGHT or e[1].key == SDLK_d)


def Left_Move_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_LEFT or e[1].key ==  SDLK_a)


def Left_Move_Up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and (e[1].key == SDLK_LEFT or e[1].key ==  SDLK_a)

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def Time_Out(e):
    return e[0] == 'TIME_OUT'


def Normal_Attack_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_f or e[1].key == SDLK_PERIOD)


def RUN(e):
    return e[0] == 'RUN'

def STOP(e):
    return e[0] == 'STOP'

def Defense_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_s or e[1].key == SDLK_DOWN)


def Fast_Attack_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_e or e[1].key == SDLK_COMMA)


def Charge_Attack_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_q or e[1].key == SDLK_SLASH)

def Charge_Attack_Up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and (e[1].key == SDLK_q or e[1].key == SDLK_SLASH)


#reforged_frame

#start_x, width
Walk_focus = [[2,39], [51,36], [100, 34], [149, 37], [203, 36], [258, 40], [316, 41], [377, 38] ]






class Idle:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0
        if Right_Move_Down(e):
            p1.Right_Move, p1.dir = True, 1
        if Left_Move_Down(e):
            p1.Left_Move, p1.dir = True, -1
        if Right_Move_Up(e):
            p1.Right_Move, p1.dir = False, 1
        if Left_Move_Up(e):
            p1.Left_Move, p1.dir = False, -1


    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.frame = 0


    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        if p1.dir == 1:
            p1.walk_image.clip_draw(44 * frame, 0, 44, 36, p1.x, p1.y, 44 * 2, 36 * 2)

        elif p1.dir == -1:
            p1.walk_image.clip_composite_draw(44 * frame, 0,44, 36, 0, 'h', p1.x, p1.y, 44 * 2, 36 * 2)


class Walk:
    @staticmethod
    def enter(p1, e):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        if Right_Move_Down(e):
            p1.Right_Move, p1.dir = True, 1

        if Left_Move_Down(e):
            p1.Left_Move, p1.dir = True, -1

        if Right_Move_Up(e):
            p1.Right_Move = False

        if Left_Move_Up(e):
            p1.Left_Move = False

        if p1.Right_Move:
            p1.dir = 1
        elif p1.Left_Move:
            p1.dir = -1


        if Left_Move_Down(e) or Right_Move_Down(e):

            if p1.Last_Input_time == None:
                p1.Last_Input_time = get_time()
                p1.Last_Input_Direction = p1.dir
            else:
                Input_time = get_time() - p1.Last_Input_time
                if Input_time <= 0.5:    # 1초 안에 2번 입력했다면
                    if p1.Last_Input_Direction == p1.dir:  # 이전과 같은 방향 이동을 시도했다면
                        p1.state_machine.handle_event(('RUN', 0))
                        print("Running_Start")
                p1.Last_Input_time = get_time()
                p1.Last_Input_Direction = p1.dir



    @staticmethod
    def exit(p1, e):
        pass



    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        if p1.Left_Move and p1.Right_Move:
            p1.dir = 0

        elif p1.Left_Move or p1.Right_Move:
            p1.x += p1.dir * RUN_SPEED_PPS * game_framework.frame_time
            p1.x = clamp(25, p1.x, 1000 - 25)

        elif not(p1.Left_Move and p1.Right_Move):
            p1.state_machine.handle_event(('STOP', 0))

    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_start_x = Walk_focus[frame][0]
        p_start_y = 0
        p_width = Walk_focus[frame][1]
        p_height = 36
        if p1.dir == 1:
            p1.walk_image.clip_draw(p_start_x, p_start_y, p_width, p_height, p1.x, p1.y, p_width * 2, p_height * 2)

        elif p1.dir == -1:
            p1.walk_image.clip_composite_draw(p_start_x, p_start_y, p_width, p_height, 0, 'h', p1.x, p1.y, p_width * 2, p_height * 2)


class Run:
    @staticmethod
    def enter(p1, e):
        p1.frame = 0
        p1.Last_Input_Direction = None



    @staticmethod
    def exit(p1, e):
        print("Running off")
        pass

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        if p1.Left_Move and p1.Right_Move:
            p1.dir = 0

        elif p1.Left_Move or p1.Right_Move:
            p1.x += (p1.dir * RUN_SPEED_PPS * game_framework.frame_time) * 2
            p1.x = clamp(25, p1.x, 1000 - 25)

        elif not (p1.Left_Move and p1.Right_Move):
            p1.state_machine.handle_event(('STOP', 0))

    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_start_x = Walk_focus[frame][0]
        p_start_y = 0
        p_width = Walk_focus[frame][1]
        p_height = 36
        if p1.dir == 1:
            p1.walk_image.clip_draw(p_start_x, p_start_y, p_width, p_height, p1.x, p1.y, p_width * 2, p_height * 2)

        elif p1.dir == -1:
            p1.walk_image.clip_composite_draw(p_start_x, p_start_y, p_width, p_height, 0, 'h', p1.x, p1.y, p_width * 2,
                                              p_height * 2)

class Normal_Attack:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.Attacking = True
        p1.frame = (p1.frame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 5
        if int(p1.frame) == 4:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Normal_Attack_focus[frame][1]
        p_size_y = 60
        if p1.Picked_Player == 'p1':
            p1.image.clip_draw(Normal_Attack_focus[frame][0], 480, p_size_x, p_size_y, p1.x + 30, p1.y, p_size_x * 2, p_size_y * 2)

        elif p1.Picked_Player == 'p2':
            p1.image.clip_composite_draw(Normal_Attack_focus[frame][0], 480, p_size_x, p_size_y, 0, 'h', p1.x - 30, p1.y,
                               p_size_x * 2, p_size_y * 2)


class Speed_Attack:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.Attacking = True
        p1.frame = (p1.frame + FRAMES_PER_FAST_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 5
        if int(p1.frame) == 4:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Speed_Attack_focus[frame][1]
        p_size_y = 60
        if p1.Picked_Player == 'p1':
            p1.image.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][2], p_size_x, p_size_y, p1.x + 30, p1.y, p_size_x * 2, p_size_y * 2)

        elif p1.Picked_Player == 'p2':
            p1.image.clip_composite_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][2], p_size_x, p_size_y,
                               0, 'h', p1.x - 30, p1.y, p_size_x * 2, p_size_y * 2)


class Charge_Attack:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0
        if Charge_Attack_Down(e):
            p1.charging = True
            p1.Time_Stamp = get_time()

        elif Charge_Attack_Up(e):
            p1.charging = False
            p1.Attacking = True

    @staticmethod
    def exit(p1, e):
        if p1.Charging_Point >= 3:
            p1.SwordStrike()
            print("oooooooooooooooooooooooooooooooooooooo")
        p1.Charging_Point = 0


    @staticmethod
    def do(p1):
        if p1.charging == True:
            p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
            p1.Charging_Point = int(get_time() - p1.Time_Stamp)
        elif  p1.charging == False:
            p1.frame = (p1.frame + FRAMES_PER_CHARGE_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 10
        if int(p1.frame) == 9:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Charge_Attack_focus[frame][1]
        p_size_y = 60
        if p1.Picked_Player == 'p1':
            p1.image.clip_draw(Charge_Attack_focus[frame][0], 480, p_size_x, p_size_y, p1.x + 30, p1.y, p_size_x * 2, p_size_y * 2)
        elif p1.Picked_Player == 'p2':
            p1.image.clip_composite_draw(Charge_Attack_focus[frame][0], 480, p_size_x, p_size_y,
                               0, 'h', p1.x - 30, p1.y, p_size_x * 2, p_size_y * 2)

        if p1.charging == True:
            p1.font.draw(p1.x - 10, p1.y + 50, f'{p1.Charging_Point:02d}', (255, 255, 0))

class Defense:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0

    @staticmethod
    def exit(p1, e):
        p1.Right_Move = False
        p1.Left_Move = False
        pass

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 9
        if int(p1.frame) == 8:
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Defense_focus[frame][1]
        p_size_y = 70
        if p1.Picked_Player == 'p1':
            p1.image.clip_draw(Defense_focus[frame][0], Defense_focus[frame][2], p_size_x, p_size_y, p1.x + 20, p1.y, p_size_x * 1.8, p_size_y * 1.8)
        elif p1.Picked_Player == 'p2':
            p1.image.clip_composite_draw(Defense_focus[frame][0], Defense_focus[frame][2], p_size_x, p_size_y,
                               0, 'h', p1.x - 20, p1.y, p_size_x * 1.8, p_size_y * 1.8)


class StateMachine:
    def __init__(self, meta_knight):
        self.player = meta_knight
        self.cur_state = Idle
        self.transitions = {
            Idle: { Right_Move_Down: Walk, Left_Move_Down: Walk, Right_Move_Up: Walk, Left_Move_Up: Walk,
                   Normal_Attack_Down: Normal_Attack, Fast_Attack_Down: Speed_Attack, Charge_Attack_Down: Charge_Attack,
                   Defense_Down: Defense, },

            Walk: { Right_Move_Down: Idle, Left_Move_Down: Idle, Right_Move_Up: Idle, Left_Move_Up: Idle,
                  Normal_Attack_Down: Normal_Attack, Fast_Attack_Down: Speed_Attack, Charge_Attack_Down: Charge_Attack,
                  Defense_Down: Defense, STOP: Idle, RUN: Run},

            Run: {Right_Move_Down: Idle, Left_Move_Down: Idle, Right_Move_Up: Idle, Left_Move_Up: Idle,
                  Normal_Attack_Down: Normal_Attack, Fast_Attack_Down: Speed_Attack, Charge_Attack_Down: Charge_Attack,
                  Defense_Down: Defense, STOP: Idle },


            Normal_Attack: {STOP: Walk, Right_Move_Down: Walk, Left_Move_Down: Walk, Right_Move_Up: Walk, Left_Move_Up: Walk},

            Speed_Attack: {STOP: Walk, Right_Move_Down: Walk, Left_Move_Down: Walk, Right_Move_Up: Walk, Left_Move_Up: Walk},

            Charge_Attack: {Charge_Attack_Up: Charge_Attack, STOP: Walk,
                            Right_Move_Down: Walk, Left_Move_Down: Walk, Right_Move_Up: Walk, Left_Move_Up: Walk},

            Defense: { STOP: Walk, }


        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)


class MetaKnight:

    def __init__(self, Player = "p1"):
        self.x, self.y = 400, 150
        self.Picked_Player = Player
        if Player == "p1":
            self.dir = 1
        else:
            self.dir = -1
        self.frame = 0

        self.Last_Input_time = None # 대쉬 파악용
        self.Last_Input_Direction = None  # 대쉬 파악용

        self.charging = False
        self.Attacking = False
        self.Charging_Point = 0
        self.Time_Stamp = 0
        self.font = load_font('resource/ENCR10B.TTF', 16)
        self.Left_Move = False
        self.Right_Move = False
        self.image = load_image('resource/Meta_Knight_3.png')
        self.walk_image = load_image('resource/Meta_Knight_Walk.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        #남은 체력 표기하기
        #self.font.draw(self.x - 10, self.y + 50, f'{self.Charging_Point:02d}', (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def SwordStrike(self):
        if self.Picked_Player == 'p1':
            S_S = Sword_Strike(self.x, self.y, self.Charging_Point)
            World.add_object(S_S)
        elif self.Picked_Player == 'p2':
            S_S = Sword_Strike(self.x, self.y, -self.Charging_Point)
            World.add_object(S_S)

    def get_bb(self):

        if self.state_machine.cur_state == Idle:
            if self.Picked_Player == 'p1':
                return self.x - 15, self.y - 25, self.x + 25, self.y + 15
            elif self.Picked_Player == 'p2':
                return self.x - 25, self.y - 25, self.x + 15, self.y + 15

        if self.state_machine.cur_state == Speed_Attack:
            if self.Picked_Player == 'p1':
                return self.x + 25, self.y - 25, self.x + 65, self.y + 20
            elif self.Picked_Player == 'p2':
                return self.x - 65, self.y - 20, self.x - 25, self.y + 20


        elif self.state_machine.cur_state == Walk:
            if self.dir == 1:
                return self.x - 15, self.y - 25, self.x + 25, self.y + 15
            elif self.dir == -1:
                return self.x - 25, self.y - 25, self.x + 15, self.y + 15
            else:
                if self.Picked_Player == 'p1':
                    return self.x - 15, self.y - 25, self.x + 25, self.y + 15
                elif self.Picked_Player == 'p2':
                    return self.x - 25, self.y - 25, self.x + 15, self.y + 15

        elif self.state_machine.cur_state == Normal_Attack:
            if self.Picked_Player == 'p1':
                return self.x + 25, self.y - 25, self.x + 65, self.y + 20
            elif self.Picked_Player == 'p2':
                return self.x - 65, self.y - 20, self.x - 25, self.y + 20

        elif self.state_machine.cur_state == Charge_Attack:
            if self.Picked_Player == 'p1':
                return self.x + 5, self.y - 45, self.x + 65, self.y + 25
            elif self.Picked_Player == 'p2':
                return self.x - 65, self.y - 45, self.x - 5, self.y + 25

        elif self.state_machine.cur_state == Defense:
            if self.Picked_Player == 'p1':
                return self.x - 15, self.y - 45, self.x + 45, self.y + 25
            elif self.Picked_Player == 'p2':
                return self.x - 45, self.y - 45, self.x + 15, self.y + 25

        else:
            return 0,0,0,0
