import pygame



class Comet(pygame.sprite.Sprite):
    
    def __init__(self,game,player):
        super().__init__()
        self.game      = game
        self.player    = player
        self.velocity  = 15
        self.image     = pygame.image.load('Partie2/Jeux/assets/comet.png') 
        self.rect      = self.image.get_rect()
        self.rect.x    = 540
        self.rect.y    = -70
        self.perte     = 10
        self.image     = pygame.transform.scale(self.image,(100,70))

    def attaquer(self):
        self.rect.y += self.velocity 
        if self.rect.y >680:
            self.game.tt_comets.remove(self)
    
    def Collision(self):

        if self.game.verifie_collision(self,self.game.tt_player):
            print("toucher")
            self.game.tt_comets.remove(self)
            self.game.player1.dommage(self.perte)
            return self.game.player1.vie_actuelle
        else:
            return 100
        


    