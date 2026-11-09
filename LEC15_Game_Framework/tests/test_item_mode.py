from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pico2d
import ball
import boy
import game_framework
import game_world
import item_mode
import play_mode


class ItemModeTests(unittest.TestCase):
    def setUp(self):
        self.small_image = Mock(name='21x21')
        self.large_image = Mock(name='41x41')
        self.menu_image = Mock(name='item_select')
        images = {'ball21x21.png': self.small_image, 'ball41x41.png': self.large_image}
        patches = [
            patch('boy.load_image', return_value=Mock()),
            patch('boy.get_time', return_value=100.0),
            patch('boy.get_canvas_width', return_value=800),
            patch('ball.load_image', side_effect=lambda name: images[name]),
            patch('ball.get_canvas_width', return_value=800),
            patch('item_mode.load_image', return_value=self.menu_image),
        ]
        for patcher in patches:
            patcher.start()
            self.addCleanup(patcher.stop)
        ball.Ball.images.clear()
        game_world.clear()
        game_framework.stack[:] = [play_mode]
        game_framework.running = True
        self.player = boy.Boy()
        play_mode.boy = self.player
        game_world.add_oject(self.player)
        self.addCleanup(game_world.clear)
        self.addCleanup(game_framework.stack.clear)

    @staticmethod
    def event(key, kind=pico2d.SDL_KEYDOWN):
        return SimpleNamespace(type=kind, key=key)

    def enter_menu(self):
        with patch('play_mode.get_events', return_value=[self.event(pico2d.SDLK_i)]):
            play_mode.handle_events()
        self.assertIs(game_framework.stack[-1], item_mode)

    def item_event(self, event):
        with patch('item_mode.get_events', return_value=[event]):
            item_mode.handle_events()

    def projectiles(self):
        return [obj for layer in game_world.world for obj in layer if isinstance(obj, ball.Ball)]

    def test_i_opens_selection_overlay_on_top_of_existing_world(self):
        self.enter_menu()
        with patch('item_mode.clear_canvas'), patch('item_mode.update_canvas'), patch('game_world.render') as render:
            item_mode.render()
        render.assert_called_once()
        self.menu_image.draw.assert_called_once_with(400, 300)

    def test_one_selects_small_ball_and_returns_to_play(self):
        self.enter_menu()
        self.item_event(self.event(pico2d.SDLK_1))
        self.assertIs(game_framework.stack[-1], play_mode)
        self.player.handle_event(self.event(pico2d.SDLK_SPACE))
        self.assertEqual(self.projectiles()[-1].ball_type, 1)
        self.assertIs(self.projectiles()[-1].image, self.small_image)

    def test_two_selects_large_ball_without_changing_existing_balls(self):
        self.player.handle_event(self.event(pico2d.SDLK_SPACE))
        small = self.projectiles()[-1]
        self.enter_menu()
        self.item_event(self.event(pico2d.SDLK_2))
        self.player.face_dir = -1
        self.player.handle_event(self.event(pico2d.SDLK_SPACE))
        large = self.projectiles()[-1]
        self.assertEqual((small.ball_type, large.ball_type, large.velocity), (1, 2, -10))
        self.assertIs(small.image, self.small_image)
        self.assertIs(large.image, self.large_image)

    def test_zero_disables_new_shots_but_keeps_existing_balls(self):
        self.player.handle_event(self.event(pico2d.SDLK_SPACE))
        old_balls = self.projectiles()
        self.enter_menu()
        self.item_event(self.event(pico2d.SDLK_0))
        self.player.handle_event(self.event(pico2d.SDLK_SPACE))
        self.assertEqual(self.player.selected_ball, 0)
        self.assertEqual(self.projectiles(), old_balls)

    def test_space_still_wakes_sleeping_boy_when_shooting_is_disabled(self):
        self.player.select_ball(0)
        self.player.fall_asleep()
        self.player.handle_event(self.event(pico2d.SDLK_SPACE))
        self.assertEqual(self.player.state, 'IDLE')
        self.assertEqual(self.projectiles(), [])
        self.player.handle_event(self.event(pico2d.SDLK_SPACE))
        self.assertEqual(self.projectiles(), [])

    def test_escape_or_i_closes_menu_without_changing_selection(self):
        for key in (pico2d.SDLK_ESCAPE, pico2d.SDLK_i):
            with self.subTest(key=key):
                self.player.select_ball(2)
                self.enter_menu()
                self.item_event(self.event(key))
                self.assertIs(game_framework.stack[-1], play_mode)
                self.assertEqual(self.player.selected_ball, 2)

    def test_direction_key_release_in_menu_does_not_leave_boy_running(self):
        self.player.handle_event(self.event(pico2d.SDLK_LEFT))
        self.assertEqual(self.player.state, 'RUN')
        self.enter_menu()
        x = self.player.x
        item_mode.update()
        self.assertEqual(self.player.x, x)
        self.item_event(self.event(pico2d.SDLK_LEFT, pico2d.SDL_KEYUP))
        self.assertEqual(self.player.state, 'IDLE')
        self.item_event(self.event(pico2d.SDLK_1))
        self.assertIs(game_framework.stack[-1], play_mode)

    def test_window_close_exits_the_game(self):
        self.enter_menu()
        self.item_event(SimpleNamespace(type=pico2d.SDL_QUIT))
        self.assertFalse(game_framework.running)

    def test_images_are_cached_per_ball_type(self):
        for kind in (1, 1, 2, 2):
            self.player.select_ball(kind)
            self.player.fire_ball()
        self.assertEqual(ball.load_image.call_count, 2)
        self.assertEqual(len(self.projectiles()), 4)

    def test_invalid_selection_is_rejected(self):
        with self.assertRaises(ValueError):
            self.player.select_ball(3)
        with self.assertRaises(ValueError):
            ball.Ball(0, 0, 10, 3)


if __name__ == '__main__':
    unittest.main()
