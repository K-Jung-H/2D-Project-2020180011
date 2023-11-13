from pico2d import (get_time, load_image, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE,
                    SDLK_LEFT, SDLK_RIGHT, SDLK_DOWN, SDLK_COMMA, SDLK_PERIOD, SDLK_SLASH,
                    SDLK_a, SDLK_s, SDLK_d, SDLK_f, SDLK_e, SDLK_q )
import World
import game_framework

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

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






walking_focus = [[3, 58], [3, 66], [10, 66], [15, 50], [6, 50], [3, 66], [5, 66]]
Normal_Attack_focus = [[110, 50],[220,60],[325, 75],[425,110], [425,110]]
Speed_Attack_focus = [[2, 50, 485], [2, 50, 485], [755, 110, 480], [2, 100, 405],[110,100,400]]
Charge_Attack_focus = [[2, 50],[110, 50],[220,60],[325, 75],[425,110], [425,110],[540, 100],[540, 100],[540, 100],[645,110]]
Defense_focus = [[445, 30, 340],[498, 35, 340], [540, 35, 340], [592, 42, 330], [636, 42, 340], [0, 50, 210], [50, 50, 210], [113, 50, 210], [163, 50, 210]]



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

        p1.Defense_time = get_time()  # 카운터를 위한 타이머
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
        p_size_x = walking_focus[frame][1]
        p_size_y = 60

        if p1.Picked_Player == 'p1':
            p1.image.clip_draw(62 * frame + walking_focus[frame][0], 655,p_size_x, p_size_y, p1.x,
                               p1.y, p_size_x * 2, p_size_y * 2)

        elif p1.Picked_Player == 'p2':
            p1.image.clip_composite_draw(62 * frame + walking_focus[frame][0], 655, p_size_x, p_size_y, 0, 'h', p1.x, p1.y,
                               p_size_x * 2, p_size_y * 2)


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
        p_size_x = walking_focus[frame][1]
        p_size_y = 60

        if p1.Picked_Player == 'p1':
            if p1.dir == 1:
                p1.image.clip_draw(62 * frame + walking_focus[frame][0], 655, p_size_x, p_size_y, p1.x, p1.y,
                                   p_size_x * 2, p_size_y * 2)
            elif p1.dir == -1:
                p1.image.clip_composite_draw(62 * frame + walking_focus[frame][0], 655, p_size_x, p_size_y, 0, 'h',
                                             p1.x, p1.y, p_size_x * 2, p_size_y * 2)

        elif p1.Picked_Player == 'p2':
            if p1.dir == 1:
                p1.image.clip_draw(62 * frame + walking_focus[frame][0], 655, p_size_x, p_size_y, p1.x, p1.y,
                                   p_size_x * 2, p_size_y * 2)
            elif p1.dir == -1:
                p1.image.clip_composite_draw(62 * frame + walking_focus[frame][0], 655, p_size_x, p_size_y, 0, 'h', p1.x, p1.y,
                                    p_size_x * 2, p_size_y * 2)

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
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
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
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
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
        elif Charge_Attack_Up(e):
            p1.charging = False
            p1.Attacking = True

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        if p1.charging == True:
            p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        elif  p1.charging == False:
            p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
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
            p1.image.clip_draw(Defense_focus[frame][0], Defense_focus[frame][2], p_size_x, p_size_y, p1.x + 30, p1.y, p_size_x * 2, p_size_y * 2)
        elif p1.Picked_Player == 'p2':
            p1.image.clip_composite_draw(Defense_focus[frame][0], Defense_focus[frame][2], p_size_x, p_size_y,
                               0, 'h', p1.x - 30, p1.y, p_size_x * 2, p_size_y * 2)


class StateMachine:
    def __init__(self, meta_knight):
        self.player = meta_knight
        self.cur_state = Idle
        self.transitions = {
            Idle: { Right_Move_Down: Run, Left_Move_Down: Run, Right_Move_Up: Run, Left_Move_Up: Run,
                   Normal_Attack_Down: Normal_Attack, Fast_Attack_Down: Speed_Attack, Charge_Attack_Down: Charge_Attack,
                   Defense_Down: Defense, },

            Run: { Right_Move_Down: Idle, Left_Move_Down: Idle, Right_Move_Up: Idle, Left_Move_Up: Idle,
                  Normal_Attack_Down: Normal_Attack, Fast_Attack_Down: Speed_Attack, Charge_Attack_Down: Charge_Attack,
                  Defense_Down: Defense, STOP: Idle },

            Normal_Attack: {STOP: Run, Right_Move_Down: Run, Left_Move_Down: Run, Right_Move_Up: Run, Left_Move_Up: Run},

            Speed_Attack: {STOP: Run, Right_Move_Down: Run, Left_Move_Down: Run, Right_Move_Up: Run, Left_Move_Up: Run},

            Charge_Attack: {Charge_Attack_Up: Charge_Attack, STOP: Run,
                            Right_Move_Down: Run, Left_Move_Down: Run, Right_Move_Up: Run, Left_Move_Up: Run},

            Defense: { STOP: Run, }


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

    def __init__(self):
        self.x, self.y = 400, 150
        self.Picked_Player = "p2"
        self.frame = 0
        self.dir = 0
        self.charging = False
        self.Attacking = False
        self.Left_Move = False
        self.Right_Move = False
        self.face_dir = 1 # 오른쪽 방향으로 얼굴 향하게
        self.image = load_image('resource/Meta_Knight_3.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

