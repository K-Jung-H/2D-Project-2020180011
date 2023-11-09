from pico2d import open_canvas, delay, close_canvas
import game_framework
import Title_mode as start_mode
import Play_mode

open_canvas(1000, 600, sync = True)
game_framework.run(start_mode)
close_canvas()

