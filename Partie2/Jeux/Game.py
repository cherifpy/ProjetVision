import pygame
from .player import Player
from .monster import Monstre
from .comet import Comet
import random 

class game:

    def __init__(self):
        self.tt_player   = pygame.sprite.Group()
        self.player1     = Player(self)
        self.touches     = {}
        self.monstre1    = Monstre(self,self.player1)
        self.tt_monsters = pygame.sprite.Group()
        self.tt_comets   = pygame.sprite.Group() 
        self.tt_player.add(self.player1)
        
    def cree_monstre(self):
        monstre = Monstre(self,self.player1)
        self.tt_monsters.add(monstre)

    def cree_comet(self):
        comet1 = Comet(self,self.tt_player)
        comet1.rect.x = random.randrange(0,1000)
        self.tt_comets.add(comet1)

        
    def verifie_collision(self,splite,groupe):
        #false est ce que il vas etre supprime
        #le dernier et le type de lacollision
        #on compare un indevidu avec un group
        return (pygame.sprite.spritecollide(splite,groupe,False,pygame.sprite.collide_mask))



    
    
        
