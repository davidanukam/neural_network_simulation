import pygame as pg


class Edge:
    screenWidth: int = 0
    screenHeight: int = 0

    def __init__(self, x1: int, y1: int, x2: int, y2: int, state: bool):
        self.x1: int = x1
        self.y1: int = y1
        self.x2: int = x2
        self.y2: int = y2
        self.state: bool = state

    def get_state(self) -> bool:
        return self.state

    def turn_on(self):
        self.state = 1

    def turn_off(self):
        self.state = 0

    def draw(self, surface, zoom, cam_x, cam_y, network_line_width):
        x1 = self.x1 * zoom + cam_x
        y1 = self.y1 * zoom + cam_y

        x2 = self.x2 * zoom + cam_x
        y2 = self.y2 * zoom + cam_y

        if (
            x1 > 0 and x2 < self.screenWidth and y1 > 0 and y2 < self.screenHeight
        ) and (x2 > 0 and x1 < self.screenWidth and y2 > 0 and y1 < self.screenHeight):
            pg.draw.line(
                surface,
                "white",  # self.colors[i]
                (x1, y1),
                (x2, y2),
                network_line_width,
            )
