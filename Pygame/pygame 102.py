import pygame

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kill Them All")

soldier = pygame.image.load("soldier.png").convert_alpha()

rect_1 = pygame.Rect(200, 100, 150, 100)

rect_2 = soldier.get_rect()
rect_2.topleft = (200, 200)

clock = pygame.time.Clock()

run = True
while run:
    
    clock.tick(60)
    
    screen.fill((255, 255, 255))
    
    #pygame.draw.rect(screen, (255, 0, 255), rect_1)
    #pygame.draw.rect(screen, (0, 255, 255), rect_2)
    
    screen.blit(soldier, rect_2)
    
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        rect_2.move_ip(-5, 0)
    elif key[pygame.K_d] == True:
        rect_2.move_ip(5, 0)
    elif key[pygame.K_w] == True:
        rect_2.move_ip(0, -5)
    elif key[pygame.K_s] == True:
        rect_2.move_ip(0, 5)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.flip()
    
pygame.quit()
