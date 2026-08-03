import pygame as pg
import random

from node import Node


class Layer:
    screenWidth: int = 0
    screenHeight: int = 0

    def __init__(self, id: int):
        self.nodes: list[Node] = []
        self.id: int = id

    def setup(self, dex: int, num_ndoes: int, radius: int, length: int):
        self.font = pg.sysfont.SysFont("arial", radius)

        for i in range(num_ndoes):
            node = Node(i, random.uniform(0.0, 1.0), radius)

            pos: list[int] = [
                (dex * node.getRadius() * length) + node.getRadius(),
                (i * node.getRadius() * 2) + node.getRadius(),
            ]

            node.setCenter(pos)
            self.addNode(node)

    def getId(self) -> int:
        return self.id

    def setId(self, new_id: int) -> int:
        self.id = new_id

    def getNodes(self) -> list[Node]:
        return self.nodes

    def addNode(self, new_node: Node):
        if new_node not in self.nodes:
            added: bool = False
            for i, node in enumerate(self.nodes):
                if node.getId() > new_node.getId():
                    self.nodes.insert(i, new_node)
                    added = True
                    break
            if not added:
                self.nodes.append(new_node)

    def removeNode(self, node: Node):
        if len(self.nodes):
            if node in self.nodes:
                self.nodes.remove(node)

    def update(self):
        pass

    def draw(self, surface: pg.SurfaceType, zoom, cam_x, cam_y):
        for node in self.nodes:

            screen_x = int(node.getCenter()[0] * zoom + cam_x)
            screen_y = int(node.getCenter()[1] * zoom + cam_y)

            screen_radius = max(1, int(node.getRadius() * zoom))

            if (
                screen_x - screen_radius > 0
                and screen_x + screen_radius < self.screenWidth
                and screen_y - screen_radius > 0
                and screen_y + screen_radius < self.screenHeight
            ):
                pg.draw.circle(
                    surface,
                    "black",
                    (screen_x, screen_y),
                    screen_radius,
                )
                pg.draw.circle(
                    surface,
                    "white",
                    (screen_x, screen_y),
                    screen_radius,
                    3,
                )

                weight_surface = self.font.render(
                    f"{round(node.getWeight(), 1)}", True, "white"
                )
                weight_rect = weight_surface.get_rect()
                weight_rect.x = (
                    node.getCenter()[0] - (weight_rect.w // 2)
                ) * zoom + cam_x
                weight_rect.y = (
                    node.getCenter()[1] - (weight_rect.h // 2)
                ) * zoom + cam_y
                scaled_weight_surface = pg.transform.smoothscale(
                    weight_surface, (screen_radius, screen_radius)
                )
                surface.blit(scaled_weight_surface, weight_rect)
