import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the screen
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pygame Continuous Sound Testbench")

    # Load a sound
    sound_path = "sound/TLS.wav"
    try:
        sound = pygame.mixer.Sound(sound_path)
    except pygame.error as e:
        print("Error loading sound:", e)
        return

    # Play the sound continuously
    sound_channel = pygame.mixer.Channel(0)  # Use channel 0 for simplicity
    sound_channel.play(sound, loops=-1)  # loops=-1 means continuous playback

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Clean up
    sound_channel.stop()  # Stop the sound
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
