#engine.py:
import math
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

class RaycastEngine:
    def __init__(self, map_size: int, fov: float, depth: float):
        self.map_size = map_size
        self.fov = fov
        self.depth = depth

    def cast_ray(self, player: Point, angle: float, world_map: List[str]) -> Tuple[float, str]:
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)

        distance = 0.0
        step = 0.05  # Smaller step size for more precise collision detection

        while distance < self.depth:
            # Calculate test position
            test_x = int(player.x + distance * cos_a)
            test_y = int(player.y + distance * sin_a)

            # Boundary check
            if (test_x < 0 or test_x >= len(world_map[0]) or
                test_y < 0 or test_y >= len(world_map)):
                return self.depth, ' '

            # Safe array access
            try:
                hit_char = world_map[test_y][test_x]
                if hit_char == '#':
                    return distance, hit_char
            except IndexError:
                return self.depth, ' '

            distance += step

        return self.depth, ' '

    def get_shade(self, distance: float) -> str:
        if distance <= self.depth/4:
            return '█'
        elif distance <= self.depth/3:
            return '▓'
        elif distance <= self.depth/2:
            return '▒'
        elif distance <= self.depth:
            return '░'
        return ' '
