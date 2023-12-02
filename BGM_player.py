from pico2d import *

class BGM:
    def __init__(self):
        self.bgm1 = load_music('resource/sound/Stage1_bgm.mp3')
        self.bgm2 = load_music('resource/sound/Sunset_bgm.mp3')
        self.bgm3 = load_music('resource/sound/Boss_Fight.mp3')
        self.bgm4 = load_music('resource/sound/Sea_bgm.mp3')
        self.set_end = load_wav('resource/sound/stage_select.wav')
        self.game_end_effect = load_wav('resource/sound/mode_select.wav')
        self.out_effect = load_wav('resource/sound/esc.wav')

        self.bgm1.set_volume(64)
        self.bgm2.set_volume(64)
        self.bgm3.set_volume(32)
        self.bgm4.set_volume(64)

        self.set_end.set_volume(64)
        self.game_end_effect.set_volume(64)
        self.out_effect.set_volume(64)




    def play(self, stage):
        if stage == 1:
            self.bgm1.play()
        elif stage == 2:
            self.bgm2.play()
        elif stage == 3:
            self.bgm3.play()
        elif stage == 4:
            self.bgm4.play()
        elif stage == -1:
            self.bgm1.stop()
            self.bgm2.stop()
            self.bgm3.stop()
            self.bgm4.stop()
            self.game_end_effect.play()
            delay(1.0)
        elif stage == -2:
            self.bgm1.stop()
            self.bgm2.stop()
            self.bgm3.stop()
            self.bgm4.stop()
            self.set_end.play()
            delay(1.0)

        elif stage == -3:
            self.bgm1.stop()
            self.bgm2.stop()
            self.bgm3.stop()
            self.bgm4.stop()
            self.out_effect.play()

