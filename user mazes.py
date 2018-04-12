import pygame
import os

yes_synonyms = ["y", "yes", "sure", "okay", "fine", "affirmative", "all right", "very well", "of course", "by all means", "certainly", "absolutely", "indeed", "right", "agreed", "roger", "ok", "yeah", "yep", "yup", "okey-dokey", "yea", "aye"]

white = (255,255,255)
black = (0,0,0)
purple = (255,0,255)
blue = (0,0,255)

maze_size = 0
while not (maze_size >= 5):
    maze_size = input("How big do you want it to be? ")
    try:
        maze_size = int(maze_size)
        if not maze_size >= 5:
            print("Please make it at least 5!")
            pass
    except ValueError:
        print("Please make it an integer.")
        maze_size = 0

maze = []

clicking_wall = False

for y in range(maze_size):
    row = []
    for x in range(maze_size):
        row.append("#")
    maze.append(row)

path = os.path.dirname(__file__)

if not os.path.exists(os.path.join(path, "mazes")):
    os.makedirs(os.path.join(path, "mazes"))

tile_size = int(600/maze_size)

pygame.init()
size = [maze_size*tile_size,maze_size*tile_size]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Fun!")

click_phase = 0

def draw(board):
    screen.fill(white)
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == ".":
                pygame.draw.rect(screen, black, [x*tile_size,y*tile_size,tile_size,tile_size])
            elif board[y][x] == "@":
                pygame.draw.rect(screen, blue, [x*tile_size,y*tile_size,tile_size,tile_size])
            elif board[y][x] == "&":
                pygame.draw.rect(screen, purple, [x*tile_size,y*tile_size,tile_size,tile_size])
    pygame.display.update()

def save_maze():
    global click_phase
    if click_phase == 0:
        click_phase = 1
        print("Select the start position.")
        return False
    if click_phase != 3:
        return False
    draw(maze)
    save_name = ""

    if not input("Are you sure it's ready? ") in yes_synonyms:
        return False

    while len(save_name) == 0:
        save_name = input("What do you want to save it as? (Don't include the extension) ")

    save_name = os.path.join(path, "mazes", save_name + ".txt")

    file = open(save_name, "w+")

    file.write("width: " + str(maze_size) + "\n")

    temp_board = maze
    for row in temp_board:
        row = str(row)
        row = row.replace("[","")
        row = row.replace("]","")
        row = row.replace("'","")
        row = row.replace(" ","")
        file.write(row + "\n")
    return True

def click_board():
    global maze
    global click_phase
    global clicking_wall
    mouse_coords = pygame.mouse.get_pos()
    clicked_coords = [int(mouse_coords[0]/tile_size),int(mouse_coords[1]/tile_size)]
    if maze[clicked_coords[1]][clicked_coords[0]] == "#":
        clicking_wall = False
        if click_phase == 0:
            pass
            #maze[clicked_coords[1]][clicked_coords[0]] = "."
        elif click_phase == 1:
            maze[clicked_coords[1]][clicked_coords[0]] = "&"
            click_phase = 2
            print("Select the end point.")
        elif click_phase == 2:
            maze[clicked_coords[1]][clicked_coords[0]] = "@"
            click_phase = 3
            save_maze()
    elif maze[clicked_coords[1]][clicked_coords[0]] == ".":
        clicking_wall = True
        #maze[clicked_coords[1]][clicked_coords[0]] = "#"
        if click_phase != 0:
            for y in range(maze_size):
                for x in range(maze_size):
                    if maze[y][x] in "@&":
                        maze[y][x] = "#"
            click_phase = 0
    elif maze[clicked_coords[1]][clicked_coords[0]] == "&":
        maze[clicked_coords[1]][clicked_coords[0]] = "#"
        click_phase = 1
        if click_phase == 3:
            for y in range(maze_size):
                for x in range(maze_size):
                    if maze[y][x] == "@":
                        maze[y][x] = "#"
        print("Select the start position.")
    elif maze[clicked_coords[1]][clicked_coords[0]] == "@":
        maze[clicked_coords[1]][clicked_coords[0]] = "#"
        click_phase = 2
        print("Select the end point.")

def click_handler():
    global clicking_wall
    mouse_coords = pygame.mouse.get_pos()
    clicked_coords = [int(mouse_coords[0]/tile_size),int(mouse_coords[1]/tile_size)]
    if pygame.mouse.get_pressed()[0] and click_phase == 0:
        if clicking_wall:
            maze[clicked_coords[1]][clicked_coords[0]] = "#"
        else:
            maze[clicked_coords[1]][clicked_coords[0]] = "."

# Simple event handler, test for quitting and saving
def event_handler(events):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key == pygame.K_s and click_phase == 0:
                save_maze()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_board()

while True:
    click_handler()
    event_handler(pygame.event.get())
    draw(maze)
