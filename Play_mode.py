from pico2d import *
import game_framework

import World
import Character_Select_mode
import Title_mode
from Background import BackGround
from player_MetaKnight import MetaKnight
from player_Kirby import Kirby


def P1_handle(event):
    if (event.key == SDLK_q or event.key == SDLK_w or event.key == SDLK_a or event.key == SDLK_s
                            or event.key == SDLK_d or event.key == SDLK_e or event.key == SDLK_f):
        return True
    return False

def P2_handle(event):
    if (event.key == SDLK_COMMA or event.key == SDLK_PERIOD or event.key == SDLK_SLASH or event.key == SDLK_UP
                                or event.key == SDLK_DOWN or event.key == SDLK_LEFT or event.key == SDLK_RIGHT):
        return True
    return False


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if P1_handle(event):
                p1.handle_event(event)
            elif P2_handle(event):
                p2.handle_event(event)


def init():
    global background
    global p1, p2
    global Check_Victory

    picked_p1 = Character_Select_mode.P1
    picked_p2 = Character_Select_mode.P2

    if picked_p1 == 0:
        p1 = Kirby("p1")
    elif picked_p1 == 1:
        p1 = MetaKnight("p1")

    if picked_p2 == 0:
        p2 = Kirby("p2")
    elif picked_p2 == 1:
        p2 = MetaKnight("p2")

    World.add_object(p1, 1)
    World.add_object(p2, 1)

    World.add_collision_pair('p1 : p2_attack_range', p1, p2.attack_area)
    World.add_collision_pair('p1 : p2_Sword_Skill', p1, None)

    World.add_collision_pair('p2 : p1_attack_range', p2, p1.attack_area)
    World.add_collision_pair('p2 : p1_Sword_Skill', p2, None)

    World.add_collision_pair('p1_Sword_Skill : p2_Sword_Skill', None, None)


    background = BackGround()
    World.add_object(background, 0)

    Check_Victory = KO()


def finish():
    World.clear()
    pass


def update():
    World.update()
    World.handle_collisions()
    Check_Victory.update()

    # delay(0.01)


def draw():
    clear_canvas()
    World.render()
    Check_Victory.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass

#game_framework.change_mode(Play_mode)
class KO:
    KO_image = None
    def __init__(self):
        if KO.KO_image == None:
            KO.KO_image = load_image('resource/KO.png')
        self.KO_time = None
        self.drawing = False

    def update(self):
        if p1.Life <= 0 or p2.Life <= 0:
            print("KO")
            self.drawing = True
            if self.KO_time is None:
                self.KO_time = get_time()
            else:
                if get_time() - self.KO_time >= 3:
                    self.KO_time = None
                    game_framework.change_mode(Title_mode)


    def draw(self):
        if self.drawing:
            self.KO_image.clip_draw(0, 0, 473, 228, 500, 300, 300, 150)



