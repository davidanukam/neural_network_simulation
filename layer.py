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

            pos: tuple = (
                (dex * node.getRadius() * length) + node.getRadius(),
                (i * node.getRadius() * 2) + node.getRadius(),
            )

            node.setCenter(pos)
            self.addNode(node)

    def fixSpacing(self, dex: int, length: int):
        for i, node in enumerate(self.nodes):
            pos: tuple = (
                (dex * node.getRadius() * length) + node.getRadius(),
                (i * node.getRadius() * 2) + node.getRadius(),
            )

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

    def draw(self, surface, cam_x, cam_y):
        for node in self.nodes:
            pg.draw.circle(
                surface,
                "black",
                (node.getCenter()[0] + cam_x, node.getCenter()[1] + cam_y),
                node.getRadius(),
            )
            pg.draw.circle(
                surface,
                "white",
                (node.getCenter()[0] + cam_x, node.getCenter()[1] + cam_y),
                node.getRadius(),
                3,
            )
