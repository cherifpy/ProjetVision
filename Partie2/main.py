import pygame
import random 
import time
from   Jeux.Game import game
from   Jeux.monster import Monstre
from   Jeux.Projectile import projectile 
from Jeux.player import *
import cv2 as cv
import numpy as np
from ColorTraking import ColorTraking, detect_inrange

pygame.init()
taille_screen = (1080,680)
screen = pygame.display.set_mode(taille_screen,pygame.DOUBLEBUF)


#definition icon
icone  = pygame.image.load('Partie2/Jeux/assets/button.png')
pygame.display.set_icon(icone)

#definition fond ecran
fond_ecran       = pygame.image.load('Partie2/Jeux/assets/bg.jpg')
fond_ecran_debut = pygame.image.load('Partie2/Jeux/assets/banner.png')
boutom_debut     = pygame.image.load('Partie2/Jeux/assets/button.png')
return_home      = pygame.image.load('Partie2/Jeux/assets/button.png')
fond_ecran_debut = pygame.transform.scale(fond_ecran_debut,(800,800))
boutom_debut     = pygame.transform.scale(boutom_debut,(200,90))
return_home      = pygame.transform.scale(return_home,(100,100))
game1            = game()
rect_buttom      = boutom_debut.get_rect()
rect_debut       = fond_ecran_debut.get_rect()
afficher         = True
clique_bouton    = False
i,j              = 0,0
nombre           = 0
time1            = time.time()
time2            = time.time()
projectile1      = projectile(game1.player1,game1)
toitoi = 2


capteur = cv.VideoCapture(0)
fps = 10

a = 0
b = 0
c = 255

lo = np.array([95,100,50])
hi = np.array([120,255,200])

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
        
        """
        font = pygame.font.Font('freesansbold.ttf', 25)
        text = font.render('Time :', True, (0,255,255))
        textRect = text.get_rect()
        textRect.center = (10,100)
        screen.blit(text, textRect)
        """

        pygame.display.flip()
        perdu = 100
    
    elif perdu==0:
        print("heh")
        capteur.release()
        cv.destroyAllWindows()
        clique_bouton = False
    else :
        """
        points = ColorTraking(capteur)

        if len(points)>0 :
            game1.player1.setPosition(points[0][1])
            
        """
        ret, frame = capteur.read()

        frame = cv.resize(frame,taille_screen)
        cv.flip(frame, 1, frame)
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        cv.circle(frame, (150,150), 20, (0,255,0), 5)
        img, mask, points = detect_inrange(frame, 1500, 4000)
        #print(img[100,100])
        if len(points)>0:
            cv.circle(frame, points[0][0], points[0][1], (0,0,255), 3)
            game1.player1.setPosition(points[0][0][0])
            #print(points[0][0])
        cv.imshow("mask", mask)
        cv.imshow("bgr img", frame)
        #cv2.imshow("hsv mask", output_hsv)

        car = cv.waitKey(10)
        if car == ord("0"):
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
            

        if game1.touches.get(pygame.K_RIGHT): game1.player1.avancer()
        if game1.touches.get(pygame.K_LEFT): game1.player1.reculer()
        
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
        game1.player1.projectile_lances.draw(screen)
        
        
        #afficher les monstres
        # test pour supprimer les monstre morts
        if (time.time()-time1)>= 2:
            game1.cree_monstre()
            time1 = time.time()
        
        #afficher les comets
        game1.tt_comets.draw(screen)

        #ajouter des comets
        if (time.time()-time2)>= 4:
            game1.cree_comet()
            time2 = time.time()
            nombre += 1

        #lancer les comets
        for comet in game1.tt_comets:
            
            comet.attaquer()
            
            perdu = comet.Collision()
            print(perdu)
        
        game1.player1.cree_bare_vie(screen)


        
 
        #print(game1.verifie_collision(game1.player1,game1.tt_monsters))
        pygame.display.flip()

cv.destroyAllWindows()
import os
import sys
os.system("python3 mainWindow.py")
sys.exit()


