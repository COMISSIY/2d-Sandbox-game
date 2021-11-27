import pygame
from random import random
pygame.init()

sc = pygame.display.set_mode((600, 400))
surf = [[pygame.Vector2([random()]*2) for x in range(200)] for y in range(200)]
surf2 = [[pygame.Vector2([random()]*2) for x in range(200//2)] for y in range(200//2)]
surf3 = [[pygame.Vector2([random()]*2) for x in range(200//10)] for y in range(200//10)]

def noise(s, st):
	step = 1
	for x in range(1, len(surf[0])-1):
		for y in range(1, len(surf)-1):
			c = 0
			n = [surf[y][x-1], surf[y][x+1], surf[y-1][x], surf[y+1][x], surf[y-1][x-1], surf[y+1][x+1], surf[y-1][x+1], surf[y+1][x-1]]
			for i in n:
				c+=surf[y][x].dot(i)
			c = c/15
			if st:
				surf[y][x] = pygame.Vector2([c, c])
			c = min(c*255, 255)
			pygame.draw.rect(sc, (c, c, c), (x*step, y*step, step, step))


for i in range(2):
	noise(surf, False)
while True:
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			exit()
	sc.fill((255, 255, 255))
	noise(surf, False)

	pygame.display.update()