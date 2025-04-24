import pygame
import random

# Initialize Pygame
pygame.init()

# Window settings
WIN_WIDTH, WIN_HEIGHT = 800, 650  # extra height for controls
CELL_SIZE = 10
COLS = WIN_WIDTH // CELL_SIZE
ROWS = WIN_HEIGHT // CELL_SIZE - 5  # reserve 5 rows for buttons

# Colors
WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
GRAY        = (200, 200, 200)
BUTTON_COLOR= (150, 150, 150)
HOVER_COLOR = (170, 170, 170)

# Initialize display and clock
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()
fps = 10  # initial frames per second

# Game state
running = False
grid = [[0]*COLS for _ in range(ROWS)]

# Classic patterns (relative coordinates)
patterns = {
    "Glider": [(0,1),(1,2),(2,0),(2,1),(2,2)],
    "Blinker": [(1,0),(1,1),(1,2)],
    "Toad": [(2,1),(2,2),(2,3),(3,0),(3,1),(3,2)],
}

# Buttons layout
button_font = pygame.font.SysFont("Arial", 18)
buttons = {}
labels = ["Start", "Step", "Clear", "Random", "Speed-", "Speed+", "Glider", "Blinker", "Toad"]
for i, label in enumerate(labels):
    rect = pygame.Rect(10 + i*85, ROWS*CELL_SIZE + 10, 80, 30)
    buttons[label] = rect

def draw_grid():
    screen.fill(WHITE)
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x]:
                pygame.draw.rect(screen, BLACK, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # grid lines
    for x in range(0, WIN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x,0), (x, ROWS*CELL_SIZE))
    for y in range(0, ROWS*CELL_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0,y), (WIN_WIDTH, y))

def count_neighbors_wrap(y, x):
    """Count neighbors with toroidal (wrap-around) boundary."""
    count = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy==dx==0: continue
            ny = (y + dy) % ROWS
            nx = (x + dx) % COLS
            count += grid[ny][nx]
    return count

def update_grid():
    new = [[0]*COLS for _ in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLS):
            n = count_neighbors_wrap(y, x)
            if grid[y][x]:
                new[y][x] = 1 if 2 <= n <= 3 else 0
            else:
                new[y][x] = 1 if n == 3 else 0
    return new

def draw_buttons():
    mx, my = pygame.mouse.get_pos()
    for label, rect in buttons.items():
        color = BUTTON_COLOR
        if rect.collidepoint(mx, my):
            color = HOVER_COLOR
        pygame.draw.rect(screen, color, rect)
        text = label
        if label == "Start":
            text = "Pause" if running else "Start"
        surf = button_font.render(text, True, BLACK)
        screen.blit(surf, (rect.x + 10, rect.y + 5))

def load_pattern(name):
    """Clear grid and place the chosen pattern at center."""
    global grid
    grid = [[0]*COLS for _ in range(ROWS)]
    coords = patterns.get(name, [])
    cy, cx = ROWS//2, COLS//2
    for dy, dx in coords:
        y, x = cy + dy, cx + dx
        if 0 <= y < ROWS and 0 <= x < COLS:
            grid[y][x] = 1

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Toggle cell when clicking on grid (only if paused)
            if y < ROWS*CELL_SIZE and not running:
                gx, gy = x//CELL_SIZE, y//CELL_SIZE
                grid[gy][gx] ^= 1
            else:
                # Check buttons
                for label, rect in buttons.items():
                    if rect.collidepoint(x, y):
                        if label == "Start":
                            running = not running
                        elif label == "Step" and not running:
                            grid = update_grid()
                        elif label == "Clear":
                            grid = [[0]*COLS for _ in range(ROWS)]
                            running = False
                        elif label == "Random":
                            grid = [[random.choice([0,0,0,1]) for _ in range(COLS)] for _ in range(ROWS)]
                        elif label == "Speed+":
                            fps = min(fps + 5, 60)
                        elif label == "Speed-":
                            fps = max(fps - 5, 1)
                        elif label in patterns:
                            load_pattern(label)

    # Auto-update
    if running:
        grid = update_grid()

    # Draw
    draw_grid()
    draw_buttons()
    pygame.display.flip()
    clock.tick(fps)
