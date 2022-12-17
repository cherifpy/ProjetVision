import pygame
import random 
from Game import game
import time
from monster import Monstre
import time
pygame.init()
taille_screen = (1080,680)
screen = pygame.display.set_mode(taille_screen)

#definition icon
icone  = pygame.image.load("hose.ico")
pygame.display.set_icon(icone)

#definition fond ecran
fond_ecran       = pygame.image.load('assets/bg.jpg')
fond_ecran_debut = pygame.image.load('assets/banner.png')
boutom_debut     = pygame.image.load('assets/button.png')
fond_ecran_debut = pygame.transform.scale(fond_ecran_debut,(800,800))
boutom_debut     = pygame.transform.scale(boutom_debut,(200,90))
game1 = game()
rect_buttom = boutom_debut.get_rect()
rect_debut = fond_ecran_debut.get_rect()


afficher       = True
clique_bouton  = False
i = 0
j = 0

nombre = 0
tour = 0
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
                j = 0
                game1.player1.lancer_prejectile()
                      
    if game1.touches.get(pygame.K_RIGHT): game1.player1.avancer()
    if game1.touches.get(pygame.K_LEFT): game1.player1.reculer()
    
    if game1.player1.rect.y <=500 :
        if game1.player1.nombre_saut <=1:
            game1.player1.sauter() 
    
    screen.blit(fond_ecran,(0,-210))

    #affciher l'ensemble des projectile
    game1.player1.tt_projectile.draw(screen)

    #afficher l'ensemble des comets
    game1.tt_comets.draw(screen)
    
    #lancer les projectile
    for projectile in game1.player1.tt_projectile:
        if not pygame.sprite.spritecollide(projectile ,game1.tt_comets,False,pygame.sprite.collide_mask):
            if j in range(0,24):
                screen.blit(game1.player1.image,game1.player1.rect)
            projectile.lancer()
        else : 
            if  j in range(0,24):
                screen.blit(game1.player1.image,game1.player1.rect)
            game1.player1.tt_projectile.remove(projectile)

    #lancer les monstres
    for zombi in game1.tt_comets:
        if not pygame.sprite.spritecollide(zombi ,game1.player1.tt_projectile,False,pygame.sprite.collide_mask):
            zombi.attacker()
        else : game1.tt_comets.remove(zombi)
    
    #afficher les comets
    if (time.time()-time1)>= 1:
        game1.cree_comet()
        time1 = time.time()
        nombre += 1

    #aficher mon joueur
    if j==0 or j==24:
        screen.blit(game1.player1.image,game1.player1.rect)

    for monstre in game1.tt_monsters:
        #suppression du monstre en cas de collision
        if pygame.sprite.spritecollide(monstre ,game1.player1.tt_projectile,False,pygame.sprite.collide_mask):
            game1.tt_monsters.remove(monstre)
            game1.player1.tt_projectile.remove(projectile)
            print("monstre sup!")
        else:
            if i >= len(monstre.animation) :
                i = 0
                screen.blit(monstre.animation[i],monstre.rect)
                i += 1
            else: 
                screen.blit(monstre.animation[i],monstre.rect)
                i+=1
            
    #print(game1.verifie_collision(game1.player1,game1.tt_monsters))
    print(nombre)
    pygame.display.flip()
    tour +=1

print(tour)  