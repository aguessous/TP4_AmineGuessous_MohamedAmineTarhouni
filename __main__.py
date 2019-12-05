from tkinter import Menu

from pipopipette.partie import PartiePipopipette
from interface.interface_pipopipette import Fenetre

if __name__ == '__main__':

    partie = PartiePipopipette()
    # partie.jouer()
    f = Fenetre(partie)
    f.mainloop()


