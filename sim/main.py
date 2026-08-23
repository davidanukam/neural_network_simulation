import pygame as pg
import pywinstyles
import sys

from node import Node
from layer import Layer
from network import Network


class Simulation:
    def __init__(self):
        pg.init()
        pg.font.init()

        self.font = pg.font.SysFont("arial", 20, True)

        self.WIDTH, self.HEIGHT = 1280, 720
        self.FPS = 60

        self.camera_x = 0
        self.camera_y = 0
        self.zoom_level = 1.0
        self.panning = False

        self.clock = pg.time.Clock()

        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption(f"Neural Nodes | FPS: {int(self.clock.get_fps())}")
        pywinstyles.change_header_color(self.screen, "black")

        # self.network = Network(self.WIDTH, self.HEIGHT, 100, 10)
        self.network = Network(self.WIDTH, self.HEIGHT, 3, [784, 10, 10], 10) # [784, 128, 10]

    def run(self):
        self.running = True
        while self.running:
            mx, my = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.panning = True

                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.panning = False

                elif event.type == pg.MOUSEMOTION and self.panning:
                    self.camera_x += event.rel[0]
                    self.camera_y += event.rel[1]

                elif event.type == pg.MOUSEWHEEL:
                    world_m_x = (mx - self.camera_x) / self.zoom_level
                    world_m_y = (my - self.camera_y) / self.zoom_level

                    zoom_factor = 1.1 if event.y > 0 else (1 / 1.1)
                    new_zoom = self.zoom_level * zoom_factor

                    self.zoom_level = max(1.0, min(10.0, new_zoom))

                    self.camera_x = mx - (world_m_x * self.zoom_level)
                    self.camera_y = my - (world_m_y * self.zoom_level)

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.camera_x = 0
                        self.camera_y = 0

                    elif event.key == pg.K_0:
                        self.zoom_level = 1.0

            # -- Update --#
            self.network.update()

            # -- Draw --#
            self.screen.fill("black")

            self.network.draw(
                self.screen, self.zoom_level, self.camera_x, self.camera_y
            )

            pg.display.set_caption(f"Neural Nodes | FPS: {int(self.clock.get_fps())}")

            pg.display.flip()
            self.clock.tick(self.FPS)

        pg.quit()
        sys.exit()


if __name__ == "__main__":
    sim = Simulation()
    sim.run()
