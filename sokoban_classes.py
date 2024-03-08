from copy import deepcopy

import pygame
from constants import *


class SokobanGame:
    def __init__(self):
        pygame.init()
        self.initialize_screen()
        self.initialize_images()
        self.levels = self.load_levels()
        self.selected_level = 1
        self.victory = False
        self.move = None
        self.dir = "down"
        self.running = True

    def initialize_screen(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("T and K Sokoban")
        icon = pygame.image.load("assets/images/playerFace.png")
        self.fon_img = pygame.image.load(
            "assets/images/fon.png").convert_alpha()
        self.fon_img = pygame.transform.scale(self.fon_img, (WIDTH, HEIGHT))
        self.screen.blit(self.fon_img, (0, 0))
        pygame.display.flip()
        pygame.display.set_icon(icon)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__del__()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return

    def initialize_images(self):
        self.wall_img = pygame.image.load(
            "assets/images/wall.png").convert_alpha()
        self.wall_img = pygame.transform.smoothscale(self.wall_img,
                                                     (TITLE_SIZE, TITLE_SIZE))
        self.floor_img = pygame.image.load(
            "assets/images/floor.png").convert_alpha()
        self.floor_img = pygame.transform.smoothscale(self.floor_img,
                                                      (TITLE_SIZE, TITLE_SIZE))
        self.x_img = pygame.image.load(
            "assets/images/target.png").convert_alpha()
        self.x_img = pygame.transform.smoothscale(self.x_img,
                                                  (TITLE_SIZE, TITLE_SIZE))
        self.up_img = pygame.image.load(
            "assets/images/player_down.png").convert_alpha()
        self.up_img = pygame.transform.smoothscale(self.up_img,
                                                   (TITLE_SIZE, TITLE_SIZE))
        self.down_img = pygame.image.load(
            "assets/images/player_up.png").convert_alpha()
        self.down_img = pygame.transform.smoothscale(self.down_img,
                                                     (TITLE_SIZE, TITLE_SIZE))
        self.right_img = pygame.image.load(
            "assets/images/player_r.png").convert_alpha()
        self.right_img = pygame.transform.smoothscale(self.right_img,
                                                      (TITLE_SIZE, TITLE_SIZE))
        self.left_img = pygame.image.load(
            "assets/images/player_l.png").convert_alpha()
        self.left_img = pygame.transform.smoothscale(self.left_img,
                                                     (TITLE_SIZE, TITLE_SIZE))
        self.crate_img = pygame.image.load(
            "assets/images/crate.png").convert_alpha()
        self.crate_img = pygame.transform.smoothscale(self.crate_img,
                                                      (TITLE_SIZE, TITLE_SIZE))

    def load_levels(self):
        with open(FILENAME) as file:
            levels = []
            for line in file:
                line = line.rstrip()
                if line:
                    if line.startswith("LEVEL"):
                        level = {"map": [], "player": [], "crates": []}
                    elif line.startswith("P: "):
                        x, y = map(int, line[3:].split(","))
                        level["player"].append((x, y))
                    elif line.startswith("C: "):
                        crates = line[3:].split()
                        for crate in crates:
                            x, y = map(int, crate.split(","))
                            level["crates"].append((x, y))
                    elif line == "END LEVEL":

                        levels.append(level)
                    else:
                        level["map"].append(line)
            return tuple(levels)

    def launch(self):
        self.level_copy = self.copy_level()
        while self.running:
            self.handle_events()
            self.update_logic()
            self.update_screen()

    def copy_level(self):
        level_copy = deepcopy(self.levels[self.selected_level - 1])
        self.dir = "down"
        return level_copy

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.victory:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if self.selected_level < len(self.levels):
                        self.selected_level += 1
                    self.level_copy = self.copy_level()
                    self.victory = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move = "up"
                    elif event.key == pygame.K_DOWN:
                        self.move = "down"
                    elif event.key == pygame.K_LEFT:
                        self.move = "left"
                    elif event.key == pygame.K_RIGHT:
                        self.move = "right"
                    elif event.key == pygame.K_ESCAPE:
                        self.level_copy = self.copy_level()

    def update_logic(self):
        if self.move:
            if self.move == "up":
                self.dir = "up"
                self.update_move_up()
            elif self.move == "down":
                self.dir = "down"
                self.update_move_down()
            elif self.move == "left":
                self.dir = "left"
                self.update_move_left()
            elif self.move == "right":
                self.dir = "right"
                self.update_move_right()
            self.move = None
            self.check_victory()

    def update_move_up(self):
        x, y = self.level_copy["player"][0]
        if (x, y - 1) in self.level_copy["crates"]:
            if ((x, y - 2) not in self.level_copy["crates"]
                    and self.level_copy["map"][y - 2][x] != "#"):
                self.level_copy["crates"].remove((x, y - 1))
                self.level_copy["crates"].append((x, y - 2))
        if (self.level_copy["map"][y - 1][x] in ["-", "X"]
                and (x, y - 1) not in self.level_copy["crates"]):
            self.level_copy["player"].pop()
            self.level_copy["player"].append((x, y - 1))

    def update_move_down(self):
        x, y = self.level_copy["player"][0]
        if (x, y + 1) in self.level_copy["crates"]:
            if ((x, y + 2) not in self.level_copy["crates"]
                    and self.level_copy["map"][y + 2][x] != "#"):
                self.level_copy["crates"].remove((x, y + 1))
                self.level_copy["crates"].append((x, y + 2))
        if (self.level_copy["map"][y + 1][x] in ["-", "X"]
                and (x, y + 1) not in self.level_copy["crates"]):
            self.level_copy["player"].pop()
            self.level_copy["player"].append((x, y + 1))

    def update_move_left(self):
        x, y = self.level_copy["player"][0]
        if (x - 1, y) in self.level_copy["crates"]:
            if ((x - 2, y) not in self.level_copy["crates"]
                    and self.level_copy["map"][y][x - 2] != "#"):
                self.level_copy["crates"].remove((x - 1, y))
                self.level_copy["crates"].append((x - 2, y))
        if (self.level_copy["map"][y][x - 1] in ["-", "X"]
                and (x - 1, y) not in self.level_copy["crates"]):
            self.level_copy["player"].pop()
            self.level_copy["player"].append((x - 1, y))

    def update_move_right(self):
        x, y = self.level_copy["player"][0]
        if (x + 1, y) in self.level_copy["crates"]:
            if ((x + 2, y) not in self.level_copy["crates"]
                    and self.level_copy["map"][y][x + 2] != "#"):
                self.level_copy["crates"].remove((x + 1, y))
                self.level_copy["crates"].append((x + 2, y))
        if (self.level_copy["map"][y][x + 1] in ["-", "X"]
                and (x + 1, y) not in self.level_copy["crates"]):
            self.level_copy["player"].pop()
            self.level_copy["player"].append((x + 1, y))

    def check_victory(self):
        self.victory = True
        for y in range(len(self.level_copy["map"])):
            for x in range(len(self.level_copy["map"][y])):
                if (self.level_copy["map"][y][x] == "X"
                        and (x, y) not in self.level_copy["crates"]):
                    self.victory = False

    def update_screen(self):
        self.screen.fill(BACKGROND_COLOR)
        self.update_game_screen()
        if self.victory:
            self.draw_victory_overlay()
        pygame.display.flip()

    def update_game_screen(self):
        self.draw_game_board()
        self.print_level()

    def draw_game_board(self):
        rows = len(self.level_copy["map"])
        start_x = (WIDTH - self.get_longest_row() * TITLE_SIZE) // 2
        start_y = (HEIGHT - rows * TITLE_SIZE) // 2
        i, j = 0, 0
        for y in range(start_y, start_y + rows * TITLE_SIZE, TITLE_SIZE):
            columns = len(self.level_copy["map"][j])
            for x in range(start_x, start_x + columns * TITLE_SIZE, TITLE_SIZE):
                s = self.level_copy["map"][j][i]
                if s == "#":
                    self.screen.blit(self.floor_img, (x, y))
                    self.screen.blit(self.wall_img, (x, y))
                elif s == "-":
                    self.screen.blit(self.floor_img, (x, y))
                elif s == "X":
                    self.screen.blit(self.floor_img, (x, y))
                    self.screen.blit(self.x_img, (x, y))
                if (i, j) in self.level_copy["player"]:
                    if self.dir == "up":
                        self.screen.blit(self.up_img, (x, y))
                    if self.dir == "down":
                        self.screen.blit(self.down_img, (x, y))
                    if self.dir == "right":
                        self.screen.blit(self.right_img, (x, y))
                    if self.dir == "left":
                        self.screen.blit(self.left_img, (x, y))

                if (i, j) in self.level_copy["crates"]:
                    self.screen.blit(self.crate_img, (x, y))
                i += 1
            i = 0
            j += 1

    def get_longest_row(self):
        return max(
            [len(line) for line in self.level_copy["map"]])

    def print_level(self):
        print(self.selected_level)

    def draw_victory_overlay(self):
        self.last_fon_img = pygame.image.load(
            "assets/images/last_fon.png").convert_alpha()
        self.last_fon_img = pygame.transform.scale(self.last_fon_img, (WIDTH, HEIGHT))
        self.screen.blit(self.last_fon_img, (0, 0))
        pygame.display.flip()

    def __del__(self):
        pygame.quit()
