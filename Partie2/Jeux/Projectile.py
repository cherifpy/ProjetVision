import pygame


class projectile(pygame.sprite.Sprite):

    def  __init__(self,player1,game):
        super().__init__()
        #pour collision
        self.game = game
        self.velocity = 2 #origine 8
        self.image = pygame.image.load('Partie2/Jeux/assets/projectile.png')
        self.player = player1
        #reduire la taille 
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = player1.rect.x+150 #origine 150
        self.rect.y = player1.rect.y+90 #origine 90
        #faireune retation
        self.angle = 0
        self.vitess_rotation = 12
        self.image_originale = self.image
        self.est_lancer = False
        self.j = 0
        self.distancer_lancement = self.player.rect.x + 70

    def rotation(self):
        
        #retation
        #le 1 tjr ad iqim 1
        self.angle += self.vitess_rotation
        self.image = pygame.transform.rotozoom(self.image_originale,self.angle,1)
        #recupere les coords du centre
        self.rect = self.image.get_rect(center=self.rect.center)


    def lancer(self):
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x += self.velocity
        self.rotation()
        #supprime si il depasse la fenetre
        if self.rect.y < -50:
            self.remove()


