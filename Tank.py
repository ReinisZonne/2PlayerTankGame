import math
import pygame
from Bullet import Bullet
pygame.init()


class Tank:
    
    def __init__(self, x, y, color):
        # Tanks atributes
        self.x = x
        self.y = y
        self.color = color
        self.bullet = Bullet()
        self.width = 70
        self.height = 20
        self.speed = 1
        # ------------
        # Turret atributes
        self.angle = 0
        self.angleSpeed = 0.01
        self.turretLenght = 40
        self.power = 0
        # -------------
        self.isMoving = False
        self.isLocked = False
        self.turn = False
        self.hit = False
        self.won = False
        self.health = 50
        
    
    def getAngleX(self):
        return math.sin(self.angle)
    
    def resetBullet(self):
        self.bullet.x = round(self.getEndX())
        self.bullet.y = round(self.getEndY())
        self.isLocked = False
        self.isMoving = False
        self.power = 0
        
    
    def getAngleY(self):
        return math.cos(self.angle)
    
    def getEndX(self):
        return round(self.getCenterX() + self.turretLenght * self.getAngleX())
    
    def getEndY(self):
        return round(self.getCenterY() - self.turretLenght * self.getAngleY())
    
    def getCenterX(self):
        return self.x + self.width//2
    
    def getCenterY(self):
        return self.y + self.height//8
    
    def isHit(self):
        if self.health > 0:
            self.health -= self.bullet.damage
    
    def draw(self, surface):

        # Draws tanks turret
        pygame.draw.line(surface, (0, 220, 0), (self.getCenterX(), self.getCenterY()), (self.getEndX(), self.getEndY()), 7)

        # Draws tanks shuttle
        pygame.draw.circle(surface, (0, 0, 0), (self.getCenterX(), self.getCenterY()), 15)

        # Draws Tank base
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        # Draws Tank's bullet
        self.bullet.draw(surface)

        # Draws Tank's health
        pygame.draw.rect(surface, (255, 0, 0), (self.x + 10, self.y-50, 50, 5))
        pygame.draw.rect(surface, (0, 255, 0), (self.x + 10, self.y-50, self.health, 5))
        