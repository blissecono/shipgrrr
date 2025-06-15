"""
Ahoy, matey! Thank you for playing ShipGrrr online, a final project submission for Stanford University's Code in Place 2025 program.

This challenging student-selected project, written in Python with the Pygame library, was part of the course requirements for the Experienced Student track, which led to a certificate of completion.

Navigate Captain Kai's ship across a dangerous ocean filled with both hidden and looming hazards! Steer the ship using the Up, Right, and Left arrow keys.

Your mission: Reach the ocean refueling station before the ship runs out of fuel.

As the navigator on Captain Kai’s ship, you must watch out for and avoid:

Ship Hazards & Sea Creatures you will encounter, such as -
* Icebergs: Stationary ship-sinking obstacles appearing randomly near the top refueling zone at the start of each new game round.
* Orcas: These large sea creatures, also known as "killer whales," swim across the ship’s navigation lanes.
* Cachalots: 50-foot toothed whales that swim from side to side and appear in open lanes.
* Kraken Tentacles: These monster-like arms unexpectedly rise up from the ocean depths and can drag a ship down below the water.

Ship navigators beware! Collisions with these hazards and sea creatures can damage or sink your ship. Steer your ship's course WISELY to avoid a shipwreck.

Challenge:

Ready to dive deeper? Install Python and the Pygame and restructure this code to create your own exciting ocean scenario.
Post your version of ShipGrrr to social media and let me know how you liked the game or if you found any bugs!

Thanks again, have fun, and happy sailing!

"""

import pygame
import random # Introduce sea creatures to the canvas in a random order; also used for the random game elements (The Kraken tentacle pops up from the screen and struck icebergs teleport to another position)
import math # Math called for game element alignment and aesthetics; also used to calculate the circular features of The Kraken's tentacles and their swinging motions

# --- 1. INITIALIZE THE GAME ---
pygame.init()
pygame.display.set_caption("ShipGrrr! A High Seas Adventure") # Game title in the browser

# --- CANVAS SETTINGS ---
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# --- COLOR SETTINGS ---
black = (0, 0, 0) # Cachalot eyes and other black game elements
blue = (20, 119, 190) # Blue canvas for the main ocean
white = (255, 255, 255) # Ship's color, same for Orca visual pattern
yellow = (255, 255, 0) # Warning text color when ship is hit
orange = (255, 165, 0) # The sun's outline
purple = (128, 0, 128) # For the ship's rudder

# --- FONT SETTINGS ---
pygame.font.init()
font = pygame.font.SysFont("arial", 33)

# --- TIMER SETTINGS ---
clock = pygame.time.Clock()
fps = 55 # Aim for 60 frames per second for smoother movement

# Constants and Variables for Round Completion Delay
ROUND_COMPLETE_DELAY_FRAMES = fps * 1 # This is usually 2 seconds of delay (e.g., 60 FPS * 2 = 120 frames)
ROUND_COMPLETE_TIMER = 0 # Initialize the timer to 0

# -- ICEBERG ZONE SETTINGS ---
ICEBERG_TOP_PADDING = 100 # Adjust to control space for icebergs
MIN_ICEBERG_WIDTH = 60
MAX_ICEBERG_WIDTH = 120
MIN_ICEBERG_HEIGHT = 50
MAX_ICEBERG_HEIGHT = 80

# The MAX_ICEBERG_HEIGHT must be no more than ICEBERG_TOP_PADDING to fit in the refuel zone
MAX_ICEBERG_HEIGHT_FITS_ZONE = ICEBERG_TOP_PADDING # Maximum height (80 pixels)

ICEBERG_COLOR = (192, 192, 192) # Silver
MAX_ICEBERG_GENERATE_ATTEMPTS = 100

OCEAN_PLAY_ZONE_BOTTOM_BUFFER = 600 # Amount of space to leave clear at the bottom of the screen

# --- SHIP PROPERTIES ---
ship_width = 50
ship_height = 50
ship_x = screen_width // 2 - ship_width // 2
ship_y = screen_height - ship_height - 0 # Start near the bottom
ship_speed = 1 # Pixels per move

ship_hull_color = (184, 134, 11) # Golden Brown (Dark Goldenrod)
ship_cabin_color = (100, 100, 100) # A darker gray for the cabin/bridge

# Flag to control if the ship is docked in a refuel station
ship_docked = False

# --- SCREEN FLASH PROPERTIES WHEN THE SHIP GETS HIT --- COMMENT OUT TO DISABLE FLASH

hit_flash_color = (139, 0, 0) # A dark, menacing red that flashes when the ship is hit
hit_flash_duration = 30 # How many frames the background stays flashed

# --- ANIMAL / SEA CREATURE PROPERTIES --- COMMENT OUT TO DISABLE SCREEN FLASH

# Orca Properties
orca_width = 90 
orca_height = 50
orca_color = (0, 0, 0)
orca_speed = 1
orcas = [] # List to hold all active, moving Orca objects

# Cachalot Whale Properties
cachalot_width = 120  # Wider than orcas
cachalot_height = 50 # Taller than orcas
cachalot_color = (170, 170, 170) # Gray
cachalot_speed = 1
cachalots = [] # List to hold all active, moving cachalot objects

# Kraken Tentacle Properties --- COMMENT OUT TO DISABLE FLASHING ON SCREEN

# Add circles and eye to The Kraken's base
kraken_base_radius = 30  # Radius of the main circular "head" of the tentacle
kraken_eye_radius = 20   # Radius of the eye circle
kraken_color = (255, 50, 200) # A menacing purple/dark red
kraken_lifetime = 40 # How many frames the tentacle stays visible (e.g., 2 seconds at 60 frames per second)

# Kraken Tentacle Chain Properties --- COMMENT OUT TO DISABLE FLASHING ON SCREEN

kraken_segment_radius = 10 # Radius of each ball in the chain / tentacle
kraken_segment_length = 20 # Distance between centers of each ball in the chain
num_kraken_segments = 5  # Number of balls in the chain (as requested)
kraken_swing_amplitude = math.radians(20) # Max angle of swing in radians (e.g., 20 degrees)
kraken_swing_speed = 0.05 # How fast the tentacle swings (adjust for desired speed)

# Refuel Station Slot and Pump Properties

refuel_zone_start_y = 0
refuel_zone_height = 80
fuel_slot_width = 100 # Width of each functional fuel slot (wide enough for ship)
fuel_slot_height = refuel_zone_height - 20 # Height of slots
fuel_slot_spacing_x = 60 # Horizontal EMPTY space BETWEEN the slots
fuel_pump_width = 25 # Width of the fuel pump visual
fuel_pump_height = 45 # Height of the fuel pump visual
fuel_pump_color = (80, 80, 80) # Dark gray for the inactive pump
slot_empty_color = (70, 70, 70) # A darker grey for empty/inactive slots

# --- TOP REFUEL SAFETY ZONE --- 

# Refuel Safety Zone properties (the 'port' or 'safe harbor' for the ship to refuel at the top)
refuel_zone_height = 50 # Height of the top refuel station / safety zone
refuel_zone_color = (240, 230, 120) # A golden color for the top refuel station

# --- BOTTOM STARTER SAFETY ZONE --- 

# Starter Safety Zone properties
starter_zone_height = 80 # Height of the ship's safety zone at the bottom
starter_zone_start_y = screen_height - starter_zone_height # Y-coordinate where the bottom zone begins
starter_zone_color = (173, 216, 230)   # Light blue for the bottom starter safety zone

# --- GAME MESSAGE FONTS ---

# Motivational Messages in the Bottom Starter Safety Zone
FONT_SIZE = 30
GAME_MOTIVATIONAL_FONT = pygame.font.Font(None, FONT_SIZE) # Using default font

# Welcome Message in the Middle of the Ocean / Canvas 
WELCOME_FONT = pygame.font.Font(None, 50)
welcome_text_timer = 0
WELCOME_TEXT_DURATION = 20 * 20 # 20 seconds * 60 frames per second = 1200 frames

# Rotating Messages for the Bottom Starter Safety Zone
# Message sets are items in the list as a tuple: ((left_line1, left_line2), (right_line1, right_line2))
MOTIVATIONAL_MESSAGES = [
    # Set 1: Core Gaming Instructions - Always Essential
    (("Move by using the up,", "right, and left arrow keys."),
     ("Navigate Captain Kai's ship", "up to the green refuel zone.")),

    # Set 2: Highlighting Fuel Importance and the Captain's Resourcefulness
    (("Fuel is lifeblood of this ship.", "The captain knows this well."),
     ("Captain's orders to the crew:", "This ship MUST refuel in time!")),

    # Set 3: Astute Observation and Danger Awareness
    (("The ocean is vast...", "and filled with hidden dangers."),
     ("Direct the captain's ship", "up to the green fuel slot.")),

    # Set 4: Determination and Challenge (with a touch of grit)
    (("Running on almost empty!", "Steer a path to the refuel zone."),
     ("Neither beast nor iceberg", "shall deter this ship's route.")),

    # Set 5: Resource Management and Strategic Thought
    (("Chart a course wisely.", "Waste not one drop of fuel."),
     ("Refuel and deliver goods.", "That's the captain's rule.")),

    # Set 6: Iceberg Specific Dangers - Caution and Fuel Link
    (("Icebergs loom ahead,", "a cold and perilous challenge."),
     ("Avoid a collision.", "The sea creatures lurk.")),

    # Set 7: Kraken Tentacle Specific - Savvy and Stay Focused
    (("Kraken tentacles hunger!", "That beast loves vessels!"),
     ("Diligent navigation and", "focus can protect our ship.")),

    # Set 8: General Ocean Dangers - Skilled and Survival
    (("The sea breeds perils", "to test a navigator's wits."),
     ("Fuel is running low.", "Avoid all obstacles!")),

    # Set 9: Determination to Resolve Against All Threats
    (("No beast nor iceberg shall", "claim victory over this ship!"),
     ("Success is refueling and a", "perceptive hand at the wheel!")),

    # Set 10: Direct Warning of The Kraken and Maneuverability
    (("That dark shadow up ahead -", "could be The Kraken's tentacle!"),
     ("Beware the frozen giants -", "plot a plan around them.")),

    # Set 11: Refueling and the High Sea's Trickery
    (("The ocean can play rough,", "but savvy navigation prevails."),
     ("Let none of the sea's hazards", "prevent us from refueling.")),
]

# Timer for cycling messages
MOTIVATIONAL_MESSAGE_TIMER = 0
MOTIVATIONAL_MESSAGE_CYCLE_DURATION = 5 * 80 # 5 seconds * 60 frames per second = 300 frames

# Index to track which message set is currently displayed
CURRENT_MOTIVATIONAL_MESSAGE_INDEX = 0

# --- OCEAN SWIM LANES / ROW PROPERTIES 

# Lane Settings for Consistent Sea Creature Movement
swim_lane_padding = 10 # Pixels of empty space between swim lanes
max_creature_display_height = max(orca_height, cachalot_height) # Height for all creatures to fit in a lane

# Distance from screen edge considered "too close" for a new creature to generate if occupied
generate_buffer_distance = 180 # Larger number = fewer animal generations near canvas edges

available_y_lanes = [] # This list holds ALL sea creatures regardless of motion direction

# Calculate height of a single lane block (creature + padding)
lane_block_height = max_creature_display_height + swim_lane_padding

# Define the target Y for the TOP edge of the creature in the lowest lane so that the bottom edge of a creature aligns exactly with the starter_zone_start_y
target_y_for_lowest_creature_top = starter_zone_start_y - max_creature_display_height

# Calculate the Top Boundary for Swim Lanes and Allow Space for Icebergs
lanes_top_boundary = refuel_zone_height + 100 # Swim lanes will not be generated above this point

temp_y_coords = [] # Temporary list to build y-coordinates from bottom-up

current_y_pos_bottom_up = target_y_for_lowest_creature_top # Start from the bottom-most possible lane and move upwards

# Loop upwards, adding lane Y-coordinates as long as they don't go above the lanes_top_boundary
while current_y_pos_bottom_up >= lanes_top_boundary:
    # Lane does not start within the refuel station's defined height
    if current_y_pos_bottom_up >= refuel_zone_height + swim_lane_padding:
        temp_y_coords.append(current_y_pos_bottom_up)
    current_y_pos_bottom_up -= lane_block_height

# Populate available_y_lanes to assign alternating swimming directions
available_y_lanes = []
for i, y_coord in enumerate(temp_y_coords[::-1]): # Iterate over reversed y-coordinates
    direction = 1 if i % 2 == 0 else -1 # Alternate swim direction: 1st lane right, 2nd left, etc.
    available_y_lanes.append((y_coord, direction))

# If no lanes were generated (i.e., screen too small), add a default lane
if not available_y_lanes:
    available_y_lanes.append((screen_height // 2, random.choice([1, -1])))

# --- 2. GAME STATE VARIABLES ---

# Track score and ship's strength, inform player when the game is over
game_over = False # Existing game_over variable
game_won = False # When the game is won
ship_strength = 3 # Existing ship strength variable
score = 0 # Existing score variable

current_round = 1   # CURRENT ROUND MUST BE PRESENT
total_rounds = 3    # ROUNDS NEED TO BE DEFINED HERE

slots_completed = [False] * total_rounds # Initialize refuel slots_completed to track completed rounds

last_iceberg_round_generated = 0 # Tracks the round for which icebergs were last generated

font = pygame.font.Font(None, 36) # Font for displaying text for ship strength and game score

# --- Blueprint Functions for Designing the Game Elements ---

# Kraken Tentacle Class
class Kraken_Tentacle:
    def __init__(self, x, y, base_radius, eye_radius, segment_radius, segment_length, num_segments, lifetime, swing_amplitude, swing_speed):
        # Base (Kraken's head) properties
        self.center_x = x
        self.center_y = y
        self.base_radius = base_radius
        self.eye_radius = eye_radius
        self.lifetime = lifetime
        self.rect = pygame.Rect(x - base_radius, y - base_radius, base_radius * 2, base_radius * 2) # Boundary box for collisions

        # Segment (chain of ball) properties
        self.segment_radius = segment_radius
        self.segment_length = segment_length
        self.num_segments = num_segments
        self.segments = [] # List to hold the (x, y) centers of each ball
        
        # Swinging animation properties
        self.swing_amplitude = swing_amplitude
        self.swing_speed = swing_speed
        self.current_frame = 0 # Drives the swing animation

        self._initialize_segments() # Set up initial position of the chain

    def _initialize_segments(self):
        
        # Base point for the chain is the top of The Kraken's 'head' circle
        prev_x = self.center_x
        prev_y = self.center_y - self.base_radius 

        for i in range(self.num_segments):
            # Each ball starts directly above the previous one
            segment_x = prev_x
            segment_y = prev_y - self.segment_length # Position above the previous ball

            self.segments.append({'x': segment_x, 'y': segment_y}) # Store ball data

            # Update prev_x, prev_y for the next ball in the chain
            prev_x, prev_y = segment_x, segment_y

    def update(self):
        self.lifetime -= 1
        self.current_frame += 1

        # Calculate the overall swing angle using a sine wave for oscillation for a smooth back-and-forth motion
        overall_swing_angle = math.sin(self.current_frame * self.swing_speed) * self.swing_amplitude

        # Update segment positions based on the swing angle
        # The first segment is connected to the top of the base circle
        # Subsequent segments connect to the previous one, inheriting and slightly offseting the swing
        
        # Starting point for the chain (top of the base circle)
        prev_x = self.center_x
        prev_y = self.center_y - self.base_radius 
        
        for i in range(self.num_segments):
            # Each ball's angle is slightly offset from the overall swing for a natural "lag" or "wave" effect in the chain
            segment_angle = overall_swing_angle + (i * math.radians(5)) # Add a small, cumulative offset for each ball

            # Calculate new x, y for the segment using trigonometry
            # x = prev_x + length * sin(angle) (for horizontal displacement)
            # y = prev_y - length * cos(angle) (for vertical displacement, negative because y-axis increases downwards in Pygame)
            segment_x = prev_x + self.segment_length * math.sin(segment_angle)
            segment_y = prev_y - self.segment_length * math.cos(segment_angle)

            self.segments[i]['x'] = segment_x
            self.segments[i]['y'] = segment_y

            # Update prev_x, prev_y for the next iteration (connecting to the current ball's end)
            prev_x, prev_y = segment_x, segment_y

    def draw(self, screen): # Called from the main drawing loop
        # Draw the base circle (head)
        pygame.draw.circle(screen, kraken_color, (int(self.center_x), int(self.center_y)), self.base_radius)

        # Draw the eye circle (black)
        pygame.draw.circle(screen, black, (int(self.center_x), int(self.center_y)), self.eye_radius)

        # Draw the segments (chain of balls)
        for segment in self.segments:
            pygame.draw.circle(screen, kraken_color, (int(segment['x']), int(segment['y'])), self.segment_radius)

        # Draw lines connecting the balls for a stronger chain effect to help visualize the connections
        prev_x, prev_y = self.center_x, self.center_y - self.base_radius # Start a line from top of base circle
        for segment in self.segments:
            pygame.draw.line(screen, black, (int(prev_x), int(prev_y)), (int(segment['x']), int(segment['y'])), 2) # Line width 2
            prev_x, prev_y = segment['x'], segment['y']

# --- Iceberg Class ---
class Iceberg:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (240, 248, 255) # Alice Blue for a nice, crisp iceberg

        # Generate random peak/valley offsets ONCE during initialization ---
        self.peak_offsets = [] # These values define the shape of each iceberg and won't change
        num_points_on_top = 6 # This creates roughly 3 peaks and 2 valleys (total 7 polygon points)
        
        # Determine the general height of the peaks and valleys
        base_peak_height = height * 0.2
        base_valley_depth = height * 0.05

        # Generate a series of points for the top edge
        for i in range(num_points_on_top): # Alternating peak and valley points along the top of the iceberg's width
            x_pos_ratio = (i + 1) / (num_points_on_top + 1) # Distribute points horizontally
            x_offset = int(width * x_pos_ratio)

            if i % 2 == 0: # Even index to make it a peak
                y_offset = random.randint(int(base_peak_height * 0.8), int(base_peak_height * 1.2))
                self.peak_offsets.append((x_offset, -y_offset)) # Negative for 'up' from self.rect.top
            else: # Odd index to make it a valley
                y_offset = random.randint(int(base_valley_depth * 0.8), int(base_valley_depth * 1.2))
                self.peak_offsets.append((x_offset, y_offset)) # Positive for 'down' from self.rect.top

    def draw(self, screen):
        # Define the vertices for the jagged iceberg shape
        polygon_points = [
            (self.rect.left, self.rect.bottom) # Bottom-left corner
        ]

        # Add the dynamically generated peak/valley points
        for x_offset, y_offset in self.peak_offsets:
            polygon_points.append((self.rect.left + x_offset, self.rect.top + y_offset))

        polygon_points.append((self.rect.right, self.rect.bottom)) # Bottom-right corner of the iceberg

        pygame.draw.polygon(screen, self.color, polygon_points)

# --- Blueprints for the Sea Creature Animals ---
        
# Orca and Cachalot Classes
class Orca:
    def __init__(self, x, y, width, height, speed_x):
        self.rect = pygame.Rect(x, y, width, height) # The actual Pygame rectangle
        self.speed_x = speed_x # Custom speed/direction attribute

class Cachalot:
    def __init__(self, x, y, width, height, speed_x):
        self.rect = pygame.Rect(x, y, width, height) # The actual Pygame rectangle
        self.speed_x = speed_x # Custom speed/direction attribute

# --- Function to Set Up Fuel Station Slots ---
def setup_fuel_slots():
    global fuel_slots # Modifies the global list
    fuel_slots = [] # Clear the list if function is called multiple times (e.g., for game restart)

    # Calculate the total width taken by all slots and their internal spacing
    total_slots_group_width = (fuel_slot_width * total_rounds) + (fuel_slot_spacing_x * (total_rounds - 1))
    
    # Calculate the starting X-coordinate for the first slot to center the entire group
    start_x_group = (screen_width // 2) - (total_slots_group_width // 2)

    slot_y = refuel_zone_start_y + 10 # Y-coordinate for the top of the slots

    for i in range(total_rounds):
        current_slot_x = start_x_group + (i * (fuel_slot_width + fuel_slot_spacing_x))
        slot_rect = pygame.Rect(current_slot_x, slot_y, fuel_slot_width, fuel_slot_height)
        
        fuel_slots.append({'rect': slot_rect, 'round': i + 1})

# --- Helper Function to Find a Safe Swim Lane for Introducing a Sea Creature ---
def find_safe_lane_and_direction(potential_object_width, potential_object_height, object_base_speed, current_orcas, current_cachalots, available_y_lanes_with_directions):
    
    shuffled_lanes = list(available_y_lanes_with_directions) # Make a mutable copy
    # Shuffle Property is used because it randomizes the order in which the game attempts to generate new sea creatures
    # This is needed for a more varied and unpredictable generating approach for the orcas and cachalots
    random.shuffle(shuffled_lanes) # Randomize which lane to try first

    for lane_info in shuffled_lanes:
        lane_y = lane_info[0]
        lane_direction = lane_info[1] # The fixed direction for this lane
        
        # Calculate the direction speed the newly generated object has in this lane
        tentative_direction_speed = lane_direction * object_base_speed

        is_lane_safe = True
        
        # Check against ALL existing sea creatures on the screen
        all_existing_obstacles = current_orcas + current_cachalots
        
        for existing_obj in all_existing_obstacles:
            # Only checks the objects that are in the SAME swim lane
            if existing_obj.rect.y == lane_y:
                # We only need to check if they are moving in the SAME direction,
                # IMPORTANT: Animals swimming in opposite directions and colliding are now prevented by these lane rules
                if existing_obj.speed_x == tentative_direction_speed:
                    
                    # If sea creatures are moving right (generated from left edge of screen)
                    if tentative_direction_speed > 0:
                        # Check if the existing object is too close to the left edge
                        # (i.e., within the 'generate_buffer_distance' from the left of the screen)
                        if existing_obj.rect.x < generate_buffer_distance:
                            is_lane_safe = False # Swim lane is NOT safe for a new sea creature
                            break # No need to check other objects in this lane
                    # If sea creatures are moving left (generate from right edge of screen)
                    else: # tentative_direction_speed < 0
                        # Check if the existing object is too close to the right generate edge
                        # (i.e., within the 'generate_buffer_distance' from the right of the screen)
                        if existing_obj.rect.x + existing_obj.rect.width > screen_width - generate_buffer_distance:
                            is_lane_safe = False # Lane is NOT safe
                            break # No need to check other objects in this lane
        
        if is_lane_safe:
            return (lane_y, lane_direction) # Found a safe swim lane, return its info to generate a sea creature
    
    return None # No safe lane found after checking all available lanes, no new sea creature

# --- 3. GAME OBJECTS (Initial Creation) ---
ship = pygame.Rect(ship_x, ship_y, ship_width, ship_height)

# Initialize our lists to hold instances of our new classes
orcas = [] 
cachalots = []
kraken_tentacles = []
fuel_slots = []
icebergs = [] 

# CALL THE FUNCTION HERE (even though the code is written above)
setup_fuel_slots() 

# --- Function to Randomly Generate Icebergs for a New Round ---

def generate_icebergs_for_round():
    global icebergs # Modify the global list

    icebergs.clear() # Clear any existing icebergs from the previous round

    # --- Determine the number of icebergs to generate ---
    # REMOVED FOR NOW: More icebergs for higher rounds, but ensure a minimum
    min_icebergs = 3 # At least 3 icebergs per rounds
    max_icebergs_per_round = 3 # Removed dynamically adding new icebergs, can add back
    num_icebergs_to_generate = random.randint(min_icebergs, max_icebergs_per_round)

    print(f"Randomly generating {num_icebergs_to_generate} icebergs for Round {current_round}...")

    # This loop places non-overlapping icebergs in the refuel safety zone
    for _ in range(num_icebergs_to_generate):
        placed = False
        attempts = 0
        while not placed and attempts < MAX_ICEBERG_GENERATE_ATTEMPTS:
            # Determine random dimensions within the defined range
            iceberg_width = random.randint(MIN_ICEBERG_WIDTH, MAX_ICEBERG_WIDTH)
            iceberg_height = random.randint(MIN_ICEBERG_HEIGHT, MAX_ICEBERG_HEIGHT_FITS_ZONE)

            # Define the absolute top boundary for an iceberg's top edge
            absolute_min_iceberg_top_y = refuel_zone_height + 10

            # Define the absolute bottom boundary for an iceberg's top edge with OCEAN_PLAY_ZONE_BOTTOM_BUFFER to define the "floor"
            absolute_max_iceberg_top_y = (screen_height - OCEAN_PLAY_ZONE_BOTTOM_BUFFER) - iceberg_height

            # Ensure that the maximum Y an iceberg can generate (absolute_max_iceberg_top_y) is never less than the minimum Y it must generate (absolute_min_iceberg_top_y)
            # If the calculated max is too low, we clamp it up to the min to prevent the ValueError for random.randint
            if absolute_max_iceberg_top_y < absolute_min_iceberg_top_y:
                absolute_max_iceberg_top_y = absolute_min_iceberg_top_y

            # Clamped values for random iceberg generation
            generate_y = random.randint(absolute_min_iceberg_top_y, absolute_max_iceberg_top_y)

            # Random X-axis position across the main game screen area
            generate_x = random.randint(0, screen_width - iceberg_width)

            # Create a temporary Rect for collision checking before placing
            temp_iceberg_rect = pygame.Rect(generate_x, generate_y, iceberg_width, iceberg_height)

            # --- CHECK FOR OVERLAP WITH EXISTING ICEBERGS ---
            overlap = False
            for existing_iceberg in icebergs:
                if temp_iceberg_rect.colliderect(existing_iceberg.rect):
                    overlap = True
                    break # Found an overlap, no need to check further

            if not overlap:
                # No overlap, so it's safe to place this iceberg here
                new_iceberg = Iceberg(generate_x, generate_y, iceberg_width, iceberg_height)
                icebergs.append(new_iceberg)
                placed = True # Successfully placed an iceberg
            
            attempts += 1 # Increment attempt counter

        if not placed: # Print debug warning
            print(f"Warning: Could not place an iceberg after {MAX_GENERATE_ATTEMPTS} attempts due to overcrowding.")

# --- Function to Randomly Generate an Orca ---

def generate_orca():
    # Attempt to find a safe lane using the helper function
    # Pass the relevant object properties and the current lists of active sea creatures
    chosen_lane_info = find_safe_lane_and_direction(
        orca_width, orca_height, orca_speed, # Properties of the object to generate
        orcas, cachalots, # Current lists of existing objects
        available_y_lanes # The list of all possible swim lanes
    )
    
    if chosen_lane_info is None:
        return # If no safe swim lane is found, don't generate an orca for now

    y = chosen_lane_info[0] # Get the y-coordinate from the safe lane info
    direction_speed = chosen_lane_info[1] * orca_speed # Get the direction from safe swim lane info

    if direction_speed > 0: # Moving right
        x = -orca_width # Start off-screen left
    else: # Moving left
        x = screen_width # Start off-screen right
    
    new_orca_obj = Orca(x, y, orca_width, orca_height, direction_speed)
    orcas.append(new_orca_obj)

# --- Function to Randomly Generate Cachalots ---

def generate_cachalot():
    # Attempt to find a safe swim lane using the helper function
    chosen_lane_info = find_safe_lane_and_direction(
        cachalot_width, cachalot_height, cachalot_speed, # Properties of the object to generate
        orcas, cachalots, # Current lists of existing objects
        available_y_lanes # The list of all possible swim lanes
    )
    
    if chosen_lane_info is None:
        return # If no safe swim lane is found, don't generate a cachalot for now

    y = chosen_lane_info[0] # Get the y-coordinate from the safe lane info
    direction_speed = chosen_lane_info[1] * cachalot_speed # Get the direction from safe lane info

    if direction_speed > 0:
        x = -cachalot_width
    else:
        x = screen_width
    
    new_cachalot_obj = Cachalot(x, y, cachalot_width, cachalot_height, direction_speed)
    cachalots.append(new_cachalot_obj)

# --- Function to Generate Kraken Tentacles ---

def generate_kraken_tentacle():
    max_generate_attempts = 10 # Limit how many times it will try to find a clear spot in the canvas / ocean to pop up
    
    for _ in range(max_generate_attempts):
        # 1. Propose a random x, y within the main ocean active play area
        # X, Y is the CENTER of The kraken's base circle
        x = random.randint(kraken_base_radius, screen_width - kraken_base_radius)
        y = random.randint(refuel_zone_height + kraken_base_radius, starter_zone_start_y - kraken_base_radius)

        # Create a temporary rectangle for the proposed tentacle position's boundary box
        # This rect is for collision detection and represents the base circle
        proposed_tentacle_rect = pygame.Rect(x - kraken_base_radius, y - kraken_base_radius, kraken_base_radius * 2, kraken_base_radius * 2)
        
        is_safe_ocean_spot = True # Assume it's safe until an overlap is found
        
        # 2. Check for overlap with existing Orcas
        # It won't randomly pop up if there's an orca in this space
        for orca in orcas:
            if proposed_tentacle_rect.colliderect(orca.rect):
                is_safe_ocean_spot = False # Overlaps with an animal, so this spot is not safe
                break # No need to check for other sea creatures; this spot is already unsafe
        if not is_safe_ocean_spot:
            continue # If not safe, skip to the next attempt in the loop

        # 3. Check for overlap with existing Cachalots
        # It won't randomly pop up if there's a cachalot in this space
        for cachalot in cachalots:
            if proposed_tentacle_rect.colliderect(cachalot.rect):
                is_safe_ocean_spot = False # Overlaps with a cachalot, so this spot is not safe
                break # No need to check for other sea creatures; this spot is already unsafe
        if not is_safe_ocean_spot:
            continue # If not safe, skip to the next attempt in the loop

        # 4. Check for overlap with the Ship
        # If the ship is there, it shouldn't pop up
        if proposed_tentacle_rect.colliderect(ship):
            is_safe_ocean_spot = False # Overlaps with the ship, so not safe
        if not is_safe_ocean_spot:
            continue # If not safe, skip to the next attempt in the loop
        
        # 5. If The Kraken made it this far with no other objects, the spot is safe to pop up
        if is_safe_ocean_spot:
            new_tentacle = Kraken_Tentacle(
                x, y,
                kraken_base_radius, kraken_eye_radius,
                kraken_segment_radius, kraken_segment_length, num_kraken_segments,
                kraken_lifetime,
                kraken_swing_amplitude, kraken_swing_speed
            )
            kraken_tentacles.append(new_tentacle)
            return # Tentacle generated successfully, exit the function

# --- 4. GAME LOOP ---
running = True # Controls whether the game is running
generate_orca_timer = 0
generate_orca_interval = 70 # How many frames until a new orca emerges
generate_cachalot_timer = 0
generate_cachalot_interval = 70 # How many frames until a new cachalot emerges
generate_kraken_timer = 0 # Timer for The Kraken's tentacles
generate_kraken_interval = 180 # How often Kraken tentacles try to emerge (e.g., every 3 seconds at 60 FPS)

# Ship Hit Flash and Message on Screen --- # COMMENT OUT TO DISABLE FLASH ---

ship_hit_flash = False # True when the ship has just been hit
hit_flash_timer = 0    # Countdown timer for the flash duration
hit_message_text = "" # The message text

while running:
    # --- A. EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: # Check if any key was pressed down
            if event.key == pygame.K_SPACE: # Check if THAT pressed key was the SPACE bar
                if game_over:
                    # Reset game state for a new game
                    game_over = False
                    game_won = False
                    score = 0
                    ship_strength = 3
                    # Reset slot completion and current round for a new game
                    slots_completed = [False] * total_rounds
                    current_round = 1
                    ship.x = screen_width // 2 - ship_width // 2
                    ship.y = screen_height - ship_height
                    orcas = [] # Clear all existing orcas
                    cachalots = [] # Clear all existing cachalots
                    kraken_tentacles = [] # Clear Kraken tentacles
                    icebergs = [] # Clear all icebergs
                    # Reset sea creature timers to ensure they start appearing after reset
                    generate_orca_timer = 0
                    generate_cachalot_timer = 0
                    generate_kraken_timer = 0
                    # Reset iceberg generation tracker
                    last_iceberg_round_generated = 0 # Ensures icebergs generate for Round 1
                    ship_hit_flash = False
                    hit_flash_timer = 0
                    hit_message_text = "" # <<< HIT FLASH INSURANCE - EVEN IF REDUNDANT, ADD THIS CODE HERE

    # --- B. GAME LOGIC ---
    # This section runs every frame of the game loop
    if not game_over: # This check that nothing moves or processes if the game is over

        # --- Iceberg Round Generation Logic---
        # Check if the current round is different from the last round for which icebergs were generated
        if current_round != last_iceberg_round_generated:
            generate_icebergs_for_round() # Call function to generate new icebergs
            last_iceberg_round_generated = current_round # Update the tracker to the current round

        # --- Flag to track if the ship's strength was reduced this frame ---
        ship_strength_reduction_this_frame = False
        
        # --- 1. Player Input and Ship Movement ---
        if not ship_docked: # Ship only moves when it's not docked in the fuel station
            keys = pygame.key.get_pressed() # Gets the state of ALL keyboard keys

            # Update ship's X position based on input
            if keys[pygame.K_LEFT]:
                ship.x -= ship_speed
            if keys[pygame.K_RIGHT]:
                ship.x += ship_speed
            if keys[pygame.K_UP]:
                ship.y -= ship_speed
            """
            # Down arrow key (Commented out to disable backward ship movement)
            if keys[pygame.K_DOWN]:
                ship.y += ship_speed
            """

            # --- IMPORTANT: CLAMP SHIP'S X POSITION WHEN REACHING FUEL STATION ---
            # Ship stays within the horizontal screen boundaries
            ship.x = max(0, min(ship.x, screen_width - ship.width))
            # Clamp vertical movement to keep it below the refuel zone
            ship.y = max(refuel_zone_height, min(ship.y, screen_height - ship.height)) # Prevents ship from going into top zone unless docking

        # --- 2. Fuel Station Docking Logic ---
        if not ship_docked: # Check for docking if the ship isn't already docked
            for slot_info in fuel_slots:
                if ship.colliderect(slot_info['rect']) and slot_info['round'] == current_round:
                    if ship.colliderect(slot_info['rect']) and \
                       slot_info['round'] == current_round and \
                       not slots_completed[slot_info['round'] - 1]:

                        ship_docked = True
                        ship.center = slot_info['rect'].center
                        ship.x -= 5 
                        ship.y += 0 
                        slots_completed[current_round - 1] = True
                        ROUND_COMPLETE_TIMER = ROUND_COMPLETE_DELAY_FRAMES

        # --- 3. Handle Round Completion Delay ---
        if ship_docked and ROUND_COMPLETE_TIMER > 0:
            ROUND_COMPLETE_TIMER -= 1 
            if ROUND_COMPLETE_TIMER <= 0:
                if ROUND_COMPLETE_TIMER <= 0: # If timer runs out, then reset game or advance to new round
                    print("Preparing for next round or game reset.")

                    score += 100 # Track the score

                    # 1. Advance to the next round
                    current_round += 1
                    print(f"Advancing to Round {current_round}")

                    # 2. Reset the ship's starting state and position for the new round
                    ship_docked = False # Allow the ship to move again
                    ship.x = screen_width // 2 - ship_width // 2 # Reset to bottom center
                    ship.y = screen_height - ship_height - 0 # Ship starts at the bottom safety zone

                    # 3. Clear all existing sea creatures (if there are any active in the lists)
                    orcas = []
                    cachalots = []
                    kraken_tentacles = []

                    # 4. IMPORTANT: Reset sea creature generating timers
                    generate_orca_timer = 0
                    generate_cachalot_timer = 0
                    generate_kraken_timer = 0

                    # 5. Check for Game Win Condition (if all rounds completed)
                    if current_round > total_rounds:
                        print("All round completed! Game Over - You Win!")
                        game_over = True 
                        game_won = True # <-- Displays the "You Win!" message
    
        # Move Orcas
        orcas_to_keep = [] # Create a new list to safely collect orcas to keep
        for orca_obj in orcas: # Iterate over orca OBJECTS
            orca_obj.rect.x += orca_obj.speed_x # Move the orca's Rect using its stored speed_x

            # Check if the orca is still on screen or moving
            if (orca_obj.speed_x > 0 and orca_obj.rect.left > screen_width) or \
               (orca_obj.speed_x < 0 and orca_obj.rect.right < 0):
                # This orca is off-screen, do NOT add it to the list of orcas_to_keep
                pass 
            else:
                orcas_to_keep.append(orca_obj) # Keep the orca only if it's still on screen or entering
        
        orcas = orcas_to_keep # Replace the old orcas list with the new filtered list

        # Introduce new orcas periodically
        generate_orca_timer += 1
        if generate_orca_timer >= generate_orca_interval:
            generate_orca()
            generate_orca_timer = 0

        # Move Cachalots
        cachalots_to_keep = [] # Create a new list for cachalots
        for cachalot_obj in cachalots: # Iterate over Cachalot OBJECTS
            cachalot_obj.rect.x += cachalot_obj.speed_x # Move the cachalot's Rect

            if (cachalot_obj.speed_x > 0 and cachalot_obj.rect.left > screen_width) or \
               (cachalot_obj.speed_x < 0 and cachalot_obj.rect.right < 0):
                pass # Do nothing, it's been removed
            else:
                cachalots_to_keep.append(cachalot_obj)
        
        cachalots = cachalots_to_keep # Replace the old cachalots list

        # Introduce new cachalots periodically
        generate_cachalot_timer += 1
        if generate_cachalot_timer >= generate_cachalot_interval:
            generate_cachalot()
            generate_cachalot_timer = 0

        # --- 5. Update and Generate Kraken Tentacles ---
        kraken_tentacles_to_keep = [] # Create a temporary list for tentacles that are still active
        # The 'for' loop defines 'tentacle' for each item in kraken_tentacles
        for tentacle in kraken_tentacles:
            tentacle.update() # Call the tentacle's position to make it swing in its lifetime

            tentacle_hit = False # Flag to know if this specific tentacle caused a hit

            # 1. Check collision with the main base circle (head)
            if ship.colliderect(tentacle.rect):
                tentacle_hit = True

            # 2. Check collision with each segment (ball) in the chain
            if not tentacle_hit: # Only check balls if the head hasn't already caused a hit
                for segment in tentacle.segments:
                    # Create a Pygame Rect for the segment for collision checking
                    segment_rect = pygame.Rect(
                        int(segment['x']) - tentacle.segment_radius,
                        int(segment['y']) - tentacle.segment_radius,
                        tentacle.segment_radius * 2,
                        tentacle.segment_radius * 2
                    )
                    if ship.colliderect(segment_rect):
                        tentacle_hit = True
                        break # Stop checking segments for this tentacle if one hit

            # 3. Handle the hit or keep the tentacle
            if tentacle_hit:
                ship_strength -= 1
                ship_hit_flash = True
                hit_flash_timer = hit_flash_duration
                hit_message_text = "Arrgghh! Blasted Kraken tentacle! Don't give an inch to that beast!" # When hit by tentacle
                if ship_strength <= 0:
                    game_over = True
                else:
                    # Reset ship position after hit
                    ship.x = screen_width // 2 - ship_width // 2
                    ship.y = screen_height - ship_height - 20
            elif tentacle.lifetime > 0: # Only keep if not hit AND still alive
                kraken_tentacles_to_keep.append(tentacle)

        # Updates the main list of tentacles   
        kraken_tentacles = kraken_tentacles_to_keep 

        # Attempt to Generate a new Kraken tentacle based on its timer
        generate_kraken_timer += 1
        if generate_kraken_timer >= generate_kraken_interval:
            generate_kraken_tentacle() # Call the function to create a new tentacle
            generate_kraken_timer = 0 # Reset the timer

        # 5. Ship Boundary Checking
        if ship.left < 0:
            ship.left = 0
        if ship.right > screen_width:
            ship.right = screen_width
        if ship.top < 0:
            ship.top = 0
        if ship.bottom > screen_height:
            ship.bottom = screen_height

        # Update the welcome text timer for the central message
        if current_round == 1 and not game_won and welcome_text_timer < WELCOME_TEXT_DURATION:
            welcome_text_timer += 1

        # Update the bottom message timer - the messages will cycle only during active gameplay
        if not game_won: # Messeges won't cycle if game is won
            MOTIVATIONAL_MESSAGE_TIMER += 1
            if MOTIVATIONAL_MESSAGE_TIMER >= MOTIVATIONAL_MESSAGE_CYCLE_DURATION:
                MOTIVATIONAL_MESSAGE_TIMER = 0 # Reset timer
                # Move to the next message set, looping back to the start if it reaches the end of the list
                CURRENT_MOTIVATIONAL_MESSAGE_INDEX = (CURRENT_MOTIVATIONAL_MESSAGE_INDEX + 1) % len(MOTIVATIONAL_MESSAGES)

        # --- COLLISION DETECTION LOGIC ---

        # --- ICEBERG Collision Action ---
        # Only process if the ship's strength wasn't already reduced in this frame, game isn't over, and the ship is not docked
        if not ship_strength_reduction_this_frame and not game_over and not ship_docked:
            for iceberg in icebergs: # Iterate through the list of iceberg objects
                # Check for collision between the ship and the current iceberg
                if ship.colliderect(iceberg.rect):
                    ship_strength -= 1 # Deduct a ship strength
        
                    # Activate visual and message feedback for a hit
                    ship_hit_flash = True
                    hit_flash_timer = hit_flash_duration
                    hit_message_text = "Impact! You struck an Iceberg!" # Iceberg hit message

                    # --- Reposition the HIT iceberg (randomly placed with safety and overlap checks) ---
                    iceberg_width = iceberg.rect.width
                    iceberg_height = iceberg.rect.height

                    # Define the iceberg's "no-generate" zone at the bottom of the screen for the ship
                    no_generate_zone_rect = pygame.Rect(0, screen_height - starter_zone_height, screen_width, starter_zone_height)

                    MAX_REPOSITION_ATTEMPTS = 50 # Limits how many attempts to find a safe spot
                    attempts = 0
                    placed_safely = False

                    while not placed_safely and attempts < MAX_REPOSITION_ATTEMPTS:
                        # Generate a potential new position within the overall screen bounds
                        potential_x = random.randint(0, screen_width - iceberg_width)
                        potential_y = random.randint(0, screen_height - iceberg_height) # Allow full canvas initially

                        # Create a temporary rectangle for this potential new position
                        temp_iceberg_rect = pygame.Rect(potential_x, potential_y, iceberg_width, iceberg_height)

                        # Check 1: Does this potential position avoid the ship's safe zone?
                        avoids_safe_zone = not temp_iceberg_rect.colliderect(no_generate_zone_rect)

                        # Check 2: Does this potential position avoid overlapping other existing icebergs?
                        avoids_other_icebergs = True
                        for other_iceberg in icebergs:
                            # Checks against the struck iceberg itself so that it doesn't move to the same position
                            if other_iceberg is not iceberg and temp_iceberg_rect.colliderect(other_iceberg.rect):
                                avoids_other_icebergs = False # Overlaps another iceberg
                                break # No need to check further

                        # If both conditions are met, it's a safe spot for the iceberg
                        if avoids_safe_zone and avoids_other_icebergs:
                            iceberg.rect.x = potential_x
                            iceberg.rect.y = potential_y
                            placed_safely = True # Iceberg successfully placed, exit the while loop

                        attempts += 1 # Increment attempt counter

                    # If a safe spot couldn't be found after many attempts, the iceberg will move, even if there's no safe spot
                    if not placed_safely:
                        # Place the struck iceberg at the very top-left corner as a last resort
                        iceberg.rect.x = 0
                        iceberg.rect.y = 0
                        print("Warning: Could not find a perfectly safe reposition for iceberg. Placed at (0,0) as fallback.")

                    # Check if it's a game over or just a ship strength reduction
                    if ship_strength <= 0:
                        game_over = True # Game over, no more strength length
                    else:
                        # Reset ship position after losing a strength
                        ship.x = screen_width // 2 - ship_width // 2
                        ship.y = screen_height - ship_height - 20
                    ship_strength_reduction_this_frame = True
                    break # Exit this iceberg loop after a hit

        # --- KRAKEN TENTACLE Collision Action ---
        kraken_tentacles_after_collision = [] # Create a temporary list for tentacles that didn't collide
        # Only process if the ship's strength wasn't already reduced in this frame, game isn't over, and the ship is not docked
        if not ship_strength_reduction_this_frame and not game_over and not ship_docked:
            for tentacle in kraken_tentacles: # Iterate over The Kraken objects
                tentacle_hit = False

                # Check collision with the main base circle (head)
                if ship.colliderect(tentacle.rect):
                    tentacle_hit = True

                # Check collision with each ball in the chain
                if not tentacle_hit: # Only check segments if the head hasn't hit
                    for segment in tentacle.segments:
                        # Create a Pygame Rect for the segment to check for collisions
                        # The segment's 'x' and 'y' are its center, so calculate top-left for Rect
                        segment_rect = pygame.Rect(
                            int(segment['x']) - tentacle.segment_radius,
                            int(segment['y']) - tentacle.segment_radius,
                            tentacle.segment_radius * 2,
                            tentacle.segment_radius * 2
                        )
                        if ship.colliderect(segment_rect):
                            tentacle_hit = True
                            break # No need to check other balls if one is hit

                if tentacle_hit:
                    ship_strength -= 1
                    ship_hit_flash = True
                    hit_flash_timer = hit_flash_duration
                    hit_message_text = "Arrgghh! Blasted Kraken tentacle! Don't give an inch to that beast!"
                    if ship_strength <= 0:
                        game_over = True
                    else:
                        # Reset ship position after hit
                        ship.x = screen_width // 2 - ship_width // 2
                        ship.y = screen_height - ship_height - 20
                    ship_strength_reduction_this_frame = True
                    break # Break out of THIS kraken loop
                elif tentacle.lifetime > 0:
                    kraken_tentacles_after_collision.append(tentacle)
        
            kraken_tentacles = kraken_tentacles_after_collision # Update the main Kraken list

        # --- ORCA Collision Action --- 
        orcas_after_collision = []
        # Only process if the ship's strength wasn't already reduced in this frame, game isn't over, and the ship is not docked
        if not ship_strength_reduction_this_frame and not game_over and not ship_docked:
            for orca_obj in orcas: # Iterate over Orca objects
                if ship.colliderect(orca_obj.rect): # Collide with the orca's Rect
                    ship_strength -= 1
                    # NEW: Activate hit flash
                    ship_hit_flash = True
                    hit_flash_timer = hit_flash_duration
                    hit_message_text = "Arrggghh, an angry orca! Hang on to your sea legs." # When ship hits an Orca
                    if ship_strength <= 0:
                        game_over = True
                    else:
                        ship.x = screen_width // 2 - ship_width // 2
                        ship.y = screen_height - ship_height - 20
                    ship_strength_reduction_this_frame = True
                    break # Break out of THIS orca loop, no need to check for other orcas
                    # If there's a collision, this orca_obj is not appended to orcas_after_collision (it's "removed" from the list)
                else:
                    orcas_after_collision.append(orca_obj) # Keep it in the list if there's no collision
            orcas = orcas_after_collision # Update the list after collision checks

        # --- CACHALOT Collision Action ---
        cachalots_after_collision = []
        # Only process if the ship's strength wasn't already reduced in this frame, game isn't over, and the ship is not docked
        if not ship_strength_reduction_this_frame and not game_over and not ship_docked:
            for cachalot_obj in cachalots: # Iterate over cachalot objects
                if ship.colliderect(cachalot_obj.rect): # Collide with the cachalot's Rect
                    ship_strength -= 1
                    # NEW: Activate hit flash
                    ship_hit_flash = True
                    hit_flash_timer = hit_flash_duration
                    hit_message_text = "Arrggghh, a blasted cachalot! All hands to the pumps!" # Ship collides with a cachalot
                    if ship_strength <= 0:
                        game_over = True
                    else:
                        ship.x = screen_width // 2 - ship_width // 2
                        ship.y = screen_height - ship_height - 20
                    ship_strength_reduction_this_frame = True
                    break # Break out of THIS cachalot loop
                else:
                    cachalots_after_collision.append(cachalot_obj)
            cachalots = cachalots_after_collision
            
        # Hit Flash Timer Code Written Here to Avoid Code Conflicts
        # Update the hit flash timer
        if ship_hit_flash:
            hit_flash_timer -= 1
            if hit_flash_timer <= 0:
                ship_hit_flash = False # Turn off flash when timer runs out
                hit_message_text = ""  # Clear the message when timer runs out
                    
    # --- C. DRAW THE CANVAS AND GAME PIECE ELEMENTS ---
    if ship_hit_flash:
        screen.fill(hit_flash_color) # Fill the canvas with red flash color if ship gets hit
    else:
        screen.fill(blue) # Fill the canvas with a normal ocean blue color

    # --- REFUEL STATION Slots --- 
    # Draw a bright green rectangle to show the active round's refuel slot
    pygame.draw.rect(screen, yellow, (refuel_zone_start_y, refuel_zone_start_y, screen_width, refuel_zone_height))

    # Draw the three refuel slots and their pumps
    for slot_info in fuel_slots:
        slot_rect = slot_info['rect']
        slot_round = slot_info['round']

        # Color of the current round's target slot (bright green)
        if slot_round == current_round:
            draw_color = (0, 255, 0, 50) # Bright green for the target refuel slot
        else:
            draw_color = slot_empty_color # Darker grey for the other inactive slots
    
        # Draw the filled-in rectangle for the fuel slot
        pygame.draw.rect(screen, draw_color, slot_rect)

        # 2. Draw the border/outline on top of the filled slot
        # Visual feedback for completed slots (gold) and the current target (bright green slot)
        if slots_completed[slot_round - 1]: # If this slot's round is marked as completed
            pygame.draw.rect(screen, (255, 215, 0), slot_rect, 3) # Gold border for completed slots

            # --- COMPLETED REFUEL MISSION: WHITE SQUARE AND SUN CODE ---
            # ALL THE SUN/RAYS CODE GOES HERE, INDENTED UNDER THE 'IF' STATEMENT
            # Calculate size and position for the white square inside the slot
            white_square_size = slot_rect.width * 0.5
            white_square_rect = pygame.Rect(0, 0, white_square_size, white_square_size)
            white_square_rect.center = slot_rect.center

            # Draw the white square
            pygame.draw.rect(screen, white, white_square_rect)
        
            # --- DRAW THE SUN AND ITS RAYS ---

            # Calculate sun's radius: Matches the original sun's proportion relative to the white square
            sun_radius = white_square_rect.width / 4

            # Draw the sun's central circle (yellow fill with outline)
            # Draw the yellow fill first
            pygame.draw.circle(screen, yellow, white_square_rect.center, sun_radius)
            # Draw the outline on top (2px thickness)
            pygame.draw.circle(screen, yellow, white_square_rect.center, sun_radius, 2)

            # Draw the sun's rays
            num_rays = 12 # Match the ship flag's sun's number of rays
            ray_length = sun_radius * 0.8 # Match the ship flag's sun's ray length proportion
            ray_thickness = 2 # Keep the ray's thickness, or adjust

            for angle_deg in range(0, 360, 360 // num_rays): # Iterate for 12 rays (360/12 = 30 degree steps)
                angle_rad = math.radians(angle_deg) # Convert degrees to radians

                # Calculate start point of the ray (on the edge of the sun)
                ray_start_x = white_square_rect.centerx + sun_radius * math.cos(angle_rad)
                ray_start_y = white_square_rect.centery + sun_radius * math.sin(angle_rad)

                # Calculate end point of the ray (extends outwards)
                ray_end_x = white_square_rect.centerx + (sun_radius + ray_length) * math.cos(angle_rad)
                ray_end_y = white_square_rect.centery + (sun_radius + ray_length) * math.sin(angle_rad)

                # Draw the sun ray as an orange line
                pygame.draw.line(screen, (255, 215, 0), (ray_start_x, ray_start_y), (ray_end_x, ray_end_y), ray_thickness)

            # Draw the yellow sun circle over the white square
            pygame.draw.circle(screen, (255, 215, 0), white_square_rect.center, sun_radius)

        elif slot_round == current_round: # Current target slot
            pygame.draw.rect(screen, black, slot_rect, 3) # Black border for the current target slot

            # NO sun or rays here, as this is the current target / sun appears when refueling is complete

        # Draw the fuel pump visual next to the slot (right side)
        pump_x = slot_rect.right + 5 # 5px to the right of the slot
        pump_y = slot_rect.bottom - fuel_pump_height # Align the bottom of the pump with the bottom of the slot
        pygame.draw.rect(screen, fuel_pump_color, (pump_x, pump_y, fuel_pump_width, fuel_pump_height))
    
        # Draw a small "nozzle" line for the pump
        pygame.draw.line(screen, black,
                         (pump_x + fuel_pump_width // 2, pump_y), # Top-center of pump
                         (pump_x + fuel_pump_width + 10, pump_y - 15), # Extends up-right
                         3) # Thickness

    # --- BOTTOM STARTER Safety Zone ---
    # Draw the Bottom Starter Zone (light blue)
    pygame.draw.rect(screen, starter_zone_color, (0, starter_zone_start_y + 10, screen_width, starter_zone_height))

    # 2. Draw the "Welcome to ShipGrrr!" Message (timed) in the middle of the canvas
    if current_round == 1 and not game_over and not game_won and welcome_text_timer < WELCOME_TEXT_DURATION:
        central_welcome_text = "Welcome to ShipGrrr!"
        welcome_surface = WELCOME_FONT.render(central_welcome_text, True, (255, 255, 255)) # White text to contrast with the ocean
        welcome_rect = welcome_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 15))
        screen.blit(welcome_surface, welcome_rect)

    # --- Display Rotating Starter Safety Zone Motivational Messages (Left and Right Sets) ---
    # Text sets will rotate and be displayed while the game is active
    if not game_over and not game_won:
        # Get the current message set based on the index
        current_left_messages, current_right_messages = MOTIVATIONAL_MESSAGES[CURRENT_MOTIVATIONAL_MESSAGE_INDEX]

        # Assign lines from the current set
        left_line1_content = current_left_messages[0]
        left_line2_content = current_left_messages[1]
        right_line1_content = current_right_messages[0]
        right_line2_content = current_right_messages[1]

        text_color = (0, 0, 0) # Black text for contrast on light blue safety zone

        # Render left text set lines
        left_line1_surface = GAME_MOTIVATIONAL_FONT.render(left_line1_content, True, text_color)
        left_line2_surface = GAME_MOTIVATIONAL_FONT.render(left_line2_content, True, text_color)

        # Render right text set lines
        right_line1_surface = GAME_MOTIVATIONAL_FONT.render(right_line1_content, True, text_color)
        right_line2_surface = GAME_MOTIVATIONAL_FONT.render(right_line2_content, True, text_color)

        # Calculate vertical center for text within the safety zone
        text_center_y = starter_zone_start_y + (starter_zone_height // 2)

        # Calculate Y positions for the left lines, centered together
        left_text_total_height = left_line1_surface.get_height() + left_line2_surface.get_height() + 5
        left_text_start_y = text_center_y - (left_text_total_height // 2 - 5)

        # Calculate Y positions for the right lines, centered together
        right_text_total_height = right_line1_surface.get_height() + right_line2_surface.get_height() + 5
        right_text_start_y = text_center_y - (right_text_total_height // 2 - 5)

        # Calculate X positions for Left Text (aligned to left with a margin)
        left_line1_x = 10
        left_line2_x = 10

        # Calculate X positions for Right Text (aligned to right with a margin)
        right_line1_x = screen_width - right_line1_surface.get_width() - 10
        right_line2_x = screen_width - right_line2_surface.get_width() - 10

        # Blit the left texts
        screen.blit(left_line1_surface, (left_line1_x, left_text_start_y))
        screen.blit(left_line2_surface, (left_line2_x, left_text_start_y + left_line1_surface.get_height() + 5))

        # Blit the right texts
        screen.blit(right_line1_surface, (right_line1_x, right_text_start_y))
        screen.blit(right_line2_surface, (right_line2_x, right_text_start_y + right_line1_surface.get_height() + 5))
    
    # Draw Orca (Black Rectangles With an Elliptical White Patch)
    for orca_obj in orcas:
        pygame.draw.rect(screen, orca_color, orca_obj.rect) # Draw the main black body

        # --- Draw the triangular tail for Orcas ---
        tail_extension = orca_obj.rect.width * 0.15 # How far the tail extends from the body (horizontal)
        tail_span = orca_obj.rect.height * 0.6 # How wide the tail flukes are (vertical)

        # Calculate the three points for the tail triangle
        if orca_obj.speed_x > 0: # Orca is moving right (tail on the left)
            # Point 1: At the center of the left edge of the orca body
            point1 = (orca_obj.rect.left, orca_obj.rect.centery)
            # Points 2 and 3: Extending leftwards (tail_extension) and upwards/downwards (tail_span)
            point2 = (orca_obj.rect.left - tail_extension, orca_obj.rect.centery - tail_span / 2)
            point3 = (orca_obj.rect.left - tail_extension, orca_obj.rect.centery + tail_span / 2)
        else: # Orca is moving left (tail on the right)
            # Point 1: At the center of the right edge of the orca's body
            point1 = (orca_obj.rect.right, orca_obj.rect.centery)
            # Points 2 and 3: Extending rightwards (tail_extension) and upwards/downwards (tail_span)
            point2 = (orca_obj.rect.right + tail_extension, orca_obj.rect.centery - tail_span / 2)
            point3 = (orca_obj.rect.right + tail_extension, orca_obj.rect.centery + tail_span / 2)

        # Draw the tail using pygame.draw.polygon, same color as the orca's body
        pygame.draw.polygon(screen, orca_color, [point1, point2, point3])
    
        # Simulate the Orca's White Patch
        white_patch_width = orca_obj.rect.width // 3  # The whale's width
        white_patch_height = orca_obj.rect.height // 2 # Half of the whale's height
        white_patch_x = orca_obj.rect.x + (orca_obj.rect.width // 4) # Position it inside the black rect
        white_patch_y = orca_obj.rect.y + (orca_obj.rect.height // 4) # Position it inside the black rect

        # Adjust white_patch_x based on swimming direction
        if orca_obj.speed_x > 0: # Orca is moving right (patch is on the right side)
            # Position the patch on the right 1/4 of the Orca's body
            white_patch_x = orca_obj.rect.x + (orca_obj.rect.width * 3 // 4) - white_patch_width // 1
        else: # Orca is moving left (patch is on the left side)
            # Position the patch on the left 1/4 of the Orca's body
            white_patch_x = orca_obj.rect.x + (orca_obj.rect.width // 3) - white_patch_width // 6 + 5
            # Left-to-right moving orcas white patch adjustment for alignment
            white_patch_x -= 2

        pygame.draw.ellipse(screen, white, (white_patch_x, white_patch_y, white_patch_width, white_patch_height))

    # Draw Cachalot Whales (grayish cachalot_color ovals)
    for cachalot_obj in cachalots:
        pygame.draw.ellipse(screen, cachalot_color, cachalot_obj.rect)

        # --- Draw the triangular tail ---
        tail_width = cachalot_obj.rect.width * 0.25  # Adjust ratios for an attractive tail
        tail_height = cachalot_obj.rect.height * 0.35 # Height of the tail from the body

        # Calculate tail base point (where it attaches to the body)
        if cachalot_obj.speed_x > 0: # Moving Right
            # Tail is on the left side of the cachalot
            tail_base_x = cachalot_obj.rect.left
            tail_base_y = cachalot_obj.rect.centery
        
            # Calculate the two fluke points
            point1 = (tail_base_x, tail_base_y)
            point2 = (tail_base_x - tail_height, tail_base_y - tail_width / 2) # Extends left and slightly up
            point3 = (tail_base_x - tail_height, tail_base_y + tail_width / 2) # Extends left and slightly down

        else: # Moving Left
            # Tail is on the right side of the cachalot
            tail_base_x = cachalot_obj.rect.right
            tail_base_y = cachalot_obj.rect.centery

            # Calculate the two fluke points
            point1 = (tail_base_x, tail_base_y)
            point2 = (tail_base_x + tail_height, tail_base_y - tail_width / 2) # Extends right and slightly up
            point3 = (tail_base_x + tail_height, tail_base_y + tail_width / 2) # Extends right and slightly down

        # Draw the tail using pygame.draw.polygon and use the same color as the cachalot body
        pygame.draw.polygon(screen, cachalot_color, [point1, point2, point3])
    
        # Add the cachalot's black eye
        eye_radius_x = cachalot_obj.rect.width // 10  # Width of the eye ellipse
        eye_radius_y = cachalot_obj.rect.height // 6  # Height of the eye ellipse
        eye_offset_y = cachalot_obj.rect.height // 3  # How far down from the top of the cachalot

        # Determine eye's horizontal position based on direction and adjust the divisor to move the eye further back
        eye_position_offset = cachalot_obj.rect.width // 3 # This value determines how far from the whale's 'front'

        if cachalot_obj.speed_x > 0: # Cachalot is moving right (eye should be on the right side, but further back)
            eye_x = cachalot_obj.rect.x + cachalot_obj.rect.width - eye_position_offset
        else: # Cachalot is moving left (eye should be on the left side, but further back)
            eye_x = cachalot_obj.rect.x + eye_position_offset

        eye_y = cachalot_obj.rect.y + eye_offset_y + 8 # Eye vertical position, moved down

        # Create the bounding rectangle for the eye ellipse
        eye_rect = pygame.Rect(eye_x - eye_radius_x, eye_y - eye_radius_y, eye_radius_x * 2, eye_radius_y * 2)

        # Draw the eye
        pygame.draw.ellipse(screen, black, eye_rect)

    # --- Draw the Icebergs ---
    for iceberg in icebergs: # Iterate through the list of active icebergs and draw each one
        iceberg.draw(screen) # Draw each iceberg

    # Draw Kraken Tentacles (Circular eye with ball chain that can swing)
    for tentacle in kraken_tentacles:
        tentacle.draw(screen) # Call the draw method of The Kraken Tentacle object

    # Draw the Ship's Main Hull (elongated ellipse as the vessel's main body)
    # The collision area is larger than the visual because of the oval shape
    hull_draw_rect = pygame.Rect(
        ship.x + ship.width * 0.20,
        ship.y + ship.height * 0.03,
        ship.width * 0.8,            # Make it narrower
        ship.height * 1.0            # Make it taller
    )
    pygame.draw.ellipse(screen, ship_hull_color, hull_draw_rect)

    # Draw a Cabin/Conning Tower (a small rectangle or circle on top of the hull)
    cabin_width = ship.width * 0.7
    cabin_height = ship.height * 0.6
    cabin_draw_rect = pygame.Rect(
        ship.centerx - cabin_width / 3, # Center horizontally
        ship.centery - cabin_height / 3, # Center vertically
        cabin_width,
        cabin_height
    )
    pygame.draw.rect(screen, black, cabin_draw_rect)

    # Add a small 'window' or detail to the cabin
    window_radius = int(cabin_width * 0.3)
    
    # Add a sun-like 'window' or detail to the cabin
    pygame.draw.circle(screen, yellow, cabin_draw_rect.center, window_radius)

    # --- Add 'rays' to the window to make it look like a sun ---
    num_rays = 12 # Number of sun rays. Adjust this for more or fewer rays
    ray_length = window_radius * 1.4 # How far the rays extend past the circle
    ray_thickness = 3 # Thickness of the rays, can be adjusted (e.g., 1 for thinner, 3 for thicker)
    ray_color = yellow # Keep rays the same color as the sun
    
    center_x, center_y = cabin_draw_rect.center # Center point of the ship's window

    for i in range(num_rays):
        # Calculate the angle for each ray
        angle = (i / num_rays) * 360 # Angle in degrees (0 to 360)
        angle_radians = math.radians(angle) # Convert to radians for math functions

        # Calculate the end point of each ray
        # cos(angle) for x-coordinate, sin(angle) for y-coordinate
        end_x = center_x + math.cos(angle_radians) * ray_length
        end_y = center_y + math.sin(angle_radians) * ray_length

        # Draw the ray line
        pygame.draw.line(screen, ray_color, (center_x, center_y), (end_x, end_y), ray_thickness)

    # --- Draw the Rudder in the middle and at the back of the ship ---
    rudder_center = (ship.centerx + 5, ship.bottom) # Rudder at the very bottom-center of the ship's rect

    # Draw the main circular part of the rudder
    rudder_radius = int(ship.width * 0.09) # Adjust size
    pygame.draw.circle(screen, ship_cabin_color, rudder_center, rudder_radius)
    
    # Draw the horizontal blade of the rudder (across the ship's width)
    blade_length_x = ship.width * 0.6 # How wide the horizontal blade is
    blade_thickness = 2 # Thickness of the lines

    pygame.draw.line(screen, purple,
                     (rudder_center[0] - blade_length_x / 3, rudder_center[1]),
                     (rudder_center[0] + blade_length_x / 3, rudder_center[1]),
                     blade_thickness)

    # IMPORTANT: The 'ship' pygame.Rect itself is still what determines its collision area. The drawing is just a visual.
    
    # Display the piratey hit message
    # This condition is for the message to appear only when there's a hit and its duration
    if ship_hit_flash and hit_flash_timer > 0:
        # Fonts are being defined outside the game loop for direct rendering
        pirate_font = pygame.font.Font(None, 36) # Defined font and size

        # Render the hit message text with the yellow color
        hit_message_surface = pirate_font.render(hit_message_text, True, yellow)

        # Define text box properties (consistent with the Game Over box style)
        hit_box_color = (0, 0, 0, 220) # Black with 220 alpha (semi-transparent)
        hit_box_padding = 20 # Padding around the text inside the box (adjust as desired)

        # Calculate box dimensions based on the rendered text
        box_width = hit_message_surface.get_width() + (hit_box_padding * 2)
        box_height = hit_message_surface.get_height() + (hit_box_padding * 2)

        # Create the transparent surface for the text box
        # pygame.SRCALPHA is crucial for transparent backgrounds
        hit_box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        hit_box_surface.fill(hit_box_color) # Fill it with the semi-transparent black color

        # Position the text box, centered horizontally, and slightly above the vertical center
        # Adjust for 'message_rect' as needed to fine-tune placement
        hit_box_rect = hit_box_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 180))

        # Blit the text box to the main screen first
        screen.blit(hit_box_surface, hit_box_rect)

        # Calculate the text's position inside the blitted box to center the text within the box's padding
        message_x = hit_box_rect.x + (hit_box_rect.width - hit_message_surface.get_width()) // 2
        message_y = hit_box_rect.y + hit_box_padding

        # Blit the hit message text on top of the box
        screen.blit(hit_message_surface, (message_x, message_y))
    
    # Draw Ship Strength Tracker (on the left side of the screen)
    strength_text = font.render(f"Strength: {ship_strength}", True, black)
    screen.blit(strength_text, (10, refuel_zone_start_y + 10))

    # Draw Score Tracker (on the rightside of the screen)
    score_text = font.render(f"Score: {score}", True, black)
    score_text_x = screen_width - score_text.get_width() - 10
    screen.blit(score_text, (score_text_x, refuel_zone_start_y + 10))

    # Display Game Over Message
    if game_over:
        if game_won:
            # Fill the entire canvas with the game over background color to cover all other game elements before drawing text
            screen.fill(blue) # Blue game_over_screen_color
    
            # Display the WIN message
            win_text = font.render("CONGRATULATIONS! You win the game!", True, (0, 255, 0)) # Green text for win
            restart_text = font.render("Press SPACE to play again.", True, (255, 255, 255)) # White text to play again

            win_text_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 2 - 20))
            restart_text_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))

            screen.blit(win_text, win_text_rect)
            screen.blit(restart_text, restart_text_rect)
        else:
            # Display the GAME OVER message
            
            # --- Start of Text Box and Game Over Message Logic ---

            # Define the content for the Game Over message
            game_over_title_text = "SHIP CRITICALLY DAMAGED!" # Red text message
            restart_game_text = "Press SPACE to play again." # White restart message

            # Define text box properties
            text_box_color = (0, 0, 0, 220) # Black with 220 alpha (semi-transparent)
            text_box_padding = 20 # Padding around the text inside the box

            # Render text and 'font' surfaces
            go_title_surface = font.render(game_over_title_text, True, (255, 0, 0)) # Red text for title
            restart_surface = font.render(restart_game_text, True, (255, 255, 255)) # White text for restart

            # --- Calculate Text Box Dimensions and Position ---
            # Determine the widest text line for box width
            max_text_width = max(go_title_surface.get_width(), restart_surface.get_width())

            # Determine total height needed for both lines + gap
            line_gap = 10 # Space between the title and the restart prompt
            total_text_height = go_title_surface.get_height() + restart_surface.get_height() + line_gap

            # Calculate box dimensions including padding
            box_width = max_text_width + (text_box_padding * 2)
            box_height = total_text_height + (text_box_padding * 2)

            # Create a new surface for the text box with SRCALPHA for transparency
            text_box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            text_box_surface.fill(text_box_color) # Fill it with the semi-transparent black color

            # Get the rectangle for the text box and center it on the screen
            text_box_rect = text_box_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 10))

            # --- Blit the Text Box to the Main Screen ---
            screen.blit(text_box_surface, text_box_rect)

            # --- Calculate Text Positions (relative to the text box) ---
            
            # Position of "SHIP CRITICALLY DAMAGED!"
            go_title_x = text_box_rect.x + (text_box_rect.width - go_title_surface.get_width()) // 2
            go_title_y = text_box_rect.y + text_box_padding

            # Position of "Press SPACE to play again."
            restart_x = text_box_rect.x + (text_box_rect.width - restart_surface.get_width()) // 2
            restart_y = go_title_y + go_title_surface.get_height() + line_gap

            # --- Blit the Text onto the Main Screen and Over the Text Box ---
            screen.blit(go_title_surface, (go_title_x, go_title_y))
            screen.blit(restart_surface, (restart_x, restart_y))

    pygame.display.flip()

    # --- D. FRAME RATE CONTROL ---
    clock.tick(fps)

# --- QUIT PYGAME ---
pygame.quit()

"""
SHIPGRRR GAME CREDITS:

ShipGrrr is written in Python IDLE and the Pygame library, authored by Michelle Bliss with some strategic assistance from Google's Gemini artificial intelligence program.

Credit for The Kraken tentacle goes to Gemini as the AI insisted on including tentacles to enrich the game's playability and improve its design concept.

Michelle Bliss's artistic collaboration on The Kraken's tentacles was to develop it in the manner of the mythical Norse sea monster that randomly pops up from beneath the sea.

The mythical Kraken creature is depicted by a coded chain of balls that swings and hits the ship.

The chain-of-balls concept was demonstrated during a Code in Place game design workshop.

Google's Gemini AI provided the mathematics for drawing The Kraken tentacle chain of balls and calculating its swinging motions.

The AI also helped with the math coding for the game's aesthetic environment (e.g. ship, sun, orca patch, etc.).

Collaborative writing credit goes to Patrick Trotta, Michelle Bliss's business partner. With a creative synergy somewhat in the manner of Lennon and McCartney,
this writing team infused their conceptualization skills into the gaming-motivational text and helped enhance the game's starting safety zone.

"""
