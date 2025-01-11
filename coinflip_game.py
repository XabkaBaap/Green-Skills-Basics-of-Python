import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 150, 250)
GREEN = (50, 250, 100)
RED = (250, 50, 50)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Coin Flip Gambling Game")

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)

# Game variables
choices = ["Heads", "Tails"]
result = None
user_choice = None
message = ""
balance = 1000  # Starting balance
bet = 100  # Default bet
flipping = False
friends = ["Arya", "Himanshu", "Ameen"]  # Friends list
fake_users = []  # List of fake winnings/losses
marquee_speed = 2  # Speed of the scrolling marquee
marquee_timer = 0  # Timer to control message generation
marquee_gap = 150  # Horizontal gap between fake user messages

# Button dimensions
button_width, button_height = 150, 50
heads_button = pygame.Rect(100, 350, button_width, button_height)
tails_button = pygame.Rect(350, 350, button_width, button_height)
increase_bet_button = pygame.Rect(450, 50, 40, 40)
decrease_bet_button = pygame.Rect(400, 50, 40, 40)

# Function to draw text on the screen
def draw_text(text, font, color, x, y, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# Function to simulate coin flip animation
def coin_flip_animation():
    global result, flipping
    flipping = True
    flip_frames = 20  # Number of frames for animation
    delay = 50  # Delay in milliseconds between frames

    for _ in range(flip_frames):
        temp_result = random.choice(choices)  # Show random side
        screen.fill(WHITE)
        draw_ui(temp_result=temp_result)
        pygame.display.flip()
        pygame.time.delay(delay)

    # Final result
    result = random.choice(choices)
    flipping = False

# Function to generate fake user activity
def generate_fake_user_activity():
    friend = random.choice(friends)
    fake_amount = random.randint(100, 10_000_000)  # Amount between ₹100 and ₹10,000,000
    fake_result = random.choice(["won", "lost"])
    fake_color = GREEN if fake_result == "won" else RED

    # Start messages at a position spaced from the previous one
    start_x = SCREEN_WIDTH + marquee_gap * len(fake_users)
    fake_users.append({
        "text": f"{friend} {fake_result} ₹{fake_amount:,}!",  # Add ₹ symbol and commas for formatting
        "color": fake_color,
        "x": start_x
    })

# Function to draw the UI
def draw_ui(temp_result=None):
    # Draw balance and bet
    draw_text(f"Balance: ₹{balance:,.0f}", font, BLACK, 50, 50)  # Format with ₹ symbol and commas
    draw_text(f"Bet: ₹{bet:,.0f}", font, BLACK, 50, 100)  # Format with ₹ symbol and commas

    # Draw betting buttons
    pygame.draw.rect(screen, GREEN, increase_bet_button)
    pygame.draw.rect(screen, RED, decrease_bet_button)
    draw_text("+", font, WHITE, increase_bet_button.centerx, increase_bet_button.centery, center=True)
    draw_text("-", font, WHITE, decrease_bet_button.centerx, decrease_bet_button.centery, center=True)

    # Draw title and buttons
    draw_text("Coin Flip Gambling Game", large_font, BLACK, SCREEN_WIDTH // 2, 150, center=True)
    if temp_result:
        draw_text(temp_result, large_font, BLUE, SCREEN_WIDTH // 2, 200, center=True)
    else:
        draw_text("Choose Heads or Tails:", font, BLACK, 50, 200)

    # Draw Heads and Tails buttons
    pygame.draw.rect(screen, BLUE, heads_button)
    pygame.draw.rect(screen, GREEN, tails_button)
    draw_text("Heads", font, WHITE, heads_button.centerx, heads_button.centery, center=True)
    draw_text("Tails", font, WHITE, tails_button.centerx, tails_button.centery, center=True)

    # Display result and message if any
    if result and not flipping:
        draw_text(f"Result: {result}", font, BLACK, 50, 250)
    if message and not flipping:
        draw_text(message, font, RED if "lost" in message else GREEN, 50, 300)

    # Draw scrolling marquee (menu for fake users)
    pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))  # Marquee background
    y_position = SCREEN_HEIGHT - 40  # Fixed vertical position for marquee
    for fake_user in fake_users:
        draw_text(fake_user["text"], font, fake_user["color"], fake_user["x"], y_position)

# Main game loop
def main():
    global result, user_choice, message, balance, bet, marquee_timer, fake_users
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Generate fake user activity periodically
        marquee_timer += 1
        if marquee_timer >= 100:  # Adjust this value to control the frequency
            generate_fake_user_activity()
            marquee_timer = 0

        # Update fake user positions for marquee scrolling
        for fake_user in fake_users[:]:
            fake_user["x"] -= marquee_speed  # Move left
            if fake_user["x"] < -300:  # Remove when fully off screen
                fake_users.remove(fake_user)

        # Draw UI
        draw_ui()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not flipping:
                if heads_button.collidepoint(event.pos):
                    user_choice = "Heads"
                    if bet <= balance:
                        coin_flip_animation()
                        check_result()
                    else:
                        message = "Insufficient balance!"
                elif tails_button.collidepoint(event.pos):
                    user_choice = "Tails"
                    if bet <= balance:
                        coin_flip_animation()
                        check_result()
                    else:
                        message = "Insufficient balance!"
                elif increase_bet_button.collidepoint(event.pos):
                    if bet + 10 <= balance:
                        bet += 10
                elif decrease_bet_button.collidepoint(event.pos):
                    if bet - 10 >= 10:
                        bet -= 10

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

# Function to check if the user guessed correctly
def check_result():
    global message, balance
    if user_choice == result:
        balance += bet  # Win: Double the bet amount
        message = f"You guessed it right! Your balance is now ₹{balance:,.0f}."  # Format with ₹ symbol
    else:
        balance -= bet  # Lose: Deduct the bet amount
        message = f"Oops, you guessed wrong! Your balance is now ₹{balance:,.0f}."  # Format with ₹ symbol

    if balance < 10:
        message = "Game Over! Insufficient balance! Restart to play again."

# Run the game
if __name__ == "__main__":
    main()
