import pygame
import os
import math
from threading import Timer
import random
import button

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT ))
pygame.display.set_caption('Level Editor')


#define game variables
ROWS = 16
MAX_COLS = 21
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 17
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
isHero = 0

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

#define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#define font
font = pygame.font.SysFont('Futura', 30)

#create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * MAX_COLS
	world_data.append(r)

#create ground
for tile in range(0, MAX_COLS):
	world_data[ROWS - 1][tile] = 0



# __________________________________________ Оприділили зміння ____________________________________________

#create function for drawing background
def draw_bg():
	screen.fill('#ff00ff')

#draw grid
def draw_grid():
	#vertical lines
	for c in range(MAX_COLS + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
	#horizontal lines
	for c in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


#function for drawing the world tiles
def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

def check_isHero():
	global world_data
	global isHero
	for x in world_data:
		for y in x:
			if y == 15:
				isHero += 1

#create buttons
load_img = pygame.image.load('img/load_btn.png').convert_alpha()
load_button = button.Button(SCREEN_WIDTH // 2 + 500, SCREEN_HEIGHT - 50, load_img, 1)

#make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 3:
		button_row += 1
		button_col = 0

# __________________________________________________________________________________________________________________
# __________________________________________ ГОЛОВНИЙ ЦИКЛ LEVEL EDITOR ____________________________________________
# __________________________________________________________________________________________________________________

run = True
while run:
	clock.tick(FPS)

	draw_bg()
	draw_grid()
	draw_world()

	# draw tile panel and tiles
	pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

	if load_button.draw(screen):
		check_isHero()
		if isHero == 1:
			run = False


	#choose a tile
	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count

	#highlight the selected tile
	pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

	#scroll the map
	if scroll_left == True and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

	#add new tiles to the screen
	#get mouse position
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE
	#check that the coordinates are within the tile area
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		#update tile value
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1
	pygame.display.update()
pygame.quit()

# __________________________________________________________________________________________________________________
# __________________________________________ ДРУГИЙ КОД ____________________________________________________________
# __________________________________________________________________________________________________________________

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
GRAVITY = 0.75
LEVEL = 0
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 17
FLOOR_LEVEL = 500
clock = pygame.time.Clock()
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ріж русню")

class World():
    def __init__(self):
        self.obstacle_list = []
        self.image_list = []
        self.gamewin = False
        self.gameover = False
        for x in range(TILE_TYPES):
            img = pygame.image.load(f'img/tile/{x}.png')
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.image_list.append(img)
    def process_data(self, data):
        for y in range(len(data)):
            row = data[y]
            for x in range(len(row)):
                tile = row[x]
                if tile >= 0:
                    img = self.image_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile == 0 or tile == 4 or tile == 5 or tile == 7 or tile == 9 or tile == 10 or tile == 12:
                        self.obstacle_list.append(tile_data)
                    elif tile == 15:
                        player = Soldier('hero--knife', x * TILE_SIZE, y * TILE_SIZE, 1.0, 5)
                    elif tile == 16:
                        enemy_group.add(Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.0, 1.7))
                    else:
                        box_group.add(Box(img, x * TILE_SIZE, y * TILE_SIZE))
        return player, enemy_group
    def draw(self):
        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1])
    def create_matrix(self):
        world_data = []
        global LEVEL
        for row in range(ROWS):
            r = [-1] * COLS
            world_data.append(r)
        with open(f'level{LEVEL}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
        return world_data

class Box(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.start_pos = x
        self.max_ammo = 20
        self.ammo = self.max_ammo
        self.char_type = char_type
        self.knife_mode = True
        self.speed = speed
        self.health = 100
        self.max_health = self.health
        self.scale = scale
        self.direction = 1
        self.jump = False
        self.in_air = False
        self.jump_height = 14
        self.vel_y = 0
        self.flip = False
        self.animation_list = []
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        # ai specific variables
        self.move_counter = 0
        for i in range(len(os.listdir(f'images/{self.char_type}'))):
            img = pygame.image.load(f'images/{self.char_type}/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.moving_left = False
        self.moving_right = False
        self.pause = False
        self.prev_left = False
        self.availible_shot = True
        self.touch_wall = False
    def update(self):
        self.check_alive()
        self.ckeck_wall_collision()
    def move(self):
        dx = 0
        dy = 0
        if self.moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if self.moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump == True:
            self.vel_y = -self.jump_height
            self.jump = False
        # Гравітація
        self.vel_y += GRAVITY
        dy += self.vel_y
        # Перевіряє на колізію з об'єктами на карті
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        # Вираховування майбутніх координат героя
        self.rect.x += dx
        self.rect.y += dy
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
    def draw(self):
        if self.moving_left or self.moving_right:
            self.update_animation()
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks()-self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index == len(self.animation_list):
            self.frame_index = 0
    def check_mode(self):
        if self.knife_mode:
            self.char_type = 'hero--knife'
        else:
            self.char_type = 'hero'
        self.animation_list.clear()
        for i in range(len(os.listdir(f'images/{self.char_type}'))):
            img = pygame.image.load(f'images/{self.char_type}/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
            self.animation_list.append(img)
        self.update_animation()
    def reload(self):
        self.ammo = self.max_ammo
    def shoot(self):
        mpos = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], True)
        ppos = Vector(self.rect.centerx, self.rect.centery, True)
        vec = mpos - ppos
        direction = -vec.y / (vec.x + 0.0000000000001)
        if (mpos.x < ppos.x) and self.flip and self.ammo > 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction, -1, self)
            bullet_group.add(bullet)
            self.ammo -= 1
        if (mpos.x > ppos.x) and not self.flip and self.ammo > 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction, 1, self)
            bullet_group.add(bullet)
            self.ammo -= 1
    def check_knife(self):
        for enemy in enemy_group:
            player_pos = Vector(self.rect.centerx, self.rect.centery, True)
            enemy_pos = Vector(enemy.rect.centerx, enemy.rect.centery, True)
            vec = player_pos - enemy_pos
            if vec.mod <= 40:
                enemy.health -= 50
    def timer_action(self):
        self.pause = False
    def availible_shot_action(self):
        self.availible_shot = True
    def ai(self):
        if self.alive and player.alive:
            if random.randint(1, 200) == 1 and not self.pause:
                self.pause = True
                if self.moving_left:
                    self.prev_left = True
                else:
                    self.prev_left = False
                self.moving_left = False
                self.moving_right = False
                timer = Timer(1.0, self.timer_action)
                timer.start()
            if not self.pause:
                if not self.moving_left and not self.moving_right:
                    if self.prev_left:
                        self.moving_left = True
                        self.moving_right = False
                    else:
                        self.moving_left = False
                        self.moving_right = True
                self.move_counter += 1
                if self.start_pos - 50 > self.rect.x or self.rect.x > self.start_pos + 50:
                    self.direction *= -1
                    self.move_counter *= -1
                    self.moving_left = not self.moving_left
                    self.moving_right = not self.moving_right
                if not self.touch_wall:
                    self.move()
            player_pos = Vector(player.rect.centerx, player.rect.centery, True)
            enemy_pos = Vector(self.rect.centerx, self.rect.centery, True)
            pos = player_pos - enemy_pos
            direction = -pos.y / (pos.x + 0.0000000000001)
            if enemy_pos.x > player_pos.x and self.flip and pos.mod < 200 and self.availible_shot:
                self.availible_shot = False
                bullet_group.add( Bullet(self.rect.centerx, self.rect.centery, direction, -1, self))
                timer = Timer(0.1, self.availible_shot_action)
                timer.start()
            if enemy_pos.x < player_pos.x and not self.flip and pos.mod < 200 and self.availible_shot:
                self.availible_shot = False
                bullet_group.add( Bullet(self.rect.centerx, self.rect.centery, direction, 1, self))
                timer = Timer(0.1, self.availible_shot_action)
                timer.start()
    def ckeck_wall_collision(self):
        if self.rect.left <= 0:
            self.touch_wall = True
            self.rect.x += 5
        elif self.rect.right >= SCREEN_WIDTH:
            self.touch_wall = True
            self.rect.x -= 5
        else:
            self.touch_wall = False

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, dir_X, arrow):
        pygame.sprite.Sprite.__init__(self)
        self.arrow = arrow
        self.speed = 10
        self.direction = direction
        self.scale = 0.2
        self.dx = dir_X * self.speed / math.sqrt(1 + self.direction**2)
        self.dy = self.dx*self.direction
        bullet_img = pygame.image.load('images/ammo/0.png')
        bullet_img = pygame.transform.scale(bullet_img, (bullet_img.get_width() * self.scale, bullet_img.get_height() * self.scale))
        self.image = pygame.transform.rotate(bullet_img,  math.atan(-self.direction) * (180.0 / math.pi))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def update(self, enemy_group):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
                self.kill()
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(player, bullet_group, False) and self.arrow != player:
                if player.alive:
                    player.health -= 5
                    self.kill()
            if pygame.sprite.spritecollide(enemy, bullet_group, False) and self.arrow != enemy:
                if enemy.alive:
                    enemy.health -= 15
                    self.kill()

class Vector():
    def __init__(self, x, y, normalize_needle=False):
        self.x = x
        self.y = y
        self.mod = math.sqrt(x**2 + y**2)
        if normalize_needle:
            self.normalize()
    def normalize(self):
        self.x = -SCREEN_WIDTH / 2 + self.x
        self.y = SCREEN_HEIGHT / 2 - self.y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

def drawMouceLine(player):
    mpos = pygame.mouse.get_pos()
    pygame.draw.line(screen, '#ff0000', (mpos[0], mpos[1]), (player.rect.center[0], player.rect.center[1]))

def draw_bg():
    screen.fill('#ff00ff')

def gameover():
    screen.fill('#000000')
    pygame.font.init()
    world.gameover = True
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render('GAME OVER', False, (200, 200, 200))
    screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - text_surface.get_height() // 2))

def gamewin():
    screen.fill('#e8e337')
    pygame.font.init()
    world.gamewin = True
    my_font = pygame.font.SysFont('Consolas', 30)
    text_surface = my_font.render('YOU WIN', False, (0, 0, 0))
    screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - text_surface.get_height() // 2))

# Створюємо Sprite групи
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
# Завантажуємо матрицю світу
world = World()
player, enemy_group = world.process_data(world_data)

# __________________________________________________________________________________________________________________
# __________________________________________ ГОЛОВНИЙ ЦИКЛ _________________________________________________________
# __________________________________________________________________________________________________________________
run = True
while run:
    clock.tick(FPS)
    if not (world.gameover or world.gamewin):
        draw_bg()
        world.draw()

        box_group.update()
        box_group.draw(screen)

        if not player.knife_mode and player.alive:
            drawMouceLine(player)

        bullet_group.update(enemy_group)
        bullet_group.draw(screen)

        for enemy in enemy_group:
            enemy.update()
            if not enemy.alive:
                enemy_group.remove(enemy)
            else:
                enemy.ai()
                enemy.draw()

        player.update()
        if player.alive:
            if not player.touch_wall:
                player.move()
            player.update()
            player.draw()
        else:
            timer_1 = Timer(0.5, gameover)
            timer_1.start()
            timer_2 = Timer(3.0, pygame.quit)
            timer_2.start()

        if len(enemy_group) == 0:
            timer_1 = Timer(0.5, gamewin)
            timer_1.start()
            timer_2 = Timer(3.0, pygame.quit)
            timer_2.start()

    for event in pygame.event.get():
        # quit pygame
        if event.type == pygame.QUIT:
            run = False
        # Перевіряє на вистріл -----------------------
        # ----------------------- -----------------------
        if event.type == pygame.MOUSEBUTTONDOWN and not player.knife_mode:
            player.shoot()
        # Перевіряє на удар ножем -----------------------
        # -----------------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN and player.knife_mode:
            player.check_knife()
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.moving_left = True
            if event.key == pygame.K_d:
                player.moving_right = True
            if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and not player.in_air:
                player.jump = True
                player.in_air = True
            if event.key == pygame.K_ESCAPE:
                run = False
        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.moving_left = False
            if event.key == pygame.K_d:
                player.moving_right = False
            if event.key == pygame.K_q:
                player.knife_mode = not player.knife_mode
                player.check_mode()
            if event.key == pygame.K_r:
                timer = Timer(2.1, player.reload)
                timer.start()
    pygame.display.update()
pygame.quit()