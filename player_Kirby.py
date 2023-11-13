from pico2d import (get_time, load_image, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE,
                    SDLK_LEFT, SDLK_RIGHT, SDLK_DOWN, SDLK_COMMA, SDLK_PERIOD, SDLK_SLASH,
                    SDLK_a, SDLK_s, SDLK_d, SDLK_f, SDLK_e, SDLK_q, draw_rectangle )
import World
import game_framework

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


# Boy Action Speed
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10


TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 10      # 일반 공격 동작 속도
FRAMES_PER_FAST_ATTACK = 15 # 빠른 공격 동작 속도 더 빠르게
FRAMES_PER_CHARGE_ATTACK = 8

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




Standing_focus = [[223,1195],[268,1195],[315,1195], [362,1195]]
walking_focus = [[25, 1070], [70, 1070], [111, 1070], [152, 1070], [197, 1070], [240, 1070], ]
Normal_Attack_focus = [[45, 800, 45, 50],[97,800, 60, 50],[160, 800, 60, 50],[227, 800, 45, 50], [290, 800, 55, 50], [362, 785, 90, 50], [455, 785, 95, 50],[555, 785, 70, 50] ]
Speed_Attack_focus = [[40, 700, 55, 50], [105, 700, 55, 50], [165, 700, 55, 50], [230, 700, 75, 50], [310, 695, 65, 50],  [390, 690, 85, 50], [570,616,85,50], [670,616,70,50], ]
Charge_Attack_focus = [
    (140, 566, 60, 40, -10, 5), (205, 560, 65, 40, -15, 0), (275, 560, 75, 40, -18, 0),
    (355, 560, 45, 40, 2, -5), (405, 560, 45, 40, 1, -5), (460, 560, 45, 40, 2, -8),
    (510, 560, 45, 40, 0, -7), (30, 480, 65, 60, 18, 0), (110, 470, 75, 60, 15, -25),
    (210, 470, 80, 60, 0, 0), (315, 460, 100, 60, 0, 0)
]
Defense_focus = [(35, 940, 40, 40,0 ,0), (75, 940, 40, 40, 0 ,0), (125, 940, 40, 40, 0 ,0), (175, 940, 50, 40, 0 ,0), (235, 930, 40, 65, 0 ,0),
                 (280, 930, 40, 65, 0 ,0), (325, 930, 40, 65, 0 ,0), (375, 930, 40, 65, 0 ,0), (420, 930, 40, 65, 0 ,0), (470, 930, 40, 65, 0 ,0),
                 (510, 940, 65, 40, 0, 0), (585, 940, 65, 40, 0, 0), (665, 940, 70, 40, 0, 0), (750, 940, 65, 40, 0, 0),]

class Idle:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0
        p1.dir = 0
        if Right_Move_Down(e):
            p1.Right_Move, p1.dir = True, 1
        if Left_Move_Down(e):
            p1.Left_Move, p1.dir = True, -1
        if Right_Move_Up(e):
            p1.Right_Move = False
        if Left_Move_Up(e):
            p1.Left_Move = False

        p1.Defense_time = get_time() # 카운터를 위한 타이머
        pass

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4


    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = 35
        p_size_y = 45
        if p1.Picked_Player == 'p1':
            p1.image.clip_draw(Standing_focus[frame][0], Standing_focus[frame][1], p_size_x, p_size_y,
                               p1.x, p1.y, p_size_x * 2, p_size_y * 2)

        elif p1.Picked_Player == 'p2':
            p1.image.clip_composite_draw(Standing_focus[frame][0], Standing_focus[frame][1], p_size_x, p_size_y,
                                         0, 'h', p1.x, p1.y, p_size_x * 2, p_size_y * 2)

        draw_rectangle(p1.x - p_size_x, p1.y - p_size_y, p1.x + p_size_x, p1.y + p_size_y)


class Run:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0
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



    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):

        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if p1.Left_Move and p1.Right_Move:
            p1.dir = 0

        elif p1.Left_Move or p1.Right_Move:
            p1.x += p1.dir * RUN_SPEED_PPS * game_framework.frame_time
            p1.x = clamp(25, p1.x, 1000 - 25)

        elif not(p1.Left_Move and p1.Right_Move):
            p1.state_machine.handle_event(('STOP', 0))

        print(p1.Left_Move, p1.Right_Move)


    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = 40
        p_size_y = 45
        if p1.Picked_Player == 'p1':
            p1.image.clip_draw(walking_focus[frame][0], walking_focus[frame][1], p_size_x, p_size_y, p1.x, p1.y, p_size_x * 2, p_size_y * 2)

        elif p1.Picked_Player == 'p2':
            p1.image.clip_composite_draw(walking_focus[frame][0], walking_focus[frame][1], p_size_x, p_size_y,
                                         0, 'h', p1.x, p1.y, p_size_x * 2, p_size_y * 2)

        draw_rectangle(p1.x - p_size_x, p1.y - p_size_y, p1.x + p_size_x, p1.y + p_size_y)



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
        p1.frame = (p1.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 9
        if int(p1.frame) == 8:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Normal_Attack_focus[frame][2]
        p_size_y = Normal_Attack_focus[frame][3]
        if p1.Picked_Player == 'p1':
            if  frame <= 4:
                p1.image.clip_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x, p_size_y, p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)
            elif frame > 4:
                p1.image.clip_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x, p_size_y, p1.x + 5*frame, p1.y -5, p_size_x * 2, p_size_y * 2)

        elif p1.Picked_Player == 'p2':
            if  frame <= 4:
                p1.image.clip_composite_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x, p_size_y,
                                             0, 'h', p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)
            elif frame > 4:
                p1.image.clip_composite_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x, p_size_y,
                                             0, 'h', p1.x - 5*frame, p1.y -5, p_size_x * 2, p_size_y * 2)

        draw_rectangle(p1.x - p_size_x, p1.y - p_size_y, p1.x + p_size_x, p1.y + p_size_y)



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
        p1.frame = (p1.frame + FRAMES_PER_FAST_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 9
        if int(p1.frame) == 8:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Speed_Attack_focus[frame][2]
        p_size_y = Speed_Attack_focus[frame][3]

        if p1.Picked_Player == 'p1':
            if frame < 3:
                p1.image.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y, p1.x, p1.y, p_size_x * 2, p_size_y * 2)
            elif 3 <= frame < 6:
                p1.image.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y, p1.x + 10 * frame, p1.y , p_size_x * 2, p_size_y * 2)
            else:
                p1.image.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y, p1.x+ 40, p1.y - 10, p_size_x * 2, p_size_y * 2)

        elif p1.Picked_Player == 'p2':
            if frame < 3:
                p1.image.clip_composite_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y,
                                             0, 'h', p1.x, p1.y, p_size_x * 2, p_size_y * 2)
            elif 3 <= frame < 6:
                p1.image.clip_composite_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y,
                                             0, 'h', p1.x - 10 * frame, p1.y, p_size_x * 2, p_size_y * 2)
            else:
                p1.image.clip_composite_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y,
                                             0, 'h', p1.x - 40, p1.y - 10, p_size_x * 2, p_size_y * 2)


class Charge_Attack:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0


        if Charge_Attack_Down(e):
            p1.frame = 0

        elif Charge_Attack_Up(e):
            p1.charging = False
            p1.Attacking = True

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        frame_increment = FRAMES_PER_CHARGE_ATTACK * ACTION_PER_TIME * game_framework.frame_time

        if not (p1.charging or p1.Attacking) and int(p1.frame) < 3:
            p1.frame = (p1.frame + frame_increment) % 4
            if int(p1.frame) == 3:
                p1.charging = True
        elif p1.charging:
            p1.frame = max(3, p1.frame)
            p1.frame = (p1.frame + frame_increment) % 7
            p1.frame = max(3, p1.frame)
        elif not p1.charging:
            p1.frame = max(p1.frame, 7)
            p1.frame = (p1.frame + frame_increment) % 12
        if int(p1.frame) == 11:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))

    @staticmethod
    def draw(p1):
        frame = int(p1.frame)

        p_size_x = Charge_Attack_focus[frame][2]
        p_size_y = Charge_Attack_focus[frame][3]
        if p1.Picked_Player == 'p1':
            p1.image.clip_draw(Charge_Attack_focus[frame][0], Charge_Attack_focus[frame][1], p_size_x, p_size_y, p1.x + Charge_Attack_focus[frame][4], p1.y + Charge_Attack_focus[frame][5], p_size_x * 2, p_size_y * 2)

        elif p1.Picked_Player == 'p2':
            p1.image.clip_composite_draw(Charge_Attack_focus[frame][0], Charge_Attack_focus[frame][1], p_size_x, p_size_y,
                                         0, 'h', p1.x - Charge_Attack_focus[frame][4], p1.y + Charge_Attack_focus[frame][5], p_size_x * 2, p_size_y * 2)



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
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 15
        if int(p1.frame) == 14:
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Defense_focus[frame][2]
        p_size_y = Defense_focus[frame][3]
        p_x = p1.x + Defense_focus[frame][4]
        p_y = p1.y + Defense_focus[frame][5]
        if p1.Picked_Player == 'p1':
            p1.image.clip_draw(Defense_focus[frame][0], Defense_focus[frame][1], p_size_x, p_size_y, p_x , p_y, p_size_x * 2, p_size_y * 2)
        elif p1.Picked_Player == 'p2':
            p1.image.clip_composite_draw(Defense_focus[frame][0], Defense_focus[frame][1], p_size_x, p_size_y,
                                         0, 'h', p_x , p_y, p_size_x * 2, p_size_y * 2)


class StateMachine:
    def __init__(self, kirby):
        self.player = kirby
        self.cur_state = Idle
        self.transitions = {
            Idle: {Right_Move_Down: Run, Left_Move_Down: Run, Right_Move_Up: Run, Left_Move_Up: Run,
                   Normal_Attack_Down: Normal_Attack, Fast_Attack_Down: Speed_Attack, Charge_Attack_Down: Charge_Attack,
                   Defense_Down: Defense, },

            Run: {Right_Move_Down: Idle, Left_Move_Down: Idle, Right_Move_Up: Idle, Left_Move_Up: Idle,
                  Normal_Attack_Down: Normal_Attack, Fast_Attack_Down: Speed_Attack, Charge_Attack_Down: Charge_Attack,
                  Defense_Down: Defense, STOP: Idle},

            Normal_Attack: {STOP: Run, Right_Move_Down: Run, Left_Move_Down: Run, Right_Move_Up: Run,
                            Left_Move_Up: Run},

            Speed_Attack: {STOP: Run, Right_Move_Down: Run, Left_Move_Down: Run, Right_Move_Up: Run, Left_Move_Up: Run},

            Charge_Attack: {Charge_Attack_Up: Charge_Attack, STOP: Run,
                            Right_Move_Down: Run, Left_Move_Down: Run, Right_Move_Up: Run, Left_Move_Up: Run},

            Defense: {STOP: Run, }


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


class Kirby:

    def __init__(self):
        self.x, self.y = 400, 150
        self.Picked_Player = "None"
        self.frame = 0
        self.dir = 0
        self.charging = False
        self.Attacking = False
        self.Left_Move = False
        self.Right_Move = False
        self.image = load_image('resource/Master_Kirby.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

