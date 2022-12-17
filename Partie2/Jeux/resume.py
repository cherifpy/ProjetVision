import pygame
import random 
from .Game import game
import time
from monster import Monstre
import time
#******************************************classe projectile******************************************

class projectile(pygame.sprite.Sprite):

    def  __init__(self,player1,game):
        super().__init__()
        #pour collision
        self.game = game
        self.velocity = 5
        self.image = pygame.image.load('assets/projectile.png')
        self.player = player1
        #reduire la taille 
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = player1.rect.x+120
        self.rect.y = player1.rect.y+80
        #faireune retation
        self.angle = 0
        self.vitess_rotation = 12
        self.image_originale = self.image

    def lancer(self): 
        
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x += self.velocity
        #retation
        #le 1 tjr ad iqim 1
        self.angle += self.vitess_rotation
        self.image = pygame.transform.rotozoom(self.image_originale,self.angle,1)
        #recupere les coords du centre
        self.rect = self.image.get_rect(center=self.rect.center)

        #supprime si il depasse la fenetre
        if self.rect.x > 1080:
            self.remove()

#******************************************classe player    ******************************************

class Player(pygame.sprite.Sprite):

    def __init__(self,game):

        super().__init__()
        self.game = game
        self.image = pygame.image.load('assets/player.png')
        self.velocity = 5
        self.vie_origine = 100
        self.vie_actuelle = 100 
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500
        #reste a comprendre!!!!
        self.a_sauter = False
        self.saut_montee = 0
        self.saut = 0
        self.saut_descendree = 10
        self.nombre_saut = 0
        #ajouter tous les projectile 
        self.tt_projectile = pygame.sprite.Group()

    def avancer(self):
        if self.rect.x < 1080 and not self.game.verifie_collision(self,self.game.tt_monsters): 
            self.rect.x += self.velocity
    
    def reculer(self):
        if self.rect.x > 0 : self.rect.x -= self.velocity
    
    def sauter(self):
        if self.a_sauter : 
            if self.saut_montee >=20:
                self.saut_descendree -= 1
                self.saut = self.saut_descendree
            else :
                self.saut_montee +=1
                self.saut = self.saut_montee
            if self.saut_descendree < 0:
                self.saut_descendree = 10
                self.saut_montee = 0
                self.a_sauter = False
        self.rect.y = self.rect.y - (self.saut)
    
    def lancer_prejectile(self):
        self.tt_projectile.add(projectile(self,self.game))
#******************************************classe monstre   ******************************************


class Monstre(pygame.sprite.Sprite):
    def __init__(self,game,player):
        super().__init__()
        self.game         = game
        self.player       = player
        self.vie          = 100
        self.vie_actuelle = 100
        self.atacke       = 5
        self.image        = pygame.image.load('assets/mummy.png')
        self.velocity     = 10
        self.rect         = self.image.get_rect()
        self.rect.x       = 1000
        self.rect.y       = 540
        self.velocity     = 2

    def deplacer(self):
        if not self.game.verifie_collision(self,self.game.tt_player):
            self.rect.x -= self.velocity


        if self.rect.x < 0 :
            self.remove()
            print("monstre sup!!")
    
    
    def blesse(self):
        return self.game.verifie_collision(self,self.game.tt_player) #:
            #self.game.tt_monsters.remove(self)
            #print("montre sup!")
#******************************************classe game      ******************************************

class game:

    def __init__(self):
        self.tt_player=pygame.sprite.Group()
        self.player1 = Player(self)
        self.tt_player.add(self.player1)
        self.touches= {}
        self.monstre1 = Monstre(self,self.player1)
        self.tt_monsters = pygame.sprite.Group()
        self.cree_monstre()
        
        


    def cree_monstre(self):
        monstre = Monstre(self,self.player1)
        self.tt_monsters.add(monstre)

    def verifie_collision(self,splite,groupe):
        #false est ce que il vas etre supprime
        #le dernier et le type de lacollision
        #on compare un indevidu avec un group
        return (pygame.sprite.spritecollide(splite,groupe,False,pygame.sprite.collide_mask))

    
        

#******************************************classe principale******************************************

pygame.init()

screen = pygame.display.set_mode((1080,680))

#definition icon
icone  = pygame.image.load("hose.ico")
pygame.display.set_icon(icone)

#definition fond ecran
fond_ecran = pygame.image.load('assets/bg.jpg')
screen.blit(fond_ecran,(0,-210))
pygame.display.flip()
projectile = pygame.image.load('assets/projectile.png')


game1 = game()

afficher = True
time1 = time.time()
while afficher:
    
    #gestion des evenement 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: afficher = False
        if event.type == pygame.KEYDOWN:
            game1.touches[event.key] = True
        elif event.type == pygame.KEYUP: game1.touches[event.key] = False
        
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_c: 
                game1.player1.a_sauter = True  
                game1.player1.nombre_saut +=1
            
            if event.key == pygame.K_SPACE:
                game1.player1.lancer_prejectile()  

    if game1.touches.get(pygame.K_RIGHT): game1.player1.avancer()
    if game1.touches.get(pygame.K_LEFT): game1.player1.reculer()
    
    if game1.player1.rect.y <=500 :
        if game1.player1.nombre_saut <=1:
            game1.player1.sauter() 
    #if (time.time() - time1) >= :
    
    #    time1 = time.time()
    #afficher mon ecran
    screen.blit(fond_ecran,(0,-210))

    #aficher mon joueur
    screen.blit(game1.player1.image,game1.player1.rect)

    #affciher l'ensemble des projectile
    game1.player1.tt_projectile.draw(screen)
    
    #afficher les monstres
     
    
    #game1.tt_monsters.draw(screen)
    
    
    #lancer les projectile
    for projectile in game1.player1.tt_projectile:
        projectile.lancer()
    
    # test pour supprimer les monstre morts
    for monstre in game1.tt_monsters:
        #suppression du monstre en cas de collision
        if pygame.sprite.spritecollide(monstre ,game1.player1.tt_projectile,False,pygame.sprite.collide_mask):
            game1.tt_monsters.remove(monstre)
            game1.player1.tt_projectile.remove(projectile)
            print("monstre sup!")

        else:
            screen.blit(monstre.image,monstre.rect)
    
    #lancer les monstres
    
    for zombi in game1.tt_monsters:
        zombi.deplacer()
    
    
    #print(game1.verifie_collision(game1.player1,game1.tt_monsters))
    
    pygame.display.flip()