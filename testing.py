import numpy as np
import pygame
import random
import sys
import matplotlib.pyplot as plt

############### Set up the game environment #####################
#Initialize Pygame
pygame.init()

# Game variables


screen_width = 400
screen_height = 600
bird_y = screen_height // 2
bird_x = 50
gravity = 0.25
bird_movement = 0
game_active = True
pipe_heights = [200, 300, 400]  # Example heights
pipe_frequency = 1500  # Milliseconds
last_pipe = pygame.time.get_ticks()

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Load images
bird_image = pygame.image.load('imgs/bird1.png').convert_alpha()
background_image = pygame.image.load('imgs/bg.png').convert_alpha()

# Main game loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and game_active:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 6

    # Bird movement
    #bird_movement += gravity
    #bird_y += bird_movement

    # Display background
    screen.blit(background_image, (0, 0))

    # Display bird
    screen.blit(bird_image, (bird_x, int(bird_y)))

    # Update the display
    pygame.display.update()

    # Frame rate
    clock.tick(60)









################ Define the Q-table #####################
# Q-learning parameters
learning_rate = 0.1
discount_factor = 0.99
exploration_rate = 1.0
max_exploration_rate = 1.0
min_exploration_rate = 0.01
exploration_decay_rate = 0.001

# Q-table initialization
action_space_size = 2  # Flap or do nothing
state_space_size = 100  # Example state space size
q_table = np.zeros((state_space_size, action_space_size)) # Initialize Q-table with zeros

# Example of updating the Q-table
def update_q_table(state, new_state, action, reward):
    max_future_q = np.max(q_table[new_state])
    current_q = q_table[state, action]
    
    # Q-learning formula
    new_q = (1 - learning_rate) * current_q + learning_rate * (reward + discount_factor * max_future_q)
    q_table[state, action] = new_q

# Exploration vs Exploitation
def choose_action(state):
    if np.random.uniform(0, 1) > exploration_rate:
        action = np.argmax(q_table[state])
    else:
        action = np.random.randint(0, action_space_size)
    return action    

################ Define the state and action spaces #####################

################ Implement the Q-learning algorithm #####################

################ Train the Q-learning agent #####################

################ Test the trained agent #####################
