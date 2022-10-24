import random

def initiate_maze():
    maze = []
    for i in range(51):
        row = []
        for j in range(51):
            row.append(0)
        maze.append(row)

    for j in range(0, len(maze), 2):
        for i in range(len(maze)):
            maze[i][j] = -1
            if i % 2 == 0:
                try:
                    maze[i][j + 1] = -1
                except:
                    continue

    values = [i for i in range(1, 626)]

    for i in range(1, len(maze) - 1):
        for j in range(1, len(maze) - 1):
            if maze[i][j] == 0:
                maze[i][j] = values.pop(0)
    return maze


def is_finished(grid):
    for i in range(1, 50, 2):
        for j in range(1, 50, 2):
            if grid[i][j] != grid[1][1]:
                return False
    return True


def generate():
    maze = initiate_maze()
    while is_finished(maze) == False:
        x = random.randint(0, 48) + 1

        if x % 2 == 0:
            y = random.randint(0, 24) * 2 + 1
        else:
            y = random.randint(0, 23) * 2 + 2

        if maze[x - 1][y] == -1:
            cell1, cell2 = maze[x][y - 1], maze[x][y + 1]
        else:
            cell1, cell2 = maze[x - 1][y], maze[x + 1][y]

        if cell1 != cell2:
            maze[x][y] = 0
            for i in range(1, 50, 2):
                for j in range(1, 50, 2):
                    if maze[i][j] == cell2:
                        maze[i][j] = cell1

    for i in range(1, 50):
        x = random.randint(0, 48) + 1

        if x % 2 == 0:
            y = random.randint(0, 24) * 2 + 1
        else:
            y = random.randint(0, 23) * 2 + 2
        maze[x][y] = 0
    return maze
