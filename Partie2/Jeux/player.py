import pygame



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

        self.a_lancer             = False
        self.peux_lancer          = True

        self.bare_vie = pygame.Rect(self.rect.x,self.rect.y,100,10)
        

    def avancer(self):
        if self.rect.x < 1080: 
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
        self.rect.x=y_*1.5
        

       
        
        

    