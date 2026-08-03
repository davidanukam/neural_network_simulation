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
        for i in range(num_ndoes):
            node = Node(i, random.uniform(0.0, 1.0), radius)

            pos: list[int] = [
                (dex * node.getRadius() * length) + node.getRadius(),
                (i * node.getRadius() * 2) + node.getRadius(),
            ]

            node.setCenter(pos)
            self.addNode(node)

    # NOTE: Can Remove Later
    def fixSpacing(self, dex: int, length: int):
        for i, node in enumerate(self.nodes):
            pos: list[int] = [
                (dex * node.getRadius() * length) + node.getRadius(),
                (i * node.getRadius() * 2) + node.getRadius(),
            ]

            node.setCenter(pos)

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

    def draw(self, surface, zoom, cam_x, cam_y):
        for node in self.nodes:

            screen_x = int(node.getCenter()[0] * zoom + cam_x)
            screen_y = int(node.getCenter()[1] * zoom + cam_y)

            screen_radius = max(1, int(node.getRadius() * zoom))

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
