import pygame
import random 
import time
from   Jeux.Game import game
from Jeux.player import *
import cv2 as cv
import numpy as np

def drawBox(frame, rectangle):
 
    x,y,w,h = int(rectangle[0]), int(rectangle[1]), int(rectangle[2]), int(rectangle[3])
    cv.rectangle(frame, (x,y),((x+w), (y+h)), (0,0,255),1,1)
    cv.putText(frame, "Tracking", (40, 80), cv.FONT_HERSHEY_COMPLEX,0.6,(0,255,0),1)
    return x+w/2, y+h/2

pygame.init()

taille_screen = (1080,680)

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FPS, 1200)

tracker = cv.TrackerCSRT_create()
ret, frame = cap.read()
cv.resize(frame, taille_screen)
cv.flip(frame,1,frame)
rectangle = cv.selectROI("Tracking", frame, False)
tracker.init(frame, rectangle)



screen = pygame.display.set_mode(taille_screen,pygame.DOUBLEBUF)


#definition icon
icone  = pygame.image.load('Partie2/Jeux/assets/button.png')
pygame.display.set_icon(icone)

#definition fond ecran
fond_ecran       = pygame.image.load('Partie2/Jeux/assets/bg.jpg')
fond_ecran_debut = pygame.image.load('Partie2/Jeux/assets/banner.png')
boutom_debut     = pygame.image.load('Partie2/Jeux/assets/button.png')
return_home      = pygame.image.load('Partie2/Jeux/assets/hose.ico')
fond_ecran_debut = pygame.transform.scale(fond_ecran_debut,(800,800))
boutom_debut     = pygame.transform.scale(boutom_debut,(200,90))
return_home      = pygame.transform.scale(return_home,(50,50))
game1            = game()
rect_buttom      = boutom_debut.get_rect()
rect_debut       = fond_ecran_debut.get_rect()
afficher         = True
clique_bouton    = False
i,j              = 0,0
nombre           = 0
time1            = time.time()
time2            = time.time()
toitoi = 2



perdu = 100


while afficher:
    if not clique_bouton:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: afficher = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 420 and event.pos[0] <= 620:
                    if event.pos[1] >=520 and event.pos[1] <=610: clique_bouton = True
        
        
        
        
                 
        screen.blit(fond_ecran,(0,-210))
        screen.blit(fond_ecran_debut,(120,-100))
        screen.blit(boutom_debut,(420,520))


        pygame.display.flip()


        perdu = 100
    
    elif perdu==0:
        
        cap.release()
        cv.destroyAllWindows()
        clique_bouton = False
    else :

        ret, frame = cap.read()
        cv.resize(frame, taille_screen)
        cv.flip(frame,1,frame)
        ret, rectangle = tracker.update(frame)

        if ret:
            x,y = drawBox(frame, rectangle)
            cv.circle(frame, (int(x), int(y)), 3, (0,255,0), 2,1)
            #affichage des coordon??e
            cv.putText(frame, "X = ",(0,30), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1)
            cv.putText(frame, str(int(x)),(40,30), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1)
            cv.putText(frame, "Y = ",(100,30), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1)
            cv.putText(frame, str(int(y)),(140,30), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1) 
            game1.player1.setPosition(x)      
        else:
            cv.putText(frame, "Lost Tracking",(50,80), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1)

        cv.imshow("Tracking", frame)
        
        car = cv.waitKey(1)&0xFF
        if car == ord("0") :
            break        


        #gestion des evenement 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: afficher = False
            if event.type == pygame.KEYDOWN:
                game1.touches[event.key] = True
            elif event.type == pygame.KEYUP: game1.touches[event.key] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >1000 and event.pos[0]<1050:
                    if event.pos[1] >0 and event.pos[1] <=50 :
                        clique_bouton = False
                        game1 = game()
            

        if game1.player1.rect.y <=500 :
            if game1.player1.nombre_saut <=1:
                game1.player1.sauter() 
        
        screen.blit(fond_ecran,(0,-210))
        screen.blit(return_home,(1000,0))
        #aficher mon joueur
        #if len(game1.player1.tt_projectile) == 0 :
        if game1.player1.peux_lancer:
            screen.blit(game1.player1.image,game1.player1.rect)
        
        #affciher l'ensemble des projectile
        #game1.player1.tt_projectile.draw(screen)
        #affciher l'ensemble des projectile lances

        
        

        
        #afficher les comets
        game1.tt_comets.draw(screen)

        #ajouter des comets
        if (time.time()-time2)>= 1.5:
            game1.cree_comet()
            time2 = time.time()
            nombre += 1

        #lancer les comets
        for comet in game1.tt_comets:
            
            comet.attaquer()
            
            perdu = comet.Collision()
            

        
        game1.player1.cree_bare_vie(screen)


        
 
        #print(game1.verifie_collision(game1.player1,game1.tt_monsters))
        pygame.display.flip()

cv.destroyAllWindows()
#exec(open('Partie2/mainWindow.py').read())



