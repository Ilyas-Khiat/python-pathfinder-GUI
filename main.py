import pygame, sys
from maze import generate
from buttons import object, button_i, button_s, clicks
from algos import astar, dij

mainClock = pygame.time.Clock()
pygame.init()

WIDTH = 765
WIDTH_EXTRA = 1215
SCREEN = pygame.display.set_mode((WIDTH_EXTRA, WIDTH))
pygame.display.set_caption('UI')

# spot color
COLOR = {'black': (55, 55, 55),
         'black_locked': (55, 55, 55),
         'blue_green': (16, 213, 146),
         'orange': (255, 191, 103),
         'light_orange': (255, 215, 159),
         'grey': (119, 136, 153),
         'white': (255, 255, 255),
         'red': (255, 108, 70),
         'violet': (220, 79, 137),
         'blue': (92, 77, 177),
         'blue_lite': (151, 140, 212),
         'light_blue': (223, 222, 255)
         }
# speed
time = 0
# notice bar variables
trans = 0
notice_state = [False, False, False]


# check if an algo is selected
def check_vis():
    for i in clicks[1]:
        if i == True:
            return True
    return False


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = COLOR['white']
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_empty(self):
        return self.color == COLOR['white']

    def is_closed(self):
        return self.color == COLOR['blue']

    def is_open(self):
        return self.color == COLOR['blue_lite']

    def is_barrier(self):
        return self.color == COLOR['black']

    def is_start(self):
        return self.color == COLOR['orange']

    def is_end(self):
        return self.color == COLOR['red']

    def is_path(self):
        return self.color == COLOR['violet']

    def reset(self):
        self.color = COLOR['white']

    def make_start(self):
        self.color = COLOR['orange']

    def make_closed(self):
        self.color = COLOR['blue']

    def make_open(self):
        self.color = COLOR['blue_lite']

    def make_barrier(self):
        self.color = COLOR['black']

    def make_end(self):
        self.color = COLOR['red']

    def make_path(self):
        self.color = COLOR['violet']

    def make_locked(self):
        self.color = COLOR['black']

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])


def make_grid(rows, width):
    grid = []
    unit = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, unit, rows)
            grid[i].append(spot)
    return grid


def maze_generator(grid, screen):
    maze = generate()
    for i in range(1, len(maze)):
        for j in range(1, len(maze)):
            if maze[i][j] == -1:
                grid[i][j].make_barrier()
                grid[i][j].draw(screen)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.time.wait(time)


def draw_grid(screen, width, rows, grid):
    unit = width // rows
    for i in range(rows):
        pygame.draw.line(screen, COLOR['light_blue'], (0, i * unit), (width, i * unit))
        for j in range(rows):
            pygame.draw.line(screen, COLOR['light_blue'], (j * unit, 0), (j * unit, width))

    edges = grid[0] + grid[-1] + list(list(zip(*grid))[0] + list(zip(*grid))[-1])
    for spot in edges:
        spot.make_locked()


# interactive ui elements___________________________________________________________________________________________
notice = (pygame.image.load('ui elements/ok.png'), pygame.image.load('ui elements/notice up.png'))

vis_notif = object(1055, 664,
                   (pygame.image.load('ui elements/vis off.png'), pygame.image.load('ui elements/vis on.png')))

# maze button generator______________________________________________________________________________________________
maze_but = button_i(790, 650, 158, 41, (
    pygame.image.load('ui elements/but maze1.png'), pygame.image.load('ui elements/but maze2.png'),
    pygame.image.load('ui elements/but maze3.png')))

# speed buttons______________________________________________________________________________________________________
slow_but = button_s(820, 455, 85, 40, (
    pygame.image.load('ui elements/slow1.png'), pygame.image.load('ui elements/slow2.png'),
    pygame.image.load('ui elements/slow3.png')), 0, 0)
average_but = button_s(948, 455, 85, 40, (
    pygame.image.load('ui elements/average1.png'), pygame.image.load('ui elements/average2.png'),
    pygame.image.load('ui elements/average3.png')), 1, 0)
fast_but = button_s(1076, 455, 85, 40, (
    pygame.image.load('ui elements/fast1.png'), pygame.image.load('ui elements/fast2.png'),
    pygame.image.load('ui elements/fast3.png')), 2, 0)

# algo buttons________________________________________________________________________________________________________
astar_but = button_s(790, 175, 200, 40, (
    pygame.image.load('ui elements/a1.png'), pygame.image.load('ui elements/a2.png'),
    pygame.image.load('ui elements/a3.png')), 0, 1)
dij_but = button_s(1005, 175, 200, 40, (
    pygame.image.load('ui elements/dj1.png'), pygame.image.load('ui elements/dj2.png'),
    pygame.image.load('ui elements/dj3.png')), 1, 1)
DFS_but = button_s(790, 230, 200, 40, (
    pygame.image.load('ui elements/DFS1.png'), pygame.image.load('ui elements/DFS2.png'),
    pygame.image.load('ui elements/DFS3.png')), 2, 1)
BFS_but = button_s(790, 285, 200, 40, (
    pygame.image.load('ui elements/BFS1.png'), pygame.image.load('ui elements/BFS2.png'),
    pygame.image.load('ui elements/BFS3.png')), 3, 1)
BF_but = button_s(790, 340, 200, 40, (
    pygame.image.load('ui elements/bf1.png'), pygame.image.load('ui elements/bf2.png'),
    pygame.image.load('ui elements/bf3.png')), 4, 1)
S_but = button_s(1005, 230, 200, 40, (
    pygame.image.load('ui elements/S1.png'), pygame.image.load('ui elements/S2.png'),
    pygame.image.load('ui elements/S3.png')), 5, 1)
CS_but = button_s(1005, 285, 200, 40, (
    pygame.image.load('ui elements/CS1.png'), pygame.image.load('ui elements/CS2.png'),
    pygame.image.load('ui elements/CS3.png')), 6, 1)
BS_but = button_s(1005, 340, 200, 40, (
    pygame.image.load('ui elements/BS1.png'), pygame.image.load('ui elements/BS2.png'),
    pygame.image.load('ui elements/BS3.png')), 7, 1)


def clear_path(grid):
    for row in grid:
        for spot in row:
            if spot.is_closed() or spot.is_path() or spot.is_open():
                spot.reset()


def draw(screen, grid, width, rows):
    for row in grid:
        for spot in row:
            if spot.is_empty:
                spot.draw(screen)

    draw_grid(screen, width, rows, grid)
    pygame.draw.rect(screen, COLOR['blue'], (765, 0, 1215 - 765, 765))
    screen.blit(pygame.image.load('ui elements/Pathfinder.png'), (790, 30))
    screen.blit(pygame.image.load('ui elements/Visualization.png'), (790, 75))
    screen.blit(pygame.image.load('ui elements/Speed.png'), (790, 430))
    screen.blit(pygame.image.load('ui elements/Algorithms.png'), (790, 137))
    screen.blit(pygame.image.load('ui elements/description.png'), (820, 530))

    for row in grid:
        for spot in row:
            if spot.is_barrier():
                spot.draw(screen)
            if spot.is_start():
                spot.draw(screen)
            if spot.is_end():
                spot.draw(screen)
            if spot.is_path():
                spot.draw(screen)
            if spot.is_closed() or spot.is_open():
                spot.draw(screen)

    maze_but.draw_button(screen)

    slow_but.draw_button(screen)
    average_but.draw_button(screen)
    fast_but.draw_button(screen)

    astar_but.draw_button(screen)
    dij_but.draw_button(screen)
    BFS_but.draw_button(screen)
    BF_but.draw_button(screen)
    DFS_but.draw_button(screen)
    S_but.draw_button(screen)
    CS_but.draw_button(screen)
    BS_but.draw_button(screen)

    vis_notif.draw(screen)
    if notice_state[2]:
        screen.blit(notice[1], (765, 735 - trans))
    else:
        screen.blit(notice[0], (765, 735 - trans))

    pygame.display.update()

# calculte the row and column pos in the grid
def get_clicked_pos(pos, width, rows):
    unit = width // rows
    x, y = pos
    return x // unit, y // unit


def main(screen, width):
    global time, trans, notice_state
    rows = 51
    grid = make_grid(rows, width)

    start = None
    end = None

    started = False
    run = True
    clicks[fast_but.m][fast_but.n] = True

    l_move = [25] + [i ** 2 for i in range(9, 0, -1)]

    screen.fill(COLOR['white'])

    while run:
        draw(screen, grid, width, rows)

        if l_move != [] and notice_state[0] == True:
            trans += l_move.pop(0)

        elif l_move != [] and notice_state[1] == True:
            trans -= l_move.pop(0)

        else:
            notice_state[0] = False
            notice_state[1] = False
            l_move = [25] + [i ** 2 for i in range(9, 0, -1)]

        if maze_but.click:
            grid = make_grid(rows, width)
            draw(screen, grid, width, rows)
            maze_generator(grid, screen)
            start, end = grid[1][1], grid[rows - 2][rows - 2]
            start.make_start()
            end.make_end()
            maze_but.click = False

        if clicks[slow_but.m][slow_but.n]:
            time = 100
        if clicks[average_but.m][average_but.n]:
            time = 20
        if clicks[fast_but.m][fast_but.n]:
            time = 0

        if start and end and check_vis():
            vis_notif.state = -1
        else:
            vis_notif.state = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and notice_state[2] == False:
                    notice_state[0] = True
                    notice_state[2] = True

                if event.key == pygame.K_DOWN and notice_state[2]:
                    notice_state[1] = True
                    notice_state[2] = False

                if event.key == pygame.K_c:
                    start, end = None, None
                    grid = make_grid(rows, width)

                if event.key == pygame.K_s and start and end:
                    clear_path(grid)
                    draw(screen, grid, width, rows)
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    if clicks[astar_but.m][astar_but.n]:
                        astar(lambda: draw(screen, grid, width, rows), grid, start, end, time)
                    if clicks[dij_but.m][dij_but.n]:
                        dij(lambda: draw(screen, grid, width, rows), grid, start, end, time)

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 750:
                    continue
                row, col = get_clicked_pos(pos, width, rows)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 750:
                    continue
                row, col = get_clicked_pos(pos, width, rows)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    clear_path(grid)
                    draw(screen, grid, width, rows)
                    start = None
                elif spot == end:
                    clear_path(grid)
                    draw(screen, grid, width, rows)
                    end = None

        pygame.display.update()
        mainClock.tick(60)


main(SCREEN, WIDTH)
pygame.quit()
