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
        self.panning = False

        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("Neural Nodes")
        pywinstyles.change_header_color(self.screen, "black")

        self.clock = pg.time.Clock()

        self.network = Network(self.WIDTH, self.HEIGHT, 10)

    def run(self):
        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.MOUSEWHEEL:
                    if event.y > 0:
                        self.network.zoomIn()
                    elif event.y < 0:
                        self.network.zoomOut()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.panning = True

                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.panning = False

                elif event.type == pg.MOUSEMOTION and self.panning:
                    self.camera_x += event.rel[0]
                    self.camera_y += event.rel[1]

            # -- Update --#

            # -- Draw --#
            self.screen.fill("black")

            self.network.draw(self.screen, self.camera_x, self.camera_y)

            pg.display.flip()
            self.clock.tick(self.FPS)

        pg.quit()
        sys.exit()


if __name__ == "__main__":
    sim = Simulation()
    sim.run()
