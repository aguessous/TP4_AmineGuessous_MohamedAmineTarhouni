# -*- coding: utf-8 -*-

from tkinter import Tk, Canvas, messagebox, Menu
from tkinter import filedialog
# Classe d'exception créée pour les besoins du labo
# Supprimez la dans votre TP.
from pipopipette.exceptions import ErreurPositionCoup
from pipopipette.partie import PartiePipopipette


class CanvasPipopipette(Canvas):
    # Dans le TP, vous devrez ajouter un argument planche en entrée
    # à ce constructeur.
    def __init__(self, parent, planche, longueur_ligne=100):
        # Nombre de pixels par case, variable.
        self.longueur_ligne = longueur_ligne
        self.largeur_ligne = self.longueur_ligne / 5
        self.dimension_boite = self.longueur_ligne + self.largeur_ligne
        self.planche = planche

        # Dans le TP, ces champs devront être remplis à partir de l'attribut planche d'un objet Partie que vous ajouterez
        # au __init__(). Vous devrez aussi ajouter un attribut self.planche.
        #
        # Ici on crée des attributs n_boites_v, n_boites_h, lignes et boites, mais dans le TP
        # on lira directement ces attributs à partir de self.planche. Ces attributs sont donc
        # seulement pour les biens du labo, mais seront tous remplacés par self.planche dans le TP.
        # Appel du constructeur de la classe de base (Canvas).
        # Dans le TP, on remplace self.n_boites_v par self.planche.N_BOITES_V. Idem pour n_boites_h.
        super().__init__(parent,
                         width=self.planche.N_BOITES_V * self.dimension_boite + self.largeur_ligne - 1,
                         height=self.planche.N_BOITES_H * self.dimension_boite + self.largeur_ligne - 1)

    def dessiner_boites(self):
        # Ici, on itère sur le dictionnaire self.boites, sans se servir de la valeur de boite.
        # Dans le TP, on itèrera sur self.planche.boites.items() et boite sera un objet de
        # type Boite.
        for position, boite in self.planche.boites.items():
            ligne, col = position

            # On retrouve les points d'ancrage en x et en y de la boîte à partir de sa ligne et de sa colonne
            debut_boite_x = col * self.dimension_boite + self.largeur_ligne
            debut_boite_y = ligne * self.dimension_boite + self.largeur_ligne
            fin_boite_x = debut_boite_x + self.longueur_ligne
            fin_boite_y = debut_boite_y + self.longueur_ligne

            # Ici, on crée des rectangles de couleur 'grey'. Dans votre TP, vous voudrez utiliser l'attribut
            # couleur de votre boite, c'est-à-dire utiliser 'fill=boite.couleur_affichage()'.
            self.create_rectangle(debut_boite_x, debut_boite_y, fin_boite_x, fin_boite_y, tags='boite',
                                  fill=boite.couleur_affichage())

    def dessiner_lignes(self):
        # Ici, on itère sur le dictionnaire self.lignes, sans se servir de la valeur de ligne.
        # Dans le TP, on itèrera sur self.planche.lignes.items() et ligne sera un objet de type
        # Ligne.
        for cle, ligne in self.planche.lignes.items():
            ligne_point, col_point, orientation = cle

            # On retrouve les points d'ancrage en x et en y de la ligne à partir de sa ligne, de sa colonne
            # et de son orientation
            if orientation == 'H':
                debut_ligne_x = col_point * self.dimension_boite + self.largeur_ligne
                debut_ligne_y = ligne_point * self.dimension_boite
                fin_ligne_x = debut_ligne_x + self.longueur_ligne
                fin_ligne_y = debut_ligne_y + self.largeur_ligne
            else:
                debut_ligne_x = col_point * self.dimension_boite
                debut_ligne_y = ligne_point * self.dimension_boite + self.largeur_ligne
                fin_ligne_x = debut_ligne_x + self.largeur_ligne
                fin_ligne_y = debut_ligne_y + self.longueur_ligne

            # Ici, on crée des rectangles de couleur 'white'. Dans votre TP, vous voudrez utiliser l'attribut
            # couleur de votre ligne, c'est-à-dire utiliser 'fill=ligne.couleur_affichage()'.
            self.create_rectangle(debut_ligne_x,
                                  debut_ligne_y,
                                  fin_ligne_x,
                                  fin_ligne_y,
                                  tags='ligne',
                                  fill=ligne.couleur_affichage(),
                                  width=1)

    def dessiner_points(self):
        # Cette fonction crée tous les points requis à partir des attributs self.n_boites_v et self.n_boites_h.
        # Dans le TP, on lira respectivement self.planche.N_BOITES_V et self.planche.N_BOITES_H
        for col in range(self.planche.N_BOITES_V + 1):
            for ligne in range(self.planche.N_BOITES_H + 1):
                origine_cercle_x = col * self.dimension_boite
                origine_cercle_y = ligne * self.dimension_boite
                fin_cercle_x = origine_cercle_x + self.largeur_ligne
                fin_cercle_y = origine_cercle_y + self.largeur_ligne

                self.create_oval(origine_cercle_x,
                                 origine_cercle_y,
                                 fin_cercle_x,
                                 fin_cercle_y,
                                 tags='point',
                                 fill='black')

    def obtenir_coup_joue(self, event):
        '''
        Méthode qui retrouve si un clic est fait sur une ligne, une boîte ou sur un point, et surtout pour retrouver
        laquelle.

        Dans votre TP, vous pourrez vous débarasser des sections de code concernant les clics sur un
        point et sur une boîte pour conserver seulement les sections sur les lignes et retourner None
        quand le clic est sur un point ou une boîte.

        Args:
            event (Event): L'objet Event relié au clic fait sur le canvas

        Returns:
            None si le clic a été fait sur un point, (int, int, orientation) s'il
            a été fait sur une ligne et (int, int, 'Boite') si c'était une boîte
        '''
        col = int(event.x // self.dimension_boite)
        ligne = int(event.y // self.dimension_boite)

        x_relatif = event.x % self.dimension_boite
        y_relatif = event.y % self.dimension_boite

        coup = None

        if x_relatif < self.largeur_ligne:
            if y_relatif > self.largeur_ligne:
                # Clic sur une ligne verticale
                coup = (ligne, col, 'V')
            else:
                # Clic sur un point, on garde le coup à None
                # pour les besoins du labo
                coup = None
        else:
            if y_relatif < self.largeur_ligne:
                # Clic sur une ligne horizontale
                coup = (ligne, col, 'H')
            else:
                # Clic sur une boîte
                coup = (ligne, col, 'Boite')

        return coup

    def actualiser(self):
        # On supprime les anciennes boîtes et on ajoute les nouvelles.
        self.delete('boite')
        self.dessiner_boites()

        # On supprime les anciennes lignes et on ajoute les nouvelles.
        self.delete('ligne')
        self.dessiner_lignes()

        # On dessine les points
        self.dessiner_points()


class Fenetre(Tk):
    def __init__(self, partie):
        super().__init__()

        self.consigurermenu()
        # Figer la fenêtre
        self.resizable(0, 0)

        # Nom de la fenêtre.
        self.title('Pipopipette')

        # Dans le TP, vous voudrez ajouter un attribut self.partie,
        # avec comme valeur une nouvelle Partie
        self.partie = partie
        # self.partie = PartiePipopipette()
        # PartiePipopipette("pipopipette/partie_en_cours.txt")

        self.title(f'Pipopipette - au tour du joueur {self.partie.couleur_joueur_courant}')
        self.initialiser_canvas()

        # On lie un clic sur le Canvas à une méthode.
        self.canvas_planche.bind('<Button-1>', self.selectionner)

    def initialiser_canvas(self):
        # Création du canvas grille.
        # Dans le TP, vous voudrez passer self.partie.planche au constructeur
        # de Canvas
        self.canvas_planche = CanvasPipopipette(self, self.partie.planche)
        self.canvas_planche.actualiser()
        self.canvas_planche.grid()

    def selectionner(self, event):
        '''
        Méthode appelée lorsqu'un clic est fait sur votre fenêtre.

        Par défaut, comme notre fenêtre contient seulement notre Canvas, on va chercher
        le coup associé au clic à l'aide de self.canvas_planche.obtenir_coup_joue(event).

        Ici, pour vous montrer la gestion des exceptions et l'affichage de messages avec
        messagebox, on lance ici une exception ErreurClicPoint et on affiche une erreur si
        le clic a été fait sur un point (associé à un retour None de obtenir_coup_joue()).

        Dans votre TP, le retour de obtenir_coup_joue() sera à None si et seulement si le clic
        N'a PAS été effectué une ligne. Ainsi, si le coup est None, on ne fera rien, sinon on le jouera
        avec self.partie.jouer_coup(). Aussi, si le coup est sur une ligne déjà jouée, on attrapera
        l'exception lancée dans Planche.valider_coup() et on affichera un message d'erreur correspondant.
        Enfin, on s'assurera aussi de faire appel à l'actualisation du canvas et à la logique de
        fin de partie.

        Args:
            event (Event): L'objet Event relié au clic fait sur le canvas
        '''
        coup = self.canvas_planche.obtenir_coup_joue(event)

        try:
            if coup is not None:
                self.partie.planche.valider_coup(coup)
                self.partie.jouer_coup(coup)
                self.title(f'Pipopipette - au tour du joueur {self.partie.couleur_joueur_courant}')
            else:
                raise ErreurPositionCoup('Exception lancée ! Vous avez cliqué dans un point !')
        except ErreurPositionCoup as e:
            messagebox.showwarning('Erreur !', e)

        # On actualise après chaque clic pour garder un canvas bien arrimé à l'état de la partie.
        self.canvas_planche.actualiser()
        self.terminerPartie()

    def terminerPartie(self):
         if self.partie.partie_terminee():
             messagebox.showinfo("Gagnant", self.partie.message_fin_partie())
             result = messagebox.askokcancel("Question", "Voulez vous rejouer la partie")
             if result:
                 self.nouvellePartie()
             else:
                 self.destroy()

    def nouvellePartie(self):
        self.destroy()
        partie = PartiePipopipette()
        self.lancer(partie)
        # Pour charger d'une partie déjà sauvegardée
        # partie = PartiePipopipette("partie_sauvegardee.txt")

    def charger(self):
        self.fichier = filedialog.askopenfilename(title="Select file",
                                                  filetypes=(("Fichier texte", "*.txt"), ("Tous les fichiers", "*.*")))
        if self.fichier != '':
            self.destroy()
            partie = PartiePipopipette(self.fichier)
            self.lancer(partie)

    def sauvegarder(self):
        self.fichier = filedialog.asksaveasfilename(title="Select file", initialfile='partie_sauvegardee',
                                                    defaultextension=".txt",
                                                    filetypes=(
                                                        ("Fichier texte", "*.txt"), ("Tous les fichiers", "*.*")))
        if self.fichier != '':
            self.partie.sauvegarder(self.fichier)
            messagebox.showinfo("Info", "La partie est sauvegardée !")

    def consigurermenu(self):
        menubar = Menu(self)
        self.config(menu=menubar)
        menufichier = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=menufichier)
        menufichier.add_command(label="Nouvelle partie", command=self.nouvellePartie)
        menufichier.add_command(label="Charger une partie", command=self.charger)
        menufichier.add_command(label="Sauvegarder une partie", command=self.sauvegarder)
        menufichier.add_command(label="Quitter", command=self.destroy)

    def lancer(self, partie):
        self.__init__(partie)
        self.mainloop()