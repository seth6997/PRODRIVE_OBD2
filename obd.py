from datetime import time
import pygame
import obd
import time
import subprocess

# DISPLAY SIZE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# COLORS USED
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class CustomGauge:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Custom Gauge")
        self.clock = pygame.time.Clock()

        # STATIC CUSTOM GAUGE BACKGROUND
        self.background_image = pygame.image.load("images/GAUGE_BG.png").convert_alpha()

        # BRING ALL CUSTOM RPM IMAGE LAYERS INTO A CALLABLE LIST
        self.rectangle_images = []
        for i in range(1, 26):
            filename = f"images/RECTANGLE_{i}.png"
            image = pygame.image.load(filename).convert_alpha()
            self.rectangle_images.append(image)

        # INIT VALUE
        self.current_rpm = 0
        self.current_speed = 0

        # FONT SETTINGS
        self.font = pygame.font.Font(None, 68)

        # Initialize the OBD connection
        self.connection = obd.OBD()  # Automatically scans for available ports

    def update_obd_data(self):
        # Retrieve RPM and speed data from the OBD adapter
        cmd_rpm = obd.commands.RPM
        cmd_speed = obd.commands.SPEED
        response_rpm = self.connection.query(cmd_rpm)
        response_speed = self.connection.query(cmd_speed)

        if not response_rpm.is_null() and not response_speed.is_null():
            self.current_rpm = response_rpm.value.magnitude
            self.current_speed = response_speed.value.magnitude

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update OBD data
            self.update_obd_data()

            # BG COLOR
            self.screen.fill(BLACK)

            # SHOW CUSTOM GAUGE
            self.screen.blit(self.background_image, (0, 0))

            # RENDER EACH CUSTOM RECTANGLE LAYER for RPM
            num_rectangles_rpm = min(self.current_rpm // 348 + 1, len(self.rectangle_images))
            for i in range(len(self.rectangle_images)):
                if i < num_rectangles_rpm:
                    self.screen.blit(self.rectangle_images[i], (0, 0))
                else:
                    break

            # RENDER RPM VALUE
            rpm_text = self.font.render(f"{int(self.current_rpm)}", True, WHITE)
            self.screen.blit(rpm_text, (620, 90))   # RPM TEXT LOCATION

            # RENDER SPEED VALUE
            speed_text = self.font.render(f"{int(self.current_speed)}", True, WHITE)
            self.screen.blit(speed_text, (300, 330))   # SPEED TEXT LOCATION

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    app = CustomGauge()
    app.run()
