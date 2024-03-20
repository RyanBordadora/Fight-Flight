import pygame
import sys
import socket
import threading
from drone_list import *
from weapon_list import *
import cv2

username = "ERROR"

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CUSTOM_BLUE = (162, 251, 255)
TEAL = (0, 255, 255)
RED = (255, 0, 0)

# Server details
HOST = '10.252.1.122'
PORT = 55555

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Title")

def play_sound_effect(sound):
    sound_effect = pygame.mixer.Sound(sound)
    sound_effect.set_volume(0.5)
    sound_effect.play()

# Load images
title_screen_image = "images/main_menu.png"
background_image = "images/gamemode_select.png"
weapon_back_image = "images/Weapon_Selection_Template.png"
drone_back_iamge = "images/Drone_Selection_Template.png"
button_image = pygame.image.load("Main2Buttons/play_button.png")
button_hover_image = pygame.image.load("Main2Buttons/play_button_selected.png")
cbutton_image = pygame.image.load("images/raptor_button.png")
cbutton_hover_image = pygame.image.load("images/raptor_button_selected.png")
stats_image = pygame.image.load("images/Play.png")
login_image = "images/login.png"

drone_button_images = [
        pygame.image.load("buttons/kr_button.png"),
        pygame.image.load("buttons/aa_button.png"),
        pygame.image.load("buttons/sv_button.png"),
        pygame.image.load("buttons/cc_button.png"),
        pygame.image.load("buttons/FV_button.png"),
        pygame.image.load("buttons/AM_button.png"),
        pygame.image.load("buttons/AN_button.png"),
        pygame.image.load("buttons/AW_button.png")
    ]

drone_button_sel_images = [
    pygame.image.load("buttons/kr_button_selected.png"),
    pygame.image.load("buttons/aa_button_selected.png"),
    pygame.image.load("buttons/sv_button_selected.png"),
    pygame.image.load("buttons/cc_button_selected.png"),
    pygame.image.load("buttons/FV_button_selected.png"),
    pygame.image.load("buttons/AM_button_selected.png"),
    pygame.image.load("buttons/AN_button_selected.png"),
    pygame.image.load("buttons/AW_button_selected.png")
    ]

# Define the path to the font file images/drone_select_image.png
font_path = "fonts/ACES07_Regular.ttf"  # Replace "path/to/your/font.ttf" with the actual path to your font file

# Load the font
custom_font_standard = pygame.font.Font(font_path, 24)  # Adjust the font size (36) as needed


# Define a dictionary to map user selections to image paths
weapon_stat_image_paths = {
    #Universal
    'AAM': "Weapon_Screens/WoC/AAM.png",
    #WOC
    'EPL': "Weapon_Screens/WoC/EPL.png",
    'HPME': "Weapon_Screens/WoC/HPME.png",
    'LRBM': "Weapon_Screens/WoC/LRBM.png",
    'QAAM': "Weapon_Screens/WoC/QAAM.png",
    #ST
    'HCAA': "Weapon_Screens/ST/HCAA.png",
    'HPAA': "Weapon_Screens/ST/HPAA.png",
    'HVAA': "Weapon_Screens/ST/HVAA.png",
    'MGP': "Weapon_Screens/ST/MGP.png",
    'SAAM': "Weapon_Screens/ST/SAAM.png",
    #GC
    'HLC': "Weapon_Screens/GC/HLC.png",
    'IIC': "Weapon_Screens/GC/IIC.png",
    'SPC': "Weapon_Screens/GC/SPC.png",
    'TLS': "Weapon_Screens/GC/TLS.png",
    #FW
    'CPC': "Weapon_Screens/FW/CPC.png",
    'EML': "Weapon_Screens/FW/EML.png",
    'PEML': "Weapon_Screens/FW/PEML.png",
    'UAV': "Weapon_Screens/FW/UAV.png"
}
host_ids = []
weapon_button_image_paths = {
    #Universal
    'AAM': "buttons/Missiles/AAM_button.png",
    #WOC
    'EPL': "buttons/Hitscan/EPL_button.png",
    'HPME': "buttons/Beams/HPME_button.png",
    'LRBM': "buttons/Missiles/LRBM_button.png",
    'QAAM': "buttons/Missiles/QAAM_button.png",
    #ST
    'HCAA': "buttons/Missiles/HCAAM_button.png",
    'HPAA': "buttons/Missiles/HPAAM_button.png",
    'HVAA': "buttons/Missiles/HVAAM_button.png",
    'MGP': "buttons/Gun/MGP_button.png",
    'SAAM': "buttons/Missiles/SAAM_button.png",
    #GC
    'HLC': "buttons/Beams/HLC_button.png",
    'IIC': "buttons/Beams/IIC_button.png",
    'SPC': "buttons/Gun/SPB_button.png",
    'TLS': "buttons/Beams/TLS_button.png",
    #FW
    'CPC': "buttons/Beams/CPC_button.png",
    'EML': "buttons/Hitscan/EML_button.png",
    'PEML': "buttons/Hitscan/PEML_button.png",
    'UAV': "buttons/Hitscan/UAV_button.png"
}

weapon_button_image_selected_paths = {
    #Universal
    'AAM': "buttons/Missiles/AAM_button_selected.png",
    #WOC
    'EPL': "buttons/Hitscan/EPL_button_selected.png",
    'HPME': "buttons/Beams/HPME_button_selected.png",
    'LRBM': "buttons/Missiles/LRBM_button_selected.png",
    'QAAM': "buttons/Missiles/QAAM_button_selected.png",
    #ST
    'HCAA': "buttons/Missiles/HCAAM_button_selected.png",
    'HPAA': "buttons/Missiles/HPAAM_button_selected.png",
    'HVAA': "buttons/Missiles/HVAAM_button_selected.png",
    'MGP': "buttons/Gun/MGP_button_selected.png",
    'SAAM': "buttons/Missiles/SAAM_button_selected.png",
    #GC
    'HLC': "buttons/Beams/HLC_button_selected.png",
    'IIC': "buttons/Beams/IIC_button_selected.png",
    'SPC': "buttons/Gun/SPB_button_selected.png",
    'TLS': "buttons/Beams/TLS_button_selected.png",
    #FW
    'CPC': "buttons/Beams/CPC_button_selected.png",
    'EML': "buttons/Hitscan/EML_button_selected.png",
    'PEML': "buttons/Hitscan/PEML_button_selected.png",
    'UAV': "buttons/Hitscan/UAV_button_selected.png"
}

def find_host_and_client(id_array):
        host_index = None
        client_index = None
        
        for i, id_entry in enumerate(id_array):
            if id_entry[-1] == 0:
                host_index = i
            else:
                client_index = i
        
        return host_index, client_index


def weapon_select(drone_number):
    if drone_number == 0:
        return ['QAAM', 'AAM', 'EPL', 'HPME', 'LRBM']
    elif drone_number == 1:
        return ['AAM', 'EPL', 'HPME', 'LRBM']
    elif drone_number == 2 or drone_number == 3:
        return ['AAM', 'HCAA', 'HPAA', 'HVAA', 'MGP', 'SAAM']
    elif drone_number == 4:
        return ['SPC', 'AAM', 'HLC', 'IIC']
    elif drone_number == 5:
        return ['TLS', 'AAM', 'HLC', 'IIC']
    elif drone_number == 6:
        return ['UAV', 'AAM', 'CPC', 'PEML']
    elif drone_number == 7:
        return ['EML', 'AAM', 'CPC', 'PEML']

# Function to load images based on user selections
def load_selected_images(selections, image_paths):
    selected_images = []
    for selection in selections:
        if selection in image_paths:
            selected_images.append(pygame.image.load(image_paths[selection]))
    return selected_images

def set_selected_images(selections, image_paths):
    selected_images = []
    for selection in selections:
        if selection in image_paths:
            selected_images.append(image_paths[selection])
    return selected_images

def display_menu(image):
        img = pygame.image.load(image).convert()
        img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
        screen.blit(img,(0,0))

def parse_message(message):
    parts = message.split('/')  # Split the message using / as the delimiter
    if len(parts) < 2:
        raise ValueError("Message format is invalid")
    nickname = parts[0]
    integers = []
    try:
        integers = [int(char) for char in parts[1]]
    except ValueError:
        raise ValueError("Non-integer found in the second part of the message")
    return nickname, integers

def parse_player_update(update_string):
    # Remove "Player Update:" from the string
    update_string = update_string.replace("Player Update:", "")
    
    # Split the update string by ','
    updates = update_string.split(',')

    # Split each update by '/' and append to the result list
    result = [update.split('/') for update in updates]

    # Join the first two elements of each sublist by '/' and add to the final result list
    final_result = [f"{item[0]}/{item[1][:4]}" for item in result]

    return final_result
# drone_button_images = [pygame.image.load("buttons/kr_button.png"), pygame.image.load("images/aa_button.png"), pygame.image.load("images/sv_button.png"), pygame.image.load("images/cc__button.png"),
#                        pygame.image.load("images/FV_button.png"), pygame.image.load("images/AM_button.png"), pygame.image.load("images/AN_button.png"), pygame.image.load("images/AW_button.png")]
# drone_button_sel_images = [pygame.image.load("buttons/kr_button_selected.png"), pygame.image.load("images/aa_button_selected.png"), pygame.image.load("images/sv_button_selected.png"), pygame.image.load("images/cc__button_selected.png"),
#                        pygame.image.load("images/FV_button_selected.png"), pygame.image.load("images/AM_button_selected.png"), pygame.image.load("images/AN_button_selected.png"), pygame.image.load("images/AW_button_selected.png")]
character_weapon_count = [4, 4, 5, 5, 2, 2, 2, 2]

# Function to display images
def blit_center(image):
    screen.blit(image, (WIDTH // 2 - image.get_width() // 2, HEIGHT // 2 - image.get_height() // 2))

# Function to check if mouse is over a button
def is_mouse_over_button(button_rect):
    mouse_pos = pygame.mouse.get_pos()
    return button_rect.collidepoint(mouse_pos)

def display_menu(image):
    img = pygame.image.load(image).convert()
    img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
    screen.blit(img,(0,0))

# Main menu loop
def main_menu():
    display_menu(title_screen_image)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# Game mode selection loop
def game_mode_selection():
    display_menu(background_image)

    menu_2_buttons = [pygame.image.load("Main2Buttons/play_button.png"), 
                      pygame.image.load("Main2Buttons/demo_button.png"), 
                      pygame.image.load("Main2Buttons/setting_button.png")]  # Corrected lowercase filenames
    menu_2_selected_buttons = [pygame.image.load("Main2Buttons/play_button_selected.png"), 
                               pygame.image.load("Main2Buttons/demo_button_selected.png"), 
                               pygame.image.load("Main2Buttons/setting_button_selected.png")]  # Corrected lowercase filenames
    
    button_rects = []

    # Define positions for each button
    button_positions = [(237, 229), (1225, 234), (756, 879)]  # Adjust positions as needed

    # Create buttons and button rects with specific positions
    for button_image, position in zip(menu_2_buttons, button_positions):
        button_rect = button_image.get_rect(topleft=position)
        button_rects.append(button_rect)

    while True:
        display_menu(background_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(event.pos):
                        return i  # Return the index of the selected button
        
        # Draw buttons
        for i, button_rect in enumerate(button_rects):
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(menu_2_selected_buttons[i], button_rect)
            else:
                screen.blit(menu_2_buttons[i], button_rect)

        pygame.display.flip()


def server_screen():
    nickname = input("Choose a nickname: ")

    # Font for displaying text
    font_path = "fonts/ACES07_Regular.ttf"  # Replace "path/to/your/font.ttf" with the actual path to your font file
    AG_path = "AgencyFBCondensed Bold.otf"
    font = pygame.font.Font(AG_path, 48)  # Replace "path/to/your/font.ttf" with the actual path to your font file
    AG_standard = pygame.font.Font(AG_path, 42)  # Adjust the font size (36) as needed
    AG_Large = pygame.font.Font(AG_path, 88)  # Adjust the font size (36) as needed

    # Server details
    HOST = '192.168.1.99'
    PORT = 55555

    # Player details
    player_list = []
    nickname_array = []
    integer_array = []
    # Client inputs
    drone_type = input("Select 0-9:")
    secondary = input("Select 0-9 ")
    team_id = input("Select 0-2")
    full_player_id = f"{nickname}/{drone_type}{secondary}{team_id}"
    team_name = AG_standard.render("A T H E N A", True, CUSTOM_BLUE)
    title_screen_image = "images/Example_Server_Template.png"
    player_name = AG_standard.render(f"{nickname}", True, CUSTOM_BLUE)
    # Define positions for each set of values
    list_positions1 = [(1536, 163), (1720, 163), None, (1390, 163)]
    list_positions2 = [(1536, 644), (1720, 644), None, (1390, 644)]
    ready_list1 = [1, 0, 1, 0, 0]
    ready_list2 = [1, 0, 0, 0, 0]
    ready_list = ["READY", "READY", "READY", "READY", "READY"]
    team_update = 0

    multi_server_buttons = [pygame.image.load("images/Server_Buttons/start_button.png"), 
                        pygame.image.load("images/Server_Buttons/quit_button.png"), 
                        pygame.image.load("images/Server_Buttons/Switch_button.png")]  # Corrected lowercase filenames
    multi_server_selected_buttons = [pygame.image.load("images/Server_Buttons/start_button_selected.png"), 
                                pygame.image.load("images/Server_Buttons/quit_button_selected.png"), 
                                pygame.image.load("images/Server_Buttons/Switch_button_selected.png")]  # Corrected lowercase filenames
    button_rects = []
    stamp_images = ["images/Stamp_boxes/WC_Stamp.png", "images/Stamp_boxes/ST_Stamp.png", "images/Stamp_boxes/GC_Stamp.png", "images/Stamp_boxes/FW_Stamp.png"]
    stamp_position = (120, 200)
    stamp_rect = pygame.image.load(stamp_images[int(drone_type)]).get_rect(topleft=stamp_position)

    # Define positions for each button
    button_positions = [(405, 920), (120, 920), (120, 1020)]  # Adjust positions as needed

    # Create buttons and button rects with specific positions
    for button_image, position in zip(multi_server_buttons, button_positions):
        button_rect = button_image.get_rect(topleft=position)
        button_rects.append(button_rect)

    def parse_message(message):
        parts = message.split('/')  # Split the message using / as the delimiter
        if len(parts) < 2:
            raise ValueError("Message format is invalid")
        nickname = parts[0]
        integers = []
        try:
            integers = [int(char) for char in parts[1]]
        except ValueError:
            raise ValueError("Non-integer found in the second part of the message")
        return nickname, integers

    def parse_player_update(update_string):
        # Remove "Player Update:" from the string
        update_string = update_string.replace("Player Update:", "")
        
        # Split the update string by ','
        updates = update_string.split(',')

        # Split each update by '/' and append to the result list
        result = [update.split('/') for update in updates]

        # Join the first two elements of each sublist by '/' and add to the final result list
        final_result = [f"{item[0]}/{item[1][:4]}" for item in result]

        return final_result

    def separate_teams(names, id_codes):
        team1_names = []
        team1_ids = []
        team2_names = []
        team2_ids = []

        for name, id_code in zip(names, id_codes):
            team_number = id_code[-2]  # Second to last value is the team number
            print(f"Name: {name}, ID Code: {id_code}, Team Number: {team_number}")
            if team_number == 1:
                team1_names.append(name)
                team1_ids.append(id_code)
            elif team_number == 2:
                team2_names.append(name)
                team2_ids.append(id_code)

        return team1_names, team1_ids, team2_names, team2_ids

    # Function to receive messages from the server
    def receive():
        global player_list, team_update
        global nickname_array, integer_array, team1_ids, team2_ids, team1_names, team2_names

        while True:
            try:
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(full_player_id.encode('ascii'))
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
                            print(f"NA: {nickname_array}")
                            print(f"IA: {integer_array}")
                        except ValueError as e:
                            print(f"Error parsing player info: {e}")
                    team1_names, team1_ids, team2_names, team2_ids = separate_teams(nickname_array, integer_array)
                    print("Received T1ID:", team1_ids)
                    print("Received T2ID:", team2_ids)
                    team_update = 1
                else:
                    print("Received message:", message)  # Handle other types of messages if needed
            except Exception as e:
                print("An error occurred:", e)
                client.close()
                break

    def foo1(value):
        if value == 0:
            return "Zero"
        if value == 1:
            return "One"
        elif value == 2:
            return "Two"
        elif value == 3:
            return "Three"
        elif value == 4:
            return "Four"
        elif value == 5:
            return "Five"
        elif value == 6:
            return "Six"
        elif value == 7:
            return "Seven"
        else:
            return "Unknown"

    def foo2(value1, value2):
        if value1 == 0:
            if value2 == 0:
                return "Even"
            elif value2 == 1:
                return "Odd"
            elif value2 == 2:
                return "Odd"
            elif value2 == 3:
                return "Odd"
            elif value2 == 4:
                return "Odd"
            elif value2 == 5:
                return "Odd"
        elif value1 == 1:
            if value2 == 0:
                return "Even"
            elif value2 == 1:
                return "Odd"
            elif value2 == 2:
                return "Odd"
            elif value2 == 3:
                return "Odd"
            elif value2 == 4:
                return "Odd"
            elif value2 == 5:
                return "Odd"
        elif value1 == 2:
            if value2 == 0:
                return "Even"
            elif value2 == 1:
                return "Odd"
            elif value2 == 2:
                return "Odd"
            elif value2 == 3:
                return "Odd"
            elif value2 == 4:
                return "Odd"
            elif value2 == 5:
                return "Odd"
        elif value1 == 3:
            if value2 == 0:
                return "Even"
            elif value2 == 1:
                return "Odd"
            elif value2 == 2:
                return "Odd"
            elif value2 == 3:
                return "Odd"
            elif value2 == 4:
                return "Odd"
            elif value2 == 5:
                return "Odd"
        elif value1 == 4:
            if value2 == 0:
                return "Even"
            elif value2 == 1:
                return "Odd"
            elif value2 == 2:
                return "Odd"
            elif value2 == 3:
                return "Odd"
            elif value2 == 4:
                return "Odd"
            elif value2 == 5:
                return "Odd"
        else:
            return "NONE"

    def render_team(id_codes, list_positions):
        for i in range(4):
            if list_positions[i] is None:
                continue  # Skip rendering if position is None
            x, y = list_positions[i]
            for array in id_codes:
                if i == 0:
                    value = array[i]
                    text = font.render(foo1(value), True, WHITE)
                elif i == 1:
                    value1 = array[i-1]
                    value2 = array[i]
                    text = font.render(foo2(value1, value2), True, WHITE)
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

    # Main loop
    # Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Start the receive thread
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    running = True
    display_menu(title_screen_image)
    screen.blit(pygame.image.load(stamp_images[int(drone_type)]),stamp_rect)
    screen.blit(player_name, (265, 227))
    screen.blit(team_name, (150, 685))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(event.pos):
                        print(i)  # Return the index of the selected button

        # Render player list
        #render_player_list(nickname_array, integer_array)
        if team_update:
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

    pygame.quit()



def game_mode_1_selection():
    display_menu(background_image)
    
    # Load and scale button images
    drone_button_images = [
        pygame.image.load("buttons/kr_button.png"),
        pygame.image.load("buttons/aa_button.png"),
        pygame.image.load("buttons/sv_button.png"),
        pygame.image.load("buttons/cc_button.png"),
        pygame.image.load("buttons/FV_button.png"),
        pygame.image.load("buttons/AM_button.png"),
        pygame.image.load("buttons/AN_button.png"),
        pygame.image.load("buttons/AW_button.png")
    ]
    drone_button_sel_images = [
        pygame.image.load("buttons/kr_button_selected.png"),
        pygame.image.load("buttons/aa_button_selected.png"),
        pygame.image.load("buttons/sv_button_selected.png"),
        pygame.image.load("buttons/cc_button_selected.png"),
        pygame.image.load("buttons/FV_button_selected.png"),
        pygame.image.load("buttons/AM_button_selected.png"),
        pygame.image.load("buttons/AN_button_selected.png"),
        pygame.image.load("buttons/AW_button_selected.png")
    ]
    
    button_width = drone_button_images[0].get_width()
    button_height = drone_button_images[0].get_height()
    hover_shift = 93
    # Calculate button positions
    button_spacing = 15
    start_x = 305
    start_y = (HEIGHT - 8 * (button_height + button_spacing)) // 2
    
    # Create buttons
    button_rects = []
    for i in range(8):
        button_rects.append(pygame.Rect(start_x, start_y + i * (button_height + button_spacing), button_width, button_height))
    next_button_rect = pygame.Rect(600, 500, button_width, button_height)

    # Stat screen images for each character selection
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

    selected_character = None
    
    while True:
        if selected_character is not None:
            display_menu(stat_screen_images[selected_character])
        else:
            display_menu(background_image)
        
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(event.pos):
                        # Reset selection
                        play_sound_effect("sound/UI_MENU_MP_countdown.wav")
                        selected_character = i if selected_character != i else None
                        break
                if next_button_rect.collidepoint(event.pos):
                    if selected_character is not None:
                        print("Character", selected_character, "selected")
                        # Display the stat screen for the selected character
                        return selected_character  # Return the selected character index
        # Draw buttons
        for i, button_rect in enumerate(button_rects):
            if selected_character == i:
                hover_image_x = button_rect.x + hover_shift + (button_rect.width - drone_button_sel_images[i].get_width()) // 2
                hover_image_y = button_rect.y + (button_rect.height - drone_button_sel_images[i].get_height()) // 2
                #pygame.draw.rect(screen, (0, 255, 0), button_rect, 2)  # Draw a green border around the selected button
                screen.blit(drone_button_sel_images[i], (hover_image_x, hover_image_y))  # Draw selected button image
            else:
                pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)  # Draw a white border around unselected buttons
                if not button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(drone_button_images[i], button_rect)  # Draw unselected button image

            if button_rect.collidepoint(pygame.mouse.get_pos()):
                # Align the hover image with the button rectangle
                hover_image_x = button_rect.x + hover_shift + (button_rect.width - drone_button_sel_images[i].get_width()) // 2
                hover_image_y = button_rect.y + (button_rect.height - drone_button_sel_images[i].get_height()) // 2
                screen.blit(drone_button_sel_images[i], (hover_image_x, hover_image_y))  # Draw hover image

        # Draw next button
        if selected_character is not None:
            screen.blit(cbutton_image, next_button_rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), next_button_rect, 2)  # Draw a red border around the next button if no character is selected

        pygame.display.flip()

def dynamic_menu(button_count, button_images, button_sel_images, stat_screen_images, weapon, background_image, menu_button):
    display_menu(background_image)
    
    if weapon == 0:
        hover_shift = 93
    else:
        hover_shift = 193
    # Calculate button positions
    button_width = button_images[0].get_width()
    button_height = button_images[0].get_height()
    button_spacing = 15
    start_x = 305
    start_y = (HEIGHT - button_count * (button_height + button_spacing)) // 2

    
    # Create buttons   
    button_rects = []
    for i in range(button_count):
        button_rects.append(pygame.Rect(start_x, start_y + i * (button_height + button_spacing), button_width, button_height))
    next_button_rect = pygame.Rect(300, 900, button_width, button_height)

    selected_option = None
    
    while True:
        if selected_option is not None:
            display_menu(stat_screen_images[selected_option])
        else:
            display_menu(background_image)
        
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(event.pos):
                        # Reset selection
                        play_sound_effect("sound/UI_MENU_MP_countdown.wav")
                        selected_option = i if selected_option != i else None
                        break
                if next_button_rect.collidepoint(event.pos):
                    if selected_option is not None:
                        print("Option", selected_option, "selected")
                        # Add your logic here for the selected option
                        return selected_option  # Return the selected option index
        
        # Draw buttons
        for i, button_rect in enumerate(button_rects):
            if selected_option == i:
                hover_image_x = button_rect.x + hover_shift + (button_rect.width - button_sel_images[i].get_width()) // 2
                hover_image_y = button_rect.y + (button_rect.height - button_sel_images[i].get_height()) // 2
                screen.blit(button_sel_images[i], (hover_image_x, hover_image_y))  # Draw selected button image
            else:
                pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)  # Draw a white border around unselected buttons
                if not button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(button_images[i], button_rect)  # Draw unselected button image

            if button_rect.collidepoint(pygame.mouse.get_pos()):
                hover_image_x = button_rect.x + hover_shift + (button_rect.width - button_sel_images[i].get_width()) // 2
                hover_image_y = button_rect.y + (button_rect.height - button_sel_images[i].get_height()) // 2
                screen.blit(button_sel_images[i], (hover_image_x, hover_image_y))  # Draw hover image
        
        # Draw next button
        if selected_option is not None:
            screen.blit(menu_button, next_button_rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), next_button_rect, 2)  # Draw a red border around the next button if no option is selected
        
        pygame.display.flip()

def experience():
    import pygame
    import sys

    # Constants
    WIDTH, HEIGHT = 1920, 1080
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    CUSTOM_BLUE = (162, 251, 255)
    TEAL = (0, 255, 255)
    RED = (255, 0, 0)

    # Server details
    HOST = '192.168.1.232'
    PORT = 55555

    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Title")

    # Load images
    title_screen_image = "images/ExperienceSelection/Experience_Blank.png"
    # background_image = "images/gamemode_select.png"
    # button_image = pygame.image.load("images/ExperienceSelection/play_button.png")
    # button_hover_image = pygame.image.load("images/ExperienceSelection/play_button_Selected.png")
    # cbutton_image = pygame.image.load("images/raptor_button.png")
    # cbutton_hover_image = pygame.image.load("images/raptor_button_Selected.png")
    # stats_image = pygame.image.load("images/Play.png")


    def display_menu(image):
        img = pygame.image.load(image).convert()
        img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
        screen.blit(img,(0,0))

    # Main game loop
    def menu_loop():
        display_menu(title_screen_image)
        # Load images for buttons
        main_buttons  = [pygame.image.load("images/ExperienceSelection/SD_Button.png"), 
                        pygame.image.load("images/ExperienceSelection/Multiplayer_Button.png"),
                        pygame.image.load("images/ExperienceSelection/Duel_Button.png"), 
                        pygame.image.load("images/ExperienceSelection/Free_Button.png"),
                        pygame.image.load("images/ExperienceSelection/Supremacy_Button.png"), 
                        pygame.image.load("images/ExperienceSelection/Final_Button.png")]
        main_selected_buttons = [pygame.image.load("images/ExperienceSelection/SD_Button_Selected.png"), 
                                pygame.image.load("images/ExperienceSelection/Multiplayer_Button_Selected.png"),
                                pygame.image.load("images/ExperienceSelection/Duel_Button_Selected.png"), 
                                pygame.image.load("images/ExperienceSelection/Free_Button_Selected.png"),
                                pygame.image.load("images/ExperienceSelection/Supremacy_Button_Selected.png"), 
                                        pygame.image.load("images/ExperienceSelection/Final_Button_Selected.png")]

        main_button_positions = [(45, 135), (1004, 135), (45, 450), (1002, 449), (45, 450), (1002, 449)]


        # Create button rects
        main_rects = []

        for button_image, position in zip(main_buttons, main_button_positions):
            button_rect = button_image.get_rect(topleft=position)
            main_rects.append(button_rect)

        stamp_position = (1002, 970)
        stamp_rect = pygame.image.load("images/ExperienceSelection/ColorSorting.png").get_rect(topleft=stamp_position)
        reset = 0
        # Initially, only the main buttons are shown
        #current_buttons = main_buttons
        #current_selected_buttons = main_selected_buttons
        current_array = [1, 1, 0, 0, 0, 0]
        while True:
            if reset:
                display_menu(title_screen_image)
            # Display menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button_rect in enumerate(main_rects):
                        if button_rect.collidepoint(event.pos):
                            play_sound_effect("sound/UI_MENU_MP_countdown.wav")
                            # Reset selection
                            if i == 0:
                                current_array = [2, 1, 1, 1, 0, 0]
                            elif i == 1:
                                current_array = [1, 2, 0, 0, 1, 1]
                            else:
                                if current_array[5] == 1:
                                    return i + 2
                                else: return i
                            break

            for i, button_rect in enumerate(main_rects):
                if current_array[i] == 1:
                    if button_rect.collidepoint(pygame.mouse.get_pos()):
                        screen.blit(main_selected_buttons[i], button_rect)
                    else:
                        screen.blit(main_buttons[i], button_rect)
                elif current_array[i] == 2:
                    screen.blit(main_selected_buttons[i], button_rect)
            if current_array[5] == 1:
                screen.blit(pygame.image.load("images/ExperienceSelection/ColorSorting.png"),stamp_rect)
            else:
                reset = 1
            

            pygame.display.flip()
    return menu_loop()

def duel_server(drone_type, secondary):

    # Font for displaying text
    font_path = "fonts/ACES07_Regular.ttf"  # Replace "path/to/your/font.ttf" with the actual path to your font file
    AG_path = "AgencyFBCondensed Bold.otf"
    font = pygame.font.Font(AG_path, 48)  # Replace "path/to/your/font.ttf" with the actual path to your font file
    AG_standard = pygame.font.Font(AG_path, 42)  # Adjust the font size (36) as needed
    AG_Large = pygame.font.Font(AG_path, 88)  # Adjust the font size (36) as needed
    custom_font_Ammo = pygame.font.Font(AG_path, 48)  # Adjust the font size (36) as needed

    # Server details
    HOST = '10.252.1.122'
    PORT = 55555

    # Player details
    global nickname_array, player_list
    player_list = []
    nickname_array = []
    # Client inputs
    #drone_type = input("Select 0-9:")
    #secondary = input("Select 0-9 ")
    team_id = 0
    full_player_id = f"{username}/{drone_type}{secondary}{team_id}"
    title_screen_image = "images/DUEL_Blank.png"
    team_update = 0
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

    def display_menu(image):
        img = pygame.image.load(image).convert()
        img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
        screen.blit(img,(0,0))

    def parse_message(message):
        parts = message.split('/')  # Split the message using / as the delimiter
        if len(parts) < 2:
            raise ValueError("Message format is invalid")
        nickname = parts[0]
        integers = []
        try:
            integers = [int(char) for char in parts[1]]
        except ValueError:
            raise ValueError("Non-integer found in the second part of the message")
        return nickname, integers

    def parse_player_update(update_string):
        # Remove "Player Update:" from the string
        update_string = update_string.replace("Player Update:", "")
        
        # Split the update string by ','
        updates = update_string.split(',')

        # Split each update by '/' and append to the result list
        result = [update.split('/') for update in updates]

        # Join the first two elements of each sublist by '/' and add to the final result list
        final_result = [f"{item[0]}/{item[1][:4]}" for item in result]

        return final_result

    global screen_set
    screen_set =0
    # Function to receive messages from the server
    def receive():
        global player_list, team_update, hosting, screen_setz
        global nickname_array, integer_array, host_index, client_index, host_ids, client_ids, ready
        hosting = 0
        while True:
            sys.stdout.flush()
            try:
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(full_player_id.encode('ascii'))
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
                    host_index, client_index = find_host_and_client(integer_array)
                    print(f"HI:{host_index}")
                    print(f"NA:{nickname_array[host_index]} vs {username}")
                    print(f"CI:{client_index}")
                    #print(f"NA:{nickname_array[1]} vs {username}")
                    if host_index is not None:
                        if nickname_array[host_index] == username:
                            hosting = 1
                            print(hosting)
                        host_ids = integer_array[host_index]
                    if client_index is not None:
                        if nickname_array[client_index] == username:
                            hosting = 2
                        client_ids = integer_array[client_index]
                    screen_set = 1
                elif message == 'Client_Ready':
                    ready = 1
                    screen_set = 1
                else:
                    print("Received message:", message)  # Handle other types of messages if needed
            except Exception as e:
                print("An error occurred:", e)
                client.close()
                break



    sys.stdout.buffering = 0
    # Connect to the server
    HOST = socket.gethostbyname(socket.gethostname())
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    # Start the receive thread
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    Ready = AG_standard.render("R E A D Y", True, WHITE)

    def find_host_and_client(id_array):
        host_index = None
        client_index = None
        
        for i, id_entry in enumerate(id_array):
            if id_entry[-1] == 0:
                host_index = i
            else:
                client_index = i
        
        return host_index, client_index
    global ready
    ready = 0
    def write(message):
        client.send(message.encode('ascii'))

    Ready_react = Ready.get_rect(center=(1585, 800))
    stamp_image = pygame.image.load(stamp_images[int(drone_type)])
    stamp_position = (161, 154)
    stamp_rect = stamp_image.get_rect(topleft=stamp_position)
    stamp_position2 = (1172, 154)
    stamp_rect2 = stamp_image.get_rect(topleft=stamp_position2)

    # Main loop
    running = True
    hosting = 0
    def menu_refresh():
        global host_index, hosting, nickname_array, player_list, host_ids, client_ids
        if (len(player_list) >= 2 or hosting == 1) and host_index is not None and host_ids is not None:
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
        if ready:
            screen.blit(Ready, Ready_react)
    while running:
        sys.stdout.flush()
        #if screen_set == 1:
        menu_refresh()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
                                    print("START")
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
        pygame.display.flip()

    return Drone()

# def supremacy_server(drone_type, secondary):
#     import pygame
#     import socket
#     import threading
#     import sys


#     # Colors
#     WHITE = (255, 255, 255)
#     BLACK = (0, 0, 0)
#     RED = (255, 0, 0)
#     CUSTOM_BLUE = (162, 251, 255)
#     TEAL = (0, 255, 255)

#     # Font for displaying text
#     font_path = "fonts/ACES07_Regular.ttf"  # Replace "path/to/your/font.ttf" with the actual path to your font file
#     AG_path = "AgencyFBCondensed Bold.otf"
#     font = pygame.font.Font(AG_path, 48)  # Replace "path/to/your/font.ttf" with the actual path to your font file
#     AG_standard = pygame.font.Font(AG_path, 42)  # Adjust the font size (36) as needed
#     AG_Large = pygame.font.Font(AG_path, 88)  # Adjust the font size (36) as needed
#     custom_font_Ammo = pygame.font.Font(AG_path, 48)  # Adjust the font size (36) as needed

#     # Server details
#     HOST = '192.168.1.232'
#     PORT = 55555

#     # Player details
#     player_list = []
#     nickname_array = []
#     integer_array = []
#     # Client inputs
#     team_id = 1
#     full_player_id = f"{username}/{drone_type}{secondary}{team_id}"
#     team_name = AG_standard.render("A T H E N A", True, CUSTOM_BLUE)
#     title_screen_image = "images/Example_Server_Template.png"
#     player_name = AG_standard.render(f"{username}", True, CUSTOM_BLUE)
#     # Define positions for each set of values
#     list_positions1 = [(1536, 163), (1720, 163), None, (1390, 163)]
#     list_positions2 = [(1536, 644), (1720, 644), None, (1390, 644)]
#     ready_list1 = [0, 0, 0, 0, 0]
#     ready_list2 = [0, 0, 0, 0, 0]
#     ready_list = ["READY", "READY", "READY", "READY", "READY"]
#     team_update = 0

#     def last_id_for_name(name_array, id_array_list, query_name):
#         # Iterate through the name array to find the index of the query name
#         for i, name in enumerate(name_array):
#             if name == query_name:
#                 # Once the query name is found, return the last id from the corresponding id array list
#                 return id_array_list[i][-1]
#         # If the query name is not found, return None
#         return None

#     multi_server_buttons = [pygame.image.load("images/Server_Buttons/start_button.png"), 
#                         pygame.image.load("images/Server_Buttons/quit_button.png"), 
#                         pygame.image.load("images/Server_Buttons/Switch_button.png")]  # Corrected lowercase filenames
#     multi_server_selected_buttons = [pygame.image.load("images/Server_Buttons/start_button_selected.png"), 
#                                 pygame.image.load("images/Server_Buttons/quit_button_selected.png"), 
#                                 pygame.image.load("images/Server_Buttons/Switch_button_selected.png")]  # Corrected lowercase filenames
#     button_rects = []
#     stamp_images = ["images/Stamp_boxes/WC_Stamp.png", "images/Stamp_boxes/ST_Stamp.png", "images/Stamp_boxes/GC_Stamp.png", "images/Stamp_boxes/FW_Stamp.png"]
#     stamp_position = (120, 200)
#     stamp_rect = pygame.image.load(stamp_images[int(drone_type)]).get_rect(topleft=stamp_position)

#     # Define positions for each button
#     button_positions = [(405, 920), (120, 920), (120, 1020)]  # Adjust positions as needed

#     # Create buttons and button rects with specific positions
#     for button_image, position in zip(multi_server_buttons, button_positions):
#         button_rect = button_image.get_rect(topleft=position)
#         button_rects.append(button_rect)

#     def display_menu(image):
#         img = pygame.image.load(image).convert()
#         img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
#         screen.blit(img,(0,0))

#     def parse_message(message):
#         parts = message.split('/')  # Split the message using / as the delimiter
#         if len(parts) < 2:
#             raise ValueError("Message format is invalid")
#         nickname = parts[0]
#         integers = []
#         try:
#             integers = [int(char) for char in parts[1]]
#         except ValueError:
#             raise ValueError("Non-integer found in the second part of the message")
#         return nickname, integers

#     def parse_player_update(update_string):
#         # Remove "Player Update:" from the string
#         update_string = update_string.replace("Player Update:", "")
        
#         # Split the update string by ','
#         updates = update_string.split(',')

#         # Split each update by '/' and append to the result list
#         result = [update.split('/') for update in updates]

#         # Join the first two elements of each sublist by '/' and add to the final result list
#         final_result = [f"{item[0]}/{item[1][:4]}" for item in result]

#         return final_result

#     def parse_ready_update(update_string):
#         # Remove "Player Update:" from the string
#         update_string = update_string.replace("Ready Update:", "")
        
#         # Split the update string by ','
#         updates = update_string.split(',')

#         return updates

#     def separate_teams(names, id_codes):
#         team1_names = []
#         team1_ids = []
#         team2_names = []
#         team2_ids = []
#         team1_uids = []
#         team2_uids = []
#         uid_list=[]

#         for name, id_code in zip(names, id_codes):
#             team_number = id_code[-2]  # Second to last value is the team number
#             print(f"Name: {name}, ID Code: {id_code}, Team Number: {team_number}")
#             if team_number == 1:
#                 team1_names.append(name)
#                 team1_ids.append(id_code)
#                 team1_uids.append(id_code[3])
#             elif team_number == 2:
#                 team2_names.append(name)
#                 team2_ids.append(id_code)
#                 team2_uids.append(id_code[3])
        
#         while len(team1_uids) < 5:
#             team1_uids.append(-1)
#         while len(team2_uids) < 5:
#             team2_uids.append(-1)
#         uid_list = team1_uids
#         uid_list.extend(team2_uids)


#         return team1_names, team1_ids, team2_names, team2_ids, uid_list
#     def write(message):
#         client.send(message.encode('ascii'))

#     solution_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#     def update_solution(status, item_number):
#         index = user_ids.index(item_number)
#         solution_array[index] = status

#     # Function to receive messages from the server
#     def receive():
#         global player_list, team_update, user_ids, ready_list1, ready_list2, user_id
#         global nickname_array, integer_array, team1_ids, team2_ids, team1_names, team2_names

#         while True:
#             sys.stdout.flush()
#             try:
#                 message = client.recv(1024).decode('ascii')
#                 if message == 'NICK':
#                     client.send(full_player_id.encode('ascii'))
#                 elif message.startswith("Player Update:"):
#                     player_list = parse_player_update(message)
#                     print(f"PL:{player_list}")
#                     nickname_array = []
#                     integer_array = []
#                     for player_info in player_list:
#                         try:
#                             nickname, integers = parse_message(player_info)
#                             nickname_array.append(nickname)
#                             integer_array.append(integers)
#                             print(f"NA: {nickname_array}")
#                             print(f"IA: {integer_array}")
#                         except ValueError as e:
#                             print(f"Error parsing player info: {e}")
#                     team1_names, team1_ids, team2_names, team2_ids, user_ids = separate_teams(nickname_array, integer_array)
#                     #print("Received T1ID:", team1_ids)
#                     #print("Received T2ID:", team2_ids)
#                     print("Received ÜIDS:", user_ids)
#                     team_update = 1
#                 elif message.startswith("Ready Update:"):
#                     updates = message.split(":")[1].split(",")
#                     print(updates)
#                     for update in updates:
#                         status, item_number = int(update[0]), int(update[1])
#                         print(status)
#                         print(item_number)
#                         update_solution(status, item_number)
#                     print(solution_array)
#                     ready_list1 = solution_array[:5]
#                     ready_list2 = solution_array[5:]
#                     print("Received RL1:", ready_list1)
#                     print("Received RL2:", ready_list2)
#                     team_update = 1
#                 elif message.startswith("UID:"):
#                     update_string = message.replace("UID:", "")
#                     user_id = int(update_string)
#                     print(f"UID: {user_id}")
#                     team_update = 1
#                 else:
#                     print("Received message:", message)  # Handle other types of messages if needed
#             except Exception as e:
#                 print("An error occurred:", e)
#                 client.close()
#                 break



#     # Function to render player list on the screen
#     def render_player_list(nickname_array, integer_array):
        
#         # Render and display nickname array
#         for i, player_info in enumerate(nickname_array):
#             text = font.render(player_info, True, WHITE)
#             screen.blit(text, (1300, 10 + i * 30))  # Display each player info vertically with spacing of 30 pixels
        
#         # Render and display integer array
#         for i, player_info in enumerate(integer_array):
#             text = font.render(str(player_info), True, WHITE)
#             screen.blit(text, (1500, 10 + i * 30))  # Display each player info vertically with spacing of 30 pixels
        
#         text = font.render(str(nickname), True, WHITE)
#         screen.blit(text, (1500, 10 + i * 30))  # Display each player info vertically with spacing of 30 pixels

#     def render_team(id_codes, list_positions):
#         for i in range(4):
#             if list_positions[i] is None:
#                 continue  # Skip rendering if position is None
#             x, y = list_positions[i]
#             for array in id_codes:
#                 if i == 0:
#                     value = array[i]
#                     text = font.render(drone_list(value), True, WHITE)
#                 elif i == 1:
#                     value1 = array[i-1]
#                     value2 = array[i]
#                     text = font.render(weapon_list(value1, value2), True, WHITE)
#                 elif i == 3:
#                     value = array[i]
#                     text = font.render(str(value), True, WHITE)
#                 else:
#                     continue  # Skip rendering for the third list
#                 text_rect = text.get_rect(center=(x, y))
#                 screen.blit(text, text_rect)
#                 y += 78  # Move to the next line for the next value

#     def render_text(screen, text_array, start_x, start_y, y_spacing, display_flags=None, center=False):
#         #font = pygame.font.SysFont(None, 36)  # You can adjust the font and size here
#         if display_flags is None:
#             display_flags = [1] * len(text_array)  # If no display flags are provided, display all
#         for i, (text, display_flag) in enumerate(zip(text_array, display_flags)):
#             if display_flag == 1:
#                 rendered_text = font.render(text, True, (255, 255, 255))  # White color
#                 text_rect = rendered_text.get_rect()
#                 if center:
#                     text_rect.center = (start_x, start_y + i * y_spacing)
#                 else:
#                     text_rect.topleft = (start_x, start_y + i * y_spacing)
#                 screen.blit(rendered_text, text_rect)
#             elif display_flag == 2:
#                 rendered_text = font.render("HOST", True, (255, 255, 255))  # White color
#                 text_rect = rendered_text.get_rect()
#                 if center:
#                     text_rect.center = (start_x, start_y + i * y_spacing)
#                 else:
#                     text_rect.topleft = (start_x, start_y + i * y_spacing)
#                 screen.blit(rendered_text, text_rect)

#     def update_ready_status(UID, Ready, uid_input, ready):
#         """
#         Update the Ready array based on the UID value and ready status.

#         Args:
#             UID (list): The UID array.
#             Ready (list): The Ready array.
#             uid_input (int): The value in the UID array to update.
#             ready (int): The value to set in the Ready array (0 or 1).

#         Returns:
#             list: The updated Ready array.
#         """
#         if uid_input in UID:
#             index = UID.index(uid_input)
#             Ready[index] = "R" if ready == 1 else "NR"
#         return Ready

#     # Example usage:
#     # uid_set = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
#     # Ready = ["R", "NR", "NR", "NR", "NR", "R", "R", "NR", "NR", "NR"]
#     # uid_input = 1
#     # ready = 1
#     # Ready = update_ready_status(uid_set, Ready, uid_input, ready)
#     #print(Ready)  # Output: ['R', 'NR', 'NR', 'NR', 'NR', 'R', 'NR', 'NR', 'NR', 'NR']

#     # Connect to the server
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect((HOST, PORT))

#     client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


#     # Start the receive thread
#     receive_thread = threading.Thread(target=receive)
#     receive_thread.start()
#     import numpy as np

#     def play_video(video_file, surface):
#         cap = cv2.VideoCapture(video_file)
#         clock = pygame.time.Clock()

#         running = True
#         while running:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV uses BGR, Pygame uses RGB
#             frame = np.rot90(frame)  # Rotate frame if necessary
#             frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
#             frame_rect = frame.get_rect()
#             frame_rect.center = (WIDTH //2, HEIGHT // 2)
            
#             surface.blit(frame, frame_rect)
#             pygame.display.flip()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False

#             clock.tick(30)  # Adjust frame rate as necessary

#         cap.release()
#     screen = pygame.display.set_mode((1920, 1080))
#     video_file = "Abstract1.mp4"  # Replace with your video file path
#     play_video(video_file, screen)

#     # Main loop
#     running = True
#     hosting = 0
#     ready = 0
#     display_menu(title_screen_image)
#     screen.blit(pygame.image.load(stamp_images[int(drone_type)]),stamp_rect)
#     screen.blit(player_name, (265, 227))
#     screen.blit(team_name, (150, 685))
#     write("UID_Request")
#     while running:
#         sys.stdout.flush()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#                 break
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 for i, button_rect in enumerate(button_rects):
#                     if button_rect.collidepoint(event.pos):
#                         if i == 1:
#                             pygame.quit()
#                         elif i == 0:
#                             if hosting == 1 and ready:
#                                 print("AAAAAAAAAAAAAAa")
#                                 # Return the index of the selected button
#                             else:
#                                 write("READY")
#                                 print("READY")
#                                 ready = 1
#                         elif i ==2:
#                             if user_ids.index(user_id) < 5:
#                                 write(f"CHANGETEAM {2}")
#                             else: write(f"CHANGETEAM {1}")
                            

#         # Render player list
#         #render_player_list(nickname_array, integer_array)
#         team_update = 1
#         if team_update:
#             display_menu(title_screen_image)
#             screen.blit(pygame.image.load(stamp_images[int(drone_type)]),stamp_rect)
#             screen.blit(player_name, (265, 227))
#             screen.blit(team_name, (150, 685))
#             team1_count = AG_Large.render(f"{len(team1_names)}", True, TEAL)
#             team2_count = AG_Large.render(f"{len(team2_names)}", True, RED)

#             render_team(team1_ids, list_positions1)
#             render_team(team2_ids, list_positions2)
#             render_text(screen, team1_names, 1210, 163, 78, center=True)
#             render_text(screen, team2_names, 1210, 644, 78, center=True)
#             render_text(screen, ready_list, 950, 150, 80, ready_list1)
#             render_text(screen, ready_list, 950, 629, 80, ready_list2)
#             screen.blit(team1_count, (215, 800))
#             screen.blit(team2_count, (578, 800))
#             team_update = 0

#         #Draw buttons
#         for i, button_rect in enumerate(button_rects):
#             if button_rect.collidepoint(pygame.mouse.get_pos()):
#                 screen.blit(multi_server_selected_buttons[i], button_rect)
#             else:
#                 screen.blit(multi_server_buttons[i], button_rect)
#         pygame.display.flip()

#     pygame.quit()

# Main game loop
# def menu_loop():
#     mode = 0
#     global drone_button_images, drone_button_sel_images
#     stat_screen_images = [
#         "Plane_Screens/KiRa.png",
#         "Plane_Screens/AlpAur.png",
#         "Plane_Screens/ShiVind.png",
#         "Plane_Screens/CrCh.png",
#         "Plane_Screens/FalVi.png",
#         "Plane_Screens/AvMo.png",
#         "Plane_Screens/AsNof.png",
#         "Plane_Screens/AsWyv.png",
#         # Add paths to stat screen images for each character selection
#     ]
#     main_menu()
#     selected_mode = game_mode_selection()
#     if selected_mode == 0:
#         while True:
#             selected_character = dynamic_menu(8, drone_button_images, drone_button_sel_images, stat_screen_images, 0, drone_back_iamge)
#             if selected_character is not None:
#                 # Add code to handle character selection (e.g., display character image)
#                 print("Selected character:", selected_character)
#                 # You can add code here to display the selected character image on the right side of the screen

#                 # After character selection, move on to the next step
#                 print("Moving on to the next step...")
#                 break
        
#         user_selections = weapon_select(selected_character)
#         drone_button_images = load_selected_images(user_selections, weapon_button_image_paths)
#         drone_button_sel_images = load_selected_images(user_selections, weapon_button_image_selected_paths)
#         drone_backgrounds = set_selected_images(user_selections, weapon_stat_image_paths)
#         weapon_choice = dynamic_menu(len(drone_button_images), drone_button_images, drone_button_sel_images, drone_backgrounds, 1, weapon_back_image)
#         mode = experience()

#         if mode == 2:
#             trup = duel_server(selected_character, weapon_choice)
#             return trup
#         elif mode == 4:
#             supremacy_server(selected_character, weapon_choice)

#     elif selected_mode == 1:
#         # Add code to start Game Mode 2
#         pass
#     elif selected_mode == 2:
#         # Add code to open Settings Menu
#         pass

#menu_loop()

def login_menu():
    display_menu(login_image)  # Replace None with your login image
    # Text variables
    input_text = ''
    input_rect = pygame.Rect(700, 655, 520, 50)
    active = False
    login = True
    # Main loop
    while login:
        display_menu(login_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        login = False
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        # Render the text input box
        pygame.draw.rect(screen, BLACK, input_rect, 2)
        text_surface = custom_font_standard.render(input_text, True, BLACK)
        # Adjust y-coordinate to center vertically
        text_rect = text_surface.get_rect(center=input_rect.center)

        # Calculate positions to place the text at the top of the screen and center vertically within the progress bars
        text_y = 655 + (50 - text_surface.get_height()) // 2  # Center vertically within the progress bars
        text1x = 700
        screen.blit(text_surface, (text1x + 5, text_y))


        pygame.display.flip()
    
    return input_text

#login_menu()