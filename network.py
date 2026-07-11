import pygame as pg
import random

from node import Node
from layer import Layer


class Network:
    def __init__(self, width: int, height: int, amount: int):
        self.layers: list[Layer] = []
        self.width: int = width
        self.height: int = height
        self.colors = [
            "red",
            "orange",
            "yellow",
            "green",
            "blue",
            "purple",
            "pink",
            "brown",
            "gray",
            "white",
        ]
        self.network_line_width = 2

        self.setup(amount)

    def setup(self, num_layers: int):
        Layer.screenWidth = self.width
        Layer.screenHeight = self.height

        for i in range(num_layers):
            layer = Layer(i)
            self.addLayer(layer)

        for i, layer in enumerate(self.layers):
            layer.setup(i, 10, 10, len(self.layers))

    def addLayer(self, new_layer: Layer):
        if new_layer not in self.layers:
            added: bool = False
            for i, layer in enumerate(self.layers):
                if layer.getId() > new_layer.getId():
                    self.layers.insert(i, new_layer)
                    added = True
                    break
            if not added:
                self.layers.append(new_layer)

    def removeLayer(self, layer: Layer):
        if len(self.layers):
            if layer in self.layers:
                self.layers.remove(layer)

    def zoomIn(self):
        mx, my = pg.mouse.get_pos()
        for i, layer in enumerate(self.layers):
            for node in layer.getNodes():
                cx = node.getCenter()[0]
                cy = node.getCenter()[1]
                dx = cx - mx
                dy = cy - my
                udx = dx / max(1, abs(dx))
                udy = dy / max(1, abs(dy))

                if node.getRadius() < 100:
                    node.setRadius(int(min(100, node.getRadius() + 1)))
                    # node.setCenter(
                    #     (node.getCenter()[0] - udx * 2, node.getCenter()[1] - udy * 2)
                    # )

            layer.fixSpacing(i, len(self.layers))

    def zoomOut(self):
        mx, my = pg.mouse.get_pos()
        for i, layer in enumerate(self.layers):
            for node in layer.getNodes():
                cx = node.getCenter()[0]
                cy = node.getCenter()[1]
                dx = cx - mx
                dy = cy - my
                udx = dx / max(1, abs(dx))
                udy = dy / max(1, abs(dy))

                if node.getRadius() > 10:
                    node.setRadius(int(max(10, node.getRadius() - 1)))
                    # node.setCenter(
                    #     (node.getCenter()[0] + udx * 2, node.getCenter()[1] + udy * 2)
                    # )

            layer.fixSpacing(i, len(self.layers))

    def draw(self, surface, cam_x, cam_y):
        for i in range(len(self.layers) - 1):
            for j in range(len(self.layers[i].getNodes())):
                for k in range(len(self.layers[i + 1].getNodes())):
                    pg.draw.line(
                        surface,
                        self.colors[i],
                        (
                            self.layers[i].getNodes()[j].getCenter()[0] + cam_x,
                            self.layers[i].getNodes()[j].getCenter()[1] + cam_y,
                        ),
                        (
                            self.layers[i + 1].getNodes()[k].getCenter()[0] + cam_x,
                            self.layers[i + 1].getNodes()[k].getCenter()[1] + cam_y,
                        ),
                        self.network_line_width,
                    )
        for i, layer in enumerate(self.layers):
            layer.draw(surface, cam_x, cam_y)
