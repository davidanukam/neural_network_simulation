import pygame as pg
import pywinstyles
import sys
import random

from package.mnist import mnist

from package.sim.network import Network


class Simulation:
    def __init__(self):
        pg.init()
        pg.font.init()

        self.font = pg.font.SysFont("arial", 20, True)
        self.font2 = pg.font.SysFont("arial", 50, True)
        self.font3 = pg.font.SysFont("arial", 30, True)

        self.WIDTH, self.HEIGHT = 1280, 720
        self.FPS = 60

        self.sim_area_width = self.WIDTH - 500
        self.sim_area_height = self.HEIGHT

        self.camera_x = 0
        self.camera_y = 0
        self.zoom_level = 1.0
        self.panning = False

        self.clock = pg.time.Clock()
        self.timer = 1
        self.waiter = 1

        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption(f"Neural Nodes | FPS: {int(self.clock.get_fps())}")
        pywinstyles.change_header_color(self.screen, "black")

        # self.network = Network(self.WIDTH, self.HEIGHT, 100, 10)
        # [784, 128, 10]
        self.network = Network(
            self.sim_area_width, self.sim_area_height, 3, [784, 10, 10], 10
        )

        # --- MNIST --- #
        self.W1, self.b1, self.W2, self.b2 = mnist.init_params()
        self.predict = mnist.Y_train
        self.acc = 0.0
        self.update_weights()

    def update_weights(self):
        W1_sum = [sum(row) / len(row) for row in self.W1.T]
        W2_sum = [sum(row) / len(row) for row in self.W2.T]

        for i, node in enumerate(self.network.getLayers()[0].getNodes()):
            node.setWeight(W1_sum[i])

        for i, node in enumerate(self.network.getLayers()[1].getNodes()):
            node.setWeight(W2_sum[i])

        for i, node in enumerate(self.network.getLayers()[2].getNodes()):
            node.setWeight(0.0)

        self.rand_idx = random.randint(0, len(self.predict))
        self.network.getLayers()[2].getNodes()[self.predict[self.rand_idx]].setWeight(
            1.0
        )

    def ndarray_to_surface(
        self, img_array: mnist.np.ndarray, scale_factor: int = 10
    ) -> pg.Surface:
        """Converts a 1D or 2D MNIST numpy array into a Pygame Surface.

        - img_array: numpy array of shape (784,) or (28, 28)
        - scale_factor: upscale multiplier (e.g., 10 turns 28x28 into 280x280)
        """
        # 1. Ensure 1D array of 784 elements regardless of input shape (784, 1), (1, 784), or (784,)
        img_flat = img_array.flatten()

        if img_flat.size != 784:
            raise ValueError(
                f"Expected 784 pixels for MNIST image, got {img_flat.size}"
            )

        # 1. Reshape to 28x28 if 1D flat array
        img_2d = img_flat.reshape((28, 28))

        # 2. Scale float values [0.0, 1.0] to integer pixel values [0, 255] if necessary
        if img_2d.max() <= 1.0:
            img_2d = img_2d * 255.0

        # 3. Ensure uint8 data type and transpose (X, Y) for Pygame
        img_uint8 = img_2d.astype(mnist.np.uint8).T

        # 4. Repeat 2D grayscale values into 3D RGB channels (28, 28, 3)
        rgb_array = mnist.np.repeat(img_uint8[:, :, mnist.np.newaxis], 3, axis=2)

        # 5. Create Pygame surface directly from the array
        surface = pg.surfarray.make_surface(rgb_array)

        # 6. Upscale (28x28 is tiny on modern displays)
        if scale_factor > 1:
            w, h = surface.get_size()
            surface = pg.transform.scale(surface, (w * scale_factor, h * scale_factor))

        return surface

    def draw_image_and_prediction(self):
        # 1. Fetch labels and the target image from X_train
        predicted_label = self.predict[self.rand_idx]
        actual_label = mnist.Y_train[self.rand_idx]
        actual_img_array = mnist.X_train[:, self.rand_idx]

        # 2. Find a sample in X_train that actually belongs to the PREDICTED class
        # Get all indices in Y_train matching predicted_label
        pred_indices = mnist.np.where(mnist.Y_train == predicted_label)[0]

        # Pick the first matching sample (or use a stored/deterministic index)
        predicted_sample_idx = pred_indices[0]
        predicted_img_array = mnist.X_train[:, predicted_sample_idx]

        # 3. Render surfaces
        pred_surf = self.ndarray_to_surface(predicted_img_array, scale_factor=6)
        actual_surf = self.ndarray_to_surface(actual_img_array, scale_factor=6)

        # 4. Render text surfaces
        pred_text_surf = self.font2.render(
            f"Prediction: {predicted_label}", True, (255, 255, 255)
        )
        actual_text_surf = self.font2.render(
            f"Actual: {actual_label}", True, (255, 255, 255)
        )
        acc_text_surf = self.font3.render(
            f"Accuracy: {self.acc}", True, (255, 255, 255)
        )

        # 5. Position and blit elements vertically
        start_x = self.sim_area_width + 150
        current_y = 50
        spacing = 15

        img_width = actual_surf.get_width()
        center_x = start_x + (img_width // 2)

        # Prediction Label
        pred_text_rect = pred_text_surf.get_rect(
            center=(center_x, current_y + pred_text_surf.get_height() // 2)
        )
        self.screen.blit(pred_text_surf, pred_text_rect)
        current_y += pred_text_surf.get_height() + spacing

        # Predicted Image (Representative digit for the model's guess)
        pred_img_rect = pred_surf.get_rect(topleft=(start_x, current_y))
        self.screen.blit(pred_surf, pred_img_rect)
        current_y += pred_surf.get_height() + (spacing * 2)

        # Actual Label
        actual_text_rect = actual_text_surf.get_rect(
            center=(center_x, current_y + actual_text_surf.get_height() // 2)
        )
        self.screen.blit(actual_text_surf, actual_text_rect)
        current_y += actual_text_surf.get_height() + spacing

        # Actual Image (The actual input feed into the network)
        actual_img_rect = actual_surf.get_rect(topleft=(start_x, current_y))
        self.screen.blit(actual_surf, actual_img_rect)

        # Accuracy Label
        acc_text_rect = acc_text_surf.get_rect(
            center=(center_x, current_y + actual_surf.get_height() + spacing + 50)
        )
        self.screen.blit(acc_text_surf, acc_text_rect)

    def run(self):
        self.running = True
        while self.running:
            mx, my = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if (
                            event.pos[0] < self.sim_area_width
                            and event.pos[1] < self.sim_area_height
                        ):
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
            # self.network.update()

            if self.timer % (self.FPS * self.waiter) == 0:
                self.W1, self.b1, self.W2, self.b2, self.predict, self.acc = mnist.test(
                    self.W1,
                    self.b1,
                    self.W2,
                    self.b2,
                    mnist.X_train,
                    mnist.Y_train,
                    0.1,
                )
                self.update_weights()

            # -- Draw --#
            self.screen.fill("black")

            self.network.draw(
                self.screen, self.zoom_level, self.camera_x, self.camera_y
            )

            # Right panel background
            pg.draw.rect(
                self.screen,
                "black",
                (self.sim_area_width, 0, self.WIDTH - self.sim_area_width, self.HEIGHT),
            )

            self.draw_image_and_prediction()

            pg.display.set_caption(f"Neural Nodes | FPS: {int(self.clock.get_fps())}")

            self.timer += 1
            pg.display.flip()
            self.clock.tick(self.FPS)

        pg.quit()
        sys.exit()


if __name__ == "__main__":
    sim = Simulation()
    sim.run()
