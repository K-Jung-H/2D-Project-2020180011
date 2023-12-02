from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import Mode_Select_mode

TIME_PER_FRAME = 0.3
FRAME_PER_TIME = 1.0 / TIME_PER_FRAME
FRAMES_PER_BACK_EFFECT = 10
black_holl = [0, 260, 520, 780, 1040, 1300]




class Message:
    image = None
    title_image = None

    def __init__(self):
        if Message.image == None:
            Message.image = load_image('resource/start_message.png')
            Message.title_image = load_image('resource/Kirby_Title.png')
        self.x = 500
        self.y = 100
        self.start_time = get_time()


    def update(self):
        pass

    def draw(self):
        if int(get_time() - self.start_time) % 2 == 1:
            self.image.clip_draw(0, 0, 696, 30, self.x, self.y, 600, 50)
        else:
            self.image.clip_draw(0, 30, 696, 59, self.x, self.y, 600, 50)



Moving = [[0,34],[48, 34]]
Fighting = [[92, 38], [142, 38], [192, 37], [241, 37], [285, 38], [335, 38]]

class Animation:
    def __init__(self):
        self.back_image = load_image('resource/Start_Loading_Background.png')
        self.image = load_image('resource/start_animation.png')
        self.Cartoon = 1
        self.c1 = 0
        self.c2 = 1000
        self.frame = 0
        self.sound1 = load_wav('resource/sound/Start_animation_background.wav')
        self.sound1.set_volume(128)
        self.sound1.play()

        self.sound2 = load_wav('resource/sound/Start_star.wav')
        self.sound2.set_volume(128)

        self.sound3 = load_wav('resource/sound/Start_animation_fight.wav')
        self.sound3.set_volume(128)


        self.sound4 = load_wav('resource/sound/Guard.wav')
        self.sound4.set_volume(128)

        self.bgm = load_music('resource/sound/Title_bgm.mp3')
        self.bgm.set_volume(128)


    def draw(self):
        frame = 0
        height = 37
        if self.Cartoon == 1:
            frame = int(self.frame) % 2
            self.image.clip_draw(Moving[frame][0], 0, Moving[frame][1], height, self.c1, 300, Moving[frame][1] * 2, height * 2)
            self.image.clip_composite_draw(Moving[frame][0], 0, Moving[frame][1], height, 0, 'h', self.c2, 300, Moving[frame][1] * 2, height * 2)

        elif self.Cartoon == 2 or self.Cartoon == 3:
            frame = int(self.frame) % 6
            self.image.clip_draw(Fighting[frame][0], 0, Fighting[frame][1], height, self.c1, 300, Fighting[frame][1] * 2, height * 2)
            self.image.clip_composite_draw(Fighting[frame][0], 0, Fighting[frame][1], height, 0, 'h', self.c2, 300, Fighting[frame][1] * 2, height * 2)



    def draw_black(self):
        frame = int(self.frame)
        self.back_image.clip_draw(black_holl[frame], 0, 240, 158, 500, 300, 1000, 600)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_BACK_EFFECT * FRAME_PER_TIME * game_framework.frame_time) % 6
        if self.Cartoon == 1:
            self.c1 += 2
            self.c2 -= 2
            if self.c2 - self.c1 < 200:
                self.Cartoon = 2
                self.sound2.play()

        elif self.Cartoon == 2:
            self.c1 -= 0.3
            self.c2 += 0.3
            if self.c2 - self.c1 >= 300:
                self.Cartoon = 3
                self.sound2.set_volume(0)
                self.sound3.play()


        elif self.Cartoon == 3:
            self.c1 += 10
            self.c2 -= 10
            if self.c2 - self.c1 < 50:
                self.sound3.set_volume(0)
                self.sound1.set_volume(0)
                self.sound4.play()
                self.bgm.repeat_play()
                self.Cartoon = 4



def init():
    global message
    global animation
    global Title_w, Title_h
    Title_w = 0
    Title_h = 0

    message = Message()
    animation = Animation()

def finish():
    animation.sound1.set_volume(0)
    animation.sound2.set_volume(0)
    animation.sound3.set_volume(0)
    animation.sound4.set_volume(0)
    animation.bgm.stop()
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            game_framework.change_mode(Mode_Select_mode)
    pass


def update():
    global Title_w, Title_h
    animation.update()
    if animation.Cartoon == 4:
        Title_w += 50
        Title_h += 50
        Title_w = clamp(0, Title_w, 1000)
        Title_h = clamp(0, Title_h, 600)


def draw():
    clear_canvas()
    animation.draw_black()
    animation.draw()
    if animation.Cartoon == 4:
        message.title_image.clip_draw(0, 0, 4210, 2571, 500, 300, Title_w, Title_h)
    message.draw()
    update_canvas()
    pass

def pause(): pass

def resume(): pass