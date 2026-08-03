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
        self.color = "white"

    def get_state(self) -> bool:
        return self.state

    def turn_on(self):
        self.state = 1

    def turn_off(self):
        self.state = 0

    def draw(self, surface, zoom, cam_x, cam_y, network_line_width, node_radius) -> int:
        x1 = self.x1 * zoom + cam_x
        y1 = self.y1 * zoom + cam_y

        x2 = self.x2 * zoom + cam_x
        y2 = self.y2 * zoom + cam_y

        screen_radius = max(1, int(node_radius * zoom))

        # NOTE: Keep all edges visible
        # # Compute bounding box of the line segment
        # min_x = min(x1, x2) - screen_radius
        # max_x = max(x1, x2) + screen_radius
        # min_y = min(y1, y2) - screen_radius
        # max_y = max(y1, y2) + screen_radius

        # # Draw ONLY IF the segment intersects the screen rect
        # if (
        #     max_x >= 0
        #     and min_x <= self.screenWidth
        #     and max_y >= 0
        #     and min_y <= self.screenHeight
        # ):
        #     self.color = "white" if self.state == 0 else "green"

        #     pg.draw.line(
        #         surface,
        #         self.color,
        #         (x1, y1),
        #         (x2, y2),
        #         network_line_width,
        #     )
        #     return 1
        # return 0

        # NOTE: Remove edges that have offscreen endpoints
        # if (
        #     x1 + screen_radius >= 0
        #     and x2 - screen_radius <= self.screenWidth
        #     and y1 + screen_radius >= 0
        #     and y2 - screen_radius <= self.screenHeight
        # ) and (
        #     x2 + screen_radius >= 0
        #     and x1 - screen_radius <= self.screenWidth
        #     and y2 + screen_radius >= 0
        #     and y1 - screen_radius <= self.screenHeight
        # ):
        #     self.color = "white" if self.state == 0 else "yellow"

        #     pg.draw.line(
        #         surface,
        #         self.color,
        #         (x1, y1),
        #         (x2, y2),
        #         network_line_width,
        #     )
        #     return 1
        # return 0

        # NOTE: Remove edges that have offscreen RIGHT, BOTTOM and TOP endpoints
        if (
            x2 - screen_radius <= self.screenWidth
            and y1 + screen_radius >= 0
            # and y2 - screen_radius <= self.screenHeight
        ) and (
            x2 + screen_radius >= 0
            and y2 + screen_radius >= 0
            and y1 - screen_radius <= self.screenHeight
        ):
            self.color = "white" if self.state == 0 else "green"

            pg.draw.line(
                surface,
                self.color,
                (x1, y1),
                (x2, y2),
                network_line_width,
            )
            return 1
        return 0

        # # NOTE: Remove edges that have offscreen RIGHT & LEFT endpoints, and BOTTOM and TOP endpoints
        # if (
        #     x1 + screen_radius >= 0
        #     or x2 - screen_radius <= self.screenWidth
        #     and y1 + screen_radius >= 0
        #     or y2 - screen_radius <= self.screenHeight
        # ) and (
        #     x2 + screen_radius >= 0
        #     or x1 - screen_radius <= self.screenWidth
        #     and y2 + screen_radius >= 0
        #     or y1 - screen_radius <= self.screenHeight
        # ):
        #     self.color = "white" if self.state == 0 else "green"

        #     pg.draw.line(
        #         surface,
        #         self.color,
        #         (x1, y1),
        #         (x2, y2),
        #         network_line_width,
        #     )
        #     return 1
        # return 0
