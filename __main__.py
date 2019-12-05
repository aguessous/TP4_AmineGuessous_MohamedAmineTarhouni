from tkinter import Menu

from pipopipette.partie import PartiePipopipette
from interface.interface_pipopipette import Fenetre

if __name__ == '__main__':
    # partie = PartiePipopipette()

    # Pour charger d'une partie déjà sauvegardée
    # partie = PartiePipopipette("partie_sauvegardee.txt")

    # Pour sauvegarder une partie
    # partie.sauvegarder("partie_sauvegardee.txt")

    # partie.jouer()
    f = Fenetre()
    menubar = Menu(f)
    f.config(menu=menubar)
    menufichier = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Menu", menu=menufichier)
    menufichier.add_command(label="Charger une partie ")
    menufichier.add_command(label="Sauvegarder une partie")
    menufichier.add_command(label="Quitter")
    f.mainloop()