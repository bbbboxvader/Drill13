from pico2d import *
import game_framework
import game_world


image = None


def init():
    global image
    image = load_image('item_select.png')


def finish():
    global image
    image = None


def update():
    pass  # 아이템 선택 중에는 게임 월드가 움직이지 않는다.


def render():
    clear_canvas()
    game_world.render()
    image.draw(400, 300)
    update_canvas()


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        if event.type != SDL_KEYDOWN:
            continue
        if event.key in (SDLK_0,):
            import play_mode
            play_mode.boy.select_ball(event.key - SDLK_0)
            game_framework.pop_mode()
            return
        if event.key in (SDLK_i, SDLK_ESCAPE):
            game_framework.pop_mode()
            return


def pause():
    pass


def resume():
    pass
