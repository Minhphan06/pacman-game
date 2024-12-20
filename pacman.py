import pygame
import random

# Constants
TILE_SIZE = 32
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Maze Layout
maze = [
    "###################",
    "#........#........#",
    "#.###.###.#.###.###",
    "#.#...............#",
    "#.#.###.#####.###.#",
    "#.....#...#...#...#",
    "###################",
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Game")
clock = pygame.time.Clock()

# Pac-Man Class
class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = TILE_SIZE

    def move(self, dx, dy, maze):
        # Check for walls before moving
        if maze[(self.y + dy) // TILE_SIZE][(self.x + dx) // TILE_SIZE] != "#":
            self.x += dx
            self.y += dy

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2), TILE_SIZE // 2)

# Ghost Class
class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = TILE_SIZE

    def move_randomly(self, maze):
        dx, dy = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])  # Up, Down, Left, Right
        if maze[(self.y + dy * self.speed) // TILE_SIZE][(self.x + dx * self.speed) // TILE_SIZE] != "#":
            self.x += dx * self.speed
            self.y += dy * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2), TILE_SIZE // 2)

# Function to Draw Maze
def draw_maze(screen, maze):
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            x = col_idx * TILE_SIZE
            y = row_idx * TILE_SIZE
            if cell == "#":
                pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
            elif cell == ".":
                pygame.draw.circle(screen, WHITE, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), 5)

# Check Collision
def check_collision(pacman, ghost):
    return pacman.x == ghost.x and pacman.y == ghost.y

# Main Function
def main():
    running = True
    score = 0

    # Initialize Pac-Man and Ghosts
    pacman = PacMan(TILE_SIZE, TILE_SIZE)
    ghosts = [Ghost(TILE_SIZE * 10, TILE_SIZE * 2), Ghost(TILE_SIZE * 15, TILE_SIZE * 4)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Pac-Man Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pacman.move(0, -pacman.speed, maze)
        if keys[pygame.K_DOWN]:
            pacman.move(0, pacman.speed, maze)
        if keys[pygame.K_LEFT]:
            pacman.move(-pacman.speed, 0, maze)
        if keys[pygame.K_RIGHT]:
            pacman.move(pacman.speed, 0, maze)

        # Ghost Movement
        for ghost in ghosts:
            ghost.move_randomly(maze)

        # Check for Collisions
        for ghost in ghosts:
            if check_collision(pacman, ghost):
                print("Game Over!")
                running = False

        # Collect Dots
        if maze[pacman.y // TILE_SIZE][pacman.x // TILE_SIZE] == ".":
            score += 1
            maze[pacman.y // TILE_SIZE] = maze[pacman.y // TILE_SIZE][:pacman.x // TILE_SIZE] + " " + maze[pacman.y // TILE_SIZE][pacman.x // TILE_SIZE + 1:]

        # Check for Win
        if not any("." in row for row in maze):
            print("You Win!")
            running = False

        # Drawing
        screen.fill(BLACK)
        draw_maze(screen, maze)
        pacman.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    print("Final Score:", score)

# Run the Game
if __name__ == "__main__":
    main()
