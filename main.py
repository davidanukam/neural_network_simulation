import pygame as pg
import pywinstyles
import sys

from node import Node
from layer import Layer
from network import Network


def main():
    pg.init()
    pg.font.init()

    font = pg.font.SysFont("arial", 20, True)

    WIDTH, HEIGHT = 1280, 720
    FPS = 60

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Neural Nodes")
    pywinstyles.change_header_color(screen, "black")

    clock = pg.time.Clock()

    network = Network(WIDTH, HEIGHT, 10)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEWHEEL:
                if event.y > 0:
                    network.zoomIn()
                elif event.y < 0:
                    network.zoomOut()

        # -- Update --#

        # -- Draw --#
        screen.fill("black")

        network.draw(screen)

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
