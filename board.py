import pygame
from random import randint


pygame.font.init()
cell_size = 50
offset_ = 900
myfont = pygame.font.SysFont('Arial', (cell_size*3)//5)


class Cell:
    def __init__(self, pos, random_mine, offset):
        self.visible = False
        self.mine = random_mine
        self.show_mine = False
        self.size = cell_size
        self.color = (187, 223, 209)
        self.pos = pos
        self.label = False
        self.mine_counter = 0
        self.font_color = (0, 0, 0)
        self.marked = False
        self.explosion = False
        self.offset = offset

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, self.color,
                             (self.pos[0] + self.offset, self.pos[1] + self.offset, self.size, self.size))
        elif self.marked:
            pygame.draw.rect(surface, (150, 50, 50),
                             (self.pos[0] + self.offset, self.pos[1] + self.offset, self.size, self.size))
        else:
            pygame.draw.rect(surface, (144, 191, 173),
                             (self.pos[0] + self.offset, self.pos[1] + self.offset, self.size, self.size))
        if self.show_mine and self.mine:
            pygame.draw.circle(surface, (10, 10, 10),
                               (self.pos[0]+cell_size//2 + self.offset, self.pos[1]+cell_size//2 + self.offset), cell_size//2)
        if self.explosion:
            pygame.draw.circle(surface, (255, 10, 10),
                               (self.pos[0]+cell_size//2 + self.offset, self.pos[1]+cell_size//2 + self.offset), cell_size//2)

        if self.label:
            self.show_label(surface, self.mine_counter, self.pos)

    def show_label(self, surface, label, pos):
        textsurface = myfont.render(label, False, self.font_color)
        surface.blit(
            textsurface, (pos[0]+self.size/2.5 + self.offset, pos[1] + (self.size * 2)//15 + self.offset))


class Grid:
    def __init__(self, player, n, mines):
        self.player = player
        self.cells = []
        self.mines = mines
        self.search_dirs = [(0, -1), (-1, -1), (-1, 0),
                            (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.n = n
        self.offset = 450 - ((cell_size*n)/2)

        for y in range(self.n):
            self.cells.append([])
            for x in range(self.n):
                self.cells[y].append(
                    Cell((x*cell_size, y*cell_size), self.mines[y][x], self.offset))

        self.lines = []

        for y in range(0, self.n + 1, 1):
            temp = []
            temp.append((0 + self.offset, y * cell_size + self.offset))
            temp.append((self.n * cell_size + self.offset,
                         y * cell_size + self.offset))
            self.lines.append(temp)

        for x in range(0, self.n + 1, 1):
            temp = []
            temp.append((x*cell_size + self.offset, 0 + self.offset))
            temp.append((x*cell_size + self.offset,
                         self.n * cell_size + self.offset))
            self.lines.append(temp)

    def random_mines(self):
        r = randint(0, 10)
        if r > 9:
            return True
        else:
            return False

    def draw(self, surface):
        for row in self.cells:
            for cell in row:
                cell.draw(surface)
        for line in self.lines:
            pygame.draw.line(surface, (72, 96, 96), line[0], line[1])

    # need to check for the edges and corners, so list index will not be out of range
    def is_within_bounds(self, x, y):
        return x >= 0 and x < self.n and y >= 0 and y < self.n

    def search(self, x, y):
        if not self.is_within_bounds(x, y):
            return

        cell = self.cells[y][x]

        if cell.visible:
            return

        if cell.mine:
            #cell.show_mine = True
            cell.explosion = True
            self.player.sub_health()
            return

        cell.visible = True

        num_mines = self.num_of_mines(x, y)

        if num_mines > 0:
            cell.label = True
            cell.mine_counter = str(num_mines)
            return

        for xx, yy in self.search_dirs:
            if self.is_within_bounds(x+xx, y+yy):
                self.search(x+xx, y+yy)

    def num_of_mines(self, x, y):
        counter = 0
        for xx, yy in self.search_dirs:
            if self.is_within_bounds(x + xx, y + yy):
                print(x + xx, y + yy)
                if self.cells[y + yy][x + xx].mine:
                    counter += 1
        return counter

    def click(self, x, y):
        grid_x, grid_y = (x - self.offset)//cell_size, (y -
                                                        self.offset)//cell_size
        print(int(grid_x), int(grid_y))
        self.search(int(grid_x), int(grid_y))

    def reload(self):
        self.player.health = 1
        for row in self.cells:
            for cell in row:
                cell.visible = False
                cell.label = False
                cell.marked = False
                cell.show_mine = False
                cell.explosion = False
                cell.mine = self.random_mines()

    def check_if_win(self):
        if self.player.health < 1:
            return False
        for row in self.cells:
            for cell in row:
                if not cell.visible and not cell.mine:
                    return False
        return True

    def show_mines(self):
        for row in self.cells:
            for cell in row:
                if not cell.show_mine:
                    cell.show_mine = True
                else:
                    cell.show_mine = False

    def mark_mine(self, x, y):
        grid_x, grid_y = int((x - self.offset)//cell_size), int((y -
                                                                 self.offset)//cell_size)
        print(grid_x, grid_y)
        self.cells[grid_y][grid_x].marked = not (
            self.cells[grid_y][grid_x].marked)
