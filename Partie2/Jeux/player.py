import pygame
from .Projectile import projectile


class Player(pygame.sprite.Sprite):


    def __init__(self,game):
        super().__init__()
        self.game                 = game
        self.image                = pygame.image.load('Partie2/Jeux/assets/player.png')
        self.velocity             = 4
        self.vie_origine          = 100
        self.vie_actuelle         = 100 
        self.rect                 = self.image.get_rect()
        self.rect.x               = 400
        self.rect.y               = 500
        #reste a comprendre!!!!
        self.a_sauter             = False
        self.saut_montee          = 0
        self.saut                 = 0
        self.saut_descendree      = 10
        self.nombre_saut          = 0
        #ajouter tous les projectile 
        self.projectile_lances    = pygame.sprite.Group()
        self.tt_projectile        = pygame.sprite.Group()
        self.a_lancer             = False
        self.peux_lancer          = True
        self.animation_projectile =[
        pygame.image.load('Partie2/Jeux/assets/player/player1.png' ),
        pygame.image.load('Partie2/Jeux/assets/player/player2.png' ),
        pygame.image.load('Partie2/Jeux/assets/player/player3.png' ),
        pygame.image.load('Partie2/Jeux/assets/player/player4.png' ),
        pygame.image.load('Partie2/Jeux/assets/player/player5.png' ),
        pygame.image.load('Partie2/Jeux/assets/player/player6.png' ),
        pygame.image.load('Partie2/Jeux/assets/player/player7.png' ),
        pygame.image.load('Partie2/Jeux/assets/player/player8.png' ),
        pygame.image.load('Partie2/Jeux/assets/player/player9.png' ), 
        pygame.image.load('Partie2/Jeux/assets/player/player10.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player11.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player12.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player13.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player14.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player15.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player16.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player17.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player18.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player19.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player20.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player21.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player22.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player23.png'),
        pygame.image.load('Partie2/Jeux/assets/player/player24.png')]  

        self.bare_vie = pygame.Rect(self.rect.x,self.rect.y,100,10)
        

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
        projectile1 = projectile(self,self.game)
        projectile1.est_lancer = True
        #self.tt_projectile.add(projectile1)
        return projectile1
    

    def cree_bare_vie(self,surface):
        
        pygame.draw.rect(surface,(60,63,60),[self.rect.x+50,self.rect.y+20,self.vie_origine,5])
        pygame.draw.rect(surface,(111,210,46),[self.rect.x+50,self.rect.y+20,self.vie_actuelle,5])

    def dommage(self,perte):
        self.vie_actuelle -=perte

        if self.vie_actuelle<=0 :
            return True
        else:
            return False


    def setPosition(self,y_):
        self.rect.x=y_
        

       
        
        

    