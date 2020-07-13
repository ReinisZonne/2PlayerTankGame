import pygame
from Tank import Tank
from random import randint

pygame.init()
pygame.font.init()


# Main loop
def main():
    
    # Window settings
    WIDTH = 1000
    HEIGHT = WIDTH * 9//16 # Sets a resulotion 16:9

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tank Game")
    clock = pygame.time.Clock()
    fps = 60
    smallFont = pygame.font.SysFont("Comic Sans MS", 12)
    bigFont = pygame.font.SysFont("Comic sans MS", 32)
    # ---------------


    # Redraws the game window
    def redraw_Window(surface, t1, t2):
        win.fill((50, 50, 50))
        
        
        # Draws classes
        t1.draw(surface)
        t2.draw(surface)
        # -------------
        # Draws Power bar
        pygame.draw.rect(surface, (255, 255, 0), (20, 120, 15, -t1.power))
        pygame.draw.rect(surface, (255, 0, 0), (960, 120, 15, -t2.power))
        # -------------
        # Draws Bullet trajectory
        if t1.power > 0 and t1.isLocked != True:
            t1.bullet.bulletTrajectory(surface, t1)
        if t2.power > 0 and t2.isLocked != True:
            t2.bullet.bulletTrajectory(surface, t2)
        #---------------
        # Draws mid line
        lineX = WIDTH // 2
        lineY = 0
        while lineY <= HEIGHT:
            pygame.draw.line(surface, (255, 255, 255), (lineX, lineY), (lineX, lineY + 10), 2)
            lineY += 25
        
        # Draws who's turn is
        if t1.turn == True:
            text = bigFont.render("Left turn", False, (0, 255, 0))
            win.blit(text, (70, 70))
        else:
            text = bigFont.render("Right turn", False, (0, 255, 0))
            win.blit(text, (800, 70))

        if t1.won:
            text = bigFont.render("Left tank won!", False, (255, 0, 0))
            win.blit(text, (WIDTH//2 - 350, HEIGHT//2))
        if t2.won:
            text = bigFont.render("Right tank won!", False, (255, 0, 0))
            win.blit(text, (WIDTH//2 + 150, HEIGHT//2))

        # Draws the text
        text = smallFont.render(str(t1.power), False, (0, 0, 0))
        win.blit(text, (22, 130))
        text = smallFont.render(str(t2.power), False, (0, 0, 0))
        win.blit(text, (962, 135))
        pygame.display.update()
        # ---------------

    # Classes
    tank1 = Tank(40, HEIGHT - 25, (255, 0, 0))
    tank2 = Tank(900, HEIGHT - 25, (0, 255, 0))
    # ---------------
    # Picks who starts first
    if randint(1,2) == 1:
        tank1.turn = True
    else:
        tank2.turn = True

    # -------------


    # Main game loop
    run = True
    while run:
        clock.tick(fps)
        

        # Key movement
        keys = pygame.key.get_pressed()
        # Tank1 movement
        if tank1.turn == True and not tank1.won and not tank2.won:
            if keys[pygame.K_d] and tank1.x + tank1.width <= WIDTH // 2 and tank1.isMoving == False: # Moves right
                tank1.x += tank1.speed
            if keys[pygame.K_a] and tank1.x >= 5 and tank1.isMoving == False: # Moves left
                tank1.x -= tank1.speed
            if keys[pygame.K_w] and tank1.angle < 1.31 and tank1.isLocked == False: # Turns the turret to the left
                tank1.angle += tank1.angleSpeed
            if keys[pygame.K_s] and tank1.angle > -1.31 and tank1.isLocked == False: # Turns the turret to the right
                tank1.angle -= tank1.angleSpeed
        # Tank2 movement
        if tank2.turn == True and not tank1.won and not tank2.won:
            if keys[pygame.K_LEFT] and tank2.x >= 5 and tank2.isMoving == False and tank2.x >= WIDTH//2 + 5: # moves left
                tank2.x -= tank2.speed
            if keys[pygame.K_RIGHT] and tank2.x + tank2.width <= WIDTH - 5 and tank2.isMoving == False: # Moves right
                tank2.x += tank2.speed
            if keys[pygame.K_UP] and tank2.angle <= 1.31 and tank2.isLocked == False: # Turns turret left
                tank2.angle += tank2.angleSpeed
            if keys[pygame.K_DOWN] and tank2.angle >= -1.31 and tank2.isLocked == False: # Turns turret right
                tank2.angle -= tank2.angleSpeed

        # Set power shot
        if tank1.turn == True and not tank1.won and not tank2.won:
            if keys[pygame.K_LSHIFT] and tank1.power < 100 and tank1.isLocked == False:
                tank1.power += 1
        if tank2.turn == True and not tank1.won and not tank2.won:
            if keys[pygame.K_RETURN] and tank2.power < 100 and tank2.isLocked == False:
                tank2.power += 1
 
        # ---------------
        # Collisions with tanks and bullets
        if tank1.bullet.x > tank2.x and tank1.bullet.x < tank2.x + tank2.width and tank1.bullet.y > tank2.y:
            tank2.isHit()
            tank1.resetBullet()
            tank1.turn = False
            tank2.turn = True

        if tank2.bullet.x < tank1.x + tank1.width and tank2.bullet.x > tank1.x and tank2.bullet.y > tank1.y:
            tank1.isHit()
            tank2.resetBullet()
            tank1.turn = True
            tank2.turn = False

        # Lockes the tank power
        if tank1.isLocked == True:
            if tank1.bullet.y < HEIGHT - tank1.bullet.radius:
                time += 0.05
                new_pos = tank1.bullet.bulletPath(x, y, power, angle, time)
                tank1.bullet.setPos(new_pos)
            else:
                tank1.resetBullet()
                tank1.turn = False
                tank2.turn = True
        if tank2.isLocked == True:
            if tank2.bullet.y < HEIGHT - tank2.bullet.radius:
                time += 0.05
                new_pos = tank2.bullet.bulletPath(x, y, power, angle, time)
                tank2.bullet.setPos(new_pos)
            else:
                tank2.resetBullet()
                tank2.turn = False
                tank1.turn = True
        # --------------
        
        # Lock power shot
        if keys[pygame.K_LCTRL] and tank1.turn == True and tank1.power > 0 and not tank1.won and not tank2.won:
            if tank1.isLocked == False:
                tank1.bullet.setPos((tank1.getEndX(), tank1.getEndY()))
                x = tank1.bullet.x
                y = tank1.bullet.y
                time = 0
                power = tank1.power
                angle = tank1.angle
                tank1.isLocked = True
                tank1.isMoving = True
        if keys[pygame.K_RCTRL] and tank2.turn == True and tank2.power > 0 and not tank1.won and not tank2.won:
            if tank2.isLocked == False:
                tank2.bullet.setPos((tank2.getEndX(), tank2.getEndY()))
                x = tank2.bullet.x
                y = tank2.bullet.y
                time = 0
                power = tank2.power
                angle = tank2.angle
                tank2.isLocked = True
                tank2.isMoving = True
        # -------------------
        # Sets the bullet in game
        if tank1.isLocked == False:
            bullet = tank1.bullet
            bullet.setPos((tank1.getEndX(), tank1.getEndY()))
        # ----------------------
        if tank2.isLocked == False:
            bullet = tank2.bullet
            bullet.setPos((tank2.getEndX(), tank2.getEndY()))
        
        if tank1.health == 0:
            tank2.won = True
        if tank2.health == 0:
            tank1.won = True
            
        # Exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # ------------
        redraw_Window(win, tank1, tank2)
                    
while (ans := input("Do you want to play again?").lower) not in ['y', 'yes']:
    main()

pygame.quit()
