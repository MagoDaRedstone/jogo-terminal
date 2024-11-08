#main.py:
from typing import List
import math
import time
from engine import RaycastEngine, Point
from renderer import Renderer, ScreenConfig
from input_handler import InputHandler, PlayerInput

class Game:
    def __init__(self):
        self.map_size = 16
        self.reset_player()

        self.screen = ScreenConfig(100, 30)
        self.engine = RaycastEngine(self.map_size, math.pi / 3, 16)
        self.renderer = Renderer(self.screen)
        self.input_handler = InputHandler()

        # Frame timing
        self.target_fps = 30
        self.frame_time = 1.0 / self.target_fps

        # Ensure all map rows have the same length
        self.world_map = [
            "################",
            "#..............#",
            "#....##....##..#",
            "#....##....##..#",
            "#..............#",
            "###.....##..####",
            "#......####....#",
            "#......##......#",
            "#....######....#",
            "#....######....#",
            "#......##......#",
            "####...##....###",
            "#......##......#",
            "#..............#",
            "#..............#",
            "################"
        ]

        # Validate map dimensions
        assert all(len(row) == self.map_size for row in self.world_map), "All map rows must have the same length"

    def reset_player(self):
        self.player = Point(2.0, 2.0)
        self.player_angle = 0

    def update(self, input_state: PlayerInput) -> bool:
        if input_state.quit:
            return False

        if input_state.reset:
            self.reset_player()
            return True

        # Update rotation
        self.player_angle += input_state.rotate

        # Calculate new position with strafing
        cos_a = math.cos(self.player_angle)
        sin_a = math.sin(self.player_angle)

        # Forward/backward movement with smooth interpolation
        new_x = self.player.x + (cos_a * input_state.move_y - sin_a * input_state.move_x)
        new_y = self.player.y + (sin_a * input_state.move_y + cos_a * input_state.move_x)

        # Collision detection with buffer
        buffer = 0.2
        test_x = int(new_x + (buffer if cos_a > 0 else -buffer))
        test_y = int(new_y + (buffer if sin_a > 0 else -buffer))

        # Boundary and collision check
        if (0 <= test_x < self.map_size and
            0 <= test_y < self.map_size and
            self.world_map[test_y][test_x] != '#'):
            self.player.x = max(0.5, min(self.map_size - 0.5, new_x))
            self.player.y = max(0.5, min(self.map_size - 0.5, new_y))

        return True

    def render(self):
        frame = self.renderer.create_frame_buffer()

        for i in range(self.screen.width):
            angle = self.player_angle - self.engine.fov/2 + (i/self.screen.width) * self.engine.fov
            distance, _ = self.engine.cast_ray(self.player, angle, self.world_map)

            # Prevent division by zero and cap wall height
            distance = max(distance, 0.1)
            wall_height = int((self.screen.height / distance) * 2)
            wall_height = min(wall_height, self.screen.height)

            wall_start = (self.screen.height - wall_height) // 2
            wall_end = wall_start + wall_height

            shade = self.engine.get_shade(distance)

            for j in range(self.screen.height):
                if j >= wall_start and j < wall_end:
                    frame[j][i] = shade
                else:
                    frame[j][i] = '.' if j > self.screen.height//2 else ' '

        stats = {
            'x': self.player.x,
            'y': self.player.y,
            'angle': self.player_angle
        }

        self.renderer.render_frame(frame, stats)

    def run(self):
        last_time = time.time()

        while True:
            # Frame timing
            current_time = time.time()
            delta_time = current_time - last_time

            if delta_time >= self.frame_time:
                self.render()
                input_state = self.input_handler.get_input()
                if not self.update(input_state):
                    break
                last_time = current_time
            else:
                # Sleep to maintain consistent frame rate
                time.sleep(max(0, self.frame_time - delta_time))

if __name__ == "__main__":
    game = Game()
    game.run()
