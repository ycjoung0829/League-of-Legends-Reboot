
#this file runs the program and opens the game window 
###############

import pygame
import os
import sys
import math
import time 


#code, images used from https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-animation/
####################
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
screenWidth = 1200
screenHeight = 800
screen = pygame.display.set_mode((screenWidth, screenHeight))

#background image from https://tr.pinterest.com/pin/404690716490658541/
background = pygame.image.load('images/aram.jpg').convert_alpha()
background = pygame.transform.scale(background, (1300, 800))
r1 = pygame.transform.scale(pygame.image.load('images/R1.png'), (35, 35)) 


l1 = pygame.transform.scale(pygame.image.load('images/L1.png'), (35, 35)) 

allyAutos = []
enemyAutos = []
allyMinions = []
enemyMinions = []
minionX, minionY = 241, 598
enemyX, enemyY = 987, 200
###################


class Background(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, screen):
        background = pygame.image.load('images/aram2.jpg').convert_alpha()
        screen.blit(background, (self.x, self.y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.doStuff = False 
        self.getMana = 3
        self.healthRegen = 1
        self.speed = 4
        self.walkCount = 0
        self.left = False
        self.right = True
        self.standing = True 
        self.health = 30
        self.originalHealth = 30
        self.visible = True 
        self.stroke = False 
        self.hitbox = (self.x + 10, self.y + 5, 20, 35)
        self.damage = 2
        self.original = 2
        self.critical = 5
        self.mana = 100 
        self.originalMana = 100 
        self.lose = False 
        self.range = False 
    
    def draw(self, screen):
        if self.visible:
            
            if not self.standing:
                if self.left:
                    screen.blit(l1, (self.x,self.y))
                elif self.right:
                    screen.blit(r1, (self.x,self.y))
            else:
                if self.left:
                    screen.blit(l1, (self.x, self.y))
                else:
                    screen.blit(r1, (self.x, self.y))
            #health bar
            #image from http://pixelartmaker.com/art/606ce310361b7da
            healthPic = pygame.image.load('images/health.png').convert_alpha()
            healthPic = pygame.transform.scale(healthPic, (50,50))
            screen.blit(healthPic, (350, 658))
            pygame.draw.rect(screen, (0, 0, 0), (389, 678, 600, 20))
            if self.health > 0:
                pygame.draw.rect(screen, (0, 128, 0), (389, 678, self.health*20, 20))
            else:
                pygame.draw.rect(screen, (0, 128, 0), (389, 678, 0, 20))
            self.hitbox = (self.x + 10, self.y + 5, 20, 35)
            #pygame font learned from https://nerdparadise.com/programming/pygame/part5
            font = pygame.font.SysFont('comicsansms', 20)
            text = font.render(str(champ.health) + '/' + str(champ.originalHealth), True, (255,255,255))
            screen.blit(text, (650, 670))
            #mana bar
            #image from https://www.youtube.com/watch?v=Z6_BVsrkF6I
            manaPic = pygame.image.load('images/mana.png').convert_alpha()
            manaPic = pygame.transform.scale(manaPic, (30,20))
            screen.blit(manaPic, (360, 698))
            pygame.draw.rect(screen, (0,0,0), (389, 698, 600, 20))
            pygame.draw.rect(screen, (0,0,255), (389, 698, 6*self.mana, 20))
            font = pygame.font.SysFont('comicsansms', 20)
            text = font.render(str(champ.mana) + '/' + str(champ.originalMana), True, (255,255,255))
            screen.blit(text, (650, 690))
            if self.range:
                pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 170, 1)
            
            
        else:
            self.lose = True 

    #player movement from https://stackoverflow.com/questions/38927892/pygame-move-a-object-to-mouse
    def update(self, mX, mY):
        dx = mX - self.x
        dy = mY - self.y
        angle = math.atan2(dy, dx)
        self.x += self.speed * math.cos(angle)
        self.y += self.speed * math.sin(angle)
    
    def hit(self, damage):
        if self.health > 0:
            self.health -= damage
        else:
            self.visible = False 

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.getMana = 3
        self.healthRegen = 1
        self.speed = 4
        self.walkCount = 0
        self.stop = True
        self.health = 30
        self.originalHealth = 30
        self.visible = True 
        self.stroke = False 
        self.hitbox = (self.x + 10 , self.y + 10, 15, 30)
        self.damage = 2
        self.original = 2
        self.critical = 5
        self.mana = 100 
        self.originalMana = 100 
        self.lose = False 
    
    def draw(self, screen):
        if self.visible:
            ePic = pygame.image.load('images/L1E.png').convert_alpha()
            ePic = pygame.transform.scale(ePic, (35,35))
            screen.blit(ePic, (self.x, self.y))
            #health bar
            pygame.draw.rect(screen, (0, 0, 0), (self.hitbox[0], self.hitbox[1] - 5, 30, 5))
            pygame.draw.rect(screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 5, 1*self.health, 5))
            #mana bar
            pygame.draw.rect(screen, (0, 0, 0), (self.hitbox[0], self.hitbox[1], 30, 5))
            pygame.draw.rect(screen, (0, 0, 255), (self.hitbox[0], self.hitbox[1], 0.3*self.mana, 5))
            self.hitbox = (self.x , self.y, 30, 40)
            # pygame.draw.rect(screen, (255,0,0), self.hitbox, 1)
            
        else:
            self.lose = True 
    
    def update(self, mX, mY):
        if not self.stop:
            dx = mX - self.x
            dy = mY - self.y
            angle = math.atan2(dy, dx)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
    
    def hit(self, damage):
        if self.health > 0:
            self.health -= damage
        else:
            self.visible = False 
       
class Minion(pygame.sprite.Sprite):
    def __init__(self, x, y, xSpeed, ySpeed, face):
        self.radius = 10
        self.x, self.y = x, y
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.face = face
        self.health = 20
        self.visible = True 
        self.hitbox = (self.x, self.y + 2, 20, 20)
        self.stop = False 
        self.qStroke = False 
        self.stroke = False 
        self.autos = []
        
    def draw(self, screen):
        allyMinionPic = pygame.image.load('images/allyMinion.png').convert_alpha()
        allyMinionPic = pygame.transform.scale(allyMinionPic, (20,20))
        enemyMinionPic = pygame.image.load('images/enemyMinion.png').convert_alpha()
        enemyMinionPic = pygame.transform.scale(enemyMinionPic, (20, 20))
        if self.face == 'left':
            minionPic = enemyMinionPic
        else:
            minionPic = allyMinionPic
        if self.visible:
            self.update()
            screen.blit(minionPic, (self.x, self.y))
            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0] - 10, self.hitbox[1] - 10, 30, 3))
            pygame.draw.rect(screen, (0, 128, 0), (self.hitbox[0] - 10, self.hitbox[1] - 10, 1.5*self.health, 3))
            self.hitbox = (self.x, self.y + 2, 20, 20)

    def update(self):
        if not self.stop:
            self.x += self.xSpeed
            self.y += self.ySpeed
    
    def hit(self, damage):
        if self.health > 0:
            self.health -= damage
        else:
            self.visible = False 
        

class autoAttacks(object):
    def __init__(self, x, y, speed, r,g,b):
        self.x = x 
        self.y = y
        self.color = (r,g,b)
        self.radius = 5
        self.speed = speed
        self.visible = True 
        self.start = False 
    
    def draw(self, screen):
        if self.visible:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, 1)
    
    def update(self, mouseX, mouseY):
        if self.visible:
            dx = mouseX - self.x
            dy = mouseY - self.y
            angle = math.atan2(dy, dx)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)

class Turret(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 50
        self.visible = True 
        self.hitbox = (self.x, self.y + 2, 50, 80)
        self.stroke = False 

    def draw(self, screen):
        if self.visible:
            #https://boards.na.leagueoflegends.com/en/c/skin-champion-concepts/WTVeA2n6-warden-nautilus-small-fat-blue-tower?show=flat
            allyTurret = pygame.image.load('images/allyTurret.png').convert_alpha()
            allyTurret = pygame.transform.scale(allyTurret, (50, 80))
            enemyNexus = pygame.image.load('images/enemyTurret.png').convert_alpha()
            enemyNexus = pygame.transform.scale(enemyNexus, (50, 80))
            if self.x < screenWidth/2:
                screen.blit(allyTurret, (self.x, self.y))
            else:
                screen.blit(enemyNexus, (self.x, self.y))
            pygame.draw.rect(screen, (255, 0, 0), (self.x , self.y - 10, 50, 5))
            pygame.draw.rect(screen, (0, 128, 0), (self.x , self.y - 10, 1*self.health, 5))
            
    def hit(self, damage):
        if self.health > 0:
            if self.health - damage >= 0:
                self.health -= damage
            else:
                self.visible = False 
        else:
            self.visible = False 

class Nexus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 50
        self.visible = True 
        self.hitbox = (self.x, self.y + 2, 100, 100)
        self.stroke = False 
        self.cStroke = False
        self.lose = False 
    
    def draw(self, screen):
        if self.visible:
            #images from https://leagueoflegends.fandom.com/wiki/Nexus
            allyNexus = pygame.image.load('images/allyNexus.png').convert_alpha()
            allyNexus = pygame.transform.scale(allyNexus, (100, 100))
            enemyNexus = pygame.image.load('images/enemyNexus.png').convert_alpha()
            enemyNexus = pygame.transform.scale(enemyNexus, (100,100))
            if self.x < screenWidth/2:
                screen.blit(allyNexus, (self.x, self.y))
            else:
                screen.blit(enemyNexus, (self.x, self.y))
            pygame.draw.rect(screen, (255, 0, 0), (self.x , self.y - 10, 100, 5))
            pygame.draw.rect(screen, (0, 128, 0), (self.x , self.y - 10, 2*self.health, 5))
            
    def hit(self, damage):
        if self.health > 0:
            self.health -= damage
        else:
            self.visible = False
            self.lose = True 

class Gold(pygame.sprite.Sprite):
    def __init__(self, x, y, gold):
        self.x = x
        self.y = y 
        self.gold = gold
    
    def draw(self, screen):
        #images from https://www.vectorstock.com/royalty-free-vector/coins-set-of-sprites-for-rotation-in-vector-20944564
        goldPic = pygame.image.load('images/gold.png').convert_alpha()
        goldPic = pygame.transform.scale(goldPic, (40, 40))
        screen.blit(goldPic, (self.x, self.y))
        font = pygame.font.SysFont('comicsansms', 50)
        text = font.render(str(self.gold), False, (255,255,255))
        screen.blit(text, (self.x + 20, self.y))

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def Boot(self):
        champ.speed += 3
        ggold.gold -= 10 
    
    def Sword(self):
        champ.damage += 1
        champ.original += 1
        ggold.gold -= 20 
    
    def AISword(self):
        enemyC.damage += 1
        enemyC.original += 1
        AIgold.gold -= 20 
    
    def draw(self, screen):
        #boot 
        #from https://boards.na.leagueoflegends.com/en/c/gameplay-balance/kEvjFFWL-boot-enchantments-idea
        bootPic = pygame.image.load('images/boot.png').convert_alpha()
        bootPic = pygame.transform.scale(bootPic, (80,80))
        screen.blit(bootPic, (self.x, self.y))
        font = pygame.font.SysFont('comicsansms', 20)
        text = font.render('10', False, (255,255,255))
        screen.blit(text, (self.x + 20, self.y))
        #sword
        #from https://www.reddit.com/r/Talonmains/comments/8p9asm/mods_asleep_upvote_local_longsword/
        swordPic = pygame.image.load('images/longSword.jpg').convert_alpha()
        swordPic = pygame.transform.scale(swordPic, (75,75))
        screen.blit(swordPic, (self.x + 80, self.y))
        font = pygame.font.SysFont('comicsansms', 20)
        text = font.render('20', False, (255,255,255))
        screen.blit(text, (self.x + 90, self.y))
        #champ speed
        font = pygame.font.SysFont('comicsansms', 20)
        text = font.render('speed = ' + str(champ.speed), False, (255,255,255))
        screen.blit(text, (self.x, self.y + 120))
        #champ damage
        font = pygame.font.SysFont('comicsansms', 20)
        text = font.render('damage = ' + str(champ.damage), False, (255,255,255))
        screen.blit(text, (self.x + 100, self.y + 120))


################

item = Item(650, 600)
ggold = Gold(350, 600, 0)
AIgold = Gold(0,0,0)
AIitem = Item(600,0)
champ = Player(300,500)
enemyC = Enemy(950, 160)
allyNexus = Nexus(200, 553)
enemyNexus = Nexus(950, 160)
enemyTurret = Turret(800, 230)
allyTurret = Turret(400, 500)
allyMinion = Minion(290, 403, 3, -1, 'right')
enemyMinion = Minion(1500, 60, -3, 1, 'left')
bg = Background(0,0)
autos = []
eAutos = []
allyTurretAutos = []
enemyTurretAutos = []
eCooldown = 0
qCooldown = 0 
eAvailable = True
AIeAvailable = True
AIqAvailable = True 
qAvailable = True 
healAvailable = True
AIhealAvailable = True

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def redrawGameWindow():
    bg.draw(screen)
    enemyTurret.draw(screen)
    enemyNexus.draw(screen)
    allyNexus.draw(screen)
    enemyC.draw(screen)
    ggold.draw(screen)
    for enemy in enemyMinions:
        enemy.draw(screen)
        for auto in enemy.autos:
            if enemy.visible:
                auto.draw(screen)
        enemy.update()
    
    for ally in allyMinions:
        ally.draw(screen)
        for auto in ally.autos:
            if ally.visible:
                auto.draw(screen)
        ally.update()
    champ.draw(screen)
    for auto in autos:
        auto.draw(screen)
    
    for auto in eAutos:
        auto.draw(screen)
    
    if allyTurret.visible:
        for auto in allyTurretAutos:
            auto.draw(screen)
    
    if enemyTurret.visible:
        for auto in enemyTurretAutos:
            auto.draw(screen)
    allyTurret.draw(screen)
    #e skill
    #https://www.memrise.com/course/1594760/league-of-legends/3/
    eSkillPic = pygame.image.load('images/ghost.png').convert_alpha()
    eSkillUsed = pygame.image.load('images/ghostUsed.png').convert_alpha()
    if eAvailable:
        screen.blit(eSkillPic, (450, 600))
    else:
        screen.blit(eSkillUsed, (450, 600))
    font = pygame.font.SysFont('comicsansms', 20)
    text = font.render('30', False, (255,255,255))
    screen.blit(text, (450, 600))
    text = font.render('E', False, (255,255,255))
    screen.blit(text, (500, 600))
    #q skill
    #from http://www.surrenderat20.net/p/49-pbe-cycle.html
    qSkillPic = pygame.image.load('images/qSkill.jpg').convert_alpha()
    qSkillPic = pygame.transform.scale(qSkillPic, (75, 75))
    qSkillUsed = pygame.image.load('images/qSkillUsed.jpg').convert_alpha()
    qSkillUsed = pygame.transform.scale(qSkillUsed, (75, 75))
    if qAvailable:
        screen.blit(qSkillPic, (550, 600))
    else:
        screen.blit(qSkillUsed, (550, 600))
    font = pygame.font.SysFont('comicsansms', 20)
    text = font.render('30', False, (255,255,255))
    screen.blit(text, (550, 600))
    text = font.render('Q', False, (255,255,255))
    screen.blit(text, (600, 600))
    
    #heal spell
    #from https://www.mobafire.com/league-of-legends/build/anivia-build-mid-8-8-529835
    healPic = pygame.image.load('images/heal.png').convert_alpha()
    healPic = pygame.transform.scale(healPic, (75,75))
    healUsedPic = pygame.image.load('images/healUsed.png').convert_alpha()
    healUsedPic = pygame.transform.scale(healUsedPic, (75,75))
    if healAvailable:
        screen.blit(healPic, (850, 600))
    else:
        screen.blit(healUsedPic, (850,600))
    font = pygame.font.SysFont('comicsansms', 20)
    text = font.render('F', False, (255,255,255))
    screen.blit(text, (900, 600))
    
    
    #AI
    if enemyC.visible:
        if AIhealAvailable:
            screen.blit(healPic, (750, 100))
        else:
            screen.blit(healUsedPic, (750,100))
            
        if AIqAvailable:
            screen.blit(qSkillPic, (550, 100))
        else:
            screen.blit(qSkillUsed, (550, 100))
        
        if AIeAvailable:
            screen.blit(eSkillPic, (650, 100))
        else:
            screen.blit(eSkillUsed, (650, 100))
        pygame.draw.rect(screen, (0,0,0), (550,10,270,90))
        #AI speed
        font = pygame.font.SysFont('comicsansms', 20)
        text = font.render('AI speed = ' + str(enemyC.speed), False, (255,255,255))
        screen.blit(text, (650, 10))
        #AI damage
        
        font = pygame.font.SysFont('comicsansms', 20)
        text = font.render('AI damage = ' + str(enemyC.damage), False, (255,255,255))
        screen.blit(text, (650, 50))
        ePic = pygame.image.load('images/L1E.png').convert_alpha()
        ePic = pygame.transform.scale(ePic, (80,80))
        screen.blit(ePic, (550, 10))
        
    
    #item 
    item.draw(screen)
    
    #intro
    #from https://www.dvsgaming.org/huge-changes-coming-to-league-of-legends-in-2019/
    if count <= 10:
        pygame.draw.rect(screen, (0,0,0), (0,0,screenWidth,screenHeight))
        logo = pygame.image.load('images/leagueLogo.png').convert_alpha()
        screen.blit(logo, (100,50))
    
    #victory
    #from https://boards.euw.leagueoflegends.com/en/c/champions-gameplay-en/OvKTF29N-additional-winning-possibility-suggestion
    if enemyNexus.lose:
        pygame.draw.rect(screen, (0,0,0), (0,0,screenWidth,screenHeight))
        winBg = pygame.image.load('images/victory.png').convert_alpha()
        screen.blit(winBg, (100,50))
    
    #defeat
    #from https://www.redbubble.com/people/commongeek/works/29473659-lol-defeat-logo?p=poster
    elif allyNexus.lose or champ.lose:
        pygame.draw.rect(screen, (0,0,0), (0,0,screenWidth,screenHeight))
        loseBg = pygame.image.load('images/defeat.jpg').convert_alpha()
        screen.blit(loseBg, (350,50))
    
    pygame.display.update()

#https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-tutorial-movement/
def champMoving():
    keys = pygame.key.get_pressed()
    if 350 < champ.x < 880:
        if -0.5*(champ.x-381) + 450 > champ.y + champ.speed:
            if keys[pygame.K_d]:
                champ.x += champ.speed
                champ.standing = False
                champ.left = False
                champ.right = True 
            if keys[pygame.K_s]:
                champ.y += champ.speed
                champ.standing = False
        elif -0.5*(champ.x-381) + 450 <= champ.y + champ.speed <= -0.5*(champ.x-436) + 530:
            if keys[pygame.K_a]:
                champ.x -= champ.speed
                champ.standing = False
                champ.left = True
                champ.right = False 
            if keys[pygame.K_d]:
                champ.x += champ.speed
                champ.standing = False
                champ.left = False
                champ.right = True 
            if keys[pygame.K_w]:
                champ.y -= champ.speed
                champ.standing = False
            if keys[pygame.K_s]:
                champ.y += champ.speed
                champ.standing = False
        elif champ.y + champ.speed > -0.5*(champ.x-436) + 530:
            if keys[pygame.K_a]:
                champ.x -= champ.speed
                champ.standing = False
                champ.left = True
                champ.right = False 
            if keys[pygame.K_w]:
                champ.y -= champ.speed
                champ.standing = False
    else:
        if keys[pygame.K_a]:
            champ.x -= champ.speed
            champ.standing = False
            champ.left = True
            champ.right = False 
        if keys[pygame.K_d]:
            champ.x += champ.speed
            champ.standing = False
            champ.left = False
            champ.right = True 
        if keys[pygame.K_w]:
            champ.y -= champ.speed
            champ.standing = False
        if keys[pygame.K_s]:
            champ.y += champ.speed
            champ.standing = False
        
def autoHelper(autoA, target, damage):
    for auto in autoA:
        if target.visible:
            if auto.y - auto.radius < target.hitbox[1] + target.hitbox[3] and auto.y + auto.radius > target.hitbox[1]:
                if auto.x - auto.radius > target.hitbox[0] and auto.x - auto.radius < target.hitbox[0] + target.hitbox[2]:
                    if len(autoA) >= 1:
                        target.hit(damage)
                        autoA.pop()
                        target.stroke = False
                        auto.visible = False

def champAutoHelper(autoA, target, damage):
    for auto in autoA:
        if target.visible:
            if auto.y - auto.radius < target.hitbox[1] + target.hitbox[3] and auto.y + auto.radius > target.hitbox[1]:
                if auto.x - auto.radius > target.hitbox[0] and auto.x - auto.radius < target.hitbox[0] + target.hitbox[2]:
                    if len(autoA) >= 1:
                        target.hit(damage)
                        autoA.pop()
                        auto.visible = False
            

def collision():
    for enemy in enemyMinions:
        for ally in allyMinions:
            autoHelper(ally.autos, enemy, 1)
    for ally in allyMinions:
        for enemy in enemyMinions:
            autoHelper(enemy.autos, ally, 1)
    
    for ally in allyMinions:
        autoHelper(ally.autos, enemyTurret, 1)
        champAutoHelper(enemyTurretAutos, ally, 5)
        autoHelper(ally.autos, enemyNexus, 1)
        autoHelper(ally.autos, enemyC, 1)
        champAutoHelper(eAutos, ally, enemyC.damage)
    
    for enemy in enemyMinions:
        autoHelper(enemy.autos, allyNexus, 1)
        autoHelper(enemy.autos, allyTurret, 1)
        champAutoHelper(allyTurretAutos, enemy, 5)
        # autoHelper(enemy.autos, champ, 1)
        champAutoHelper(autos, enemy, champ.damage)
    champAutoHelper(autos, enemyC, champ.damage)
    
    autoHelper(enemyTurretAutos, champ, 5)
    autoHelper(allyTurretAutos, enemyC, 5)
    champAutoHelper(autos, enemyTurret, champ.damage)
    # champAutoHelper(eAutos, champ, enemyC.damage)

    champAutoHelper(autos, enemyNexus, champ.damage)
    champAutoHelper(eAutos, allyTurret, enemyC.damage)
    champAutoHelper(eAutos, allyNexus, enemyC.damage)

######minions###########
def allyAuto():
    for ally in allyMinions:
        for auto in ally.autos:
            if not auto.start:
                auto.x = ally.x + 15
                auto.y = ally.y + 15
            else:
                for enemy in enemyMinions:
                    if enemy.stroke:
                        if enemy.visible:
                            auto.update(enemy.x + 10, enemy.y + 10)
                        else:
                            ally.autos.pop()
                if enemyTurret.stroke:
                    if enemyTurret.visible:
                        auto.update(enemyTurret.x + 20, enemyTurret.y + 40)
                    else:
                        ally.autos.pop()
                elif enemyNexus.stroke:
                    if enemyNexus.visible:
                        auto.update(enemyNexus.x + 20, enemyNexus.y + 40)
                    else:
                        ally.autos.pop()

def enemyAuto():
    for enemy in enemyMinions:
        if enemy.visible:
            for auto in enemy.autos:
                if not auto.start:
                    auto.x = enemy.x + 15
                    auto.y = enemy.y + 15
                else:
                    for ally in allyMinions:
                        if ally.visible:
                            if ally.stroke:
                                auto.update(ally.x + 10, ally.y + 10)
                        else:
                            enemy.autos.pop()
                            auto.start = False 
                    if allyTurret.stroke:
                        if allyTurret.visible:
                            auto.update(allyTurret.x, allyTurret.y + 40)
                        else:
                            enemy.autos.pop()
                    if allyNexus.stroke:
                        if allyNexus.visible:
                            auto.update(allyNexus.x , allyNexus.y + 40)
                        else:
                            enemy.autos.pop()

def allyAttackEnemy():
    for ally in allyMinions:
        if ally.visible:
            for auto in ally.autos:
                for enemy in enemyMinions:
                    if enemy.stroke:
                        if enemy.visible:
                            auto.update(enemy.x + 10, enemy.y + 10)
                        else:
                            auto.start = False
            for enemy in enemyMinions:
                if enemy.visible:
                    if distance(ally.x, ally.y, enemy.x, enemy.y) < 150 and enemy.visible:
                        if len(ally.autos) == 0:
                            auto = autoAttacks(ally.x + 20, ally.y, 4, 66,200,244)
                            auto.start = True
                            enemy.stroke = True 
                            ally.autos.append(auto)

def allyAttackEnemyChamp():
    for ally in allyMinions:
        if ally.visible:
            for auto in ally.autos:
                if enemyC.stroke:
                    if enemyC.visible:
                        auto.update(enemyC.x + 10, enemyC.y + 10)
                    else:
                        auto.start = False
                        ally.autos.pop()
            for enemy in enemyMinions:
                if distance(ally.x, ally.y, enemy.x, enemy.y) > 150:
                    if distance(ally.x, ally.y, enemyC.x, enemyC.y) < 150: 
                        if enemyC.visible:
                            if len(ally.autos) == 0:
                                auto = autoAttacks(ally.x + 20, ally.y, 4, 66,200,244)
                                auto.start = True
                                enemyC.stroke = True 
                                ally.autos.append(auto)

def enemyAttackChamp():
    for enemy in enemyMinions:
        if enemy.visible:
            for auto in enemy.autos:
                if champ.stroke:
                    if champ.visible:
                        auto.update(champ.x + 10, champ.y + 10)
                    else:
                        auto.start = False 
                        enemy.autos.pop()
            for ally in allyMinions:
                if distance(enemy.x, enemy.y, champ.x, champ.y) < 150:
                    if len(enemy.autos) == 0:
                        auto = autoAttacks(enemy.x + 20, enemy.y, 4, 244,65,65)
                        auto.start = True
                        champ.stroke = True 
                        enemy.autos.append(auto)

def enemyAttackAlly():
    for enemy in enemyMinions:
        if enemy.visible:
            for auto in enemy.autos:
                for ally in allyMinions:
                    if ally.stroke:
                        if ally.visible:
                            auto.update(ally.x + 10, ally.y + 10)
                        else:
                            auto.start = False 
            for ally in allyMinions:
                if ally.visible:
                    if distance(ally.x, ally.y, enemy.x, enemy.y) < 150:
                        if len(enemy.autos) == 0:
                            auto = autoAttacks(enemy.x + 10, enemy.y + 10, 4, 244, 65, 65)
                            auto.start = True
                            ally.stroke = True
                            enemy.autos.append(auto)

########### minions, AI movement ##############

def AImove():
    if allyTurret.visible:
        if distance(allyTurret.x, allyTurret.y, enemyC.x, enemyC.y) < 150:
            enemyC.stop = True
    else:
        enemyC.stop = False
    
    if allyNexus.visible:
        if distance(allyNexus.x, allyNexus.y, enemyC.x, enemyC.y) < 150:
            enemyC.stop = True
    else:
        enemyC.stop = False 
    
    if not enemyC.stop:
        if enemyC.health >= enemyC.originalHealth/3:
            enemyC.update(allyNexus.x, allyNexus.y)
        else:
            enemyC.update(enemyTurret.x, enemyTurret.y)
    
  
    for ally in allyMinions:
        if distance(ally.x, ally.y, enemyC.x, enemyC.y) < 170:
            enemyC.stop = True
        else:
            enemyC.stop = False 

def move():
    
    for enemy in enemyMinions:              
        for ally in allyMinions:
            if distance(ally.x, ally.y, enemy.x, enemy.y) < 150:
                if ally.visible:
                    enemy.stop = True
                    ally.stop = True 
                else:
                    allyMinions.remove(ally)
            else:
    
                enemy.stop = False 
    
    for ally in allyMinions:
        for enemy in enemyMinions:
            if distance(ally.x, ally.y, enemy.x, enemy.y) < 150:
                if enemy.visible:
                    ally.stop = True
                    enemy.stop = True 
                else:
                    enemyMinions.remove(enemy)
            else:
                if distance(ally.x, ally.y, enemyC.x, enemyC.y) < 150:
                    if ally.visible:
                        enemyC.stop = True 
                    if enemyC.visible:
                        if len(enemyMinions) <= 1:
                            ally.stop = True
                    else:
                        ally.stop = False 
    for ally in allyMinions:
        if distance(ally.x, ally.y, enemyC.x, enemyC.y) < 170:
            if ally.visible:
                if enemyC.visible:
                    enemyC.stop = True 

    if len(enemyMinions) == 0:
        for ally in allyMinions:
            ally.stop = False 
    
    if len(allyMinions) == 0:
        for enemy in enemyMinions:
            enemy.stop = False 
            if enemyC.visible:
                enemyC.stop = False 
    
    for enemy in enemyMinions:
        if distance(enemy.x, enemy.y, allyTurret.x, allyTurret.y) < 150:
            if not enemyTurret.visible:
                for auto in enemy.autos:
                    auto.start = False 
        # for ally in allyMinions:
        #     if distance(enemy.x, enemy.y, ally.x, ally.y) < 150:
        #         if not ally.visible:
        #             for auto in enemy.autos:
        #                 auto.start = False 

    if not enemyC.stop:
        eAutos = []
    
    #enemy turret
    for ally in allyMinions:
        if enemyTurret.visible:
            if distance(ally.x, ally.y, enemyTurret.x, enemyTurret.y) < 150:
                ally.stop = True
            else:
                enemyTurretAutos = []
        else:
            enemy.stop = False 
            for enemy in enemyMinions:
                if distance(enemy.x, enemy.y, ally.x, ally.y) < 150:
                    ally.stop = True 
                else:
                    ally.stop = False 
        if distance(ally.x, ally.y, enemyTurret.x, enemyTurret.y) < 150:
            if not ally.visible:
                allyMinions.remove(ally)
    
    #ally turret
    for enemy in enemyMinions:
        if allyTurret.visible:
            if distance(enemy.x, enemy.y, allyTurret.x, allyTurret.y) < 150:
                enemy.stop = True
        else:
            enemy.stop = False
            
            for ally in allyMinions:
                if distance(enemy.x, enemy.y, ally.x, ally.y) < 150:
                    enemy.stop = True 
                else:
                    enemy.stop = False 
        if distance(enemy.x, enemy.y, allyTurret.x, allyTurret.y) < 150:
            if not enemy.visible:
                enemyMinions.remove(enemy)
    #enemy nexus
    for ally in allyMinions:
        if enemyNexus.visible:
            if distance(ally.x, ally.y, enemyNexus.x, enemyNexus.y) < 150:
                ally.stop = True
        else:
            for enemy in enemyMinions:
                if distance(enemy.x, enemy.y, ally.x, ally.y) < 150:
                    ally.stop = True 
                else:
                    ally.stop = False 
            if distance(enemyC.x, enemyC.y, ally.x, ally.y) < 150:
                ally.stop = True
            else:
                ally.stop = False 
    
    #ally Nexus 
    for enemy in enemyMinions:
        if allyNexus.visible:
            if distance(enemy.x, enemy.y, allyNexus.x, allyNexus.y) < 150:
                enemy.stop = True
        else:
            for ally in allyMinions:
                if distance(enemy.x, enemy.y, ally.x, ally.y) < 150:
                    enemy.stop = True 
                else:
                    enemy.stop = False 
    #when moving, the auto attacks disappear 
    # for ally in allyMinions:
    #     if not ally.stop:
    #         ally.autos = []
    
    for enemy in enemyMinions:
        if not enemy.stop:
            enemy.autos = []

########### AI ##############

def enemyChampAuto():
    if enemyC.visible:
        for auto in eAutos:
            if not auto.start:
                auto.x = enemyC.x + 15
                auto.y = enemyC.y + 15
            else:
                for ally in allyMinions:
                    if ally.visible:
                        if ally.stroke:
                            auto.update(ally.x + 10, ally.y + 10)
                    else:
                        eAutos.pop()
                if allyTurret.stroke:
                    if allyTurret.visible:
                        auto.update(allyTurret.x + 20, allyTurret.y + 40)
                    else:
                        eAutos.pop()
                if allyNexus.stroke:
                    if allyNexus.visible:
                        auto.update(allyNexus.x + 20, allyNexus.y + 40)
                    else:
                        eAutos.pop()

def enemyChampAttackAlly():
    if enemyC.visible:
        for auto in eAutos:
            for ally in allyMinions:
                if ally.stroke:
                    if ally.visible:
                        auto.update(ally.x + 10, ally.y + 10)
                    else:
                        auto.start = False 
                        eAutos.pop()
        for ally in allyMinions:
            if ally.visible:
                if distance(ally.x, ally.y, enemyC.x, enemyC.y) < 170:
                    if len(eAutos) == 0:
                        auto = autoAttacks(enemyC.x + 10, enemyC.y + 10, 6, 244, 65, 65)
                        auto.start = True
                        ally.stroke = True
                        eAutos.append(auto)

def enemyChampAttackTurret():
    if enemyC.visible:
        if distance(enemyC.x, enemyC.y, allyTurret.x, allyTurret.y) < 170:
            if len(eAutos) == 0:
                auto = autoAttacks(enemyC.x, enemyC.y, 6, 244, 65, 65)
                auto.start = True
                allyTurret.stroke = True
                eAutos.append(auto)
        for auto in eAutos:
            if allyTurret.stroke:
                if allyTurret.visible:
                    auto.update(allyTurret.x + 20, allyTurret.y + 40)
                else:
                    eAutos.pop()
                    allyTurret.stroke = False 

def enemyChampAttackChamp():
    if enemyC.visible:
        if distance(enemyC.x, enemyC.y, champ.x, champ.y) < 170:
            if len(eAutos) == 0:
                auto = autoAttacks(enemyC.x, enemyC.y, 6, 244, 65, 65)
                auto.start = True
                champ.stroke = True
                eAutos.append(auto)
        for auto in eAutos:
            if champ.stroke:
                auto.update(champ.x + 20, champ.y + 30)
            else:
                eAutos.pop()
                champ.stroke = False 

##########turret & nexus ###############

def turretAttackChamp():
    if enemyTurret.visible:
        if distance(enemyTurret.x, enemyTurret.y, champ.x, champ.y) < 170:
            if len(enemyTurretAutos) == 0:
                auto = autoAttacks(enemyTurret.x + 20, enemyTurret.y + 20, 7, 244,65,65)
                auto.start = True
                champ.stroke = True 
                enemyTurretAutos.append(auto)
        for auto in enemyTurretAutos:
            if champ.stroke:
                auto.update(champ.x + 10, champ.y + 20)

def turretAttackEnemyChamp():
    if allyTurret.visible:
        if distance(allyTurret.x, allyTurret.y, enemyC.x, enemyC.y) < 170:
            if  len(allyTurretAutos) == 0:
                auto = autoAttacks(allyTurret.x + 20, allyTurret.y + 20, 7, 66, 200, 244)
                auto.start = True
                enemy.stroke = True
                allyTurretAutos.append(auto)

        for auto in allyTurretAutos:
            if distance(allyTurret.x, allyTurret.y, enemyC.x, enemyC.y) < 170:
                if enemyC.stroke:
                    if enemyC.visible:
                    
                        auto.update(enemyC.x + 10, enemyC.y + 10)

def turretAttackEnemyMinion():
    if allyTurret.visible:
        for enemy in enemyMinions:
            if enemy.visible:
                if distance(allyTurret.x, allyTurret.y, enemy.x, enemy.y) < 170:
                    if len(allyTurretAutos) == 0:
                        auto = autoAttacks(allyTurret.x + 20, allyTurret.y + 20, 7, 66, 200, 244)
                        auto.start = True
                        enemy.stroke = True
                        allyTurretAutos.append(auto)

        for auto in allyTurretAutos:
            for enemy in enemyMinions:
                if distance(allyTurret.x, allyTurret.y, enemy.x, enemy.y) < 170:
                    if enemy.stroke:
                        if enemy.visible:
                        
                            auto.update(enemy.x + 10, enemy.y + 10)

def turretAttackAllyMinion():
    if enemyTurret.visible:
        for ally in allyMinions:
            if ally.visible:
                if distance(enemyTurret.x, enemyTurret.y, ally.x, ally.y) < 170:
                    if len(enemyTurretAutos) == 0:
                        auto = autoAttacks(enemyTurret.x + 20, enemyTurret.y + 20, 7, 244, 65, 65)
                        auto.start = True
                        ally.stroke = True
                        enemyTurretAutos.append(auto)
                for auto in enemyTurretAutos:
                    for ally in allyMinions:
                        if distance(enemyTurret.x, enemyTurret.y, ally.x, ally.y) < 170:
                            if ally.stroke:
                                if ally.visible:
                                    auto.update(ally.x + 10, ally.y + 10)
                                else:
                                    enemyTurretAutos.pop()
                                    ally.stroke = False

def enemyMinionAttackTurret():
    if allyTurret.visible:
        for enemy in enemyMinions:
            if enemy.visible:
                for auto in enemy.autos:
                    
                    if allyTurret.stroke:
                        if allyTurret.visible:
                            auto.update(allyTurret.x + 20, allyTurret.y + 40)
                    
                        else:
                            enemy.autos.pop()
                            allyTurret.stroke = False 
                if distance(enemy.x, enemy.y, allyTurret.x, allyTurret.y) < 150:
                    if len(enemy.autos) == 0:
                        auto = autoAttacks(enemy.x, enemy.y, 4, 244, 65, 65)
                        auto.start = True
                        allyTurret.stroke = True
                        enemy.autos.append(auto) 
         
def allyMinionAttackTurret():
    for ally in allyMinions:
        if ally.visible:
            if distance(ally.x, ally.y, enemyTurret.x, enemyTurret.y) < 150:
                if len(ally.autos) == 0:
                    auto = autoAttacks(ally.x, ally.y, 4, 66, 200, 244)
                    auto.start = True
                    enemyTurret.stroke = True
                    ally.autos.append(auto)
            for auto in ally.autos:
                if enemyTurret.stroke:
                    if enemyTurret.visible:
                        auto.update(enemyTurret.x + 20, enemyTurret.y + 40)
                    else:
                        ally.autos.pop()

def enemyMinionAttackNexus():
    for enemy in enemyMinions:
        if enemy.visible:
            if distance(enemy.x, enemy.y, allyNexus.x, allyNexus.y) < 150:
                if len(enemy.autos) == 0:
                    auto = autoAttacks(enemy.x + 10, enemy.y + 10, 4, 244, 65, 65)
                    auto.start = True
                    allyNexus.stroke = True
                    enemy.autos.append(auto) 
            for auto in enemy.autos:
                if allyNexus.stroke:
                    if allyNexus.visible:
                        auto.update(allyNexus.x + 20, allyNexus.y + 40)
                    else:
                        enemy.autos.pop()

def allyMinionAttackNexus():
    for ally in allyMinions:
        if ally.visible:
            if distance(ally.x, ally.y, enemyNexus.x, enemyNexus.y) < 150:
                if len(ally.autos) == 0:
                    auto = autoAttacks(ally.x + 10, ally.y + 10, 4, 66, 200, 244)
                    auto.start = True
                    enemyNexus.stroke = True
                    ally.autos.append(auto) 
            for auto in ally.autos:
                if enemyNexus.stroke:
                    if enemyNexus.visible:
                        auto.update(enemyNexus.x + 20, enemyNexus.y + 40)
                    else:
                        ally.autos.pop()

################## player ###############

def champAuto():
    for auto in autos:
        if not auto.start:
            auto.x = champ.x + 15
            auto.y = champ.y + 15
        else:
            for enemy in enemyMinions:
                if enemy.visible:
                    if enemy.stroke:
                        auto.update(enemy.x + 10, enemy.y + 10)
                else:
                    autos.pop()
            if enemyC.stroke:
                if enemyC.visible:
                    auto.update(enemyC.x + 15, enemyC.y + 10)
                else:
                    autos.pop()
            if enemyTurret.stroke:
                if enemyTurret.visible:
                    auto.update(enemyTurret.x + 20, enemyTurret.y + 40)
            if enemyNexus.stroke:
                if enemyNexus.visible:
                    auto.update(enemyNexus.x + 20, enemyNexus.y + 40)
                
def champAttackMinion(mouseX, mouseY):
    for enemy in enemyMinions:
        if enemy.visible:
            if distance(champ.x, champ.y, enemy.x, enemy.y) < 170:
                        if mouseY < enemy.hitbox[1] + enemy.hitbox[3]  and mouseY > enemy.hitbox[1]:
                            if mouseX > enemy.hitbox[0] and mouseX < enemy.hitbox[0] + enemy.hitbox[2]:
                                if len(autos) == 0:
                                    enemy.stroke = True 
                                    auto = autoAttacks(champ.x+10, champ.y+10, 10,138, 43, 226)
                                    auto.start = True 
                                    autos.append(auto)

def champAttackAI(mouseX, mouseY):
        if enemyC.visible:
            if distance(champ.x, champ.y, enemyC.x, enemyC.y) < 170:
                        if mouseY < enemyC.hitbox[1] + enemyC.hitbox[3]  and mouseY > enemyC.hitbox[1]:
                            if mouseX > enemyC.hitbox[0] and mouseX < enemyC.hitbox[0] + enemyC.hitbox[2]:
                                if len(autos) == 0:
                                    enemyC.stroke = True 
                                    auto = autoAttacks(champ.x+10, champ.y+10, 10,138, 43, 226)
                                    auto.start = True 
                                    autos.append(auto)

def champAttackTurret(mouseX, mouseY):
    if enemyTurret.visible:
        if distance(champ.x, champ.y, enemyTurret.x, enemyTurret.y) < 170:
            if mouseY < enemyTurret.hitbox[1] + enemyTurret.hitbox[3]  and mouseY > enemyTurret.hitbox[1]:
                        if mouseX > enemyTurret.hitbox[0] and mouseX < enemyTurret.hitbox[0] + enemyTurret.hitbox[2]:
                            if len(autos) == 0:
                                auto = autoAttacks(champ.x+10, champ.y+10, 10, 138, 43, 226)
                                auto.start = True
                                enemyTurret.stroke = True
                                autos.append(auto)

def champAttackNexus(mouseX, mouseY):
    if enemyNexus.visible:
        if distance(champ.x, champ.y, enemyNexus.x, enemyNexus.y) < 170:
            if mouseY < enemyNexus.hitbox[1] + enemyNexus.hitbox[3]  and mouseY > enemyNexus.hitbox[1]:
                        if mouseX > enemyNexus.hitbox[0] and mouseX < enemyNexus.hitbox[0] + enemyNexus.hitbox[2]:
                            if len(autos) == 0:
                                auto = autoAttacks(champ.x+10, champ.y+10, 10, 138, 43, 226)
                                auto.start = True
                                enemyNexus.stroke = True
                                autos.append(auto)

#############################

minionMoveCount = 0
enemyMinionMoveCount = 0 
count = 0
wave = 0 
eUsing = False 
AIeUsing = False 
lastUsedE = 0 
AIlastUsedE = 0
qUsing = False
AIqUsing = False 
lastUsedQ = 0 
AIlastUsedQ = 0 
AIeCooldown = 0
AIqCooldown = 0
playing = True


while playing:
    clock.tick(50)
    count += 1
    if count == 40:
        enemyC.stop = False 
    if count % 20 == 0:
        if champ.mana <= champ.originalMana - champ.getMana:
            champ.mana += champ.getMana 
        if enemyC.mana <= enemyC.originalMana - enemyC.getMana:
            enemyC.mana += enemyC.getMana 
    
    if count % 40 == 0:
        if champ.health <= champ.originalHealth - champ.healthRegen:
            champ.health += champ.healthRegen
        if enemyC.health <= enemyC.originalHealth - enemyC.healthRegen:
            enemyC.health += enemyC.healthRegen
        
    now = pygame.time.get_ticks()
    nowQ = pygame.time.get_ticks()
    nowAI = pygame.time.get_ticks()
    nowQAI = pygame.time.get_ticks()
    if count % 10 == 0:
        ggold.gold += 1
        AIgold.gold += 1
    ##minion wave ##
    #each minion spawns every second in total of 6 minions
    if minionMoveCount <= 2:
        if count % 20 == 0:
            minionMoveCount += 1
            xspeed = 1.8
            yspeed = 1
            allyMinion = Minion(minionX, minionY - minionMoveCount*10, xspeed, -yspeed,'right')
            allyMinions.append(allyMinion)
    if enemyMinionMoveCount <= 2:
        if count % 20 == 0:
            enemyMinionMoveCount += 1
            xspeed = 1.8
            yspeed = 1
            enemyMinion = Minion(enemyX, enemyY - enemyMinionMoveCount*10, -xspeed, yspeed, 'left')
            enemyMinions.append(enemyMinion)
    if len(enemyMinions) == 0:
        enemyMinionMoveCount = 0 
    if len(allyMinions) == 0:
        minionMoveCount = 0 
    #collision
    collision()
    ##events##
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouseX, mouseY = event.pos
            champAttackMinion(mouseX, mouseY)
            champAttackAI(mouseX, mouseY)
            champAttackTurret(mouseX, mouseY)
            champAttackNexus(mouseX, mouseY)
    
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseX, mouseY = event.pos
            if 650  < mouseX < 650 + 80:
                if 600 < mouseY < 600 + 80:
                    if ggold.gold >= 10:
                        item.Boot()
            elif 650 + 80 < mouseX < 650 + 160:
                if 600 < mouseY < 600 + 80:
                    if ggold.gold >= 20:
                        item.Sword()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            champ.range = True
        else:
            champ.range = False 
        
        if keys[pygame.K_f]:
            if healAvailable:
                if champ.health <= champ.originalHealth*0.5:
                    champ.health += 10
                    healAvailable = False 
            
        
        if keys[pygame.K_q]:
            if not qUsing and nowQ - lastUsedQ > qCooldown and champ.mana - 30 >= 0:
                champ.damage = champ.critical
                champ.mana -= 30 
                lastUsedQ = nowQ
                qUsing = True
                qCooldown = 7000
        if nowQ - lastUsedQ <= qCooldown:
            qAvailable = False
        else:
            qAvailable = True
        if qUsing and nowQ - lastUsedQ > 4000:
            champ.damage = champ.original
            qUsing = False 
        if keys[pygame.K_e]:
            if not eUsing and now - lastUsedE > eCooldown and champ.mana - 30 >= 0:
                champ.speed += 2
                champ.mana -= 30
                lastUsedE = now 
                eUsing = True 
                eCooldown = 10000
        if now - lastUsedE <= eCooldown:
            eAvailable = False 
        else:
            eAvailable = True 
        if eUsing and now - lastUsedE > 3000:
            champ.speed -= 3
            eUsing = False
        
        #AI Q skill 
        if count >= 100:
            if enemyC.mana >= enemyC.originalMana * 0.5:
                if enemyC.health >= enemyC.originalHealth*0.5:
                    if not AIqUsing and nowQAI - AIlastUsedQ > AIqCooldown and enemyC.mana - 30 >= 0:
                        enemyC.damage = enemyC.critical
                        enemyC.mana -= 30 
                        AIlastUsedQ = nowQAI
                        AIqUsing = True
                        AIqCooldown = 7000
            
            if nowQAI - AIlastUsedQ <= AIqCooldown:
                AIqAvailable = False
            else:
                AIqAvailable = True
            if AIqUsing and nowQAI - AIlastUsedQ > 4000:
                enemyC.damage = enemyC.original
                AIqUsing = False 
    
    #buy sword
    if AIgold.gold >= 20:
        AIitem.AISword()
    #heal
    if AIhealAvailable:
        if enemyC.health <= enemyC.originalHealth*0.3:
            enemyC.health += 10
            AIhealAvailable = False 
    
    if not enemyC.visible:
        eAutos = []
    
    
    
    
    for auto in autos:
        for enemy in enemyMinions:
            if enemy.stroke:
                if enemy.visible:
                    auto.update(enemy.x + 10, enemy.y + 10)
                else:
                    auto.start = False
                    autos.pop()
    champAuto()
    enemyChampAuto()
    champMoving()
    move()
    AImove()
    allyAuto()
    allyAttackEnemy()
    enemyAuto()
    enemyAttackAlly()
    turretAttackEnemyMinion()
    turretAttackAllyMinion()
    turretAttackChamp()
    turretAttackEnemyChamp()
    enemyMinionAttackTurret()
    allyMinionAttackTurret()
    allyAttackEnemyChamp()
    enemyMinionAttackNexus()
    allyMinionAttackNexus()
    enemyChampAttackAlly()
    enemyChampAttackTurret()
    
    
    
    ##draw##
    redrawGameWindow()

pygame.quit()

