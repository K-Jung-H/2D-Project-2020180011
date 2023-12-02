from pico2d import *

player_character = 'Master_Kirby'
player_side = 'Left'
p1_score = 2
p2_score = 2
difficulty = 1

solo_mode_result = None

Background_stage = 1

number_list = [[25, 8], [35, 6], [43, 8], [53, 8], [63, 8]]

class Score:
    image = None
    def __init__(self):
        if Score.image is None:
            Score.image = load_image('resource/Life.png')

    def draw(self):
        num_height = 16
        #p1
        p1_point = clamp(0 , p1_score, 4)

        self.image.clip_draw(0, 0, 34, 16, 40, 480, 80, 50)
        self.image.clip_draw(number_list[p1_point][0], 0, number_list[p1_point][1], 16, 40 + 50, 480, number_list[p1_point][1] * 2, 50)

        #p2
        p2_point = max(0, p2_score)
        self.image.clip_draw(0, 0, 34, 16, 930, 480, 80, 50)
        self.image.clip_draw(number_list[p2_point][0], 0, number_list[p2_point][1], 16, 980, 480, number_list[p2_point][1] * 2, 50)
