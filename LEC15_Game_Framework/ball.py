from pico2d import get_canvas_width, load_image

import game_world


class Ball:
    images = {}
    IMAGE_FILES = {1: 'ball21x21.png', 2: 'ball41x41.png'}

    def __init__(self, x, y, velocity, ball_type=1):
        if ball_type not in self.IMAGE_FILES:
            raise ValueError('발사할 공은 1 또는 2여야 합니다.')
        if ball_type not in Ball.images:
            Ball.images[ball_type] = load_image(self.IMAGE_FILES[ball_type])
        self.image = Ball.images[ball_type]
        self.ball_type = ball_type
        self.x, self.y = x, y
        self.velocity = velocity

    def update(self):
        self.x += self.velocity
        if self.x < 0 or self.x > get_canvas_width():
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)
