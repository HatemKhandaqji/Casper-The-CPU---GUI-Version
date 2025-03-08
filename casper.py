import pygame
import json
import random

pygame.init()

# Window setup
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
pygame.display.set_caption("Casper The CPU")


background_color = (255, 255, 255)
black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)
dark_gray = (150, 150, 150)
text_color = (0, 0, 0)

feedback_rect = pygame.Rect(0, window_height - 30, window_width, 30)  # Define the area for feedback text
score_rect = pygame.Rect(0, 0, 200, 50)  # Define the area for score text
high_score_rect = pygame.Rect(0, 50, 200, 50)  # Define the area for high score text

font = pygame.font.Font(None, 60)  # Title font
button_font = pygame.font.Font(None, 40)  # Button font
submit_button_font = pygame.font.Font(None, 30)  # Smaller font for submit button

# Title text (moved higher)
title_text = font.render("Casper The CPU", True, (0, 0, 0))
title_rect = title_text.get_rect(center=(window_width // 2, window_height // 4))  # Adjusted position

# Button dimensions
button_width, button_height = 250, 60
button_spacing = 20
button_color = (200, 200, 200)

# Buttons (centered)
start_button_rect = pygame.Rect(0, 0, button_width, button_height)
achievements_button_rect = pygame.Rect(0, 0, button_width, button_height)
settings_button_rect = pygame.Rect(0, 0, button_width, button_height)  # New Settings button
exit_button_rect = pygame.Rect(0, 0, button_width, button_height)

# Button positions
start_button_rect.centerx = achievements_button_rect.centerx = settings_button_rect.centerx = exit_button_rect.centerx = window_width // 2
start_button_rect.top = title_rect.bottom + 50  # Increased spacing
achievements_button_rect.top = start_button_rect.bottom + button_spacing
settings_button_rect.top = achievements_button_rect.bottom + button_spacing  # Positioning Settings button
exit_button_rect.top = settings_button_rect.bottom + button_spacing

current_screen = "menu"
# Initialization
show_confirmation_popup = False
caspers_sprite_taps = 0

# Achievements
achievements = [
    {
        "name": "First Day on the Job",
        "description": "Awarded for making the first correct guess",
        "reward": "light_pink",
        "condition": lambda data: data["total_correct_guesses"] >= 1,  # Check total correct guesses
        "unlocked": False
    },
    {
        "name": "Third Time's the Charm!",
        "description": "Awarded for making 3 correct consecutive guesses",
        "reward": "light_blue",
        "condition": lambda data: data["correct_consecutive_guesses"] >= 3,
        "unlocked": False
    },
    {
        "name": "The Big 5",
        "description": "Awarded for making 5 correct consecutive guesses",
        "reward": "yellow",
        "condition": lambda data: data["correct_consecutive_guesses"] >= 5,
        "unlocked": False
    },
    {
        "name": "Lucky Number",
        "description": "Awarded for making 7 correct consecutive guesses",
        "reward": "green",
        "condition": lambda data: data["correct_consecutive_guesses"] >= 7,
        "unlocked": False
    },
    {
        "name": "The Impossible",
        "description": "Awarded for making 10 correct consecutive guesses",
        "reward": "galaxy",
        "condition": lambda data: data["correct_consecutive_guesses"] >= 10,
        "unlocked": False
    },
    {
        "name": "The Start",
        "description": "Awarded for 5 total correct guesses",
        "reward": "black",
        "condition": lambda data: data["total_correct_guesses"] >= 5,
        "unlocked": False
    },
    {
        "name": "Hobbyist",
        "description": "Awarded for 25 total correct guesses",
        "reward": "rainbow",
        "condition": lambda data: data["total_correct_guesses"] >= 25,
        "unlocked": False
    },
    {
        "name": "Expert Guesser",
        "description": "Awarded for 50 total correct guesses",
        "reward": "food_rain",
        "condition": lambda data: data["total_correct_guesses"] >= 50,
        "unlocked": False
    },
    {
        "name": "Bad Start",
        "description": "Awarded for 5 total incorrect guesses",
        "reward": "brown",
        "condition": lambda data: data["incorrect_guesses"] >= 5,
        "unlocked": False
    },
    {
        "name": "Going Lower",
        "description": "Awarded for 25 total incorrect guesses",
        "reward": "dark_green",
        "condition": lambda data: data["incorrect_guesses"] >= 25,
        "unlocked": False
    },
    {
        "name": "Bottom of the Barrel",
        "description": "Awarded for 50 total incorrect guesses",
        "reward": "poop",
        "condition": lambda data: data["incorrect_guesses"] >= 50,
        "unlocked": False
    },
    {
        "name": "Avid Collector",
        "description": "Awarded for Collecting all backgrounds",
        "reward": "party_hat",
        "condition": lambda data: data.get("all_backgrounds_collected", False),
        "unlocked": False
    },
    {
        "name": "Who's a good boy?",
        "description": "Awarded for tapping on Casper's sprite 10 times",
        "reward": "cat_ears",
        "condition": lambda data: data.get("caspers_sprite_taps", 0) >= 10,
        "unlocked": False
    },
    {
        "name": "Master Guesser",
        "description": "Awarded for completing all other achievements",
        "reward": "caspers_gf",
        "condition": lambda data: all(ach["unlocked"] for ach in achievements[:-1]),  # All other achievements must be unlocked
        "unlocked": False
    }
]

def load_and_scale_background(image_path, window_width, window_height):
    background_image = pygame.image.load(image_path)
    background_image = pygame.transform.scale(background_image, (window_width, window_height))
    return background_image

def transition_to_menu():
    screen.fill(white)  # Clear the entire screen
    

    
    current_sprite = neutral_sprite
    feedback_text = ""

    
def render_feedback_text(feedback_text):
    # Clear the feedback text area
    screen.fill(white, feedback_rect)

    # Render and draw the new feedback text
    feedback_surface = button_font.render(feedback_text, True, black)
    screen.blit(feedback_surface, feedback_rect)
    pygame.display.flip()  # Refresh the display

def transition_to_gameplay():
    # Clear the entire screen
    screen.fill(white)

    # Apply equipped background
    background_image = None
    if "background" in player_data["equipped"]:
        background = player_data["equipped"]["background"]
        if background == "galaxy":
            background_image = load_and_scale_background("Sprites/Galaxy_background.png", window_width, window_height)
        elif background == "rainbow":
            background_image = load_and_scale_background("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\Rainbow_background.png", window_width, window_height)
        elif background == "food_rain":
            background_image = load_and_scale_background("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\food_rain_background.png", window_width, window_height)
        elif background == "poop":
            background_image = load_and_scale_background("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\poop_background.png", window_width, window_height)
        
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            if background == "light_pink":
                screen.fill((255, 192, 203))  # Light pink
            elif background == "light_blue":
                screen.fill((173, 216, 230))  # Light blue
            elif background == "yellow":
                screen.fill((255, 255, 0))  # Yellow
            elif background == "green":
                screen.fill((0, 255, 0))  # Green
            elif background == "black":
                screen.fill((0, 0, 0))  # Black
            elif background == "brown":
                screen.fill((139, 69, 19))  # Brown
            elif background == "dark_green":
                screen.fill((0, 100, 0))  # Dark Green
    else:
        screen.fill(white)  # Default to white background

    # Additional transition logic...
    # Reset relevant game variables, prepare UI elements, etc.

def clear_background():
    screen.fill(white) # currently not in use
    
def check_achievements():
    global achievements
    for achievement in achievements:
        if not achievement["unlocked"] and achievement["condition"](player_data):
            achievement["unlocked"] = True
            player_data["achievements"][achievement["name"]] = True

            # Update equipped dictionary based on the reward type
            player_data["equipped"] = player_data.get("equipped", {})
            if achievement["reward"] in ["light_pink", "light_blue", "yellow", "green", "black", "galaxy", "rainbow", "food_rain", "brown", "dark_green", "poop"]:
                player_data["equipped"]["background"] = achievement["reward"]
            elif achievement["reward"] in ["party_hat", "cat_ears", "caspers_gf"]:
                player_data["equipped"]["sprite"] = achievement["reward"]
            
            print(f"Achievement Unlocked: {achievement['name']}")

    # Save player data after checking achievements
    save_player_data()

def reset_player_data():
    global player_data, high_score, correct_consecutive_guesses, total_correct_guesses, incorrect_guesses, caspers_sprite_taps
    high_score = 0
    correct_consecutive_guesses = 0
    total_correct_guesses = 0
    incorrect_guesses = 0
    caspers_sprite_taps = 0
    player_data = {
        "high_score": high_score,
        "correct_consecutive_guesses": correct_consecutive_guesses,
        "total_correct_guesses": total_correct_guesses,
        "incorrect_guesses": incorrect_guesses,
        "caspers_sprite_taps": caspers_sprite_taps,
        "achievements": {achievement["name"]: False for achievement in achievements},
        "equipped": {}  # Ensure equipped key is initialized
    }
    
    save_player_data()
    
# Gameplay GUI elements
guess_input = ""
input_active = False
feedback_text = ""
score = 0
high_score = 0
correct_consecutive_guesses = 0
total_correct_guesses = 0
total_incorrect_guesses = 0

def generate_new_casper_number():
    return random.randint(1, 10)

casper_number = generate_new_casper_number()


player_data = {}
try:
    with open("player_datas.json", "r") as file:
        file_content = file.read().strip()
        if file_content:
            player_data = json.loads(file_content)
        else:
            player_data = {}
        high_score = player_data.get("high_score", 0)
        correct_consecutive_guesses = player_data.get("correct_consecutive_guesses", 0)
        total_correct_guesses = player_data.get("total_correct_guesses", 0)
        incorrect_guesses = player_data.get("incorrect_guesses", 0)  # Load incorrect guesses
        caspers_sprite_taps = player_data.get("caspers_sprite_taps", 0)  # Load sprite taps
        player_data["equipped"] = player_data.get("equipped", {})  # Ensure equipped key is present
        # Initialize achievements key if not present
        if "achievements" not in player_data:
            player_data["achievements"] = {achievement["name"]: False for achievement in achievements}
        print("Loaded Player Data: ", player_data)
except (FileNotFoundError, json.JSONDecodeError):
    high_score = 0
    correct_consecutive_guesses = 0
    total_correct_guesses = 0
    incorrect_guesses = 0
    caspers_sprite_taps = 0  # Initialize sprite taps
    player_data = {
        "equipped": {},  # Initialize equipped rewards
        "achievements": {achievement["name"]: False for achievement in achievements}
    }
    

# Load achievements status
for achievement in achievements:
    achievement_name = achievement["name"]
    achievement["unlocked"] = player_data["achievements"].get(achievement_name, False)

# Load Casper's sprites
neutral_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\Casper_sprite.png")
angry_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\angry_casper.png")
neutral_sprite = pygame.transform.scale(neutral_sprite, (600, 600))  # Resizing sprites
angry_sprite = pygame.transform.scale(angry_sprite, (600, 600))

# Load the speech bubble sprite
speech_bubble_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\speech_bubble.png")
speech_bubble_sprite = pygame.transform.scale(speech_bubble_sprite, (450, 225))  # Resize to make it bigger

current_sprite = neutral_sprite  # Set the initial sprite
current_sprite_rect = current_sprite.get_rect(center=(window_width // 4, window_height // 2))
speech_bubble_rect = speech_bubble_sprite.get_rect(center=(current_sprite_rect.right + 100, current_sprite_rect.top + 50))

# Input and Submit button
submit_button_width = 200
submit_button_height = 50
submit_button_rect = pygame.Rect(0, 0, submit_button_width, submit_button_height)
input_box = pygame.Rect(0, 0, 200, 50)  # Resizing input box to be the same size as submit button

# Main Menu button (shared)
main_menu_button_rect = pygame.Rect(0, 0, 200, 50)
main_menu_button_rect.x = window_width - 220
main_menu_button_rect.y = 50  # Positioning near the top right, horizontally aligned with input and submit box

# Update the player's score and achievements
def update_score(correct_guess):
    global score, high_score, correct_consecutive_guesses, total_correct_guesses, incorrect_guesses
    if correct_guess:
        score += 1
        correct_consecutive_guesses += 1
        total_correct_guesses += 1
        if score > high_score:
            high_score = score
    else:
        score = 0
        correct_consecutive_guesses = 0
        incorrect_guesses += 1  # Increment incorrect guesses count

    # Check achievements after score update
    check_achievements()


# Update player data file
def save_player_data():
    global player_data  # Ensure we're modifying the global player_data dictionary
    player_data["high_score"] = high_score
    player_data["correct_consecutive_guesses"] = correct_consecutive_guesses
    player_data["total_correct_guesses"] = total_correct_guesses
    player_data["incorrect_guesses"] = incorrect_guesses  # Save incorrect guesses
    player_data["caspers_sprite_taps"] = caspers_sprite_taps  # Save sprite taps
    player_data["achievements"] = {achievement["name"]: achievement["unlocked"] for achievement in achievements}
    player_data["equipped"] = player_data.get("equipped", {})  # Ensure equipped key is saved
    with open("player_datas.json", "w") as file:
        json.dump(player_data, file)

        
cursor = pygame.Rect(input_box.x + 10, input_box.y + 10, 2, button_font.get_height())
cursor_visible = True
cursor_timer = pygame.time.get_ticks()

clock = pygame.time.Clock()
running = True
scroll_offset = 0  # Variable to keep track of scroll offset

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            window_width, window_height = event.w, event.h
            screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

            # Update positions on resize
            title_rect.center = (window_width // 2, window_height // 4)
            start_button_rect.centerx = achievements_button_rect.centerx = settings_button_rect.centerx = exit_button_rect.centerx = window_width // 2
            start_button_rect.top = title_rect.bottom + 50
            achievements_button_rect.top = start_button_rect.bottom + button_spacing
            settings_button_rect.top = achievements_button_rect.bottom + button_spacing  # Adjusted position
            exit_button_rect.top = settings_button_rect.bottom + button_spacing
            submit_button_rect.x = window_width - 280  # Moved slightly to the left
            submit_button_rect.y = window_height // 2 + 30
            input_box.x = window_width - 280  # Moved slightly to the left
            input_box.y = window_height // 2 - 30
            current_sprite_rect.center = (window_width // 4, window_height // 2)
            speech_bubble_rect.center = (current_sprite_rect.right + 100, current_sprite_rect.top + 50)
            main_menu_button_rect.x = window_width - 220
            main_menu_button_rect.y = 50

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "menu":
                if start_button_rect.collidepoint(event.pos):
                    current_screen = "gameplay"
                    transition_to_gameplay()
                    casper_number = generate_new_casper_number()  # Generate new number at the start of each game
                    current_sprite = neutral_sprite  # Reset to neutral sprite at the start of the game
                    score = 0  # Reset score at the start of each game
                    if start_button_rect.collidepoint(event.pos):
                        current_screen = "gameplay"
                        casper_number = generate_new_casper_number()  # Generate new number at the start of each game
                        current_sprite = neutral_sprite  # Reset to neutral sprite at the start of the game
                        score = 0  # Reset score at the start of each game
                        
                        # Initialize equipped key if not present
                        player_data["equipped"] = player_data.get("equipped", {})

                        # Apply equipped background
                        print("Applying equipped background:", player_data["equipped"].get("background"))  # Debug print statement
                        if "background" in player_data["equipped"]:
                                if player_data["equipped"]["background"] == "light_pink":
                                    screen.fill((255, 192, 203))  # Light pink
                                    print("Background set to light pink")  # Debug print statement
                                elif player_data["equipped"]["background"] == "light_blue":
                                    screen.fill((173, 216, 230))  # Light blue
                                    print("Background set to light blue")  # Debug print statement
                                elif player_data["equipped"]["background"] == "yellow":
                                    screen.fill((255, 255, 0))  # Yellow
                                    print("Background set to yellow")  # Debug print statement
                                elif player_data["equipped"]["background"] == "green":
                                    screen.fill((0, 255, 0))  # Green
                                    print("Background set to green")  # Debug print statement
                                elif player_data["equipped"]["background"] == "black":
                                    screen.fill((0, 0, 0))  # Black
                                    print("Background set to black")  # Debug print statement
                                elif player_data["equipped"]["background"] == "galaxy":
                                    background_image = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\Galaxy_background.png")
                                    screen.blit(pygame.transform.scale(background_image, (window_width, window_height)), (0, 0))
                                    print("Background set to galaxy")  # Debug print statement
                                elif player_data["equipped"]["background"] == "rainbow":
                                    background_image = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\Rainbow_background.png")
                                    screen.blit(pygame.transform.scale(background_image, (window_width, window_height)), (0, 0))
                                    print("Background set to rainbow")  # Debug print statement
                                elif player_data["equipped"]["background"] == "food_rain":
                                    background_image = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\food_rain_background.png")
                                    screen.blit(pygame.transform.scale(background_image, (window_width, window_height)), (0, 0))
                                    print("Background set to food rain")  # Debug print statement
                                elif player_data["equipped"]["background"] == "brown":
                                    screen.fill((139, 69, 19))  # Brown
                                    print("Background set to brown")  # Debug print statement
                                elif player_data["equipped"]["background"] == "dark_green":
                                    screen.fill((0, 100, 0))  # Dark Green
                                    print("Background set to dark green")  # Debug print statement
                                elif player_data["equipped"]["background"] == "poop":
                                    background_image = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\poop_background.png")
                                    screen.blit(pygame.transform.scale(background_image, (window_width, window_height)), (0, 0))
                                    print("Background set to poop")  # Debug print statement
                                else:
                                    screen.fill(white)  # Default to white background
                                    print("Background set to default white")  # Debug print statement
                        else:
                            screen.fill(white)  # Default to white background
                            print("Background set to default white - no background equipped")  # Debug print statement
                        # Apply equipped sprite
                        default_sprite_size = (600, 600)
                        if "sprite" in player_data["equipped"]:
                            if player_data["equipped"]["sprite"] == "party_hat":
                                current_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\party_casper.png")
                                current_sprite = pygame.transform.scale(current_sprite, default_sprite_size)  # Resize sprite
                            elif player_data["equipped"]["sprite"] == "cat_ears":
                                current_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\cat_casper.png")
                                current_sprite = pygame.transform.scale(current_sprite, default_sprite_size)  # Resize sprite
                            elif player_data["equipped"]["sprite"] == "caspers_gf":
                                current_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\caspers_gf.png")
                                current_sprite = pygame.transform.scale(current_sprite, default_sprite_size)  # Resize sprite
                            else:
                                current_sprite = pygame.transform.scale(neutral_sprite, default_sprite_size)  # Ensure default sprite is resized as well
                        else:
                            current_sprite = pygame.transform.scale(neutral_sprite, default_sprite_size)  # Default to neutral sprite

                        # Your existing gameplay logic...
                        screen.blit(current_sprite, current_sprite_rect)  # Draw the current sprite
                        screen.blit(speech_bubble_sprite, speech_bubble_rect)  # Draw the speech bubble
                        pygame.draw.rect(screen, dark_gray if input_active else gray, input_box)
                        guess_text = button_font.render(guess_input, True, text_color)
                        screen.blit(guess_text, (input_box.x + 10, input_box.y + 10))

                        # Draw the text inside the speech bubble
                        bubble_font = pygame.font.Font(None, 28)  # Adjust font size for speech bubble text
                        bubble_text = bubble_font.render("Guess the number I'm thinking of from 1-10!", True, black)
                        bubble_text_rect = bubble_text.get_rect(center=(speech_bubble_rect.centerx, speech_bubble_rect.centery - 40))  # Move text further up
                        screen.blit(bubble_text, bubble_text_rect)

                        if input_active:
                            current_time = pygame.time.get_ticks()
                            if current_time - cursor_timer >= 500:  # Blink every 500 milliseconds
                                cursor_visible = not cursor_visible
                                cursor_timer = current_time

                            if cursor_visible:
                                cursor.topleft = (input_box.x + 10 + button_font.size(guess_input)[0], input_box.y + 10)
                                pygame.draw.rect(screen, text_color, cursor)

                        feedback_surface = button_font.render(feedback_text, True, black)
                        feedback_rect = feedback_surface.get_rect(center=(window_width // 2, window_height - 50))  # Moved to bottom
                        screen.blit(feedback_surface, feedback_rect)
                        feedback_text = ""

                        score_surface = button_font.render("Score: " + str(score), True, black)
                        screen.blit(score_surface, (10, 10))

                        high_score_surface = button_font.render("High Score: " + str(high_score), True, black)
                        screen.blit(high_score_surface, (10, 50))

                        pygame.draw.rect(screen, gray, submit_button_rect)
                        submit_text = submit_button_font.render("Submit", True, text_color)
                        screen.blit(submit_text, submit_text.get_rect(center=submit_button_rect.center))

                        # Draw Main Menu button
                        pygame.draw.rect(screen, gray, main_menu_button_rect)
                        main_menu_text = submit_button_font.render("Main Menu", True, text_color)
                        screen.blit(main_menu_text, main_menu_text.get_rect(center=main_menu_button_rect.center))


                elif achievements_button_rect.collidepoint(event.pos):
                    current_screen = "achievements"
                elif settings_button_rect.collidepoint(event.pos):
                    current_screen = "settings"
                elif exit_button_rect.collidepoint(event.pos):
                    running = False
            
            if current_screen == "gameplay":
                    if input_box.collidepoint(event.pos):
                        input_active = not input_active
                    else:
                        input_active = False

                    if submit_button_rect.collidepoint(event.pos):
                        try:
                            guess = int(guess_input)
                            if guess == casper_number:
                                feedback_text = f"Correct, you guessed the number Casper was thinking of: {casper_number}"
                                current_sprite = neutral_sprite  # Revert to neutral sprite
                                update_score(True)  # Update the score for a correct guess
                                
                            else:
                                feedback_text = f"Incorrect, you didn't guess the number Casper was thinking of. Try again!"
                                current_sprite = angry_sprite  # Switch to angry sprite
                                update_score(False)  # Update the score for an incorrect guess
                                
                            casper_number = generate_new_casper_number()  # Generate new number after each guess
                        except ValueError:
                            feedback_text = "Please enter a valid number."
                        guess_input = ""
                    
                    if current_sprite_rect.collidepoint(event.pos):
                        caspers_sprite_taps += 1  # Increment sprite taps count
                        player_data["caspers_sprite_taps"] = caspers_sprite_taps  # Update player data for sprite taps
                        check_achievements()  # Check achievements after updating sprite taps
                        save_player_data()  # Save player data after each tap

                    if main_menu_button_rect.collidepoint(event.pos):
                        current_screen = "menu"
                        transition_to_menu()
                        save_player_data()  # Save player data when returning to the menu
        
            elif current_screen == "achievements":
                if main_menu_button_rect.collidepoint(event.pos):
                    current_screen = "menu"
    
        
        if event.type == pygame.KEYDOWN:
            if current_screen == "gameplay" and input_active:
                if event.key == pygame.K_RETURN:
                    input_string = guess_input.strip()  # Trim any whitespace
                    if input_string == "pollenbee":
                        print("Cheat code detected! Unlocking all achievements.")
                        for achievement in achievements:
                            achievement["unlocked"] = True
                            player_data["achievements"][achievement["name"]] = True

                        # Save the updated player_data to the .json file
                        with open("player_datas.json", "w") as file:
                            json.dump(player_data, file)
                        
                        # Optionally reset the input_string and guess_input to prevent repeated use
                        input_string = ""
                        guess_input = ""
                    else:
                        try:
                            guess = int(guess_input)
                            if guess == casper_number:
                                feedback_text = f"Correct, you guessed the number Casper was thinking of: {casper_number}"
                                current_sprite = neutral_sprite  # Revert to neutral sprite
                                update_score(True)  # Update the score for a correct guess
                            else:
                                feedback_text = f"Incorrect, you didn't guess the number Casper was thinking of. Try again! Your guess was: {guess}"
                                current_sprite = angry_sprite  # Switch to angry sprite
                                update_score(False)  # Update the score for an incorrect guess
                            casper_number = generate_new_casper_number()  # Generate new number after each guess
                            render_feedback_text(feedback_text)

                            # Clear the feedback text area
                            screen.fill(white, feedback_rect)

                            # Render and draw the new feedback text
                            feedback_surface = button_font.render(feedback_text, True, black)
                            screen.blit(feedback_surface, feedback_rect)
                            pygame.display.flip()  # Refresh the display
                        except ValueError:
                            feedback_text = "Please enter a valid number."
                            render_feedback_text(feedback_text)

                            # Clear the feedback text area
                            screen.fill(white, feedback_rect)

                            # Render and draw the new feedback text
                            feedback_surface = button_font.render(feedback_text, True, black)
                            screen.blit(feedback_surface, feedback_rect)
                            pygame.display.flip()  # Refresh the display

                        guess_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    guess_input = guess_input[:-1]
                else:
                    guess_input += event.unicode

            elif current_screen == "achievements":
                if event.key == pygame.K_UP:
                    scroll_offset = min(scroll_offset + 20, 0)  # Scroll up
                elif event.key == pygame.K_DOWN:
                    scroll_offset -= 20  # Scroll down

    if current_screen == "menu":
        screen.fill(background_color)
        screen.blit(title_text, title_rect)

        pygame.draw.rect(screen, gray, start_button_rect)
        pygame.draw.rect(screen, gray, achievements_button_rect)
        pygame.draw.rect(screen, gray, settings_button_rect)  # Draw Settings button
        pygame.draw.rect(screen, gray, exit_button_rect)

        start_text = button_font.render("Start Game", True, text_color)
        achievements_text = button_font.render("Achievements", True, text_color)
        settings_text = button_font.render("Settings", True, text_color)  # Render Settings text
        exit_text = button_font.render("Exit", True, text_color)

        screen.blit(start_text, start_text.get_rect(center=start_button_rect.center))
        screen.blit(achievements_text, achievements_text.get_rect(center=achievements_button_rect.center))
        screen.blit(settings_text, settings_text.get_rect(center=settings_button_rect.center))  # Position Settings text
        screen.blit(exit_text, exit_text.get_rect(center=exit_button_rect.center))
    
    elif current_screen == "gameplay":
        transition_to_gameplay()
        # Clear specific areas before drawing new text
        feedback_rect = pygame.Rect(0, window_height - 30, window_width, 30)
        screen.fill(background_color, feedback_rect)
        screen.fill(background_color, score_rect)
        screen.fill(background_color, high_score_rect)

        # Apply equipped background
        background_image = None
        if "background" in player_data["equipped"]:
            if player_data["equipped"]["background"] == "galaxy":
                background_image = load_and_scale_background("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\Galaxy_background.png", window_width, window_height)
            elif player_data["equipped"]["background"] == "rainbow":
                background_image = load_and_scale_background("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\Rainbow_background.png", window_width, window_height)
            elif player_data["equipped"]["background"] == "food_rain":
                background_image = load_and_scale_background("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\food_rain_background.png", window_width, window_height)
            elif player_data["equipped"]["background"] == "poop":
                background_image = load_and_scale_background("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\poop_background.png", window_width, window_height)

            if background_image:
                screen.blit(background_image, (0, 0))
            else:
                if background_image == "light_pink":
                    screen.fill((255, 192, 203))  # Light pink
                elif background_image == "light_blue":
                    screen.fill((173, 216, 230))  # Light blue
                elif background_image == "yellow":
                    screen.fill((255, 255, 0))  # Yellow
                elif background_image == "green":
                    screen.fill((0, 255, 0))  # Green
                elif background_image == "black":
                    screen.fill((0, 0, 0))  # Black
                elif background_image == "brown":
                    screen.fill((139, 69, 19))  # Brown
                elif background_image == "dark_green":
                    screen.fill((0, 100, 0))  # Dark Green)
        else:
            screen.fill(white)  # Default to white background

        # Clear specific areas before drawing new text
        feedback_rect = pygame.Rect(0, window_height - 30, window_width, 30)
        screen.fill(background_color, feedback_rect)
        screen.fill(background_color, score_rect)
        screen.fill(background_color, high_score_rect)

        # Draw updated texts and other elements
        screen.blit(current_sprite, current_sprite_rect)  # Draw the current sprite
        screen.blit(speech_bubble_sprite, speech_bubble_rect)  # Draw the speech bubble
        pygame.draw.rect(screen, dark_gray if input_active else gray, input_box)
        guess_text = button_font.render(guess_input, True, text_color)
        screen.blit(guess_text, (input_box.x + 10, input_box.y + 10))

        # Draw the text inside the speech bubble
        bubble_font = pygame.font.Font(None, 28)  # Adjust font size for speech bubble text
        bubble_text = bubble_font.render("Guess the number I'm thinking of from 1-10!", True, black)
        bubble_text_rect = bubble_text.get_rect(center=(speech_bubble_rect.centerx, speech_bubble_rect.centery - 40))  # Move text further up
        screen.blit(bubble_text, bubble_text_rect)

        if input_active:
            current_time = pygame.time.get_ticks()
            if current_time - cursor_timer >= 500:  # Blink every 500 milliseconds
                cursor_visible = not cursor_visible
                cursor_timer = current_time

            if cursor_visible:
                cursor.topleft = (input_box.x + 10 + button_font.size(guess_input)[0], input_box.y + 10)
                pygame.draw.rect(screen, text_color, cursor)
        
        feedback_surface = button_font.render(feedback_text, True, black)
        feedback_rect = feedback_surface.get_rect(center=(window_width // 2, window_height - 15))  # Moved to bottom
        screen.blit(feedback_surface, feedback_rect)
        

        score_surface = button_font.render("Score: " + str(score), True, black)
        screen.blit(score_surface, (10, 10))

        high_score_surface = button_font.render("High Score: " + str(high_score), True, black)
        screen.blit(high_score_surface, (10, 50))

        pygame.draw.rect(screen, gray, submit_button_rect)
        submit_text = submit_button_font.render("Submit", True, text_color)
        screen.blit(submit_text, submit_text.get_rect(center=submit_button_rect.center))

        # Draw Main Menu button
        pygame.draw.rect(screen, gray, main_menu_button_rect)
        main_menu_text = submit_button_font.render("Main Menu", True, text_color)
        screen.blit(main_menu_text, main_menu_text.get_rect(center=main_menu_button_rect.center))

    elif current_screen == "achievements":
        screen.fill(white)

        # Achievements title
        achievements_title = font.render("Achievements", True, black)
        screen.blit(achievements_title, (window_width // 2 - achievements_title.get_width() // 2, 10))

        # Scrollable surface for achievements
        achievements_surface = pygame.Surface((window_width, window_height * 2))  # Make surface taller for scrolling
        achievements_surface.fill(white)

        equip_button_rects = []  # Store equip button rectangles for event handling

        # Sample rows for each achievement
        row_y = 100 + scroll_offset  # Apply scroll offset
        for achievement in achievements:
            # Padlock sprite (made smaller and moved to the left)
            padlock_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\locked_padlock.png" if not achievement["unlocked"] else "C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\unlocked_padlock.png")
            padlock_sprite = pygame.transform.scale(padlock_sprite, (30, 30))  # Resize padlock sprite
            padlock_rect = padlock_sprite.get_rect(topleft=(20, row_y + 15))
            achievements_surface.blit(padlock_sprite, padlock_rect)

            # Achievement box (made longer to fit all text)
            achievement_box = pygame.Rect(60, row_y, 600, 60)
            pygame.draw.rect(achievements_surface, dark_gray if not achievement["unlocked"] else gray, achievement_box)
            achievement_name = button_font.render(achievement["name"], True, text_color)
            achievement_desc = submit_button_font.render(achievement["description"], True, text_color)
            achievements_surface.blit(achievement_name, (achievement_box.x + 10, achievement_box.y + 5))
            achievements_surface.blit(achievement_desc, (achievement_box.x + 10, achievement_box.y + 30))

             # Equip/Unequip button
            equip_button_rect = pygame.Rect(700, row_y, 100, 60)
            # Updated logic to check the equipped state
            equip_button_text = "Equip"
            if (player_data["equipped"].get("background") == achievement["reward"] or 
                player_data["equipped"].get("sprite") == achievement["reward"]):
                equip_button_text = "Unequip"
                
            pygame.draw.rect(achievements_surface, gray, equip_button_rect)
            equip_text = button_font.render(equip_button_text, True, text_color)
            achievements_surface.blit(equip_text, equip_text.get_rect(center=equip_button_rect.center))
            equip_button_rects.append((equip_button_rect, achievement["name"], achievement["reward"]))  # Store equip button rect, achievement name, and reward
 

            # Reward sprite (color rectangle, moved to the right)
            if achievement["reward"] == "light_pink":
                reward_color = (255, 192, 203)  # Light pink
                reward_rect = pygame.Rect(820, row_y, 60, 60)
                pygame.draw.rect(achievements_surface, reward_color, reward_rect)
            elif achievement["reward"] == "light_blue":
                reward_color = (173, 216, 230)  # Light blue
                reward_rect = pygame.Rect(820, row_y, 60, 60)
                pygame.draw.rect(achievements_surface, reward_color, reward_rect)
            elif achievement["reward"] == "yellow":
                reward_color = (255, 255, 0)  # Yellow
                reward_rect = pygame.Rect(820, row_y, 60, 60)
                pygame.draw.rect(achievements_surface, reward_color, reward_rect)
            elif achievement["reward"] == "green":
                reward_color = (0, 255, 0)  # Green
                reward_rect = pygame.Rect(820, row_y, 60, 60)
                pygame.draw.rect(achievements_surface, reward_color, reward_rect)
            elif achievement["reward"] == "black":
                reward_color = (0, 0, 0)  # Black
                reward_rect = pygame.Rect(820, row_y, 60, 60)
                pygame.draw.rect(achievements_surface, reward_color, reward_rect)
            elif achievement["reward"] == "galaxy":
                reward_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\Galaxy_background.png")
                reward_sprite = pygame.transform.scale(reward_sprite, (60, 60))  # Resize galaxy sprite
                achievements_surface.blit(reward_sprite, (820, row_y))
            elif achievement["reward"] == "rainbow":
                reward_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\Rainbow_background.png")
                reward_sprite = pygame.transform.scale(reward_sprite, (60, 60))  # Resize rainbow sprite
                achievements_surface.blit(reward_sprite, (820, row_y))
            elif achievement["reward"] == "food_rain":
                reward_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\food_rain_background.png")
                reward_sprite = pygame.transform.scale(reward_sprite, (60, 60))  # Resize food rain sprite
                achievements_surface.blit(reward_sprite, (820, row_y))
            elif achievement["reward"] == "brown":
                reward_color = (139, 69, 19)  # Brown
                reward_rect = pygame.Rect(820, row_y, 60, 60)
                pygame.draw.rect(achievements_surface, reward_color, reward_rect)
            elif achievement["reward"] == "dark_green":
                reward_color = (0, 100, 0)  # Dark Green
                reward_rect = pygame.Rect(820, row_y, 60, 60)
                pygame.draw.rect(achievements_surface, reward_color, reward_rect)
            elif achievement["reward"] == "poop":
                reward_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\poop_background.png")
                reward_sprite = pygame.transform.scale(reward_sprite, (60, 60))  # Resize poop sprite
                achievements_surface.blit(reward_sprite, (820, row_y))
            elif achievement["reward"] == "party_hat":
                reward_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\party_casper.png")
                reward_sprite = pygame.transform.scale(reward_sprite, (60, 60))  # Resize party hat sprite
                achievements_surface.blit(reward_sprite, (820, row_y))
            elif achievement["reward"] == "cat_ears":
                reward_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\cat_casper.png")
                reward_sprite = pygame.transform.scale(reward_sprite, (60, 60))  # Resize cat ears sprite
                achievements_surface.blit(reward_sprite, (820, row_y))
            elif achievement["reward"] == "caspers_gf":
                reward_sprite = pygame.image.load("C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\question_mark.png" if not achievement["unlocked"] else "C:\\Users\\hatem\\OneDrive\\Desktop\\Sprites\\caspers_gf.png")
                reward_sprite = pygame.transform.scale(reward_sprite, (60, 60))  # Resize sprite
                achievements_surface.blit(reward_sprite, (820, row_y))

            row_y += 80  # Move to the next row for each achievement

        # Blit achievements surface onto screen
        screen.blit(achievements_surface, (0, 0))

        # Draw Main Menu button in achievements screen
        pygame.draw.rect(screen, gray, main_menu_button_rect)
        main_menu_text = submit_button_font.render("Main Menu", True, text_color)
        screen.blit(main_menu_text, main_menu_text.get_rect(center=main_menu_button_rect.center))

        # Event handling for achievements screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle scrolling
                if event.button == 4:  # Scroll up
                    scroll_offset = min(scroll_offset + 20, 0)
                elif event.button == 5:  # Scroll down
                    scroll_offset = max(scroll_offset - 20, window_height - achievements_surface.get_height())

                # Handle button clicks
                if main_menu_button_rect.collidepoint(event.pos):
                    current_screen = "menu"
                    save_player_data()  # Save player data when returning to the menu

                
                if "equipped" not in player_data:
                    player_data["equipped"] = {}  # Initialize if missing

                for rect, achievement_name, reward in equip_button_rects:
                    if rect.collidepoint(event.pos):
                        print(f"Clicked on {achievement_name}, reward: {reward}")  # Debug print statement
                        # Check if the achievement is unlocked before equipping/unequipping
                        if player_data["achievements"].get(achievement_name, False):
                            if reward in ["light_pink", "light_blue", "yellow", "green", "black", "galaxy", "rainbow", "food_rain", "brown", "dark_green", "poop"]:
                                if player_data["equipped"].get("background") == reward:
                                    print(f"Unequipping background: {reward}")  # Debug print statement
                                    del player_data["equipped"]["background"]  # Unequip the background
                                else:
                                    print(f"Equipping background: {reward}")  # Debug print statement
                                    player_data["equipped"]["background"] = reward  # Equip the background
                            elif reward in ["party_hat", "cat_ears", "caspers_gf"]:
                                if player_data["equipped"].get("sprite") == reward:
                                    print(f"Unequipping sprite: {reward}")  # Debug print statement
                                    del player_data["equipped"]["sprite"]  # Unequip the sprite
                                else:
                                    print(f"Equipping sprite: {reward}")  # Debug print statement
                                    player_data["equipped"]["sprite"] = reward  # Equip the sprite

                            save_player_data()  # Save the updated equipped state
                            break

            elif event.type == pygame.MOUSEMOTION:
                # Handle scrolling with mouse motion
                if event.buttons[1]:  # Right mouse button held down
                    scroll_offset += event.rel[1]
                    scroll_offset = max(min(scroll_offset, 0), window_height - achievements_surface.get_height())
               
    elif current_screen == "settings":
        screen.fill(white)

        # Settings title
        settings_title = font.render("Settings", True, black)
        screen.blit(settings_title, (window_width // 2 - settings_title.get_width() // 2, 10))

        # Draw Reset Player Data button
        reset_button_rect = pygame.Rect(window_width // 2 - 150, window_height // 2 - 30, 300, 60)  # Adjusted size
        pygame.draw.rect(screen, gray, reset_button_rect)
        reset_text = button_font.render("Reset Player Data", True, text_color)
        screen.blit(reset_text, reset_text.get_rect(center=reset_button_rect.center))

        # Draw Main Menu button in settings screen
        pygame.draw.rect(screen, gray, main_menu_button_rect)
        main_menu_text = submit_button_font.render("Main Menu", True, text_color)
        screen.blit(main_menu_text, main_menu_text.get_rect(center=main_menu_button_rect.center))

        # Handle button click event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if reset_button_rect.collidepoint(event.pos):
                show_confirmation_popup = True
            elif main_menu_button_rect.collidepoint(event.pos):
                current_screen = "menu"

        # Confirmation popup
        if show_confirmation_popup:
            confirmation_rect = pygame.Rect(window_width // 2 - 200, window_height // 2 - 100, 400, 200)  # Define confirmation_rect
            screen.fill(white, confirmation_rect)  # Clear confirmation popup area

            pygame.draw.rect(screen, white, confirmation_rect)
            pygame.draw.rect(screen, black, confirmation_rect, 2)

            confirmation_text = font.render("Confirm Reset", True, black)
            screen.blit(confirmation_text, confirmation_text.get_rect(center=(confirmation_rect.centerx, confirmation_rect.top + 40)))

            confirm_button_rect = pygame.Rect(confirmation_rect.left + 40, confirmation_rect.bottom - 70, 100, 50)
            cancel_button_rect = pygame.Rect(confirmation_rect.right - 140, confirmation_rect.bottom - 70, 100, 50)

            pygame.draw.rect(screen, gray, confirm_button_rect)
            pygame.draw.rect(screen, gray, cancel_button_rect)

            confirm_text = pygame.font.Font(None, 25).render("Confirm", True, text_color)  # Smaller font size for confirm button
            cancel_text = pygame.font.Font(None, 25).render("Cancel", True, text_color)  # Matching font size for cancel button

            screen.blit(confirm_text, confirm_text.get_rect(center=confirm_button_rect.center))
            screen.blit(cancel_text, cancel_text.get_rect(center=cancel_button_rect.center))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirm_button_rect.collidepoint(event.pos):
                    # Reset player data
                    player_data = {
                        "high_score": 0,
                        "correct_consecutive_guesses": 0,
                        "total_correct_guesses": 0,
                        "incorrect_guesses": 0,
                        "caspers_sprite_taps": 0,  # Include sprite taps
                        "equipped": {},  # Initialize equipped key
                        "achievements": {achievement["name"]: False for achievement in achievements}
                    }
                    with open("player_datas.json", "w") as file:
                        json.dump(player_data, file)
                    high_score = 0
                    correct_consecutive_guesses = 0
                    total_correct_guesses = 0
                    incorrect_guesses = 0
                    caspers_sprite_taps = 0  # Reset sprite taps
                    for achievement in achievements:
                        achievement["unlocked"] = False
                    show_confirmation_popup = False
                    print("Player data has been reset.")

    pygame.display.flip()
    clock.tick(60)
    
# Save player data to file
player_data["high_score"] = high_score
player_data["achievements"] = {achievement["name"]: achievement["unlocked"] for achievement in achievements}
with open("player_datas.json", "w") as file:
    json.dump(player_data, file)

pygame.quit()
