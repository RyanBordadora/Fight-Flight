import tkinter as tk
from tkinter import ttk
import configparser

# Define your ColorVision and MachineVision classes here

class VisionSelectionMenu:
    def __init__(self, root, config_file, frame):
        self.root = root
        self.config_file = config_file
        self.frame = frame  # Pass the frame as an argument

        # Read initial configuration
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self.initial_vision = self.config['Game']['vision_type']

        # Create the vision selection GUI components
        self.create_vision_selection_widgets()

    def create_vision_selection_widgets(self):
        # Create a combo box for selecting vision type
        self.vision_label = ttk.Label(self.frame, text="Select Vision Type:")
        self.vision_label.grid(row=0, column=0, padx=10, pady=10)
        
        vision_options = ['ColorVision', 'MachineVision']
        self.selected_vision = tk.StringVar(value=self.initial_vision)
        self.vision_combobox = ttk.Combobox(self.frame, textvariable=self.selected_vision, values=vision_options)
        self.vision_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.vision_combobox.bind("<<ComboboxSelected>>", self.handle_selection)

        # Create placeholders for the second combo boxes
        self.color_combobox = None
        self.drone_combobox = None
        
        # Display the appropriate combo box based on initial vision type
        if self.initial_vision == "MachineVision":
            self.pack_machine_vision_combobox()
        elif self.initial_vision == "ColorVision":
            self.pack_color_combobox()

    def handle_selection(self, event):
        selected_vision = self.selected_vision.get()
        self.config['Game']['vision_type'] = selected_vision
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        print("Selected vision:", selected_vision)

        # Remove any existing second combo boxes
        self.remove_second_comboboxes()

        # If MachineVision is selected, pack a combo box with drone options
        if selected_vision == "MachineVision":
            self.pack_machine_vision_combobox()
        # If ColorVision is selected, pack a combo box with color options
        elif selected_vision == "ColorVision":
            self.pack_color_combobox()

    def pack_machine_vision_combobox(self):
        # Create and pack the combo box for selecting drones
        drone_options = ['Drone1', 'Drone2']
        initial_drone_option = self.config['MachineVision'].get('drone_option', 'Drone1')
        self.selected_drone = tk.StringVar(value=initial_drone_option)
        self.drone_combobox = ttk.Combobox(self.frame, textvariable=self.selected_drone, values=drone_options)
        self.drone_combobox.grid(row=1, column=1, padx=10, pady=10)

        # Update config when selection changes
        self.drone_combobox.bind("<<ComboboxSelected>>", self.update_machine_vision_option)

    def pack_color_combobox(self):
        # Create and pack the combo box for selecting colors
        color_options = ['Pink', 'Yellow', 'Blue', 'Green']  # Add more colors as needed
        initial_color_option = self.config['Game'].get('color_option', 'Pink')
        self.selected_color = tk.StringVar(value=initial_color_option)
        self.color_combobox = ttk.Combobox(self.frame, textvariable=self.selected_color, values=color_options)
        self.color_combobox.grid(row=1, column=1, padx=10, pady=10)

        # Update config when selection changes
        self.color_combobox.bind("<<ComboboxSelected>>", self.update_color_vision_option)

    def update_machine_vision_option(self, event):
        selected_drone = self.selected_drone.get()
        self.config['MachineVision']['drone_option'] = selected_drone
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        print("Selected drone:", selected_drone)

    def update_color_vision_option(self, event):
        selected_color = self.selected_color.get()
        self.config['Game']['color_option'] = selected_color
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        print("Selected color:", selected_color)

    def remove_second_comboboxes(self):
        # Remove the second combo boxes if they exist
        if self.drone_combobox:
            self.drone_combobox.grid_forget()
            self.drone_combobox = None
        if self.color_combobox:
            self.color_combobox.grid_forget()
            self.color_combobox = None

# Create main application window
root = tk.Tk()
root.title("Vision Configurator")

# Create a frame to contain the widgets
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Initialize the vision selection menu
vision_menu = VisionSelectionMenu(root, 'config.ini', frame)

# Run the Tkinter event loop
root.mainloop()
