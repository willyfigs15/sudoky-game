import pygame

# Initialize pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define cell size and margins
CELL_SIZE = 50
MARGIN = 5

# Define window size
WINDOW_SIZE = [CELL_SIZE * 9 + MARGIN * 10, CELL_SIZE * 9 + MARGIN * 10]

# Initialize window
screen = pygame.display.set_mode(WINDOW_SIZE)

# Load font
font = pygame.font.Font(None, 36)

def draw_grid():
    """Draw the sudoku grid"""
    for row in range(10):
        if row % 3 == 0:
            pygame.draw.line(screen, BLACK, [0, row * CELL_SIZE + row * MARGIN], [WINDOW_SIZE[0], row * CELL_SIZE + row * MARGIN], 2)
            pygame.draw.line(screen, BLACK, [row * CELL_SIZE + row * MARGIN, 0], [row * CELL_SIZE + row * MARGIN, WINDOW_SIZE[1]], 2)
        else:
            pygame.draw.line(screen, BLACK, [0, row * CELL_SIZE + row * MARGIN], [WINDOW_SIZE[0], row * CELL_SIZE + row * MARGIN], 1)
            pygame.draw.line(screen, BLACK, [row * CELL_SIZE + row * MARGIN, 0], [row * CELL_SIZE + row * MARGIN, WINDOW_SIZE[1]], 1)

def draw_puzzle(puzzle):
    """Draw the puzzle on the screen"""
    for row in range(9):
        for col in range(9):
            value = puzzle[row][col]
            if value != 0:
                text = font.render(str(value), True, BLACK, WHITE)
                x = col * CELL_SIZE + (col + 1) * MARGIN
                y = row * CELL_SIZE + (row + 1) * MARGIN
                screen.blit(text, [x + CELL_SIZE // 2 - text.get_width() // 2, y + CELL_SIZE // 2 - text.get_height() // 2])

def generate_sudoku():
    """Generate a 9x9 sudoku puzzle"""
    puzzle = [[0 for x in range(9)] for y in range(9)]
    fill_puzzle(puzzle, 0, 0)
    return puzzle

def fill_puzzle(puzzle, i, j):
    """Fill the puzzle using a backtracking algorithm"""
    if i == 9:
        return True
    if j == 9:
        return fill_puzzle(puzzle, i + 1, 0)
    if puzzle[i][j] != 0:
        return fill_puzzle(puzzle, i, j + 1)
    for value in range(1, 10):
        if is_valid_move(puzzle, i, j, value):
            puzzle[i][j] = value
    if fill_puzzle(puzzle, i, j + 1):
        return True
    puzzle[i][j] = 0
    return False

def is_valid_move(puzzle, i, j, value):
    """Check if it's a valid move to fill in the cell with the given value"""
    # Check row
    for x in range(9):
        if puzzle[i][x] == value:
            return False
                        
    # Check column
    for x in range(9):
        if puzzle[x][j] == value:
            return False

    # Check 3x3 sub-grid
    x0 = (i // 3) * 3
    y0 = (j // 3) * 3
    for x in range(3):
        for y in range(3):
            if puzzle[x0 + x][y0 + y] == value:
                return False

    return True

def play_game(puzzle):
    """Play the sudoku game"""
    running = True
    selected = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // (CELL_SIZE + MARGIN)
                row = pos[1] // (CELL_SIZE + MARGIN)
                if 0 <= row < 9 and 0 <= col < 9:
                    selected = (row, col)
            elif event.type == pygame.KEYDOWN:
                if selected is not None and event.unicode.isdigit() and int(event.unicode) >= 1 and int(event.unicode) <= 9:
                    puzzle[selected[0]][selected[1]] = int(event.unicode)
                    selected = None
        screen.fill(WHITE)
        draw_grid()
        draw_puzzle(puzzle)
        if selected is not None:
            pygame.draw.rect(screen, (200, 200, 200), [selected[1] * CELL_SIZE + (selected[1] + 1) * MARGIN, selected[0] * CELL_SIZE + (selected[0] + 1) * MARGIN, CELL_SIZE, CELL_SIZE], 2)
        pygame.display.update()
    pygame.quit()

# Generate a random sudoku puzzle
puzzle = generate_sudoku()

# Play the game
play_game(puzzle)
