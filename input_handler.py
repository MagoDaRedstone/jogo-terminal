#input_handler.py:
import os
import sys
from dataclasses import dataclass

@dataclass
class PlayerInput:
    move_x: float = 0
    move_y: float = 0
    rotate: float = 0
    quit: bool = False
    reset: bool = False

class InputHandler:
    def __init__(self):
        self.movement_speed = 0.3
        self.rotation_speed = 0.1

    def get_input(self) -> PlayerInput:
        if os.name == 'posix':
            import tty
            import termios

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        else:
            # Fallback para Windows sem msvcrt
            ch = input().lower()
            if not ch:
                ch = ' '
            else:
                ch = ch[0]

        return self._process_input(ch)

    def _process_input(self, key: str) -> PlayerInput:
        input_state = PlayerInput()

        if key == 'x':
            input_state.quit = True
        elif key == 'r':
            input_state.reset = True
        elif key == 'w':
            input_state.move_y = self.movement_speed
        elif key == 's':
            input_state.move_y = -self.movement_speed
        elif key == 'a':
            input_state.rotate = -self.rotation_speed
        elif key == 'd':
            input_state.rotate = self.rotation_speed
        elif key == 'q':  # Strafe left
            input_state.move_x = -self.movement_speed
        elif key == 'e':  # Strafe right
            input_state.move_x = self.movement_speed

        return input_state
