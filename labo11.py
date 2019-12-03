from tkinter import Tk, Canvas


class CanvasPipopipette(Canvas):
    def __init__(self, parent, n_pixels_par_case=200):
        self.n_pixels_case = n_pixels_par_case

        self.n_lignes = 3
        self.n_colonnes = 3
        self.lignes = {
            (0, 0, 'H'): '00H',
            (0, 0, 'V'): '00V',
            (0, 1, 'H'): '01H',
            (0, 1, 'V'): '01V',
            (0, 2, 'H'): '02H',
            (0, 2, 'V'): '02V',
            (1, 0, 'H'): '10H',
            (1, 0, 'V'): '10V',
            (1, 1, 'H'): '11H',
            (1, 1, 'V'): '11V',
            (1, 2, 'H'): '12H',
            (1, 2, 'V'): '12V',
            (2, 0, 'H'): '20H',
            (2, 0, 'V'): '20V',
            (2, 1, 'H'): '21H',
            (2, 1, 'V'): '21V',
            (2, 2, 'H'): '22H',
            (2, 2, 'V'): '22V',
            (3, 0, 'H'): '30H',
            (0, 3, 'V'): '03V',
            (3, 1, 'H'): '31H',
            (1, 3, 'V'): '13V',
            (3, 2, 'H'): '32H',
            (2, 3, 'V'): '23V',
        }
        self.boites = {
            (0, 0): 'Boite_00',
            (0, 1): 'Boite_01',
            (0, 2): 'Boite_02',
            (1, 0): 'Boite_10',
            (1, 1): 'Boite_11',
            (1, 2): 'Boite_12',
            (2, 0): 'Boite_20',
            (2, 1): 'Boite_21',
            (2, 2): 'Boite_22',
        }
        super().__init__(parent, width=3*self.n_pixels_case, height=3*self.n_pixels_case)

    def actualiser_canvas(self):
        self.dessiner_boite()

    def dessiner_boite(self):
        for index_boite in self.boites.keys():
            ligne, colonne = index_boite

            debut_x = colonne * self.n_pixels_case
            debut_y = ligne * self.n_pixels_case

            fin_x = debut_x + self.n_pixels_case
            fin_y = debut_y + self.n_pixels_case

            self.create_rectangle(debut_x, debut_y, fin_x, fin_y, fill="grey")

class Fenetre(Tk):
    def __init__(self):
        super().__init__()

        self.canvas = CanvasPipopipette(self)
        self.canvas.actualiser_canvas()
        self.canvas.grid()
        self.canvas.bind('<Button-1>', self.clic_canvas)

    def clic_canvas(self, event):
        boite_clic = self.obtenir_boite_clic(event)

        print(boite_clic)

    def obtenir_boite_clic(self, event):
        x = event.x
        y = event.y
        ligne = y // self.canvas.n_pixels_case
        col = x // self.canvas.n_pixels_case

        boite_clic = self.canvas.boites[ligne, col]

        return boite_clic


if __name__=='__main__':
    f = Fenetre()
    f.mainloop()

