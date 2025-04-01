import pygame
import random

# Initialize Pygame
pygame.init()

# Window settings
WIN_WIDTH, WIN_HEIGHT = 800, 600
CELL_SIZE = 10
COLS = WIN_WIDTH // CELL_SIZE
ROWS = (WIN_HEIGHT - 50) // CELL_SIZE  # 50px for controls

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BUTTON_COLOR = (150, 150, 150)

# Initialize display
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

# Game state
running = False
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# UI Elements
button_font = pygame.font.SysFont("Arial", 18)
buttons = {
    "start": pygame.Rect(20, WIN_HEIGHT-40, 80, 30),
    "clear": pygame.Rect(120, WIN_HEIGHT-40, 80, 30),
    "random": pygame.Rect(220, WIN_HEIGHT-40, 80, 30)
}

def draw_grid():
    """Draw cells and grid lines"""
    screen.fill(WHITE)
    
    # Draw living cells
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x]:
                rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect)
    
    # Draw grid lines
    for x in range(0, WIN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, ROWS*CELL_SIZE))
    for y in range(0, ROWS*CELL_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIN_WIDTH, y))

def count_neighbors(y, x):
    """Count living neighbors"""
    count = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == dx == 0:
                continue
            ny, nx = y + dy, x + dx
            if 0 <= ny < ROWS and 0 <= nx < COLS:
                count += grid[ny][nx]
    return count

def update_grid():
    """Calculate next generation"""
    new_grid = [[0]*COLS for _ in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLS):
            neighbors = count_neighbors(y, x)
            if grid[y][x]:
                new_grid[y][x] = 1 if 2 <= neighbors <= 3 else 0
            else:
                new_grid[y][x] = 1 if neighbors == 3 else 0
    return new_grid

def draw_buttons():
    """Draw control buttons"""
    for btn, rect in buttons.items():
        pygame.draw.rect(screen, BUTTON_COLOR, rect)
        label = "Pause" if running and btn == "start" else btn.capitalize()
        text = button_font.render(label, True, BLACK)
        screen.blit(text, (rect.x+10, rect.y+5))

# Main loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            
            # Grid interaction
            if y < ROWS*CELL_SIZE and not running:
                grid_x = x // CELL_SIZE
                grid_y = y // CELL_SIZE
                if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
                    grid[grid_y][grid_x] ^= 1  # Toggle cell
            
            # Button handling
            elif buttons["start"].collidepoint(x, y):
                running = not running
            elif buttons["clear"].collidepoint(x, y):
                grid = [[0]*COLS for _ in range(ROWS)]
                running = False
            elif buttons["random"].collidepoint(x, y):
                grid = [[random.choice([0, 0, 0, 1]) for _ in range(COLS)] for _ in range(ROWS)]

    # Update grid
    if running:
        grid = update_grid()

    # Draw everything
    draw_grid()
    draw_buttons()
    pygame.display.flip()
    clock.tick(10)