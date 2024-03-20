import cv2
import numpy as np
import pygame

pygame.init()

# Set your desired width and height
WIDTH, HEIGHT = 1920, 1080

def play_video(video_file, audio_file, surface):
    cap = cv2.VideoCapture(video_file)
    clock = pygame.time.Clock()

    # Load and play audio
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV uses BGR, Pygame uses RGB

        # Flip the frame horizontally if needed
        # frame = np.flip(frame, axis=1)

        # Flip the frame vertically if needed
        # frame = np.flip(frame, axis=0)

        #frame = np.rot90(frame)  # Rotate frame if necessary
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        frame_rect = frame.get_rect()
        frame_rect.center = (WIDTH // 2, HEIGHT // 2)
        
        surface.blit(frame, frame_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to end prematurely
                    running = False

        clock.tick(30)  # Adjust frame rate as necessary

    cap.release()
    pygame.mixer.music.stop()

# Example usage
if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    play_video("video/intro.mp4", "video/intro.wav", screen)
    pygame.quit()
