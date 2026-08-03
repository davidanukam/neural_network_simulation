import pygame as pg
import random

from node import Node


class Layer:
    screenWidth: int = 0
    screenHeight: int = 0

    def __init__(self, id: int):
        self.nodes: list[Node] = []
        self.id: int = id

    def setup(self, dex: int, num_ndoes: int, radius: int):
        self.font = pg.sysfont.SysFont("arial", radius * radius)

        for i in range(num_ndoes):
            node = Node(i, random.uniform(0.0, 1.0), 0, radius)

            pos: list[int] = [
                (dex * radius * 10) + radius * 2,
                (i * radius * 2) + (radius * 2),
            ]

            node.setCenter(pos)
            self.addNode(node)

    # TODO: Finish this method
    def setup_centered(
        self, dex: int, num_ndoes: int, radius: int, prev_height: int
    ) -> int:
        self.font = pg.sysfont.SysFont("arial", radius)

        def get_layer_height(num_ndoes: int, radius: int) -> int:
            height = 0

            for i in range(num_ndoes):
                y = (i * radius * 2) + (radius * 2)
                height += y // radius

            return height

        layer_height = get_layer_height(num_ndoes, radius)

        for i in range(num_ndoes):
            node = Node(i, random.uniform(0.0, 1.0), 0, radius)

            # pos: list[int] = [
            #     (dex * node.getRadius() * 10) + node.getRadius() * 2,
            #     (i * node.getRadius() * 2)
            #     + (node.getRadius() * 1.5)
            #     + (prev_height // 2),
            # ]

            pos: list[int] = [
                (dex * radius * 10) + radius() * 2,
                (i * radius * 2) + (radius * 2) + (prev_height // 2),
                -(layer_height // 2),
            ]

            node.setCenter(pos)
            self.addNode(node)

        return layer_height

    def getId(self) -> int:
        return self.id

    def setId(self, new_id: int):
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
        for node in self.nodes:
            node.setWeight(random.uniform(0.0, 1.0))
            if random.randint(0, 1):
                node.turn_on()
            else:
                node.turn_off()

    def draw(self, surface: pg.SurfaceType, zoom, cam_x, cam_y):
        for node in self.nodes:
            screen_x = int(node.getCenter()[0] * zoom + cam_x)
            screen_y = int(node.getCenter()[1] * zoom + cam_y)

            screen_radius = max(1, int(node.getRadius() * zoom))

            if (
                screen_x + screen_radius >= 0
                and screen_x - screen_radius <= self.screenWidth
                and screen_y + screen_radius >= 0
                and screen_y - screen_radius <= self.screenHeight
            ):
                pg.draw.circle(
                    surface,
                    "black",
                    (screen_x, screen_y),
                    screen_radius,
                )

                node.color = "white" if node.state == 0 else "green"

                pg.draw.circle(
                    surface,
                    node.color,
                    (screen_x, screen_y),
                    screen_radius,
                    3,
                )

                weight_text = f"{round(node.getWeight(), 1)}"
                weight_surface = self.font.render(weight_text, True, node.color)

                # Scale proportionally based on node radius
                orig_w, orig_h = weight_surface.get_size()
                target_h = int(screen_radius * 0.8)  # Leave padding around text

                if orig_h > 0 and target_h > 0:
                    aspect_ratio = orig_w / orig_h
                    target_w = int(target_h * aspect_ratio)

                    scaled_weight_surface = pg.transform.smoothscale(
                        weight_surface, (target_w, target_h)
                    )

                    # Center the text directly onto (screen_x, screen_y)
                    scaled_weight_rect = scaled_weight_surface.get_rect(
                        center=(screen_x, screen_y)
                    )

                    surface.blit(scaled_weight_surface, scaled_weight_rect)
