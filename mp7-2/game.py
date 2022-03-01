import os
import keyboard
import time


nb_map =input('Quelle map voulez vous ?(1 ou 2)')
chemin = "maps/map" + nb_map+".txt"#afin d'avoir le chemin jusqu'a la map choisie

class Game:
    def __init__(self):#Le constructeur du jeu, il contient les infos de base essentielles
        self.lst_lemming = []
        self.debut_x = self.get_debut_x()
        self.debut_y = self.get_debut_y()
        self.map = []
        self.PERIODE = 0.7
        self.score = 0
        """
        Permet de créer un tableau de la taille de la map, ou les murs sont des 1,
        le vide sont des 0, l'entrée un I et la sortie un O.
        La map de base doit etre un rectangle (ne pas avoir de trou (un espace n'est pas un trou))
        """
        with open(chemin, 'r') as fichier: 
            j = fichier.readlines()
        for i in j:
            ajouter = []
            for n in i:
                if n != '\n':
                    if n == '#':
                        ajouter.append(1)
                    elif n == ' ':
                        ajouter.append(0)
                    elif n == 'I':
                        ajouter.append(2)
                    else:
                        ajouter.append(3)
            self.map.append(ajouter)

    def get_debut_x(self): # Renvoie la bonne coordonée x de départ selon la map
        if nb_map == 1:
            return 2
        else:
            return 2
    
    def get_debut_y(self):# Renvoie la bonne coordonée y de départ selon la map
        if nb_map == 1:
            return 1
        else :
            return 1

    def tour(self): #Effectue un tour du jeu pour chaque lemming présent
        compteur = 0
        for i in self.lst_lemming:#On parcours tous les lemmings
            
            if Case(i.x+i.direction,i.y).terrain == 3: #Détecte si lors du déplacement, le lemming sera sur la sortie
                self.map[i.y][ i.x] = 0
                del self.lst_lemming[compteur] #Si la condition précédente est validée, l'efface
                self.score += 1
            i.suivant()
            compteur +=1

        self.build_map()
        print('Votre score actuel est:',self.score)

    def demarrer(self):
        """
        La boucle afin de faire tourner le jeu, elle marche tant que 'q' n'est pas préssé,
        lorsque '+' est préssé, un lemming est rajouter et il effectue un tour de jeu à chaque tour 
        de boucle, un tour dur environ self.PERIODE
        """
        while not keyboard.is_pressed('q'):

            if keyboard.is_pressed('+'):
                self.gen()
            self.tour()
            
            time.sleep(self.PERIODE)
        print('Votre score final est:', self.score)

    def gen(self): 
        """
        On rajoute dans la map qu'il y a un lemming à l'endroit du début, représenter par un 4,
        puis le rajoute dans la liste des lemmings.
        """
        self.map[self.debut_y][self.debut_x] = 4
        self.lst_lemming.append(Lemming(self.debut_x,self.debut_y))

    def build_map(self):
            """
            Construit la map a afficher dans la console à l'utilisateur.
            On se sert de la map crée au préalable dans le constructeur, ou sont
            représentés tous les éléments de la map.
            """
            for i in range(len(self.map)):
                st = ""
                for j in range(len(self.map[1])):
                    if Case(j,i).terrain == 1:
                        st += "# "
                    elif Case(j,i).terrain == 2:
                        st += "I "

                    elif Case(j,i).terrain == 3:
                        st += "O "


                    elif Case(j,i).terrain == 4: #Si il y a un lemming, on doit vérifier lequel c'est et quelle direction il a
                        for n in self.lst_lemming:
                            if n.x == j and n.y == i:
                                if n.direction == 1:
                                    st += "> "
                                else:
                                    st += "< "

                    else:
                        st += "  "
                print(st)
            
            
class Lemming:
    def __init__(self,x,y):#Les informations essentielles du lemming
        self.x = x
        self.y = y
        self.direction = 1
    
    def avancer(self):
        self.x += self.direction
    
    def retourner(self):
        self.direction *= -1
    
    def tomber(self):
        self.y += 1

    def suivant(self):
        """
        Permet d'effectuer le mouvement suivant lors d'un tour. On vérifie si la case du dessous est libre, si il l'est, on y descend (tombe), sinon on vérifie si la case suivante(en direction de l'ou on va) est libre, si oui, on y va. Sinon on retourne le lemming
        """
        if Case(self.x, self.y+1).est_libre():
            Case(self.x, self.y).liberer()
            self.tomber()
            Case(self.x, self.y).occuper()
        elif Case(self.x+self.direction, self.y).est_libre():
            Case(self.x, self.y).liberer()
            self.avancer()
            Case(self.x, self.y).occuper()
        else:
            self.retourner()
        

class Case:
    def __init__(self, x, y):#Constructeur d'une case. Contient les coordonnées de la case ainsi que son état (terrain).
        self.x = x
        self.y = y
        self.terrain = self.get_terrain()


    def est_libre(self):
        if self.terrain == 0:
            return True
        return False
    
    def is_lemming(self):
        if self.terrain == 4:
            return True
        return False

    def get_terrain(self):
        return game.map[self.y][self.x]

    def occuper(self):
        game.map[self.y][self.x] = 4

    def liberer(self):
        game.map[self.y][self.x] = 0
    
game = Game()
game.demarrer()