import pygame as pg
import random

from package.sim.node import Node
from package.sim.layer import Layer
from package.sim.edge import Edge


class Network:

    def __init__(
        self,
        width: int,
        height: int,
        num_layers: int,
        num_nodes: int | list[int],
        node_radius: int,
    ):
        self.layers: list[Layer] = []
        self.edges: list[Edge] = []

        self.width: int = width
        self.height: int = height

        self.network_line_width = 2
        self.node_radius = node_radius

        self.setup(num_layers, num_nodes, self.node_radius)

    def setup(self, num_layers: int, num_nodes: int | list[int], node_radius: int):
        Layer.screenWidth = self.width
        Layer.screenHeight = self.height
        Edge.screenWidth = self.width
        Edge.screenHeight = self.height

        for i in range(num_layers):
            layer = Layer(i)
            self.addLayer(layer)

        # TODO: Used for centering each layer relative to the previous one
        # prev_height = 0
        # if isinstance(num_nodes, int):
        #     for i, layer in enumerate(self.layers):
        #         height = layer.setup_centered(i, num_nodes, 10, prev_height)
        #         print(height)
        #         prev_height = height
        # elif isinstance(num_nodes, list):
        #     for i, layer in enumerate(self.layers):
        #         height = layer.setup_centered(i, num_nodes[i], 10, prev_height)
        #         print(height)
        #         prev_height = height

        if isinstance(num_nodes, int):
            for i, layer in enumerate(self.layers):
                layer.setup(i, num_nodes, node_radius)
        elif isinstance(num_nodes, list):
            for i, layer in enumerate(self.layers):
                layer.setup(i, num_nodes[i], node_radius)

        for i in range(len(self.layers) - 1):
            for j in range(len(self.layers[i].getNodes())):
                for k in range(len(self.layers[i + 1].getNodes())):
                    self.edges.append(
                        Edge(
                            self.layers[i].getNodes()[j].getCenter()[0],
                            self.layers[i].getNodes()[j].getCenter()[1],
                            self.layers[i + 1].getNodes()[k].getCenter()[0],
                            self.layers[i + 1].getNodes()[k].getCenter()[1],
                            0,
                        )
                    )

        # Note: Testing node and edge state and color changes
        # for i in range(random.randint(1, len(self.edges))):
        #     dex = random.randint(0, len(self.edges) - 1)
        #     self.edges[dex].turn_on()

        # for i in range(random.randint(1, len(self.layers))):
        #     for j in range(random.randint(1, len(self.layers[i].getNodes()))):
        #         dex = random.randint(0, len(self.layers[i].getNodes()) - 1)
        #         self.layers[i].getNodes()[dex].turn_on()

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

    def getLayers(self) -> list[Layer]:
        return self.layers

    # Note: Testing states and weights
    def update(self):
        for layer in self.layers:
            layer.update()

        for edge in self.edges:
            if random.randint(0, 1):
                edge.turn_on()
            else:
                edge.turn_off()

    def draw(self, surface: pg.SurfaceType, zoom, cam_x, cam_y):
        num = 0
        for edge in self.edges:
            num += edge.draw(
                surface, zoom, cam_x, cam_y, self.network_line_width, self.node_radius
            )
        # print(num) # Debugging

        for layer in self.layers:
            layer.draw(surface, zoom, cam_x, cam_y)
