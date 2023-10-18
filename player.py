# 이것은 각 상태들을 객체로 구현한 것임.
import math

from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP, SDLK_a


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def Auto_Run_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def Auto_Run_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

class Run:

    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy.dir, boy.action = 1, 1
        elif left_down or right_up(e): # 왼쪽으로 RUN
            boy.dir, boy.action = -1, 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5
        if boy.x <= 50:  boy.x += 5
        elif boy.x >= 800: boy.x -= 5
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)



class Idle:

    @staticmethod
    def enter(boy, e):
        if boy.action == 0:
            boy.action = 2
        elif boy.action == 1:
            boy.action = 3
        boy.frame = 0
        boy.start_time = get_time()
        print('Idle Enter')

    @staticmethod
    def exit(boy, e):
        print('Idle Exit')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3.0:
            boy.state_machine.handle_event(('TIME_OUT', 0))
        print('Idle Do')

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass


class Sleep:

    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        print('고개 숙이기')

    @staticmethod
    def exit(boy, e):
        print('고개 들기')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        print('드르렁')

    @staticmethod
    def draw(boy):
        if boy.action == 2:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100, math.pi/2, '',
                                      boy.x + 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100, math.pi/2, '',
                                      boy.x + 25, boy.y - 25, 100, 100)
        pass

class Auto_Run:

    @staticmethod
    def enter(boy, e):
        if  boy.action == 0 or boy.action == 2:
            boy.dir, boy.action = -1, 0
        elif  boy.action == 1 or boy.action == 3:
            boy.dir, boy.action = 1, 1

        boy.frame = 0
        boy.start_time = get_time()
        print('무적모드 시작')

    @staticmethod
    def exit(boy, e):
        print('무적 모드 끝')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if  boy.x <= 50 or boy.x >= 800: # 경계 면에 닿게 되면 방향 전환
            boy.dir *= -1
            if boy.dir < 0:
                boy.action = 0
                print('자동 방향 전환')
            else:
                boy.action = 1
                print('자동 방향 전환')

        boy.x += boy.dir * 10
        last_time = 5 - (get_time() - boy.start_time)
        if last_time <= 0.0:
            boy.state_machine.handle_event(('TIME_OUT', 0))
        print('무적 남은 시간: ', last_time)

    @staticmethod
    def draw(boy):
        if boy.action == 1:
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y + 30, 200, 200)
        elif boy.action == 0:
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y + 30, 200, 200)
        pass

class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.table = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run,
                   Auto_Run_down: Auto_Run, Auto_Run_up: Auto_Run, time_out: Sleep},
            Run: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle,
                  Auto_Run_down: Idle,  Auto_Run_up: Idle},
            Sleep: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Idle,
                    Auto_Run_down: Auto_Run, Auto_Run_up: Auto_Run,},
            Auto_Run: {right_down: Run, left_down: Run,  time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('START', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True # 성공적으로 이벤트 변환

        return False # 이벤트를 소모하지 못함

    def draw(self):
        self.cur_state.draw(self.boy)





class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.image = load_image('resource/Sword_Kirby.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    #pico2d event --> state event handling
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
