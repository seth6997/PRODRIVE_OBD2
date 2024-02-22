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

        # FONT SETTINGS
        self.font = pygame.font.Font(None, 68)

        # Initialize the OBD connection
        self.connection = obd.OBD()  # Automatically scans for available ports

    def update_obd_data(self):
        # Retrieve RPM, speed, oil pressure, oil temperature, and coolant temperature data from the OBD adapter
        cmd_rpm = obd.commands.RPM
        cmd_speed = obd.commands.SPEED
        cmd_oil_pressure = obd.commands.OIL_PRESSURE
        cmd_oil_temp = obd.commands.COOLANT_TEMP
        cmd_coolant_temp = obd.commands.COOLANT_TEMP
        response_rpm = self.connection.query(cmd_rpm)
        response_speed = self.connection.query(cmd_speed)
        response_oil_pressure = self.connection.query(cmd_oil_pressure)
        response_oil_temp = self.connection.query(cmd_oil_temp)
        response_coolant_temp = self.connection.query(cmd_coolant_temp)

        if not (response_rpm.is_null() or response_speed.is_null() or response_oil_pressure.is_null() or
                response_oil_temp.is_null() or response_coolant_temp.is_null()):
            self.current_rpm = response_rpm.value.magnitude
            self.current_speed = response_speed.value.magnitude
            self.current_oil_pressure = response_oil_pressure.value.magnitude
            self.current_oil_temperature = response_oil_temp.value.magnitude
            self.current_coolant_temperature = response_coolant_temp.value.magnitude

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

            # RENDER OIL PRESSURE VALUE
            oil_pressure_text = self.font.render(f"{int(self.current_oil_pressure)}", True, WHITE)
            self.screen.blit(oil_pressure_text, (670, 250))   # OIL PRESSURE TEXT LOCATION

            # RENDER OIL TEMPERATURE VALUE
            oil_temperature_text = self.font.render(f"{int(self.current_oil_temperature)}", True, WHITE)
            self.screen.blit(oil_temperature_text, (40, 257))   # OIL TEMPERATURE TEXT LOCATION

            # RENDER COOLANT TEMPERATURE VALUE
            coolant_temperature_text = self.font.render(f"{int(self.current_coolant_temperature)}", True, WHITE)
            self.screen.blit(coolant_temperature_text, (40, 350))   # COOLANT TEMPERATURE TEXT LOCATION

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    app = CustomGauge()
    app.run()