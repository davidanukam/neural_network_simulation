import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Setup a test object in WORLD coordinates (lives at 400, 300 in our infinite canvas)
obj_surface = pygame.Surface((100, 100))
obj_surface.fill((0, 0, 255))
world_rect = obj_surface.get_rect(center=(400, 300))

# Camera/Canvas offset to track panning
camera_x = 0
camera_y = 0
panning = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Start panning when Left Click is pressed anywhere
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (
                event.button == 1
            ):  # Left click (or use event.button == 2 for Middle Click)
                panning = True

        # Stop panning when Left Click is released
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                panning = False

        # Pan the camera based on relative mouse motion
        elif event.type == pygame.MOUSEMOTION and panning:
            camera_x += event.rel[0]
            camera_y += event.rel[1]

    # --- Drawing Phase ---
    screen.fill((255, 255, 255))

    # Convert WORLD coordinates to SCREEN coordinates by adding the camera offset
    screen_x = world_rect.x + camera_x
    screen_y = world_rect.y + camera_y

    # Draw the object at its screen position
    screen.blit(obj_surface, (screen_x, screen_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
