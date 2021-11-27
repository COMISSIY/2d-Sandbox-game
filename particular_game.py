import pygame, math
from random import randint, choice, random
pygame.init()

RES = 800, 600
sc = pygame.display.set_mode(RES)
pygame.display.set_caption('Terraria for Linux')
clock = pygame.time.Clock()
f1 = pygame.font.Font(None, 30)
world_width = 500
world_height = 600

world_data = [[ [x, y, 0] for x in range(world_width)] for y in range(world_height)]

p_pos = [world_width//2, 325]
gravity_coef = 1

r_d = 60
b_size_x = RES[0] // r_d
b_size_y = RES[1] // r_d

speed = 1
bright_coef = 1.2
current_block = 8

pygame.mouse.set_visible(False)
def distance(a, b):
	return math.sqrt(a.x**2-b.x**2+a.y**2-b.y**2)

def generate_land(data):
	print("land generation...")
	offset = randint(-50, 50)
	for x in range(0, len(data[0])):
		# height = min(int(abs((math.sin(x/50)-math.cos(x/10))-25)*10), world_height)
		height = min(int(abs((math.cos((x-offset)/15 )+math.sin((x-offset)/40))*20)+250), world_height)
		height = min(int((abs(((math.sin(abs(x-offset))/2.5)**3+(math.cos(abs(x-offset)**0.8)/5)-10)*20)+height)/2), world_height)
		height = min(int((height + abs((math.sin((x-offset)/7)-1)*4)+math.cos(x-offset)/2)*2)//2, world_height)
		for n, y in enumerate(range(len(data)-height, len(data))):
			if n < randint(1, 4):
				data[y][x][2] = 1
			elif (n > (height-randint(0, 10)) // 3 or randint(0, 100)==26) and n <= height - 15:
				data[y][x][2] = randint(5, 6)
			elif n > height -randint(1, 16):
				data[y][x][2] = 7
			else:
				if n > height - 15:
					data[y][x][2] = randint(5, 7)
				else:
					data[y][x][2] = 3
	print('land generation done')
	print('planting trees...')
	for x in range(0, len(data[0])-1):
		for y in range(0, len(data)-1):
			tree = randint(0, 20)
			if data[y][x][2] == 1:
				if tree != 10:
					break
				tree = randint(10, 25)
				for n, i in enumerate(range(y, y-tree, -1)):
					if (tree // 3) > n:
						data[i][x][2]=4
					else:
						data[i][x-1][2], data[i][x][2], data[i][x+1][2] = 1, 1, 1
	print('planting trees done')

	return data
generate_land(world_data)

while True:
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			exit()
		if i.type == pygame.KEYDOWN:
			if i.key == pygame.K_DOWN:
				if cursor_hegiht < 1:
					cursor_hegiht += 1
			if i.key == pygame.K_UP:
				if cursor_hegiht > -1:
					cursor_hegiht -= 1
			if i.key == pygame.K_LEFT:
				if current_block >0:
					current_block -= 1
			if i.key == pygame.K_RIGHT:
				if current_block < 8:
					current_block += 1

	clock.tick(30)
	sc.fill((102, 178, 255))
	for rel_y, y in enumerate(world_data[max(p_pos[1]-r_d, 0):min(p_pos[1]+r_d, world_height)]):
		for rel_x, x in enumerate(y[max(p_pos[0]-r_d, 0):min(p_pos[0]+r_d, world_width)]):
			if x[2]:
				if x[2] == 1:
					color = (0, 153, 0)#grass
				if x[2] == 2:
					color = (255, 165, 0)#build block
				if x[2] == 3:
					color = (150, 80, 30)#dirt
				if x[2] == 4:
					color = (125, 0, 0)#wood
				if x[2] == 5:
					color = (169, 169, 169)#stone
				if x[2] == 6:
					color = (140, 140, 140)#dark stone
				if x[2] == 7:
					color = (10, 10, 10)#obsidian
				if x[2] == 8:
					color = (50, 150, 255)#water
					try:
						if not world_data[x[1]+1][x[0]][2]:
							world_data[x[1]+1][x[0]][2] = 8
							x[2] = 0
						elif not world_data[x[1]][x[0]-1][2] and not world_data[x[1]][x[0]+1][2]:
							world_data[x[1]][x[0]+1][2] = 8
							x[2] = 0
						elif not world_data[x[1]][x[0]-1][2]:
							world_data[x[1]][x[0]-1][2] = 8
							x[2] = 0	
						elif not world_data[x[1]][x[0]+1][2]:
							world_data[x[1]][x[0]+1][2] = 8
							x[2] = 0
							
					except:
						pass

				pygame.draw.rect(sc, (max(0, color[0]-(rel_y*bright_coef)), max(0, color[1]-(rel_y*bright_coef)), max(0, color[2]-(rel_y*bright_coef))), (rel_x*b_size_x-(RES[0]//2), rel_y*b_size_y-(RES[1]//2), b_size_x, b_size_y))
			if x[0:2] == p_pos:
				pygame.draw.rect(sc, (255, 0, 255), (rel_x*b_size_x-(RES[0]//2), rel_y*b_size_y-(RES[1]//2), b_size_x, b_size_y*2))
			# if x[0:2] == cursor_pos:
			# 	pygame.draw.rect(sc, (255, 0, 255), (rel_x*b_size_x-(RES[0]//2), rel_y*b_size_y-(RES[1]//2), b_size_x, b_size_y*2), 1)
	try:
		if not world_data[p_pos[1]+2][p_pos[0]][2] or world_data[p_pos[1]+2 ][p_pos[0]][2]==8:
			if p_pos[1] - gravity_coef > 0:
				p_pos[1]+=gravity_coef
			else:
				is_jump = False 
	except:
		pass

	keys = pygame.key.get_pressed()
	event = pygame.mouse.get_pressed()
	try:
		if keys[pygame.K_a]:
			if not world_data[p_pos[1]][p_pos[0]-1][2] or world_data[p_pos[1]][p_pos[0]-1][2]==8:
				p_pos[0]-=speed
			if not world_data[p_pos[1]-1][p_pos[0]-1][2] and world_data[p_pos[1]+1][p_pos[0]][2]:
				p_pos[1]-=1
		elif keys[pygame.K_d]:
			if not world_data[p_pos[1]][p_pos[0]+1][2] or world_data[p_pos[1]][p_pos[0]+1][2]==8:
				p_pos[0]+=speed
			if not world_data[p_pos[1]-1][p_pos[0]+1][2] and world_data[p_pos[1]+1][p_pos[0]][2]:
				p_pos[1]-=1

		if keys[pygame.K_k] or event[2]:
			m = pygame.mouse.get_pos()
			world_data[(p_pos[1]+int(m[1]/b_size_y))-r_d//2][(p_pos[0]+int(m[0]/b_size_x)-r_d//2)][2] = 0
		if keys[pygame.K_j] or event[0]:
			world_data[(p_pos[1]+int(m[1]/b_size_y))-r_d//2][(p_pos[0]+int(m[0]/b_size_x)-r_d//2)][2]=current_block
		if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and (not world_data[p_pos[1]-1][p_pos[0]][2] or world_data[p_pos[1]][p_pos[0]][2]==8):
			p_pos[1] -= 2
	except:
		pass
	sc.blit(f1.render(str(p_pos), 1, (255, 255, 255)), (0, 0))
	m = pygame.mouse.get_pos()
	pygame.draw.circle(sc, (255, 0, 255), (m[0], m[1]), b_size_y//2)

	pygame.display.update()