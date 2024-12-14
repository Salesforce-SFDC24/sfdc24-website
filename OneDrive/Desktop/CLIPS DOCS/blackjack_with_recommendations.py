import pygame
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack - Recommendations and Probabilities")

# Colors
TABLE_GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 149, 237)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Card deck
CARD_SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
CARD_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Game variables
player_cash = 200
min_bet = 40
bet = min_bet
player_hand = []
dealer_hand = []
deck = []
game_over = False
round_result = None  # Tracks the result of the round (e.g., "Player Wins")

# Constants for card dimensions
CARD_WIDTH = 80
CARD_HEIGHT = 120

# Load card images
CARD_IMAGES = {}
for value in CARD_VALUES:
    for suit in CARD_SUITS:
        file_name = f"{value}_of_{suit}.png".lower()
        path = os.path.join("cards", file_name)
        try:
            image = pygame.image.load(path)
            CARD_IMAGES[(value, suit)] = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        except pygame.error:
            print(f"Error: Could not load image for {file_name}. Please check the file.")
            exit()

# Load and resize the card back image
CARD_BACK = pygame.image.load(os.path.join("cards", "back.png"))
CARD_BACK = pygame.transform.scale(CARD_BACK, (CARD_WIDTH, CARD_HEIGHT))

# Helper functions
def create_deck():
    """Create a shuffled deck of cards."""
    deck = [(value, suit) for value in CARD_VALUES for suit in CARD_SUITS]
    random.shuffle(deck)
    return deck

def calculate_hand_value(hand):
    """Calculate the value of a Blackjack hand."""
    value, aces = 0, 0
    for card in hand:
        card_value = card[0]
        if card_value in 'JQK':
            value += 10
        elif card_value == 'A':
            value += 11
            aces += 1
        else:
            value += int(card_value)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def calculate_probability(player_value, dealer_value):
    """Estimate the probability of winning based on player's hand."""
    if player_value > 21:
        return 0.0
    elif player_value == 21:
        return 0.9  # High probability for blackjack
    elif dealer_value > 21:
        return 1.0
    elif player_value >= dealer_value:
        return 0.6 + (player_value - dealer_value) * 0.05
    else:
        return 0.4 - (dealer_value - player_value) * 0.05

def resolve_game():
    """Determine the winner and update balances."""
    global round_result, player_cash, game_over
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if player_value > 21:
        round_result = "Player Busts! Dealer Wins!"
        player_cash -= bet
    elif dealer_value > 21 or player_value > dealer_value:
        round_result = "Player Wins!"
        player_cash += bet
    elif player_value < dealer_value:
        round_result = "Dealer Wins!"
        player_cash -= bet
    else:
        round_result = "It's a Tie!"

    game_over = True

def draw_card(deck, hand):
    """Draw a card from the deck."""
    hand.append(deck.pop())

def draw_text(text, x, y, color=WHITE, center=False):
    """Draw text on the screen."""
    surface = font.render(text, True, color)
    if center:
        rect = surface.get_rect(center=(x, y))
        screen.blit(surface, rect)
    else:
        screen.blit(surface, (x, y))

def draw_buttons():
    """Draw clickable buttons for Hit, Stand, Restart, and Quit."""
    mouse = pygame.mouse.get_pos()
    buttons = {}

    # Hit Button
    hit_button = pygame.Rect(150, 650, 100, 40)
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR if hit_button.collidepoint(mouse) else BUTTON_COLOR, hit_button)
    draw_text("Hit", 200, 670, center=True)
    buttons['hit'] = hit_button

    # Stand Button
    stand_button = pygame.Rect(300, 650, 100, 40)
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR if stand_button.collidepoint(mouse) else BUTTON_COLOR, stand_button)
    draw_text("Stand", 350, 670, center=True)
    buttons['stand'] = stand_button

    # Restart Button
    restart_button = pygame.Rect(700, 650, 100, 40)
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR if restart_button.collidepoint(mouse) else BUTTON_COLOR, restart_button)
    draw_text("Restart", 750, 670, center=True)
    buttons['restart'] = restart_button

    # Quit Button
    quit_button = pygame.Rect(850, 650, 100, 40)
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR if quit_button.collidepoint(mouse) else BUTTON_COLOR, quit_button)
    draw_text("Quit", 900, 670, center=True)
    buttons['quit'] = quit_button

    return buttons

def draw_hands():
    """Draw the dealer's and player's hands."""
    # Dealer's hand
    draw_text("Dealer Cards", SCREEN_WIDTH // 2, 50, center=True)
    for i, card in enumerate(dealer_hand):
        if i == 0 and not game_over:  # Hide dealer's first card
            screen.blit(CARD_BACK, (SCREEN_WIDTH // 2 - (CARD_WIDTH + 20) * len(dealer_hand) // 2 + i * (CARD_WIDTH + 20), 100))
        else:
            screen.blit(CARD_IMAGES[card], (SCREEN_WIDTH // 2 - (CARD_WIDTH + 20) * len(dealer_hand) // 2 + i * (CARD_WIDTH + 20), 100))

    # Player's hand
    draw_text("Player Cards", SCREEN_WIDTH // 2, 300, center=True)
    for i, card in enumerate(player_hand):
        screen.blit(CARD_IMAGES[card], (SCREEN_WIDTH // 2 - (CARD_WIDTH + 20) * len(player_hand) // 2 + i * (CARD_WIDTH + 20), 350))

def draw_status():
    """Display cash, bet, recommendations, and probabilities."""
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    # Cash and Bet
    draw_text(f"Cash: ${player_cash}", 50, SCREEN_HEIGHT - 200)
    draw_text(f"Bet: ${bet}", 50, SCREEN_HEIGHT - 160)

    # Recommendations
    if player_value > 21:
        recommendation = "Bust! Restart or Quit."
    elif player_value <= 16:
        recommendation = "Recommendation: Hit"
    else:
        recommendation = "Recommendation: Stand"
    draw_text(recommendation, SCREEN_WIDTH // 2, 550, center=True)

    # Probability of Winning
    probability = calculate_probability(player_value, dealer_value)
    draw_text(f"Win Probability: {int(probability * 100)}%", SCREEN_WIDTH // 2, 580, center=True)

    # Game Outcome
    if game_over and round_result:
        draw_text(round_result, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, color=RED, center=True)

def reset_game():
    """Reset the game for a new round."""
    global deck, player_hand, dealer_hand, game_over, round_result, bet
    deck = create_deck()
    player_hand = []
    dealer_hand = []
    draw_card(deck, player_hand)
    draw_card(deck, player_hand)
    draw_card(deck, dealer_hand)
    game_over = False
    round_result = None

# Initialize game
reset_game()

# Game loop
running = True
while running:
    screen.fill(TABLE_GREEN)  # Background

    # Draw elements
    draw_hands()
    draw_status()
    buttons = draw_buttons()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                if buttons['hit'].collidepoint(event.pos):
                    draw_card(deck, player_hand)
                    if calculate_hand_value(player_hand) > 21:
                        resolve_game()
                elif buttons['stand'].collidepoint(event.pos):
                    while calculate_hand_value(dealer_hand) < 17:
                        draw_card(deck, dealer_hand)
                    resolve_game()
            elif buttons['restart'].collidepoint(event.pos):
                reset_game()
            elif buttons['quit'].collidepoint(event.pos):
                running = False

    pygame.display.flip()

pygame.quit()
