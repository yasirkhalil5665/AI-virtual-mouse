import time

import numpy as np
from pynput.mouse import Button, Controller

from . import config


class VirtualMouse:
    def __init__(self, screen_w: int, screen_h: int):
        self.mouse = Controller()
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.prev_x, self.prev_y = 0.0, 0.0
        self.last_click_time = 0.0

    def move_to(self, x1: int, y1: int, frame_w: int, frame_h: int):
        reduction = config.FRAME_REDUCTION

        x3 = np.interp(x1, (reduction, frame_w - reduction), (0, self.screen_w))
        y3 = np.interp(y1, (reduction, frame_h - reduction), (0, self.screen_h))

        curr_x = self.prev_x + (x3 - self.prev_x) / config.SMOOTHENING
        curr_y = self.prev_y + (y3 - self.prev_y) / config.SMOOTHENING

        self.mouse.position = (self.screen_w - curr_x, curr_y)
        self.prev_x, self.prev_y = curr_x, curr_y

    def maybe_click(self, distance: float) -> bool:

        if distance >= config.CLICK_DISTANCE_THRESHOLD:
            return False

        now = time.time()
        if now - self.last_click_time <= config.CLICK_DELAY:
            return False

        self.mouse.click(Button.left, 1)
        self.last_click_time = now
        return True
