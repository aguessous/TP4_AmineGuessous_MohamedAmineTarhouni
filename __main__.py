
from pipopipette.partie import PartiePipopipette
from interface.interface_pipopipette import Fenetre

if __name__ == '__main__':
    # partie = PartiePipopipette()

    # Pour charger d'une partie déjà sauvegardée
    partie = PartiePipopipette("interface/partie_en_cours.txt")

    # Pour sauvegarder une partie
    # partie.sauvegarder("partie_sauvegardee.txt")

    # partie.jouer()
    f = Fenetre(partie)
    f.mainloop()