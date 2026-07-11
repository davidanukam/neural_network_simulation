import pygame as pg
import math

pg.init()
WIDTH, HEIGHT = 800, 600
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()


class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 100
        self.h = 100
        self.rect = pg.Rect(x, y, self.w, self.h)

    def get_center(self):
        return (self.rect.x + (self.rect.w // 2), self.rect.y + (self.rect.h // 2))

    def get_size(self):
        return (self.rect.w, self.rect.h)

    def get_rect(self):
        return self.rect

    def set_rect(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, cam_x, cam_y):
        self.rect.x = self.x + cam_x
        self.rect.y = self.y + cam_y

    def draw(self, surface):
        pg.draw.rect(surface, "blue", self.rect)


obj = Object(H_WIDTH, H_HEIGHT)

# Camera/Canvas offset to track panning
camera_x = 0
camera_y = 0
panning = False

running = True
while running:
    x, y = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Start panning when Left Click is pressed anywhere
        elif event.type == pg.MOUSEBUTTONDOWN:
            if (
                event.button == 1
            ):  # Left click (or use event.button == 2 for Middle Click)
                panning = True

        # Stop panning when Left Click is released
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                panning = False

        # Pan the camera based on relative mouse motion
        elif event.type == pg.MOUSEMOTION and panning:
            camera_x += event.rel[0]
            camera_y += event.rel[1]

        elif event.type == pg.MOUSEWHEEL:
            if event.y > 0:
                # print(f"UP: {x - H_WIDTH}, {y - H_HEIGHT}")

                # dis = abs(obj.get_rect().center)
                dis = abs(math.dist((x, y), obj.get_center()))
                print(f"dis: {dis}")
                factor = 10

                dir = -(x - H_WIDTH) / abs(x - H_WIDTH)
                print(f"dir: {dir}")

                camera_x += dir * (dis / factor)
                camera_y += -(y - H_HEIGHT) / abs(y - H_HEIGHT) * 20
                # print(f"camera: {camera_x}, {camera_y}")
                obj.rect.w += 10
                obj.rect.h += 10
            if event.y < 0:
                # print(f"DOWN: {x - H_WIDTH}, {y - H_HEIGHT}")
                if obj.get_size()[0] > 10 and obj.get_size()[1] > 10:
                    obj.rect.w -= 10
                    obj.rect.h -= 10

                    camera_x += (x - H_WIDTH) / abs(x - H_WIDTH) * 20
                    camera_y += (y - H_HEIGHT) / abs(y - H_HEIGHT) * 20

    # --- Update Phase --- #
    obj.update(camera_x, camera_y)

    # --- Drawing Phase --- #
    screen.fill((255, 255, 255))

    # Draw the object at its screen position
    obj.draw(screen)

    pg.draw.line(screen, "black", (0, y), (WIDTH, y), 2)
    pg.draw.line(screen, "black", (x, 0), (x, HEIGHT), 2)
    pg.draw.line(
        screen,
        "red",
        (obj.get_center()[0], obj.get_center()[1]),
        (x, y),
        2,
    )

    pg.display.flip()
    clock.tick(60)

pg.quit()
