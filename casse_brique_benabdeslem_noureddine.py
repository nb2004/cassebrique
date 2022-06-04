# Créé par Nono, le 15/12/2021 en Python 3.7
# Créé par BENABDNOUR, le 13/12/2021 en Python 3.7
import random  # Pour les tirages aleatoires
import sys  # Pour quitter proprement
import pygame  # le module Pygame
import pygame.freetype  #pour afficher du texte
import math

pygame.init()  # initialisation de Pygame

#pour le texte
pygame.freetype.init()
myfont = pygame.freetype.SysFont(None, 20)  # le texte de taille 20

#taille de la fenetre
width, height = 900, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping")

# Pour limiter le nombre d'images par seconde
clock = pygame.time.Clock()
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE=(255,0,0)
VERTE=(0,255,0)
BLUE=(0,0,255)
VIOLET=(81,20,106)
BLEUCIEL=(20,106,103)
JAUNE=(213,223,48)
RAYON_BALLE = 10
XMIN, YMIN = 0, 0
XMAX, YMAX = width, height

fond = pygame.image.load("imageetoile.jpg")
fond = pygame.transform.scale(fond, (width, height))

class Balle:
    def vitesse_par_angle(self, angle):
        self.vx = self.vitesse * math.cos(math.radians(angle))
        self.vy = -self.vitesse * math.sin(math.radians(angle))

    def __init__(self):
        self.x, self.y = (400, 400)
        self.vitesse = 8 #vitesse initiale
        self.vitesse_par_angle(60) #vecteur vitesse
        self.sur_raquette = True
        self.vie=3# correspond au nombres de balles disponibles

    def afficher(self):
        pygame.draw.rect(screen, JAUNE,
                         (int(self.x - RAYON_BALLE), int(self.y - RAYON_BALLE),
                          2 * RAYON_BALLE, 2 * RAYON_BALLE), 0)

    def deplacer(self, raquette):
        if self.sur_raquette:
            self.y = raquette.y - 2*RAYON_BALLE
            self.x = raquette.x
        else:
            self.x += self.vx
            self.y += self.vy
        if raquette.collision_balle(self) and self.vy > 0:
            self.rebond_raquette(raquette)


        if self.x + RAYON_BALLE > XMAX:

            self.vx = -self.vx
        if self.x - RAYON_BALLE < XMIN:
            self.vx = -self.vx
        if self.y + RAYON_BALLE > YMAX:
            # le cas ou la balle n'arrive pas sur la raquete
            self.vie=self.vie-1
            self.sur_raquette = True
        if self.y - RAYON_BALLE < YMIN:

            self.vy =-self.vy

    def rebond_raquette(self, raquette):
        diff = raquette.x -self.x
        longueur_totale = raquette.longueur/2 + RAYON_BALLE
        angle = 90 + 80 * diff/longueur_totale
        self.vitesse_par_angle(angle)

class Raquette:
    def __init__(self):
        self.x = (XMIN+XMAX)/2
        self.y = YMAX - RAYON_BALLE
        self.longueur = 10*RAYON_BALLE

    def afficher(self):
        pygame.draw.rect(screen, ROUGE, (int(self.x-self.longueur/2), int(self.y-RAYON_BALLE),self.longueur, 2*RAYON_BALLE),0)

    def deplacer(self, x):
        if x - self.longueur/2 < XMIN:
            self.x = XMIN + self.longueur/2
        elif x + self.longueur/2 > XMAX:
            self.x = XMAX - self.longueur/2
        else:
            self.x = x
    def collision_balle(self,balle):
      vertical = abs(self.y - balle.y) < 2*RAYON_BALLE
      horizontal = abs(self.x - balle.x) < self.longueur/2+RAYON_BALLE
      return vertical and horizontal


class Brique:
    def __init__(self, x, y,coleur=BLANC):
        self.coleur=coleur
        self.x = x
        self.y = y
        self.vie = 1
        self.longueur = 5 * RAYON_BALLE
        self.largeur = 3 * RAYON_BALLE

    def en_vie(self):
        return self.vie > 0

    def afficher(self):
        pygame.draw.rect(screen, self.coleur, (int(self.x-self.longueur/2),
        int(self.y-self.largeur/2),
        self.longueur, self.largeur), 0)

    def collision_balle(self, balle):
        # on suppose que largeur < longueur
        marge = self.largeur/2 + RAYON_BALLE
        dy = balle.y - self.y
        touche = False
        if balle.x >= self.x: # on regarde a droite
            dx = balle.x - (self.x + self.longueur/2 - self.largeur/2)
            if abs(dy) <= marge and dx <= marge: # on touche
                touche = True
                if dx <= abs(dy):
                    balle.vy = -balle.vy
                else: # a droitee
                    balle.vx = -balle.vx
        else: # on regarde a gauche
            dx = balle.x - (self.x - self.longueur/2 + self.largeur/2)
            if abs(dy) <= marge and -dx <= marge: # on touche
                touche = True
                if -dx <= abs(dy):
                    balle.vy = -balle.vy
                else: # a gauche
                    balle.vx = -balle.vx
        if touche:
            self.vie -= 1
        return touche


class Jeu:
    def __init__(self):
        self.balle = Balle()
        self.raquette = Raquette()
        #self.brique = Brique(400, 400)
        self.liste_briques = [Brique(random.randint(XMIN, XMAX), random.randint(YMIN, YMAX),BLUE),Brique(200,100,BLUE),Brique(300,150,ROUGE),Brique(500,200,VERTE),Brique(250,300),Brique(500,100),Brique(100,10,VIOLET),Brique(200,200,BLEUCIEL)]
    def gestion_evenements(self):
        # Gestions des evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit() #Pour quitter
            elif event.type == pygame.MOUSEBUTTONDOWN: #on vient de cliquer
                if event.button == 1: #Bouton gauche
                    if self.balle.sur_raquette:
                        self.balle.sur_raquette = False
                        self.balle.vitesse_par_angle(60)


    def mise_a_jour(self):
        x,y = pygame.mouse.get_pos()
        self.balle.deplacer(self.raquette)
        #  traiter le cas de plusieurs Briques
        for i in range(len(self.liste_briques)):
            if self.liste_briques[i].en_vie():
                self.liste_briques[i].collision_balle(self.balle)

        #if self.brique.en_vie():
           # self.brique.collision_balle(self.balle)
        self.raquette.deplacer(x)

    def affichage(self):
        screen.blit(fond, (0,0)) # on efface l'écran
        self.balle.afficher()
        self.raquette.afficher()

        etiquete ="Ma Vie : "+str(self.balle.vie)

        texte, rect = myfont.render(etiquete, VERTE, size=40)
        rect.midleft = (700,10)
        screen.blit(texte, rect)

        #  traiter le cas de plusieurs Briques
        for i in range(len(self.liste_briques)):
            if self.liste_briques[i].en_vie():
                self.liste_briques[i].afficher()
        #if self.brique.en_vie():
         #   self.brique.afficher()






jeu = Jeu()


while True:

    if jeu.balle.vie==0:
        texte, rect = myfont.render("GAME OVER", ROUGE, size=45)
        rect.midleft = (300,400)
        screen.blit(texte, rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit() #Pour quitter
            elif event.type == pygame.MOUSEBUTTONDOWN: #on vient de cliquer
                if event.button == 1: #Bouton gauche
                    jeu= Jeu()
    else:
        jeu.gestion_evenements()
        jeu.mise_a_jour()
        jeu.affichage()

    pygame.display.flip() # envoi de l'image à la carte graphique
    clock.tick(60)        # on attend pour ne pas dépasser 60 image par secondes



