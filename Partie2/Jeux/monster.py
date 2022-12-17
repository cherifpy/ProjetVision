import pygame


class Monstre(pygame.sprite.Sprite):
    def __init__(self,game,player):
        super().__init__()
        self.game         = game
        self.player       = player
        self.vie          = 100
        self.vie_actuelle = 100
        self.atacke       = 5
        self.image        = pygame.image.load('Partie2/Jeux/assets/mummy.png')
        self.velocity     = 10
        self.rect         = self.image.get_rect()
        self.rect.x       = 1000
        self.rect.y       = 540
        self.velocity     = 0.1
        self.animation    = [pygame.image.load(f'Partie2/Jeux/assets/mummy/mummy{i}.png') for i in range(1,25)] 


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
            

