import pygame as pg

pg.init()
WIDTH, HEIGHT = 800, 600
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()


class Object:
    def __init__(self, x, y, color="blue"):
        # self.x and self.y are the immutable WORLD coordinates
        self.x = x
        self.y = y
        self.w = 100
        self.h = 100
        self.color = color
        # self.rect will act as the SCREEN position container
        self.rect = pg.Rect(0, 0, self.w, self.h)

    def get_center(self):
        return self.rect.center

    def update(self, zoom, cam_x, cam_y):
        # 1. Scale the width and height for screen rendering
        scaled_w = int(self.w * zoom)
        scaled_h = int(self.h * zoom)

        # Enforce a minimum size of 1x1 so the rect remains valid
        self.rect.w = max(1, scaled_w)
        self.rect.h = max(1, scaled_h)

        # 2. Translate world position to screen position
        self.rect.x = int(self.x * zoom + cam_x)
        self.rect.y = int(self.y * zoom + cam_y)

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)


# Spawn our objects array
objs: list[Object] = [
    Object(H_WIDTH - 100, H_HEIGHT - 100, color="red"),
    Object(H_WIDTH + 100, H_HEIGHT - 100, color="orange"),
    Object(H_WIDTH - 100, H_HEIGHT + 100, color="yellow"),
    Object(H_WIDTH + 100, H_HEIGHT + 100, color="blue"),
]

zoom_level = 1.0
camera_x, camera_y = 0, 0
panning = False

running = True
while running:
    mx, my = pg.mouse.get_pos()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                panning = True

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                panning = False

        elif event.type == pg.MOUSEMOTION and panning:
            camera_x += event.rel[0]
            camera_y += event.rel[1]

        # --- GLOBAL ZOOM MECHANIC ---
        elif event.type == pg.MOUSEWHEEL:
            # 1. Capture where the mouse is in world space before zooming
            world_m_x = (mx - camera_x) / zoom_level
            world_m_y = (my - camera_y) / zoom_level

            # 2. Apply multiplicative zoom factors
            zoom_factor = 1.1 if event.y > 0 else (1 / 1.1)
            new_zoom = zoom_level * zoom_factor

            # Clamp the zoom so things don't disappear or instantly crash the engine
            zoom_level = max(0.1, min(10.0, new_zoom))

            # 3. Readjust camera position so that the world point remains under the screen mouse coordinates
            camera_x = mx - (world_m_x * zoom_level)
            camera_y = my - (world_m_y * zoom_level)

    # --- Update Phase ---
    for obj in objs:
        obj.update(zoom_level, camera_x, camera_y)

    # --- Drawing Phase ---
    screen.fill((255, 255, 255))

    for obj in objs:
        obj.draw(screen)

    # Crosshair guides
    pg.draw.line(screen, "black", (0, my), (WIDTH, my), 2)
    pg.draw.line(screen, "black", (mx, 0), (mx, HEIGHT), 2)

    # DEBUG
    target_obj = objs[-1]
    obj_center = target_obj.get_center()

    pg.draw.line(screen, "red", obj_center, (mx, obj_center[1]), 2)
    pg.draw.line(screen, "blue", (mx, obj_center[1]), (mx, my), 2)
    pg.draw.line(screen, "green", obj_center, (mx, my), 2)

    pg.display.flip()
    clock.tick(60)

pg.quit()
