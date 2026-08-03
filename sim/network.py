import pygame as pg
import random

from node import Node
from layer import Layer


class Network:
    def __init__(
        self, width: int, height: int, num_layers: int, num_nodes: int | list[int]
    ):
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

        self.setup(num_layers, num_nodes)

    def setup(self, num_layers: int, num_nodes: int | list[int]):
        Layer.screenWidth = self.width
        Layer.screenHeight = self.height

        for i in range(num_layers):
            layer = Layer(i)
            self.addLayer(layer)

        if isinstance(num_nodes, int):
            for i, layer in enumerate(self.layers):
                layer.setup(i, num_nodes, 10, len(self.layers))
        elif isinstance(num_nodes, list):
            for i, layer in enumerate(self.layers):
                layer.setup(i, num_nodes[i], 10, len(self.layers))

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

    def update(self):
        pass

    def draw(self, surface: pg.SurfaceType, zoom, cam_x, cam_y):
        for i in range(len(self.layers) - 1):
            for j in range(len(self.layers[i].getNodes())):
                for k in range(len(self.layers[i + 1].getNodes())):
                    x1 = self.layers[i].getNodes()[j].getCenter()[0] * zoom + cam_x
                    y1 = self.layers[i].getNodes()[j].getCenter()[1] * zoom + cam_y

                    x2 = self.layers[i + 1].getNodes()[k].getCenter()[0] * zoom + cam_x
                    y2 = self.layers[i + 1].getNodes()[k].getCenter()[1] * zoom + cam_y

                    if (
                        x1 > 0 and x2 < self.width and y1 > 0 and y2 < self.height
                    ) and (x2 > 0 and x1 < self.width and y2 > 0 and y1 < self.height):
                        pg.draw.line(
                            surface,
                            "white",  # self.colors[i]
                            (x1, y1),
                            (x2, y2),
                            self.network_line_width,
                        )

        for layer in self.layers:
            layer.draw(surface, zoom, cam_x, cam_y)
