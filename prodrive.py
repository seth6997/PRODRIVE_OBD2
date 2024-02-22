from datetime import time
import pygame
import obd
import time

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
        pygame.display.set_caption('Custom Gauge')
        self.clock = pygame.time.Clock()

        # STATIC CUSTOM GAUGE BACKGROUND
        self.background_image = pygame.image.load('IMAGES/GAUGE_BG.png').convert_alpha()

        # BRING ALL CUSTOM RPM IMAGE LAYERS INTO A CALLABLE LIST
        self.rectangle_images = []
        for i in range(1, 26):
            filename = f'IMAGES/RECTANGLE_{i}.png'
            image = pygame.image.load(filename).convert_alpha()
            self.rectangle_images.append(image)

        # FONT SETTINGS
        self.font = pygame.font.Font(None, 68)

        # Initialize the OBD connection
        self.connection = obd.OBD()  # Automatically scans for available ports

        # Initialize variables for OBD data
        self.current_rpm = 0
        self.current_speed = 0
        self.current_oil_temperature = 0
        self.current_coolant_temperature = 0

    def update_obd_data(self):
        while True:
            # Update RPM
            response = self.connection.query(obd.commands.RPM)
            if response.value is not None:
                self.current_rpm = response.value.magnitude

            # Update Speed
            # response = self.connection.query(obd.commands.SPEED)
            # if response.value is not None:
                # self.current_speed = response.value.magnitude

            # Update Oil Temperature
            # response = self.connection.query(obd.commands.OIL_TEMP)
            # if response.value is not None:
                # self.current_oil_temperature = response.value.magnitude

            # Update Coolant Temperature
            # response = self.connection.query(obd.commands.COOLANT_TEMP)
            # if response.value is not None:
                # self.current_coolant_temperature = response.value.magnitude

            time.sleep(0.01)  # Adjust the sleep interval as needed

    def run(self):
        self.update_obd_data()  # Update OBD data in the main thread

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

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
            self.screen.blit(rpm_text, (620, 90))  # RPM TEXT LOCATION

            # RENDER SPEED VALUE
            # speed_text = self.font.render(f"{int(self.current_speed)}", True, WHITE)
            # self.screen.blit(speed_text, (300, 330))  # SPEED TEXT LOCATION

            # RENDER OIL TEMPERATURE VALUE
            # oil_temperature_text = self.font.render(f"{int(self.current_oil_temperature)}", True, WHITE)
            # self.screen.blit(oil_temperature_text, (40, 257))  # OIL TEMPERATURE TEXT LOCATION

            # RENDER COOLANT TEMPERATURE VALUE
            # coolant_temperature_text = self.font.render(f"{int(self.current_coolant_temperature)}", True, WHITE)
            # self.screen.blit(coolant_temperature_text, (40, 350))  # COOLANT TEMPERATURE TEXT LOCATION

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    app = CustomGauge()
    app.run()
