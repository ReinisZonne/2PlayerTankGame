import pygame
import math
pygame.init()

class Bullet:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = (0, 0, 0)
        self.radius = 5
        self.damage = 10
        self.time = 0
    
    

    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def bulletTrajectory(self, surface, t):
        posX = t.getEndX()
        posY = t.getEndY()
        time = 0.05
        while time < 0.5:
            new_pos = t.bullet.bulletPath(posX, posY, t.power//2, t.angle, time)
            pygame.draw.circle(surface, (220, 220, 220), new_pos, 3, False)
            posX = new_pos[0]
            posY = new_pos[1]
            time += 0.05
    
    def draw(self, surface):
        # Draws the bullet
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
    
    def bulletPath(self, startx, starty, power, ang, time):
        angle = ang
        velx = math.sin(angle) * power
        vely = math.cos(angle) * power

        distX = velx * time
        distY = (vely * time) + ((-9.8 * (time ** 2)) / 2)

        newx = round(distX + startx)
        newy = round(starty - distY)

        return (newx, newy)