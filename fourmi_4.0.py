#Salim Najib, utf8, juillet 2019

"""La fourmi de Langton est un simple programme informatique
où une 'fourmi' reçoit deux instructions: si elle est sur une
case blanche, elle doit pivoter de 90° vers la droite puis
avancer tout en colorant la case initiale en noir; si elle
est sur une case noire, elle doit pivoter vers la gauche, puis
avancer, et colorer la case précédente en blanc.

Cependant, des comportements variés naissent de ces instructions
simples, avec, dans l'ordre:
1) des figures symétriques;
2) de l'asymétrie et du chaos;
3) "l'autoroute", un motif récurrent à l'infini.
Et cela a été vérifié dans nombre de configurations initiales,
sans encore de contre-exemple.

Ce programme est une simulation de la fourmi de Langton, permettant
d'étudier des situations initiales, des variations apportées
à la grille durant le travail de la fourmi et les altérations qui
feront varier le résultat."""

#IMPORTANT: THONNY N'EST PAS RECOMMANDE POUR CE PROG.
#Si néanmoins vous utilisez Thonny, passez en mode plein écran (au moins
#il y aura toutes les fonctionnalités).

#Moins important: d'habitude je mettrais des tests pour vérifier que Python
#reçoit bien un nombre de la part de l'utilisateur là où il demande un
#un nombre, mais là je compte un peu sur vous.

#Je voulais simplement vous montrer à quoi ressemblent des programmes plus complets
#que ceux du PDF - et si vous voulez vous amuser avec la fourmi, allez-y.

#J'exagère un peu ici mais tout bon programme doit être bien commenté (là j'en
#rajoute pour montrer des trucs bien sûr mais tout ce qui relève de notions
#communes Python n'ont normalement pas leur place. Dans les commentaires, vous
#devez plutôt expliquer le rôle de fonctions / classes / variables / boucles,etc.
#que vous jugez un minimum intéressantes (souvent presque toutes), la logique
#derrière, etc. Cela revient à montrer qu'on sait ce qu'on fait.

import tkinter as tk
from tkinter import ttk

class Ant(tk.Tk):
    """Définition de la fenêtre principale de la simulation."""
    def __init__(self, compteur=0, orient='nord',mode = 'first',
    X = 54, Y = 54, debug = [], side = 107, size = 5):
    #Dans le cas peu probable où la grille est trop grande pour votre écran:
    #réduisez side ci-dessus (80 par ex). Il faut au moins 56 cases pour arriver
    #à l'autoroute.
    #Supprimez les sauvegardes auparavant pour éviter les problèmes.

    #Paramétrage de la fenêtre + de qlqs variables
        tk.Tk.__init__(self) #Hors programme sur les classes.
        self.side = side #Nombre de carrés de la grille
        self.S = size #Taille des carrés

        self.compteur = compteur #0 sauf si grille chargée
        self.mode = mode #détermine s'il y a eu chargement ou non
        self.orient = orient #nord sauf grille chargée
        self.running = True #pause ou pas pause
        self.grilleaux = debug #... Longue histoire. Si vous avez étudié l'hors
        #programme et que vous ne comprenez pas l'utilité de ça, passez moi un message.

        #Instructions de routine: (hors-prog, tkinter)
        self.title('La fourmi de Langton - Main')
        self.configure(background='orange')
        self.geometry('%dx%d+%d+%d' %
          (self.side*self.S+128,self.side*self.S+3,
          self.winfo_screenwidth()/2-(self.side*self.S+100)/2,
          self.winfo_screenheight()/2-self.side*self.S/2-30))
        self.can = tk.Canvas(self,width=self.side*self.S,height=self.side*self.S,
          bg='orange',highlightbackground='orange')
        self.can.grid(row=1,column=2,rowspan=40)
        self.focus_force()

    #Création de la grille
        if self.mode == 'first': #Cas grille sans sauvegarde
            self.X = self.Y = self.side//2 + 1
            self.grille=[] #On crée une liste vide à laquelle on ajoute des éléments
            for i in range(self.side): #avec append, qui s'avèrent être des sous-
                self.grille.append([]) #listes vides auxquelles on ajoute des 1
                for j in range(self.side): #pour des cases blanches.
                    self.CreateCase(i,j,self.S,'white','no')
                    self.grille[i].append(1)
            #La grille se présente ainsi: liste[abscisseX][ordonnéeY],
            #il y a (nombre de cases par côté) self.side sous-listes d'abscisses
            #contenant self.side ordonnées: on a donc créé un tableau ou grille
            #dans laquelle nous pouvons situer les cases et la fourmi.

        elif self.mode != 'first': #Cas grille chargée
            self.X = X #on prend les valeurs X,Y chargées pour la localisation
            self.Y = Y #de la fourmi
            self.grille = self.grilleaux #alias, sans problème
            for i in range(self.side):
                for j in range(self.side):
                    if self.grille[i][j] > 0:
                        self.CreateCase(i,j,self.S,'white','no')
                    elif self.grille[i][j] == 0:
                        self.CreateCase(i,j,self.S,'black','no')
        #La grille était ici déjà pleine, ne restait plus qu'à créer une case noire
        #à l'emplacement de chaque 0 et une blanche pour les 1.

        #Case initiale de la fourmi
        self.ini=self.can.create_rectangle(self.X*self.S,
        self.Y*self.S,(self.X+1)*self.S,
        (self.Y+1)*self.S,fill='red') #centre, par défaut

    #Lecture des sauvegardes
        try:

            self.saves=[]
            self.fichier = open('SavesFourmi.txt','r')
            self.savesaux = self.fichier.readlines()
            try:
                for i in range(len(self.savesaux)):
                    if self.savesaux[i].split()[0] == 'Title':
                      self.saves.append(self.savesaux[i].split()[1:])
                #On parcourt le fichier txt de sauvegardes à la recherche de tous
                #les titres, qu'on place tous dans une liste qui sera affichée
                #dans un menu déroulant.
            except:
                pass

        except: #au cas où le fichier n'a pas été créé
            self.fichier=open('SavesFourmi.txt','w')

    #Boutons, étiquettes, etc.
        tk.Label(self,text='Nombre de mvmts?',bg='orange').grid(row=1,
          column=1)
        self.mvmts=tk.StringVar(self,value='15000')
        tk.Entry(self,textvariable=self.mvmts).grid(row=2,column=1)

        tk.Button(self,text='Lancer!',command=self.Go).grid(row=5,
          column=1)

        tk.Label(self,text='Compteur:',bg='orange').grid(row=7,
          column=1)
        self.compteurlab=tk.Label(self, text=str(self.compteur),bg='orange')
        self.compteurlab.grid(row=8,column=1)

        tk.Button(text='Effacer la grille',command=self.Reset).grid(row=10,
          column=1)

        tk.Button(text='Pause/Reprendre',command=self.Stop).grid(row=12,column=1)

            #Du ttkinter, oui 2 t. Puissiez-vous ne jamais avoir à en utiliser.
        self.style_combobox = ttk.Style()
        self.style_combobox.theme_create(self.style_combobox,parent='alt',
          settings = {'TCombobox':
          {'configure':
          {'fieldforeground': 'white','foreground': 'black',
           'fieldbackground': 'white','background': 'white'}}})
        self.style_combobox.theme_use(self.style_combobox)
        self.choix_orient = tk.StringVar()
        tk.Label(self,text='Orientation initiale:',bg='orange').grid(row=14,
          column=1)
        self.orient_combob = ttk.Combobox(self)
        self.orient_combob.config(textvariable=self.choix_orient,
        values=['nord','est','ouest','sud'])
        self.orient_combob.grid(row=15,column=1)
        self.orient_combob.current(0)

        tk.Button(text='Afficher la fourmi',command=self.Know).grid(row=17,column=1)
        self.releve_lab=tk.Label(text='Orientation actuelle:',bg='orange')
        self.releve_lab.grid(row=18,column=1)
        self.releve=tk.Label(text=str(self.orient),bg='orange')
        self.releve.grid(row=19,column=1)

        self.choix_nomsave = tk.StringVar()
        tk.Label(text='Nom sauvegarde?',bg='orange').grid(row=21,column=1)
        tk.Entry(textvariable=self.choix_nomsave).grid(row=22,column=1)

        self.savebutton=tk.Button(text='Sauvegarder la grille',command=self.Save)
        self.savebutton.grid(row=23,column=1)

        tk.Button(text='Charger une sauvegarde',command=
          lambda mod='load':self.Find(mod)).grid(row=25,column=1)

        tk.Button(text='Supprimer une sauvegarde',command=
          lambda mod='del':self.Find(mod)).grid(row=26,column=1)

        self.charge = tk.StringVar()
        self.saves_combob=ttk.Combobox(textvariable=self.charge,
          values=self.saves)
        self.saves_combob.grid(row=27,column=1)
        try:
            self.saves_combob.current(0)
        except:
            pass

        tk.Button(text='Aides et Astuces',command=self.Help).grid(row=37,
          column=1)

        tk.Label(text='Vitesse en ms?',bg='orange').grid(row=38,column=1)
        self.vit=tk.StringVar(self,value='2')
        tk.Entry(textvariable=self.vit).grid(row=39,column=1)

    #Associations des clics de souris pour le changement de la grille
    #(emplacement initial + cases noires/blanches ajoutées)
        self.can.bind('<Button-3>',self.ChangeLocIni)
        self.can.bind('<Button-1>',self.InvertColor)

        self.mainloop()

    def CreateCase(self,X,Y,S,color,alter='yes'):
        """Méthode pour la création d'une case et l'altération, s'il y a lieu, de
        la liste grille."""
        if alter == 'yes': #alter permet d'utiliser cette méthode pour les cases
            self.grille[X].pop(Y) #rouges initiales + chargements.
        self.carre=self.can.create_rectangle(X*S,Y*S,(X+1)*S,(Y+1)*S,fill=color)
        if alter == 'yes':
            if color == 'white':
                self.grille[X].insert(Y,1)
            elif color == 'black':
                self.grille[X].insert(Y,0)

    def ChangeLocIni(self,event):
        """Méthode pour choisir la case de départ."""
        if event.x > self.S*self.side or \
        event.y > self.S*self.side:
        #on ignore les clics hors grille
            pass
        else:
            #Suppression de la localisation précédente
            self.CreateCase(self.X,self.Y,self.S,'white')

            #Repérage et représentation de la case choisie
            self.X = int(event.x/self.S) #event.x et y sont les coordonnées du
            self.Y = int(event.y/self.S) #clic.
            self.CreateCase(self.X,self.Y,self.S,'red','no')

    def InvertColor(self,event):
        """Méthode pour changer la couleur d'une case à la souris."""
        self.subX = int(event.x/self.S)
        self.subY = int(event.y/self.S)

        if self.grille[self.subX][self.subY] > 0:
            self.CreateCase(self.subX,self.subY,self.S,'black')

        else:
            self.CreateCase(self.subX,self.subY,self.S,'white')

    def Go(self):
        """Méthode de lancement de la silumation."""
        self.move=int(self.mvmts.get())
        self.XY = self.grille[self.X][self.Y] #XY est la position de la fourmi
        self.vitint=int(self.vit.get())       #sur la grille; (abs,ord).
        self.orient=self.choix_orient.get()
        #On récupère toutes les valeurs utiles, qu'elles soient chargées ou entrées
        self.Go2() #à la main.

    def Go2(self):
        """Méthode auxiliaire récursive de la simulation."""
        if self.move and self.running:
            try:
                if self.XY > 0: #case blanche
                    self.CreateCase(self.X,self.Y,self.S,'black')
                    if self.orient == 'sud':
                        self.X = self.X-1 #axe des X de gauche (0) à droite, comme
                        self.orient = 'ouest' #d'habitude (sans abscisses négatives)
                    elif self.orient == 'nord':
                        self.X = self.X+1
                        self.orient = 'est'
                    elif self.orient == 'ouest':
                        self.Y = self.Y-1 #axe des Y de haut (0) en bas, repère
                        self.orient = 'nord' #donc indirect (par défaut dans
                    elif self.orient == 'est': #tkinter).
                        self.Y = self.Y+1
                        self.orient = 'sud'

                else:
                    self.CreateCase(self.X,self.Y,self.S,'white')
                    if self.orient == 'nord':
                        self.X = self.X-1
                        self.orient = 'ouest'
                    elif self.orient == 'sud':
                        self.X = self.X+1
                        self.orient = 'est'
                    elif self.orient == 'ouest':
                        self.Y = self.Y+1
                        self.orient = 'sud'
                    elif self.orient == 'est':
                        self.Y = self.Y-1
                        self.orient = 'nord'
                #Si la fourmi regarde vers le haut ou vers le bas (de l'écran),
                #sa droite et sa gauche seront l'est ou l'ouest selon le cas.
                #Si elle regarde vers la droite ou la gauche de l'écran, ce seront
                #le nord ou le sud.

                self.XY = self.grille[self.X][self.Y]
                #Mise à jour de la position de la fourmi.

                self.move = self.move - 1
                self.compteur = self.compteur + 1
                self.compteurlab.configure(text=str(self.compteur),bg='orange')
                self.releve.configure(text=self.orient,bg='orange')
                self.after(self.vitint,self.Go2) #récursivité tkinter (hors-prog)

            except:
                pass

    def Reset(self):
        """Méthode pour effacer et redémarrer l'application."""
        self.destroy()
        Ant()

    def Stop(self):
        """Méthode pour mettre en pause/relancer la simulation."""
        if self.running == True:
            self.running = False
        elif self.running == False:
            self.running = True
            self.Go()

    def Help(self):
        """Méthode pour faire apparaître la page d'aides."""
        self.destroy()
        Aides()

    def Know(self):
        """Afficher la fourmi en permanence consomme des ressources et est peu
        utile. Cette méthode permet de connaître sa position et orientation
        quand on le désire."""
        self.running=True
        self.Stop()
        self.CreateCase(self.X,self.Y,self.S,'red','no')

    def Save(self):
        """Méthode pour sauvegarder une situation (grille/compteur/etc.)."""
        self.fichier.close()
        self.fichier = open('SavesFourmi.txt','a')
        self.temp=self.choix_nomsave.get()
        if not self.temp:
            self.temp = 'Le néant' #nom par défaut si rien n'est entré
        self.fichier.writelines('Title '+self.temp+'\n')
        for i in self.grille:
            self.fichier.writelines(str(i)+'@\n')
        self.fichier.writelines(str(self.compteur)+'@\n'+str(self.X)+'@\n'+\
          str(self.Y)+'@\n'+self.orient+'@\n')
        self.fichier.close()
        self.Reset()
    #On copie dans le fichier: le nom, la grille, le compteur, X, Y, l'orientation.

    def Find(self,mod):
        """Méthode qui trouve un nom de sauvegarde et agit en fonction."""
        for i in range(len(self.savesaux)):
            try:
                if self.savesaux[i] == 'Title '+self.charge.get()+'\n':

                    if mod == 'del': #delete
                        for j in range(i,i+self.side+5):
                            self.savesaux.pop(i)
                        #On enlève toute trace de la sauvegarde de la liste aux,
                        #puis on réécrit tout le document avec ce qui reste dans
                        #la liste. Il y a d'autres moyens mais bref.

                        self.fichier.close()
                        self.fichier=open('SavesFourmi.txt','w')
                        self.fichier.writelines(self.savesaux)
                        self.fichier.close()
                        self.Reset()

                    elif mod == 'load': #chargement
                        self.grilleaux=[]
                        #Vous devez pouvoir expliquer ce qui suit si vous avez
                        #bossé vos listes lul. Jusqu'à la ligne '####...'.
                        #Regardez aussi comment une sauvegarde se présente dans
                        #le fichier txt.
                        for j in range(i+1,i+self.side+1):
                            self.grilleaux.append(
                            self.BecomeList(self.savesaux[j].split('@')[0]))
                            #MERCI LE TYPAGE DYNAMIQUE
                        self.compteuraux = int(self.savesaux[i+self.side+1].split(
                        '@')[0])
                        self.Xaux = int(self.savesaux[i+self.side+2].split('@')[0])
                        self.Yaux = int(self.savesaux[i+self.side+3].split('@')[0])
                        self.orientaux = self.savesaux[i+self.side+4].split('@')[0]
                        ####...
                        self.fichier.close()
                        self.destroy()
                        Ant(self.compteur,self.orientaux,'NO',self.Xaux,self.Yaux,
                        self.grilleaux)

            except:
                pass

    def BecomeList(self,string):
        """Méthode qui convertit tous les nombres présents dans un liste enfermée
        dans un str."""
        liste_nombres=[]
        for i in string:
            try:
                liste_nombres.append(int(i)) #qui échouera pour tout ce qui n'est
            except: #pas un nombre, on n'aura alors que des nombres dans la liste.
                pass
        return liste_nombres
    #MERCI LE TYPAGE DYNAMIQUE

class Aides(tk.Tk):
    """Petite classe pour définir une fenêtre avec aides et astuces."""
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('La fourmi de Langton - Aides')
        self.configure(background='orange')
        self.geometry('%dx%d+%d+%d' %
          (450,480,
          self.winfo_screenwidth()/2-450/2,
          self.winfo_screenheight()/2-480/2-20))
        self.focus_set()

        tk.Label(text='    ',bg='orange').pack()

        tk.Label(text='>Clic ou double clic gauche inverse la couleur d\'une case,\n\
 clic droit la choisit comme nouvelle position de la fourmi.',bg='orange').pack()

        tk.Label(text='    ',bg='orange').pack()

        tk.Label(text='>Vous pouvez cliquer avant et aussi PENDANT une\n\
 simulation. N\'oubliez pas le bouton de pause.',bg='orange').pack()

        tk.Label(text='    ',bg='orange').pack()

        tk.Label(text='>Une manière plutôt intéressante de procéder sans\n\
 perdre de temps est d\'aller à vitesse 0 jusqu\'à un\n\
 certain moment puis lancer de 10 en 10 par ex, dans le\n\
 \'Nombre de mvmts\'.',bg='orange').pack()

        tk.Label(text='    ',bg='orange').pack()

        tk.Label(text='>N\'oubliez pas de sauvegarder les situations intéressantes.',
        bg='orange').pack()

        tk.Label(text='    ',bg='orange').pack()

        tk.Label(text='>Sur une grille initialement totalement blanche, le\n\
 dernier motif symétrique est fait après 472 mouvements\n\
 et l\'autoroute débute après 10.087 mouvements.',bg='orange').pack()

        tk.Label(text='    ',bg='orange').pack()

        tk.Label(text='>Attention quand le nombre de mvmts désiré est\n\
 atteint: réappuyer sur Lancer continuera la simulation\n\
 mais avec celle dans le champ \'Orientation initiale\',\n\
 veillez donc à mettre celle "actuelle" à sa place, sauf\n\
 bien sûr si vous cherchez à changer l\'orientation.\n\
 De même quand vous continuez une simulation chargée.',bg='orange').pack()


        tk.Button(text='Retour',command=self.Quit).pack(side='bottom')

        self.mainloop()

    def Quit(self):
        self.destroy()
        Ant()

if __name__=='__main__':
    Ant()
