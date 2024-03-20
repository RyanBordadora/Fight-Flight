import socket
import threading
import pygame
import serial
import vision
import numpy as np
import cv2
import configparser
from classes import *
from weapon_list import weapon_bank
from drone_list import drone_bank
from main_menu import *
from video import play_video
# Initialize Pygame
pygame.init()
#WIDTH, HEIGHT = 1280, 720
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fight Flight Client")

def display_menu(image):
    img = pygame.image.load(image).convert()
    img = pygame.transform.scale(img, (WIDTH,HEIGHT))
    screen.blit(img,(0,0))

def center_image_on_screen(screen, image):
    screen_width, screen_height = screen.get_size()
    image_width, image_height = image.get_size()
    center_x = (screen_width - image_width) // 2
    center_y = (screen_height - image_height) // 2
    screen.blit(image, (center_x, center_y))

# Initialize the serial connection
ser = serial.Serial('COM4', 9600, timeout=1)

# Get the host IP address
HOST = ''
# Get the host PORT
PORT = 55555

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

play_video("video/intro.mp4", "video/intro.wav", screen)

Energy_Shield = 0
Player_Duration = 0
Disruption = 0
Energy_Charge = 0

#nickname = input("Choose a nickname: ")
nickname = "HOST"
AG_path = "AgencyFBCondensed Bold.otf"  # Replace "path/to/your/font.ttf" with the actual path to your font file
AG_standard = pygame.font.Font(AG_path, 42)  # Adjust the font size (36) as needed
AG_Large = pygame.font.Font(AG_path, 88)  # Adjust the font size (36) as needed
custom_font_Ammo = pygame.font.Font(AG_path, 48)  # Adjust the font size (36) as needed

# Load images
title_screen_image = "images/main_menu.png"
background_image = "images/gamemode_select.png"
button_image = pygame.image.load("images/PlayButton.png")
button_hover_image = pygame.image.load("images/DemoButton.png")
cbutton_image = pygame.image.load("images/raptor_button.svg")
cbutton_hover_image = pygame.image.load("images/raptor_select.svg")
stats_image = pygame.image.load("images/Play.png")
menu_button1 = pygame.image.load("buttons/Confirm_Contract_button.png")
menu_button2 = pygame.image.load("buttons/Confirm_Weapon_button.png")

reticles = [pygame.image.load("reticles/Abrams.png"), pygame.image.load("reticles/lemon.png"),
             pygame.image.load("reticles/TDot.png"), pygame.image.load("reticles/UFO.png")]

character_weapon_count = [4, 4, 5, 5, 2, 2, 2, 2]

player = 0
opponent = 1
players = [None, None]
p_id = 1
opp_id = 2

global solution_array

# Initialize the socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect((HOST, PORT))

# Font for displaying text
font = pygame.font.Font(None, 36)

# Button parameters
button_width, button_height = 200, 50
button_rect = pygame.Rect((WIDTH - button_width) // 2, (HEIGHT - button_height) // 3, button_width, button_height)

# Second button parameters
button2_rect = pygame.Rect((WIDTH - button_width) // 2, (HEIGHT - button_height) // 3 * 2, button_width, button_height)
button2_pressed = False

# Third button parameters
button3_rect = pygame.Rect((WIDTH - button_width) // 2, (HEIGHT - button_height) // 3 * 5 / 2, button_width, button_height)
button3_pressed = False

# Second Weapon parameters
wr_width, wr_height = 10, 100
weapon2_rect = pygame.Rect(WIDTH - 330, HEIGHT - 210, wr_width, wr_height)

ability2_rect = pygame.Rect(WIDTH - 40, HEIGHT - 210, wr_width, wr_height)

# Define UI elements
info_box_rect = pygame.Rect(WIDTH - 340, HEIGHT - 250, 320, 230)
divider_x = WIDTH - 170

ready = 100

# Define the path to the font file images/drone_select_image.png
font_path = "fonts/ACES07_Regular.ttf"  # Replace "path/to/your/font.ttf" with the actual path to your font file

# Load the font
custom_font_standard = pygame.font.Font(font_path, 24)  # Adjust the font size (36) as needed
custom_font = pygame.font.Font(font_path, 36)  # Adjust the font size (36) as needed
custom_font_Ammo = pygame.font.Font(font_path, 52)  # Adjust the font size (36) as needed

#Variable Init
weapon = 0
drain = 0
weapon1_cooldown_end = 0
weapon2_cooldown_end = 0  # cooldown end time
ability_cooldown_end = 0
weapon_velocity = 0
weapon_precision = 0
Project_Air = 0
Beam_Fire = 0
hit = 0
miss = 0
hosting = 0
Flight_Time = 0
prevbutton2_state = 0
Chaff = False
Chaff_count = 3
cooldown_duration = 0
a_cooldown_height = 0
weapon_2 = None
song1 = 'Comona.mp3'

def play_video_na(video_file, surface):
        cap = cv2.VideoCapture(video_file)
        clock = pygame.time.Clock()

        running = True
        while running:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV uses BGR, Pygame uses RGB
            #frame = np.rot90(frame)  # Rotate frame if necessary
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frame_rect = frame.get_rect()
            frame_rect.center = (WIDTH //2, HEIGHT // 2)
            
            surface.blit(frame, frame_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(30)  # Adjust frame rate as necessary

        cap.release()


#initalize opencv
vc = cv2.VideoCapture(0,cv2.CAP_DSHOW) #windows
#vc = cv2.VideoCapture(0) #macos
vc.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

rval, frame = vc.read()
pink_detection = vision.Vision(rval,vc,frame,HEIGHT,WIDTH)
ammo_gun = 100

# Health bar parameters
health_bar_width, health_bar_height = WIDTH - 40, 30
health_bar_rect = pygame.Rect(20, HEIGHT - health_bar_height - 20, health_bar_width, health_bar_height)

# Initial values
button_pressed = False
health = 100
health_decrease_rate = 0.1
cooldown_height = 0

def separate_teams(names, id_codes):
        team1_names = []
        team1_ids = []
        team2_names = []
        team2_ids = []
        team1_uids = []
        team2_uids = []
        uid_list=[]

        for name, id_code in zip(names, id_codes):
            team_number = id_code[-2]  # Second to last value is the team number
            print(f"Name: {name}, ID Code: {id_code}, Team Number: {team_number}")
            if team_number == 1:
                team1_names.append(name)
                team1_ids.append(id_code)
                team1_uids.append(id_code[3])
            elif team_number == 2:
                team2_names.append(name)
                team2_ids.append(id_code)
                team2_uids.append(id_code[3])
        
        while len(team1_uids) < 5:
            team1_uids.append(-1)
        while len(team2_uids) < 5:
            team2_uids.append(-1)
        uid_list = team1_uids
        uid_list.extend(team2_uids)


        return team1_names, team1_ids, team2_names, team2_ids, uid_list


def render_team(id_codes, list_positions):
        for i in range(4):
            if list_positions[i] is None:
                continue  # Skip rendering if position is None
            x, y = list_positions[i]
            for array in id_codes:
                if i == 0:
                    value = array[i]
                    text = font.render(drone_list(value), True, WHITE)
                elif i == 1:
                    value1 = array[i-1]
                    value2 = array[i]
                    text = font.render(weapon_list(value1, value2), True, WHITE)
                elif i == 3:
                    value = array[i]
                    text = font.render(str(value), True, WHITE)
                else:
                    continue  # Skip rendering for the third list
                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)
                y += 78  # Move to the next line for the next value

def render_text(screen, text_array, start_x, start_y, y_spacing, display_flags=None, center=False):
    #font = pygame.font.SysFont(None, 36)  # You can adjust the font and size here
    try:
        if display_flags is None:
            display_flags = [1] * len(text_array)  # If no display flags are provided, display all
        for i, (text, display_flag) in enumerate(zip(text_array, display_flags)):
            if display_flag == 1:
                rendered_text = font.render(text, True, (255, 255, 255))  # White color
                text_rect = rendered_text.get_rect()
                if center:
                    text_rect.center = (start_x, start_y + i * y_spacing)
                else:
                    text_rect.topleft = (start_x, start_y + i * y_spacing)
                screen.blit(rendered_text, text_rect)
            elif display_flag == 2:
                rendered_text = font.render("HOST", True, (255, 255, 255))  # White color
                text_rect = rendered_text.get_rect()
                if center:
                    text_rect.center = (start_x, start_y + i * y_spacing)
                else:
                    text_rect.topleft = (start_x, start_y + i * y_spacing)
                screen.blit(rendered_text, text_rect)
            else:
                pass
    except:
        print("ERROR PRINTING TEXT")

def update_solution(status, item_number):
    index = user_ids.index(item_number)
    solution_array[index] = status

def initialize_game():
    global button_rect, health_bar_rect, button_pressed, health
    button_rect = pygame.Rect((WIDTH - button_width) // 2, (HEIGHT - button_height) // 2, button_width, button_height)
    health_bar_rect = pygame.Rect(20, HEIGHT - health_bar_height - 20, health_bar_width, health_bar_height)
    button_pressed = False
    health = 100
supremacy =0 
free = 0
duel = 0
#Sends its data to the server
def write(message, message_type = 0):
    if message_type == 0:
        client.send(message.encode('ascii'))
    elif message_type == 1:
        if supremacy:
            if 'W1' in message.upper():
                client.send((f"SCOREUPDATE {players[player].weapon_1.get_weapon_damage(Overcharge)}").encode('ascii'))
            elif 'W2' in message.upper():
                client.send((f"SCOREUPDATE {players[player].weapon_2.get_weapon_damage(Overcharge)}").encode('ascii'))
        elif free:
            pass
        else:
            if radar_lock:
                client.send(message.encode('ascii'))
    elif message_type == 2:
        if free:
            pass
        else:
            client.send(message.encode('ascii'))

# Create a separate Pygame surface for the HUD
hud_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
def check_zeros(array):
    for element in array:
        if element == 0:
            return 0
    return 1
game_start = 0
Overcharge = 0
Invulnerable = 0
Adaptive_Armor = 0
Leech = 0
victory = 0
drain = 0
game_ready = 0
Energy_Charge = 0

solution_array = [-1, -1, -1, -1, -1, -1, 1, -1, -1, -1]

# Function to receive messages from the server
def receive():
    global health, players, opponent, drain, Disruption, Invulnerable, Adaptive_Armor, Overcharge, Leech
    global player_list, team_update, hosting, screen_set, game_start, victory, solution_array
    global nickname_array, integer_array, host_index, client_index, host_ids, client_ids, ready
    global user_ids, ready_list1, ready_list2, user_id, team1_score, team2_score, game_ready
    global nickname_array, integer_array, team1_ids, team2_ids, team1_names, team2_names
    while True:
            sys.stdout.flush()
            try:
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(full_player_id.encode('ascii'))
                elif message == 'START':
                    game_start = 1
                elif message.startswith("Player Update:"):
                    player_list = parse_player_update(message)
                    print(f"PL:{player_list}")
                    nickname_array = []
                    integer_array = []
                    for player_info in player_list:
                        try:
                            nickname, integers = parse_message(player_info)
                            nickname_array.append(nickname)
                            integer_array.append(integers)
                        except ValueError as e:
                            print(f"Error parsing player info: {e}")
                    team1_names, team1_ids, team2_names, team2_ids, user_ids = separate_teams(nickname_array, integer_array)
                    print("Received T1ID:", team1_ids)
                    print("Received T2ID:", team2_ids)
                    print("Received ÜIDS:", user_ids)
                    team_update = 1

                    host_index, client_index = find_host_and_client(integer_array)
                    print(f"HI:{host_index}")
                    print(f"NA:{nickname_array[host_index]} vs {username}")
                    print(f"CI:{client_index}")
                    #print(f"NA:{nickname_array[1]} vs {username}")
                    if host_index is not None:
                        if nickname_array[host_index] == username or len(player_list) == 1 or len(host_ids) > 1:
                            hosting = 1
                            print(hosting)
                        host_ids = integer_array[host_index]
                    if client_index is not None:
                        if nickname_array[client_index] == username or (len(player_list) == 1 and hosting == 0) :
                            hosting = 2
                        client_ids = integer_array[client_index]
                    screen_set = 1
                elif message == 'Client_Ready':
                    ready = 1
                    screen_set = 1
                elif message.startswith("Ready Update:"):
                    solution_array = [-1, -1, -1, -1, -1, -1, 1, -1, -1, -1]
                    print("SolAS:", solution_array)
                    set_array(user_ids, solution_array)
                    updates = message.split(":")[1].split(",")
                    print("Updates:",updates)
                    for update in updates:
                        status, item_number = int(update[0]), int(update[1])
                        print("stat",status)
                        print("index", item_number)
                        update_solution(status, item_number)
                    print("SolA:", solution_array)
                    ready_list1 = solution_array[:5]
                    ready_list2 = solution_array[5:]
                    print("Received RL1:", ready_list1)
                    print("Received RL2:", ready_list2)
                    if check_zeros(solution_array):
                        game_ready = 1
                        print("Standby")
                    else:
                        game_ready = 0
                    team_update = 1
                elif message.startswith("UID:"):
                    update_string = message.replace("UID:", "")
                    user_id = int(update_string)
                    print(f"UID: {user_id}")
                    if user_id == 0:
                        print("You're Host!")
                        hosting = 1
                    team_update = 1
                elif message.startswith("Score:"):
                    # Split the string by '/'
                    parts = message.split('/')

                    # Extract the team scores from the split parts
                    team1_score = int(parts[0].split(':')[1])
                    team2_score = int(parts[1])

                    print("Team 1 score:", team1_score)
                    print("Team 2 score:", team2_score)
                    team_update = 1
                elif game_running:
                    if message[0] == str(opp_id):
                        if 'W1' in message.upper():
                            players[player].decrease_health(players[opponent].weapon_1.get_weapon_damage(Overcharge), Invulnerable, Adaptive_Armor)
                        elif 'W2' in message.upper():
                            players[player].decrease_health(players[opponent].weapon_2.get_weapon_damage(Overcharge), Invulnerable, Adaptive_Armor)
                            drain = drain + players[player].weapon_2.get_weapon_leech(Leech)
                        elif 'END' in message.upper():
                            victory = 1
                        else:
                            if players[player].ability.get_ability_type() == 'D':
                                if players[opponent].ability.get_ability_name() == "OV":
                                    Overcharge = 1
                                elif players[opponent].ability.get_ability_name() == "DP":
                                    Disruption = 1
                                elif players[opponent].ability.get_ability_name() == "EL":
                                    Leech = 1
                            elif players[player].ability.get_ability_type() == 'L':
                                    break
                else:
                    print(message)
            except:
                print("An error occurred!")
                client.close()
                break

#Server connection
#receive_thread = threading.Thread(target=receive)

initialize_game()
# Load your music files
song2 = 'C:/Users/ryanr/Documents/SimpleChatRoom/Showdown.ogg'

# Function to play a specific song
def play_song(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # You can adjust the loop parameter as needed

def play_sound_effect(sound):
    sound_effect = pygame.mixer.Sound(sound)
    sound_effect.set_volume(0.5)
    sound_effect.play()

def draw_progress_bar(team1_score, team2_score, box_width, box_height):
    total_score = team1_score + team2_score
    team1_width = (team1_score / total_score) * box_width
    team2_width = box_width - team1_width

   # Calculate positions to place the progress bars and text at the top of the screen
    progress_bar_y = 10  # Adjust this value as needed for vertical placement
    progress_bar_x = (WIDTH - box_width) // 2

    # Draw progress bars
    pygame.draw.rect(screen, TEAL, (progress_bar_x, progress_bar_y, team1_width, box_height))
    pygame.draw.rect(screen, RED, (progress_bar_x + team1_width, progress_bar_y, team2_width, box_height))

    # Write text
    if team1_score > team2_score:
        text1 = "Superiority"
        text2 = "Denial"
    elif team1_score < team2_score:
        text1 = "Denial"
        text2 = "Superiority"
    else:
        text1 = "Equality"
        text2 = "Equality"

    if team1_score >= 3 * team2_score:
        text1 = "Supremacy"
    elif team2_score >= 3 * team1_score:
        text2 = "Supremacy"

    if team1_score <= team2_score / 3:
        text1 = "Incapability"
    elif team2_score <= team1_score / 3:
        text2 = "Incapability"

    text_surface1 = AG_standard.render(text1, True, BLACK)
    text_surface2 = AG_standard.render(text2, True, BLACK)

    # Calculate positions to place the text at the top of the screen and center vertically within the progress bars
    text_y = progress_bar_y + (box_height - text_surface1.get_height()) // 2  # Center vertically within the progress bars
    text1_x = max(progress_bar_x, (WIDTH - box_width - text_surface1.get_width()) // 2)
    text2_x = min(progress_bar_x + box_width - text_surface2.get_width(), (WIDTH + box_width - text_surface2.get_width()) // 2)

    # Draw text at the top of the screen
    screen.blit(text_surface1, (text1_x + 5, text_y))
    screen.blit(text_surface2, (text2_x - 5, text_y))



def set_array(arr1, arr2):
    for i in range(len(arr1)):
        if arr1[i] == -1:
            arr2[i] = -1
    return arr2
# Example of using the play_song function
play_song(song1)
clock = pygame.time.Clock()

# Initialize game variables and parameters...
# Your existing game initialization code here...

def handle_serial_input():
    global button_pressed, button2_pressed, weapon2_cooldown_end, Chaff, weapon, cooldown_height, weapon1_cooldown_end, button3_pressed
    try:
        serial_data = ser.readline().decode('utf-8', errors='replace').strip()
        if serial_data:
            # Filter out invalid characters
            serial_data = serial_data.replace('\x00', '')
            # Split the data into button states
            button_states = [int(state) for state in serial_data.split(',') if state]

            if len(button_states) == 3: 
                # Extract button states
                button1_state, button2_state, button3_state = button_states
                button_pressed = button1_state == 1
                button2_pressed = button2_state == 1
                button3_pressed = button3_state == 1

            # Process serial data and update game state accordingly
            # Your existing serial input handling code here...
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}")

def render_full_game():
    global button_pressed, button2_pressed, button3_pressed, weapon2_cooldown_end, drain, cooldown_height, weapon1_cooldown_end
    global weapon, a_cooldown_height, Energy_Shield, team1_score, team2_score  # Declare global variables

    if victory == 1 and failure == 0:
        game_over_text = custom_font_Ammo.render("MISSION SUCCESS", True, GREEN)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        return
    # Calculate remaining time
    elapsed_time = pygame.time.get_ticks() - start_time + drain
    remaining_time = max(0, 180 - elapsed_time // 1000)  # Convert milliseconds to seconds

    # Draw the timer at the top of the screen
    timer_text = font.render(f"Time: {remaining_time // 60:02d}:{remaining_time % 60:02d}", True, RED)
    screen.blit(timer_text, (20, 20))

    if supremacy == 1:
        draw_progress_bar(team1_score, team2_score, box_width= 900, box_height= 50)

    if remaining_time == 0 or failure == 1:
        # Write "Game Over" on the screen
        game_over_text = custom_font_Ammo.render("MISSION FAILURE", True, RED)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        return
    
    # Draw info box outline
    pygame.draw.rect(screen, WHITE, info_box_rect, 2)

    # Draw dividing line
    pygame.draw.line(screen, WHITE, (divider_x, HEIGHT - 250), (divider_x, HEIGHT - 100), 2)

    equipped = "ERROR"
    equipped_ammo = "ERROR"
    unequipped = "ERROR"
    unequipped_ammo = "ERROR"
    if weapon == 0:
        equipped = players[player].weapon_1.get_weapon_name()
        equipped_ammo = players[player].weapon_1.get_ammo()
        unequipped = players[player].weapon_2.get_weapon_name()
        unequipped_ammo = players[player].weapon_2.get_ammo()
        if players[player].weapon_1.get_weapon_type() == 'P':
            center_image_on_screen(screen,reticles[2])
        #Hitscan Weapon
        elif players[player].weapon_1.get_weapon_type() == 'H':
            center_image_on_screen(screen,reticles[3])
        #Beam Weapon
        elif players[player].weapon_1.get_weapon_type() == 'B':
            center_image_on_screen(screen,reticles[1])
        #Gun Weapon
        elif players[player].weapon_1.get_weapon_type() == 'G':
            center_image_on_screen(screen,reticles[0])
        
    elif weapon == 1:
        equipped = players[player].weapon_2.get_weapon_name()
        equipped_ammo = players[player].weapon_2.get_ammo()
        unequipped = players[player].weapon_1.get_weapon_name()
        unequipped_ammo = players[player].weapon_1.get_ammo()
        if players[player].weapon_2.get_weapon_type() == 'P':
            center_image_on_screen(screen,reticles[2])
        #Hitscan Weapon
        elif players[player].weapon_2.get_weapon_type() == 'H':
            center_image_on_screen(screen,reticles[3])
        #Beam Weapon
        elif players[player].weapon_2.get_weapon_type() == 'B':
            center_image_on_screen(screen,reticles[1])
        #Gun Weapon
        elif players[player].weapon_2.get_weapon_type() == 'G':
            center_image_on_screen(screen,reticles[0])


    # Render secondary text with larger font size (Ammo)
    secondary_weapon_text2 = custom_font_Ammo.render(f"{equipped_ammo}", True, RED)
    ammo_rect = secondary_weapon_text2.get_rect()
    ammo_rect.center = (WIDTH - 250, HEIGHT - 130)  # Adjusted position

    # Render secondary text with larger font size (Weapon)
    secondary_weapon_text = custom_font.render(f"{equipped}", True, RED)
    weapon_rect = secondary_weapon_text.get_rect()
    weapon_rect.centerx = ammo_rect.centerx  # Center horizontally with respect to the ammo text

    # Draw weapon information on the left side
    gun_text = custom_font_standard.render(f"{unequipped} {unequipped_ammo}", True, RED)
    primary_rect = secondary_weapon_text.get_rect()
    primary_rect.centerx = ammo_rect.centerx  # Center horizontally with respect to the ammo text
    # Keep the y-coordinate unchanged
    primary_rect.centery = HEIGHT - 220  # Adjusted position

    # Keep the y-coordinate unchanged
    weapon_rect.centery = HEIGHT - 170  # Adjusted position

    # Blit the text surfaces
    screen.blit(gun_text, (WIDTH - 290, HEIGHT - 220))  # Adjusted position
    screen.blit(secondary_weapon_text2, ammo_rect)
    screen.blit(secondary_weapon_text, weapon_rect)

    # Draw additional information on the right side (Ability)
    ability_text = custom_font.render(f"{players[player].ability.get_ability_name()}", True, RED)
    ability_rect = ability_text.get_rect()
    ability_rect.topleft = (WIDTH - 140, HEIGHT - 200)  # Adjusted position
    screen.blit(ability_text, ability_rect)

    # Calculate the center position for the "Ready" text
    ready_rect = font.render("READY", True, RED).get_rect()
    ready_rect.centerx = ability_rect.centerx  # Center horizontally with respect to the ability text
    ready_rect.top = ability_rect.bottom + 10  # Place below the ability text

    # Check if "Ready" should be displayed or a value from 0 to 100
    ready = max(0, 1 - (ability_cooldown_end - pygame.time.get_ticks()) / players[player].ability.get_cooldown())
    ready = 100 * ready
    if ready >= 100:
        ready_text = custom_font.render("READY", True, RED)
    else:
        ready_text = custom_font.render("OFF", True, RED)

    # Center the "Ready" text horizontally with respect to the ability text
    ready_text_rect = ready_text.get_rect(center=(ready_rect.centerx, ready_rect.centery))

    # Blit the text surfaces
    screen.blit(ready_text, ready_text_rect)


    # Display "Hull" string at the top
    hull_title_text = custom_font_standard.render("Hull:", True, WHITE)
    screen.blit(hull_title_text, (WIDTH - 310, HEIGHT - 90))  # Adjusted position

    # Draw vertical cooldown rectangle (Weapon 2)
    if button2_pressed or (weapon2_cooldown_end > pygame.time.get_ticks()):
        cooldown_progress = max(0, 1 - (weapon2_cooldown_end - pygame.time.get_ticks()) / players[player].weapon_2.get_weapon_cooldown())
        cooldown_height = int(cooldown_progress * wr_height)
        pygame.draw.rect(screen, RED, (weapon2_rect.left, weapon2_rect.bottom - cooldown_height, wr_width, cooldown_height))
    else:
        pygame.draw.rect(screen, GREEN, (weapon2_rect.left, weapon2_rect.top, wr_width, cooldown_height))  # Use green when not on cooldown
    pygame.draw.rect(screen, RED, (weapon2_rect.left, weapon2_rect.top, wr_width, wr_height), 2)  # Draw outline

    # Draw vertical cooldown rectangle (Ability)
    if button2_pressed or (ability_cooldown_end > pygame.time.get_ticks()):
        a_cooldown_progress = max(0, 1 - (ability_cooldown_end - pygame.time.get_ticks()) / players[player].ability.get_cooldown())
        a_cooldown_height = int(a_cooldown_progress * wr_height)
        pygame.draw.rect(screen, RED, (ability2_rect.left, ability2_rect.bottom - a_cooldown_height, wr_width, a_cooldown_height))
    else:
        pygame.draw.rect(screen, GREEN, (ability2_rect.left, ability2_rect.top, wr_width, a_cooldown_height))  # Use green when not on cooldown
    pygame.draw.rect(screen, RED, (ability2_rect.left, ability2_rect.top, wr_width, wr_height), 2)  # Draw outline


    # Draw health bar at the bottom of the box
    health_bar_width = 220
    health_bar_height = 20
    health_bar_rect = pygame.Rect(WIDTH - 310, HEIGHT - 60, health_bar_width, health_bar_height)  # Adjusted position
    pygame.draw.rect(screen, RED, health_bar_rect, 2)
    
    # Draw health bar
    st_health = players[player].get_health()
    if st_health > 100:
        st_health = 100
    current_health_rect = pygame.Rect(health_bar_rect.left, health_bar_rect.top, st_health * (health_bar_width / 100), health_bar_height)
    if Energy_Shield:
        pygame.draw.rect(screen, GREEN, current_health_rect)
    else:
        pygame.draw.rect(screen, RED, current_health_rect)
    # Display health value to the right of the health bar
    health_text = custom_font_standard.render(f"{round(players[player].get_health())}", True, WHITE)
    screen.blit(health_text, (health_bar_rect.right + 10, health_bar_rect.top))

    pygame.display.flip()

w1fire = False
failure = 0
# Function to handle onscreen button events
def handle_button_events():
    global weapon2_cooldown_end, button_pressed, button2_pressed, Energy_Shield, Energy_Charge, button3_pressed, Adaptive_Armor, Chaff, Chaff_count, Invulnerable
    global Project_Air, weapon, health, drain, ability_cooldown_end, ammo_gun, Beam_Fire, failure, weapon1_cooldown_end, w1fire
    Player_Duration = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Perform action for button 1
                    button_pressed = True
                    button2_pressed = False  # Ensure the other button is not pressed
                elif event.key == pygame.K_q:
                    if not button2_pressed and pygame.time.get_ticks() >= weapon2_cooldown_end:
                        # Perform action for button 2
                        button_pressed = False
                        button2_pressed = True
                elif event.key == pygame.K_TAB:
                    # Perform action for button 3
                    button3_pressed = True
                    button2_pressed = False  # Ensure the other button is not pressed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    button_pressed = False
                elif event.key == pygame.K_q:
                    button2_pressed = False
                elif event.key == pygame.K_TAB:
                    button3_pressed = False

        if button2_pressed and not Disruption:
            ability_cooldown_end = pygame.time.get_ticks() + players[player].ability.get_cooldown()
            if players[player].ability.get_ability_type() == 'S':
                if players[player].ability.get_ability_name() == "NR":
                   players[player].heal(players[player].ability.get_effect())
            elif players[player].ability.get_ability_type() == 'P':
                Player_Duration = 1
                PA_Duration = pygame.time.get_ticks() + players[player].ability.get_duration()
                if players[player].ability.get_ability_name() == "IEWS":
                    Invulnerable = 1
                elif players[player].ability.get_ability_name() == "EC":
                    Energy_Charge = 1
                elif players[player].ability.get_ability_name() == "ADA":
                    Adaptive_Armor = 1
                elif players[player].ability.get_ability_name() == "ES":
                    Energy_Shield = 1
                    current_health = players[player].get_health()
                    players[player].heal(players[player].ability.get_effect())
            else: 
                write('Ability', 2)
            button2_pressed = False  # Reset button2_pressed after handling"
        
        if button3_pressed:
            weapon = not weapon
            button3_pressed = False


        Chaff = False

        if button_pressed:
            if weapon == 0 and weapon1_cooldown_end <= pygame.time.get_ticks() and players[player].weapon_1.get_ammo() > 0:
                weapon1_cooldown_end = pygame.time.get_ticks() + players[player].weapon_1.get_weapon_cooldown()
                play_sound_effect(players[player].weapon_1.get_sound_link())
                w1sound_path = players[player].weapon_2.get_sound_link()
                w1fire = True
                try:
                    w1sound = pygame.mixer.Sound(w1sound_path)
                except pygame.error as e:
                    print("Error loading sound:", e)

                # Play the sound continuously
                w1_channel = pygame.mixer.Channel(2)  # Use channel 1
                w1_channel.play(w1sound, loops=-1)  # loops=-1 means continuous playback
                write(f'{p_id}W1', 1)
                players[player].weapon_1.decrease_ammo()

            elif weapon and weapon2_cooldown_end <= pygame.time.get_ticks() and players[player].weapon_2.get_ammo() > 0:
                weapon2_cooldown_end = pygame.time.get_ticks() + players[player].weapon_2.get_weapon_cooldown()
                #write('2Fired')
                #Missile Weapon
                print(pink_detection.is_detected())
                if players[player].weapon_2.get_weapon_type() == 'P':
                    write(f'{p_id}MFired', 2)
                    Project_Air = 1
                    Flight_Time = pygame.time.get_ticks() + players[player].weapon_2.get_weapon_time()
                    play_sound_effect(players[player].weapon_2.get_sound_link())
                    play_sound_effect("sound/FOX2_ST.wav")
                #Hitscan Weapon
                elif players[player].weapon_2.get_weapon_type() == 'H':
                    write(f'{p_id}W2', 1)
                #Beam Weapon
                elif players[player].weapon_2.get_weapon_type() == 'B':
                    write(f'{p_id}W2', 1)
                    Beam_Fire = 1
                    Beam_Time = pygame.time.get_ticks() + players[player].weapon_2.get_weapon_time()
                    # Load the sound
                    sound_path = players[player].weapon_2.get_sound_link()
                    try:
                        sound = pygame.mixer.Sound(sound_path)
                    except pygame.error as e:
                        print("Error loading sound:", e)

                    # Play the sound continuously
                    w2_channel = pygame.mixer.Channel(1)  # Use channel 1
                    w2_channel.play(sound, loops=-1)  # loops=-1 means continuous playback

                #Gun Weapon
                elif players[player].weapon_2.get_weapon_type() == 'G':
                    write(f'{p_id}W2', 1)
                if not Energy_Charge:
                    drain = drain + players[player].weapon_2.get_weapon_drain()
                players[player].weapon_2.decrease_ammo()
                button_pressed = False
        elif w1fire:
            w1_channel.stop()
            w1fire = False
                

        if Project_Air:
            hit = 60
            miss = 40
            if Flight_Time <= pygame.time.get_ticks():
                if hit / (hit + miss) * 100 > (1 - players[player].weapon_2.get_weapon_precision()):
                    write(f'{p_id}W2', 1)
                    play_sound_effect("sound/ST_MHIT.wav")
                    Project_Air = 0
                else:
                    write('2MMiss')
                    Project_Air = 0

        if Beam_Fire:
            if Beam_Time >= pygame.time.get_ticks():
                    write(f'{p_id}W2',1)
            else:
                    Beam_Fire = 0
                    w2_channel.stop()

        if Player_Duration:
            if PA_Duration <= pygame.time.get_ticks() or Disruption:
                Invulnerable = 0
                Energy_Charge = 0
                Adaptive_Armor = 0
                Energy_Shield = 0
                if players[player].ability.get_ability_name() == "ES" and current_health < players[player].get_health():
                    players[player].set_health(current_health)
        
        if players[player].get_health() <= 0:
            write(f'{p_id}END')
            failure = 1

                



# Thread objects for video capture, color detection, and serial input detection
video_thread = None
color_detection_thread = None
serial_input_thread = None
 # Start the receive thread for handling server messages
# receive_thread = threading.Thread(target=receive)
# receive_thread.start()

#serial_thread = threading.Thread(target=handle_serial_input)
button_events_thread = threading.Thread(target=handle_button_events)
# video_feed_thread = threading.Thread(target=render_combined_feed)

# Main game loop
running = True
game_start = False
game_running = False


# # # Start rendering the video feed in a separate thread
# video_feed_thread = threading.Thread(target=render_combined_feed)
# video_feed_thread.start()

# # # Start the serial input handling thread


# # # Start the button events handling thread
# button_events_thread = threading.Thread(target=handle_button_events)
# button_events_thread.start()
# # Render the combined video feed and HUD

def duel_server(drone_type, secondary):
    # Font for displaying text
    play_song("sound/FireAhead.mp3")
    font_path = "fonts/ACES07_Regular.ttf"  # Replace "path/to/your/font.ttf" with the actual path to your font file
    AG_path = "AgencyFBCondensed Bold.otf"
    font = pygame.font.Font(AG_path, 48)  # Replace "path/to/your/font.ttf" with the actual path to your font file
    AG_standard = pygame.font.Font(AG_path, 42)  # Adjust the font size (36) as needed
    AG_Large = pygame.font.Font(AG_path, 88)  # Adjust the font size (36) as needed
    custom_font_Ammo = pygame.font.Font(AG_path, 48)  # Adjust the font size (36) as needed

    # Server details
    HOST = 
    PORT = 55555

    # Player details
    global nickname_array, player_list, full_player_id
    player_list = []
    nickname_array = []
    # Client inputs
    #drone_type = input("Select 0-9:")
    #secondary = input("Select 0-9 ")
    team_id = 0
    full_player_id = f"{username}/{drone_type}{secondary}{team_id}"
    title_screen_image = "images/DUEL_Blank.png"
    global hosting
    hosting = 0

    multi_server_buttons = [pygame.image.load("images/Server_Buttons/start_button.png"), 
                        pygame.image.load("images/Server_Buttons/quit_button.png")]  # Corrected lowercase filenames
    multi_server_selected_buttons = [pygame.image.load("images/Server_Buttons/start_button_selected.png"), 
                                pygame.image.load("images/Server_Buttons/quit_button_selected.png")]  # Corrected lowercase filenames
    button_rects = []
    stamp_images = ["images/Stamp_boxes/WC_Stamp.png","images/Stamp_boxes/WC_Stamp.png", "images/Stamp_boxes/ST_Stamp.png","images/Stamp_boxes/ST_Stamp.png",
                    "images/Stamp_boxes/GC_Stamp.png", "images/Stamp_boxes/GC_Stamp.png", "images/Stamp_boxes/FW_Stamp.png", "images/Stamp_boxes/FW_Stamp.png"]

    # Define positions for each button
    #button_positions = [(446, 874), (161, 874)]  # Adjust positions as needed
    button_positions = [(1459, 874), (1174, 874)]
    # Create buttons and button rects with specific positions
    
    for button_image, position in zip(multi_server_buttons, button_positions):
        button_rect = button_image.get_rect(topleft=position)
        button_rects.append(button_rect)

    button_rects2 = []
    button_positions2 = [(446, 874), (161, 874)]
    for button_image, position in zip(multi_server_buttons, button_positions2):
        button_rect = button_image.get_rect(topleft=position)
        button_rects2.append(button_rect)


    global screen_set
    screen_set =0
    # Function to receive messages from the server

    sys.stdout.buffering = 0
    # Connect to the server
    client.connect((HOST, PORT))

    client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    # Start the receive thread
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    Ready = AG_standard.render("R E A D Y", True, WHITE)

    global ready
    ready = 0

    Ready_react = Ready.get_rect(center=(1585, 800))
    stamp_image = pygame.image.load(stamp_images[int(drone_type)])
    stamp_position = (161, 154)
    stamp_rect = stamp_image.get_rect(topleft=stamp_position)
    stamp_position2 = (1172, 154)
    stamp_rect2 = stamp_image.get_rect(topleft=stamp_position2)
    
    import numpy as np

    def play_video(video_file, surface):
        cap = cv2.VideoCapture(video_file)
        clock = pygame.time.Clock()

        running = True
        while running:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV uses BGR, Pygame uses RGB
            frame = np.rot90(frame)  # Rotate frame if necessary
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frame_rect = frame.get_rect()
            frame_rect.center = (WIDTH //2, HEIGHT // 2)
            
            surface.blit(frame, frame_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(30)  # Adjust frame rate as necessary

        cap.release()

    screen = pygame.display.set_mode((1920, 1080))
    video_file = "Abstract1.mp4"  # Replace with your video file path
    play_video(video_file, screen)

    # Main loop
    running = True
    def menu_refresh():
        global host_index, hosting, nickname_array, player_list, host_ids, client_ids
        backup = 0
        if (len(player_list) >= 2 or hosting == 1) and host_index is not None and host_ids is not None and len(host_ids) > 0:
            # print(f"NAMS:{nickname_array}")
            # print(f"HIMS:{host_index}")
            #print(f"HIDS:{host_ids}")
            host_name = AG_standard.render(f"{nickname_array[host_index]}", True, CUSTOM_BLUE)
            host_drone_name = AG_standard.render(drone_list(int(host_ids[0])), True, CUSTOM_BLUE)
            host_faction = AG_standard.render(faction_list(int(host_ids[0])), True, CUSTOM_BLUE)
            host_weapon_name = AG_standard.render(weapon_list(int(host_ids[0]), int(host_ids[1])), True, WHITE)
            host_weapon_rect = host_weapon_name.get_rect(center=(305, 800))
            display_menu(title_screen_image)
            screen.blit(pygame.image.load(stamp_images[int(host_ids[0])]),stamp_rect)
            screen.blit(host_name, (275, 175))
            screen.blit(host_drone_name, (200, 640))
            screen.blit(host_faction, (195, 258))
            screen.blit(host_weapon_name, host_weapon_rect)
            backup = 1
        if (len(player_list) >= 2 or hosting == 2) and client_index is not None:
            client_name = AG_standard.render(f"{nickname_array[client_index]}", True, CUSTOM_BLUE)
            client_drone_name = AG_standard.render(drone_list(int(client_ids[0])), True, CUSTOM_BLUE)
            client_faction = AG_standard.render(faction_list(int(client_ids[0])), True, CUSTOM_BLUE)
            client_weapon_name = AG_standard.render(weapon_list(int(client_ids[0]), int(client_ids[1])), True, WHITE)
            client_weapon_rect = client_weapon_name.get_rect(center=(1330, 800))
            screen.blit(client_name, (1310, 175))
            screen.blit(client_drone_name, (1230, 640))
            screen.blit(client_faction, (1225, 258))
            screen.blit(pygame.image.load(stamp_images[int(client_ids[0])]),stamp_rect2)
            screen.blit(client_weapon_name, client_weapon_rect)
            backup = 1
        if ready:
            screen.blit(Ready, Ready_react)
            backup = 1
        if backup == 0:
            #time.sleep(1000)
            print(f'HIDS: {host_ids}')
            print(f'HOSTING: {hosting}')
            write("RU")
            play_video(video_file, screen)
            
    while running:
        sys.stdout.flush()
        #if screen_set == 1:
        menu_refresh()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                play_sound_effect("sound/UI_MENU_select_basic.wav")
                if hosting == 2:
                    for i, button_rect in enumerate(button_rects):
                        if button_rect.collidepoint(event.pos):
                            if i == 1:
                                pygame.quit()
                            elif i == 0:
                                    write("Client_Ready")
                                    ready = 1
                elif hosting == 1:
                    for i, button_rect in enumerate(button_rects2):
                        if button_rect.collidepoint(event.pos):
                            if i == 1:
                                pygame.quit()
                            elif i == 0 and ready:
                                    write("START")
                                    running = False
                                


        # Render player list
        #render_player_list(nickname_array, integer_array)

        #Draw buttons
        if hosting == 2:
            for i, button_rect in enumerate(button_rects):
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(multi_server_selected_buttons[i], button_rect)
                else:
                    screen.blit(multi_server_buttons[i], button_rect)
        else:
            for i, button_rect in enumerate(button_rects2):
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(multi_server_selected_buttons[i], button_rect)
                else:
                    screen.blit(multi_server_buttons[i], button_rect)

        if game_start:
            running = False
        pygame.display.flip()

    return 
ready_list1 = [-1, -1, -1, -1, -1]
ready_list2 = [-1, -1, -1, -1, -1]

def supremacy_server(drone_type, secondary):
    play_song("sound/FireAhead.mp3")
    global solution_array, ready_list1, ready_list2, nickname_array, player_list, full_player_id, team_update, team1_names, team2_names, ready_list, hosting, user_id
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    CUSTOM_BLUE = (162, 251, 255)
    TEAL = (0, 255, 255)

    # Font for displaying text
    font_path = "fonts/ACES07_Regular.ttf"  # Replace "path/to/your/font.ttf" with the actual path to your font file
    AG_path = "AgencyFBCondensed Bold.otf"
    font = pygame.font.Font(AG_path, 48)  # Replace "path/to/your/font.ttf" with the actual path to your font file
    AG_standard = pygame.font.Font(AG_path, 42)  # Adjust the font size (36) as needed
    AG_Large = pygame.font.Font(AG_path, 88)  # Adjust the font size (36) as needed
    custom_font_Ammo = pygame.font.Font(AG_path, 48)  # Adjust the font size (36) as needed

    # Server details
    HOST = ''
    PORT = 55555

    # Player details
    player_list = []
    nickname_array = []
    integer_array = []
    # Client inputs
    team_id = 1
    full_player_id = f"{username}/{drone_type}{secondary}{team_id}"
    team_name = AG_standard.render("A T H E N A", True, CUSTOM_BLUE)
    title_screen_image = "images/Example_Server_Template.png"
    player_name = AG_standard.render(f"{username}", True, CUSTOM_BLUE)
    # Define positions for each set of values
    list_positions1 = [(1536, 163), (1720, 163), None, (1390, 163)]
    list_positions2 = [(1536, 644), (1720, 644), None, (1390, 644)]
    # ready_list1 = [-1, -1, -1, -1, -1]
    # ready_list2 = [-1, -1, -1, -1, -1]
    ready_list = ["READY", "READY", "READY", "READY", "READY"]
    team_update = 0

    multi_server_buttons = [pygame.image.load("images/Server_Buttons/start_button.png"), 
                        pygame.image.load("images/Server_Buttons/quit_button.png"), 
                        pygame.image.load("images/Server_Buttons/Switch_button.png")]  # Corrected lowercase filenames
    multi_server_selected_buttons = [pygame.image.load("images/Server_Buttons/start_button_selected.png"), 
                                pygame.image.load("images/Server_Buttons/quit_button_selected.png"), 
                                pygame.image.load("images/Server_Buttons/Switch_button_selected.png")]  # Corrected lowercase filenames
    button_rects = []
    stamp_images = ["images/Stamp_boxes/WC_Stamp.png","images/Stamp_boxes/WC_Stamp.png", "images/Stamp_boxes/ST_Stamp.png","images/Stamp_boxes/ST_Stamp.png",
                    "images/Stamp_boxes/GC_Stamp.png", "images/Stamp_boxes/GC_Stamp.png", "images/Stamp_boxes/FW_Stamp.png", "images/Stamp_boxes/FW_Stamp.png"]

    stamp_position = (120, 200)
    stamp_rect = pygame.image.load(stamp_images[int(drone_type)]).get_rect(topleft=stamp_position)

    # Define positions for each button
    button_positions = [(405, 920), (120, 920), (120, 1020)]  # Adjust positions as needed

    # Create buttons and button rects with specific positions
    for button_image, position in zip(multi_server_buttons, button_positions):
        button_rect = button_image.get_rect(topleft=position)
        button_rects.append(button_rect)

    solution_array = [-1, -1, -1, -1, -1, -1, 1, -1, -1, -1]
    # Connect to the server
    #client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


    # Start the receive thread
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    import numpy as np

    def play_video(video_file, surface):
        cap = cv2.VideoCapture(video_file)
        clock = pygame.time.Clock()

        running = True
        while running:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV uses BGR, Pygame uses RGB
            frame = np.rot90(frame)  # Rotate frame if necessary
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frame_rect = frame.get_rect()
            frame_rect.center = (WIDTH //2, HEIGHT // 2)
            
            surface.blit(frame, frame_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(30)  # Adjust frame rate as necessary

        cap.release()
    screen = pygame.display.set_mode((1920, 1080))
    video_file = "Abstract1.mp4"  # Replace with your video file path
    play_video(video_file, screen)
    # Main loop
    running = True
    display_menu(title_screen_image)
    screen.blit(pygame.image.load(stamp_images[int(drone_type)]),stamp_rect)
    screen.blit(player_name, (265, 227))
    screen.blit(team_name, (150, 685))
    write("UID_Request")
    while running:
        sys.stdout.flush()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(event.pos):
                        play_sound_effect("sound/UI_MENU_select_basic.wav")
                        if i == 1:
                            pygame.quit()
                        elif i == 0:
                            if hosting == 1 and game_ready:
                                write("START")
                                running = False
                                return
                                # Return the index of the selected button
                            else:
                                write("READY")
                                print("READY")
                        elif i ==2:
                            if user_ids.index(user_id) < 5:
                                write(f"CHANGETEAM {2}")
                            else: write(f"CHANGETEAM {1}")
                            

        # Render player list
        # render_player_list(nickname_array, integer_array)
        if team_update:
            display_menu(title_screen_image)

            screen.blit(pygame.image.load(stamp_images[int(drone_type)]),stamp_rect)
            screen.blit(player_name, (265, 227))
            screen.blit(team_name, (150, 685))
            team1_count = AG_Large.render(f"{len(team1_names)}", True, TEAL)
            team2_count = AG_Large.render(f"{len(team2_names)}", True, RED)

            render_team(team1_ids, list_positions1)
            render_team(team2_ids, list_positions2)
            render_text(screen, team1_names, 1210, 163, 78, center=True)
            render_text(screen, team2_names, 1210, 644, 78, center=True)

            render_text(screen, ready_list, 950, 150, 80, ready_list1)
            render_text(screen, ready_list, 950, 629, 80, ready_list2)
            screen.blit(team1_count, (215, 800))
            screen.blit(team2_count, (578, 800))
            team_update = 0

        #Draw buttons
        for i, button_rect in enumerate(button_rects):
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(multi_server_selected_buttons[i], button_rect)
            else:
                screen.blit(multi_server_buttons[i], button_rect)

        pygame.display.flip()

mode = 0
def menu_loop():
    global drone_button_images, drone_button_sel_images, mode, selected_character, weapon_choice, full_player_id, free, username
    stat_screen_images = [
        "Plane_Screens/KiRa.png",
        "Plane_Screens/AlpAur.png",
        "Plane_Screens/ShiVind.png",
        "Plane_Screens/CrCh.png",
        "Plane_Screens/FalVi.png",
        "Plane_Screens/AvMo.png",
        "Plane_Screens/AsNof.png",
        "Plane_Screens/AsWyv.png",
        # Add paths to stat screen images for each character selection
    ]
    main_menu()
    selected_mode = game_mode_selection()
    play_song("sound/MMG.wav")
    username = login_menu()
    play_sound_effect("sound/UI_MENU_bleep.wav")
    if selected_mode == 0:
        while True:
            selected_character = dynamic_menu(8, drone_button_images, drone_button_sel_images, stat_screen_images, 0, drone_back_iamge, menu_button1)
            play_sound_effect("sound/UI_MENU_THRU.wav")
            if selected_character is not None:
                # Add code to handle character selection (e.g., display character image)
                print("Selected character:", selected_character)
                # You can add code here to display the selected character image on the right side of the screen

                # After character selection, move on to the next step
                print("Moving on to the next step...")
                break
        
        user_selections = weapon_select(selected_character)
        drone_button_images = load_selected_images(user_selections, weapon_button_image_paths)
        drone_button_sel_images = load_selected_images(user_selections, weapon_button_image_selected_paths)
        drone_backgrounds = set_selected_images(user_selections, weapon_stat_image_paths)
        weapon_choice = dynamic_menu(len(drone_button_images), drone_button_images, drone_button_sel_images, drone_backgrounds, 1, weapon_back_image, menu_button2)
        play_sound_effect("sound/UI_MENU_THRU.wav")
        mode = experience()
        play_sound_effect("sound/UI_MENU_select_basic.wav")
        if mode == 2:
            duel_server(selected_character, weapon_choice)
        elif mode == 3:
            full_player_id = f"{username}/{selected_character}{weapon_choice}{0}"

            #client.connect((HOST, PORT))

            #client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            free = 1
            # Start the receive thread
            #receive_thread = threading.Thread(target=receive)
            #receive_thread.start()


        elif mode == 4:
            supremacy_server(selected_character, weapon_choice)

    elif selected_mode == 1:
        # Add code to start Game Mode 2
        pass
    elif selected_mode == 2:
        # Add code to open Settings Menu
        pass
team1_score = 10
team2_score = 10

def read_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    vision_type = config.get('Game', 'vision_type')
    color_option = config.get('Game', 'color_option')
    
    if vision_type != 'ColorVision':
        print("Error: Vision type is not ColorVision.")
    
    return color_option

def seeing():
    global radar_lock
    pink_detection = vision.Vision(rval,vc,frame, HEIGHT, WIDTH)
    pink_detection.see_variable(read_config('config.ini'))
    radar_lock = pink_detection.is_detected()

radar_lock = False

menu_loop()
if mode == 2:
    duel = True
    print(f'HIDS: {host_ids}')
    print(f'HOSTING: {client_ids}')
    if hosting == 1:
        p_id = 0
        opp_id = 1
        players[p_id] = drone_bank(int(host_ids[0]), weapon_bank(int(host_ids[0]), int(host_ids[1])))
        players[opp_id] = drone_bank(int(client_ids[0]), weapon_bank(int(client_ids[0]), int(client_ids[1])))
        player = p_id
        opponent = opp_id
    else:
        p_id = 1
        opp_id = 0
        players[opp_id] = drone_bank(int(host_ids[0]), weapon_bank(int(host_ids[0]), int(host_ids[1])))
        players[p_id] = drone_bank(int(client_ids[0]), weapon_bank(int(client_ids[0]), int(client_ids[1])))
        player = p_id
        opponent = opp_id
    game_running = True
elif mode == 4:
    supremacy = True
    p_id = 0
    opp_id = 1
    players[p_id] = drone_bank(int(selected_character), weapon_bank(selected_character, int(weapon_choice)))
    players[opp_id] = drone_bank(0, weapon_bank(0, 0))
    player = p_id
    opponent = opp_id
elif mode == 3:
    free = True
    supremacy = False
    p_id = 0
    opp_id = 1
    players[p_id] = drone_bank(int(selected_character), weapon_bank(selected_character, int(weapon_choice)))
    players[opp_id] = drone_bank(0, weapon_bank(0, 0))
    player = p_id
    opponent = opp_id
play_video_na("video/LoadingScreen.mp4", screen)
button_events_thread.start()
vision_thread = threading.Thread(target=seeing)
vision_thread.start()
#serial_thread = threading.Thread(target=handle_serial_input)
#serial_thread.daemon = True
#serial_thread.start()
start_time = pygame.time.get_ticks()
play_sound_effect("sound/ST_INTRO.wav")
play_song("sound/Showdown.mp3")
while True:
    #modify video feed for pygame
    frame = np.fliplr(frame)
    frame = np.rot90(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = cv2.resize(frame, (1080, 1920))
    surf = pygame.surfarray.make_surface(frame)
    surf = pygame.transform.scale(surf, (WIDTH, HEIGHT))
    screen.blit(surf, (0,0))
    rval, frame = vc.read()
    render_full_game()
    #print(radar_lock)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        pygame.quit()
        client.close()
        break

# Quit pygame
pygame.quit()
