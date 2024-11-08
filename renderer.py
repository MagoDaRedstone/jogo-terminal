#render.py:
from typing import List
import os
import sys

from dataclasses import dataclass

@dataclass
class ScreenConfig:
    width: int = 100
    height: int = 30

class Renderer:
    def __init__(self, config: ScreenConfig):
        self.config = config
        # Initialize terminal
        print('\033[?25l')  # Hide cursor
        print('\033[2J')    # Clear screen
        # Disable line wrapping
        print('\033[?7l')
        sys.stdout.write('\033[0;0H')

    def __del__(self):
        # Reset terminal settings on exit
        print('\033[?25h')  # Show cursor
        print('\033[?7h')   # Enable line wrapping

    def create_frame_buffer(self) -> List[List[str]]:
        return [[' ' for _ in range(self.config.width)]
                for _ in range(self.config.height)]

    def render_frame(self, frame_buffer: List[List[str]], stats: dict):
        # Move to top-left and clear screen
        sys.stdout.write('\033[H')

        # Render frame efficiently using join
        frame_str = '\n'.join(''.join(row) for row in frame_buffer)
        sys.stdout.write(frame_str)

        # Print stats and controls
        sys.stdout.write(f"\n\nPosition: ({stats['x']:.1f}, {stats['y']:.1f}) Angle: {stats['angle']:.1f}")
        sys.stdout.write("\nControls: W/S - Move forward/backward, Mouse/A/D - Turn")
        sys.stdout.write("\n         E/Q - Strafe right/left, R - Reset position, X - Quit")
        sys.stdout.flush()
