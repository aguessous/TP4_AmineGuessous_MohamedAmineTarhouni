# -*- coding: utf-8 -*-

from partie import PartiePipopipette
from planche import Planche
from boite import Boite
from ligne import Ligne

from collections import Counter
import traceback
import colorama

CRED = '\033[91m'
CGREEN = '\33[92m'
CEND = '\033[0m'


class Testeur:
    def __init__(self, *groupes):
        self.groupes = groupes

    def test(self):
        for groupe in self.groupes:
            groupe.executer_tous_tests()

        print("\n***BILAN FINAL***\n")

        for groupe in self.groupes:
            groupe.bilan_final()


class GroupeTest:
    def __init__(self, nom, tests, fonction_a_tester):
        self.nom = nom
        self.tests = tests
        self.fonction_a_tester = fonction_a_tester
        self.tests_echoues = []

    def executer_tous_tests(self):
        print("\n***DÉBUT TESTS {}***\n".format(self.nom.upper()))

        for test in self.tests:
            succes, msg = test.executer(self.fonction_a_tester)

            if not succes:
                self.tests_echoues.append(test.nom)
                print(CRED, end='')
                print()
                print(msg)
                print(CEND, end='')

        self._bilan_execution()

    def _bilan_execution(self):
        print()
        if len(self.tests_echoues) == 0:
            print(CGREEN, end='')
            print("Tous les {} tests du groupe {!r} ont été complétés avec succès.".format(len(self.tests), self.nom))
            print(CEND, end='')
        else:
            print(
                "Sur les {} tests du groupe {!r}, {} ont échoué. Il s'agit des tests nommés {}" \
                "Voir la sortie en console plus haut pour plus de détails." \
                .format(len(self.tests), self.nom, len(self.tests_echoues), "".join(("\n\n", CRED, *[test + "\n" for test in self.tests_echoues], CEND, "\n")))
            )

    def bilan_final(self):
        if len(self.tests_echoues) == 0:
            print(CGREEN, end='')
            print("Tous les {} tests du groupe {!r} ont été complétés avec succès.".format(len(self.tests), self.nom))
            print(CEND, end='')
        else:
            print(CRED, end='')
            print("{} des {} tests du groupe {!r} ont échoué.".format(len(self.tests_echoues), len(self.tests),
                                                                      self.nom))
            print(CEND, end='')


def _formatter_arguments(**kwargs):
    n_arguments = len(kwargs)

    if n_arguments == 0:
        return " d'appeler "
    elif n_arguments == 1:
        return " de fournir {!r}={!r} à ".format(*[item for paire in kwargs.items() for item in paire])
    else:
        pre = " de fournir les arguments " + "{!r}={!r}," * (n_arguments - 2)
        return (pre + "{!r}={!r} et {!r}={!r} à ").format(*[item for paire in kwargs.items() for item in paire])


def _formatter_attributs(**attributs):
    n_attributs = len(attributs)

    def format_attribut(nom_attribut, valeur):
        return "self.{}={}".format(nom_attribut, valeur)

    if n_attributs == 1:
        return " {}\n".format(*[format_attribut(nom, valeur) for nom, valeur in attributs.items()])
    else:
        pre = " {}\n\n" * (n_attributs - 2)
        return (pre + " {}\n\n et {} ").format(*[format_attribut(nom, valeur) for nom, valeur in attributs.items()])


def _message_erreur_sortie_defaut(nom_test, nom_fonction_a_tester, kwargs, sortie_attendue, sortie_actuelle,
                                  precisions):
    arguments = _formatter_arguments(**kwargs)

    premiere_ligne = "ÉCHEC DU TEST {} !\n".format(nom_test.upper())
    corps = "En essayant " + arguments + "votre fonction {}(), la sortie attendue était {!r} mais a " \
        "plutôt été {!r}. Pensez à utiliser le débogueur ou encore à faire imprimer des valeurs intermédiaires dans " \
        "votre fonction pour {}() pour cerner la source du problème !".format(
        nom_fonction_a_tester, sortie_attendue, sortie_actuelle, nom_fonction_a_tester)

    if precisions != '':
        corps += '\n\nLes précisions suivantes vous sont données pour vous aider à cerner le problème :\n' + precisions

    return premiere_ligne + corps


def _message_erreur_attributs_defaut(nom_test, nom_fonction_a_tester, kwargs, attributs_attendus, attributs_actuels,
                                     precisions):
    arguments = _formatter_arguments(**kwargs)
    attributs_attendus_formattes = _formatter_attributs(**attributs_attendus)
    attributs_actuels_formattes = _formatter_attributs(**attributs_actuels)

    premiere_ligne = "ÉCHEC DU TEST {} !\n".format(nom_test.upper())
    corps = "En essayant " + arguments + "votre fonction {}(), les attributs attendus étaient\n\n{}\n\nmais ont " \
        "plutôt été\n\n{}\n\nPensez à utiliser le débogueur ou encore à faire imprimer des valeurs intermédiaires dans " \
        "votre fonction pour {}() pour cerner la source du problème !".format(
        nom_fonction_a_tester, attributs_attendus_formattes, attributs_actuels_formattes, nom_fonction_a_tester)

    if precisions != '':
        corps += '\n\nLes précisions suivantes vous sont données pour vous aider à cerner le problème :\n' + precisions

    return premiere_ligne + corps


def _message_erreur_exception_defaut(nom_test, fonction_a_tester, kwargs):
    arguments = _formatter_arguments(**kwargs)

    premiere_ligne = "ÉCHEC DU TEST {} !\n".format(nom_test.upper())
    corps = "En essayant " + arguments + "votre fonction {}(), une erreur a été retournée. Cette erreur est " \
        "la suivante : \n\n{}".format(fonction_a_tester, traceback.format_exc())

    return premiere_ligne + corps


def formattage_erreur_cles_dict(paires_manquantes, paires_en_trop):
    msg = 'Les clés de dictionaire attendues ne correspondaient pas à celle reçues.\n'

    if len(paires_manquantes) > 0:
        if len(paires_manquantes) == 1:
            msg += "Une clé attendue était manquante:\n\n{}\n".format(paires_manquantes[0])
        else:
            msg += "Plusieurs clés attendues étaient manquantes:\n\n"
            msg += ("{}\n" * len(paires_manquantes)).format(*[paire for paire in paires_manquantes])

    if len(paires_en_trop) > 0:
        if len(paires_en_trop) == 1:
            msg += "Une clé reçue était en trop:\n\n{}\n".format(paires_en_trop[0])
        else:
            msg += "Plusieurs clés reçues étaient en trop:\n\n"
            msg += ("{}\n" * len(paires_en_trop)).format(*[paire for paire in paires_en_trop])

    return msg


def formattage_erreur_valeurs_dict(valeurs_non_identiques):
    msg = 'Les valeurs de dictionaire attendues ne correspondaient pas à celle reçues.\n'

    if len(valeurs_non_identiques) == 1:
        msg += "Une valeur à la clé {} était différente: on attendait {} mais on a reçu {}\n".format(*(
            valeurs_non_identiques[0]))
    else:
        msg += "Plusieurs clés étaient différentes:\n\n"
        for t in valeurs_non_identiques:
            msg += "À la clé {} on attendait {} mais on a reçu {}\n".format(*t)

    return msg


def formattage_erreur_items_liste(items_absents, items_en_trop):
    msg = 'Les items de liste attendus ne correspondaient pas à ceux reçus.\n'

    if len(items_absents) > 0:
        msg += "Les items suivants étaient attendus mais n'ont pas été reçus:\n\n"
        for item, nb_manquant in items_absents.items():
            for _ in range(nb_manquant):
                msg += '{}\n'.format(item)

    if len(items_en_trop) > 0:
        msg += "Les items suivants ont été reçus mais n'étaient pas attendus:\n\n"
        for item, nb_en_trop in items_en_trop.items():
            for _ in range(nb_en_trop):
                msg += '{}\n'.format(item)

    return msg


def _operateur_egalite_defaut(sortie_attendue, sortie_recue):
    type_attendu, type_recu = type(sortie_attendue), type(sortie_recue)

    if type_attendu is type_recu:
        if isinstance(sortie_attendue, dict):
            cles_manquantes = set(sortie_attendue.keys()) - set(sortie_recue.keys())
            cles_en_trop = set(sortie_recue.keys()) - set(sortie_attendue.keys())

            if len(cles_manquantes | cles_en_trop) > 0:
                return formattage_erreur_cles_dict([(cle, sortie_attendue[cle]) for cle in cles_manquantes],
                                                   [(cle, sortie_recue[cle]) for cle in cles_en_trop])

            valeurs_non_identiques = [(cle, sortie_attendue[cle], sortie_recue[cle]) for cle in sortie_attendue
                                      if _operateur_egalite_defaut(sortie_attendue[cle], sortie_recue[cle]) is not None]

            if len(valeurs_non_identiques) == 0:
                return None
            else:
                return formattage_erreur_valeurs_dict(valeurs_non_identiques)
        elif isinstance(sortie_attendue, list) or isinstance(sortie_attendue, tuple):
            items_absents = Counter(sortie_attendue)
            items_absents.subtract(Counter(sortie_recue))
            items_absents = {k: v for k, v in items_absents.items() if v > 0}

            items_en_trop = Counter(sortie_recue)
            items_en_trop.subtract(Counter(sortie_attendue))
            items_en_trop = {k: v for k, v in items_en_trop.items() if v > 0}

            if sum(items_absents.values()) + sum(items_en_trop.values()) > 0:
                return formattage_erreur_items_liste(items_absents, items_en_trop)
            else:
                return None
        elif isinstance(sortie_attendue, Boite) or isinstance(sortie_attendue, Ligne):
            if _operateur_egalite_defaut(vars(sortie_attendue), vars(sortie_recue)) is None:
                return None
            else:
                return ''
        else:
            if sortie_attendue == sortie_recue:
                return None
            else:
                return ''
    else:
        return 'La sortie attendue était de type {} alors que la sortie reçue a plutôt été de type {}'.format(
            type_attendu, type_recu)


def operateur_egalite_un_item_tuple(index_a_tester):
    return lambda sortie_attendue, sortie_recue: _operateur_egalite_defaut(sortie_attendue, sortie_recue[index_a_tester]
                                                                           )


class TestSortieObjet:
    def __init__(self,
                 objet,
                 nom,
                 kwargs,
                 sortie_attendue,
                 msg_erreur_sortie=_message_erreur_sortie_defaut,
                 msg_erreur_exception=_message_erreur_exception_defaut,
                 operateur_egalite=_operateur_egalite_defaut):
        self.objet = objet
        self.nom = nom
        self.kwargs = kwargs
        self.sortie_attendue = sortie_attendue
        self.msg_erreur_sortie = msg_erreur_sortie
        self.msg_erreur_exception = msg_erreur_exception
        self.operateur_egalite = operateur_egalite

    def executer(self, nom_fonction_a_tester):
        try:
            self.objet = self.objet()
            sortie_actuelle = getattr(self.objet, nom_fonction_a_tester)(**self.kwargs)

            msg_erreur = self.operateur_egalite(self.sortie_attendue, sortie_actuelle)
            if msg_erreur is None:
                return True, None
            else:
                return False, self.msg_erreur_sortie(self.nom, nom_fonction_a_tester, self.kwargs, self.sortie_attendue,
                                                     sortie_actuelle, msg_erreur)

        except:
            return False, self.msg_erreur_exception(self.nom, nom_fonction_a_tester, self.kwargs)


class TestAttributsObjet:
    def __init__(self,
                 objet,
                 nom,
                 kwargs,
                 attributs_attendus,
                 msg_erreur_attribut=_message_erreur_attributs_defaut,
                 msg_erreur_exception=_message_erreur_exception_defaut,
                 operateur_egalite=_operateur_egalite_defaut):
        self.objet = objet
        self.nom = nom
        self.kwargs = kwargs
        self.attributs_attendus = attributs_attendus
        self.msg_erreur_attribut = msg_erreur_attribut
        self.msg_erreur_exception = msg_erreur_exception
        self.operateur_egalite = operateur_egalite

    def executer(self, nom_fonction_a_tester):
        try:
            self.objet = self.objet()
            getattr(self.objet, nom_fonction_a_tester)(**self.kwargs)

            attributs_actuels = {nom: getattr(self.objet, nom) for nom in self.attributs_attendus}

            msg_erreurs = [
                self.operateur_egalite(attendu, actuel)
                for attendu, actuel in zip(self.attributs_attendus.values(), attributs_actuels.values())
            ]

            if all([msg is None for msg in msg_erreurs]):
                return True, None
            else:
                return False, self.msg_erreur_attribut(self.nom, nom_fonction_a_tester, self.kwargs,
                                                       self.attributs_attendus, attributs_actuels,
                                                       '\n\n'.join([msg for msg in msg_erreurs if msg is not None]))

        except:
            return False, self.msg_erreur_exception(self.nom, nom_fonction_a_tester, self.kwargs)


def planche_vide():
    return Planche()


def planche_presque_vide():
    planche = Planche()

    planche.lignes[(0, 0, 'H')].jouee = True

    return planche


def planche_pleine():
    planche = Planche()

    for ligne in planche.lignes.values():
        ligne.jouee = True

    for index, boite in planche.boites.items():
        num = index[0] + index[1]

        boite.assigner_couleur("rouge" if num % 2 == 0 else "bleu")

    return planche


def planche_presque_pleine():
    planche = planche_pleine()

    planche.lignes[(0, 0, 'H')].jouee = False
    planche.boites[(0, 0)].pleine = False
    planche.boites[(0, 0)].couleur = ''

    return planche


def obj_to_func(obj):
    return lambda: obj


def groupe_init_boites():
    tests = []

    boites_attendues = {
        (0, 0): Boite(),
        (1, 0): Boite(),
        (2, 0): Boite(),
        (0, 1): Boite(),
        (1, 1): Boite(),
        (2, 1): Boite(),
        (0, 2): Boite(),
        (1, 2): Boite(),
        (2, 2): Boite()
    }

    tests.append(TestAttributsObjet(planche_vide, 'test_initilisation_boites', {}, {'boites': boites_attendues}))
    tests.append(TestAttributsObjet(planche_pleine, 'test_reinitilisation_boites', {}, {'boites': boites_attendues}))

    return GroupeTest('Planche.init_boites', tests, 'initialiser_boites')


def groupe_init_lignes():
    tests = []

    lignes_attendues = {
        (0, 3, 'V'): Ligne(),
        (1, 3, 'V'): Ligne(),
        (2, 3, 'V'): Ligne(),
        (3, 0, 'H'): Ligne(),
        (3, 1, 'H'): Ligne(),
        (3, 2, 'H'): Ligne(),
        (0, 0, 'H'): Ligne(),
        (0, 0, 'V'): Ligne(),
        (1, 0, 'H'): Ligne(),
        (1, 0, 'V'): Ligne(),
        (2, 0, 'H'): Ligne(),
        (2, 0, 'V'): Ligne(),
        (0, 1, 'H'): Ligne(),
        (0, 1, 'V'): Ligne(),
        (1, 1, 'H'): Ligne(),
        (1, 1, 'V'): Ligne(),
        (2, 1, 'H'): Ligne(),
        (2, 1, 'V'): Ligne(),
        (0, 2, 'H'): Ligne(),
        (0, 2, 'V'): Ligne(),
        (1, 2, 'H'): Ligne(),
        (1, 2, 'V'): Ligne(),
        (2, 2, 'H'): Ligne(),
        (2, 2, 'V'): Ligne()
    }

    ma_planche_pleine = planche_vide()
    for ligne in ma_planche_pleine.lignes.values():
        ligne.jouee = True

    tests.append(TestAttributsObjet(planche_vide, 'test_initilisation_lignes', {}, {'lignes': lignes_attendues}))
    tests.append(
        TestAttributsObjet(obj_to_func(ma_planche_pleine), 'test_reinitilisation_lignes', {},
                           {'lignes': lignes_attendues}))

    return GroupeTest('Planche.init_lignes', tests, 'initialiser_lignes')


def tests_etape_1():
    print("*******TESTS ÉTAPE 1*******\n")
    testeur = Testeur(groupe_init_boites(), groupe_init_lignes())
    testeur.test()


def groupe_coup_dans_les_limites():
    tests = []

    tests.append(TestSortieObjet(planche_vide, 'test_horizontale_en_jeu', {'index_ligne': (1, 0, 'H')}, True))
    tests.append(TestSortieObjet(planche_vide, 'test_verticale_en_jeu', {'index_ligne': (1, 2, 'V')}, True))
    tests.append(TestSortieObjet(planche_vide, 'test_colonne_negative', {'index_ligne': (1, -1, 'H')}, False))
    tests.append(TestSortieObjet(planche_vide, 'test_colonne_trop_elevee', {'index_ligne': (1, 4, 'H')}, False))
    tests.append(TestSortieObjet(planche_vide, 'test_ligne_negative', {'index_ligne': (-1, 1, 'H')}, False))
    tests.append(TestSortieObjet(planche_vide, 'test_ligne_trop_elevee', {'index_ligne': (4, 0, 'H')}, False))
    tests.append(TestSortieObjet(planche_vide, 'test_orientation_invalide', {'index_ligne': (1, 0, 'Invalide')}, False))
    tests.append(TestSortieObjet(planche_vide, 'test_ligne_horizontale_bas', {'index_ligne': (3, 0, 'H')}, True))
    tests.append(TestSortieObjet(planche_vide, 'test_verticale_droite', {'index_ligne': (1, 3, 'V')}, True))

    return GroupeTest('Planche.coup_dans_les_limites', tests, 'coup_dans_les_limites')


def groupe_est_pleine():
    tests = []

    tests.append(TestSortieObjet(planche_vide, 'test_planche_vide', {}, False))
    tests.append(TestSortieObjet(planche_pleine, 'test_planche_pleine', {}, True))

    return GroupeTest('Planche.est_pleine', tests, 'est_pleine')


def groupe_jouer_coup():
    tests = []

    ligne_jouee = Ligne()
    ligne_jouee.jouee = True
    lignes_attendues = {
        (0, 3, 'V'): Ligne(),
        (1, 3, 'V'): Ligne(),
        (2, 3, 'V'): Ligne(),
        (3, 0, 'H'): Ligne(),
        (3, 1, 'H'): Ligne(),
        (3, 2, 'H'): Ligne(),
        (0, 0, 'H'): Ligne(),
        (0, 0, 'V'): Ligne(),
        (1, 0, 'H'): Ligne(),
        (1, 0, 'V'): Ligne(),
        (2, 0, 'H'): Ligne(),
        (2, 0, 'V'): Ligne(),
        (0, 1, 'H'): Ligne(),
        (0, 1, 'V'): Ligne(),
        (1, 1, 'H'): Ligne(),
        (1, 1, 'V'): Ligne(),
        (2, 1, 'H'): Ligne(),
        (2, 1, 'V'): Ligne(),
        (0, 2, 'H'): Ligne(),
        (0, 2, 'V'): ligne_jouee,
        (1, 2, 'H'): Ligne(),
        (1, 2, 'V'): Ligne(),
        (2, 2, 'H'): Ligne(),
        (2, 2, 'V'): Ligne()
    }

    tests.append(
        TestAttributsObjet(planche_vide, 'test_jouer_coup_rouge', {
            'index_ligne': (0, 2, 'V'),
            'couleur': 'rouge'
        }, {
            'lignes': lignes_attendues,
            'couleur_dernier_coup': 'rouge',
            'position_dernier_coup': (0, 2, 'V')
        }))
    tests.append(
        TestAttributsObjet(planche_vide, 'test_jouer_coup_bleu', {
            'index_ligne': (0, 2, 'V'),
            'couleur': 'bleu'
        }, {
            'lignes': lignes_attendues,
            'couleur_dernier_coup': 'bleu',
            'position_dernier_coup': (0, 2, 'V')
        }))

    return GroupeTest('Planche.jouer_coup', tests, 'jouer_coup')


def groupe_valider_coup():
    tests = []

    tests.append(
        TestSortieObjet(planche_vide,
                        'test_coup_valide', {'index_ligne': (0, 0, 'H')},
                        True,
                        operateur_egalite=operateur_egalite_un_item_tuple(index_a_tester=0)))
    tests.append(
        TestSortieObjet(planche_vide,
                        'test_orientation_invalide', {'index_ligne': (0, 0, 'Invalide')},
                        False,
                        operateur_egalite=operateur_egalite_un_item_tuple(index_a_tester=0)))
    tests.append(
        TestSortieObjet(planche_vide,
                        'test_coup_hors_limites', {'index_ligne': (-1, -1, 'H')},
                        False,
                        operateur_egalite=operateur_egalite_un_item_tuple(index_a_tester=0)))
    tests.append(
        TestSortieObjet(planche_pleine,
                        'test_ligne_deja_jouee', {'index_ligne': (0, 0, 'H')},
                        False,
                        operateur_egalite=operateur_egalite_un_item_tuple(index_a_tester=0)))

    return GroupeTest('Planche.valider_coup', tests, 'valider_coup')


def groupe_obtenir_coups_possible():
    tests = []

    toutes_lignes = [(0, 3, 'V'), (1, 3, 'V'), (2, 3, 'V'), (3, 0, 'H'), (3, 1, 'H'), (3, 2, 'H'), (0, 0, 'H'),
                     (0, 0, 'V'), (1, 0, 'H'), (1, 0, 'V'), (2, 0, 'H'), (2, 0, 'V'), (0, 1, 'H'), (0, 1, 'V'),
                     (1, 1, 'H'), (1, 1, 'V'), (2, 1, 'H'), (2, 1, 'V'), (0, 2, 'H'), (0, 2, 'V'), (1, 2, 'H'),
                     (1, 2, 'V'), (2, 2, 'H'), (2, 2, 'V')]
    presque_toutes_lignes = toutes_lignes.copy()
    presque_toutes_lignes.remove((0, 0, 'H'))
    aucune_ligne = []
    une_ligne = [(0, 0, 'H')]

    tests.append(TestSortieObjet(planche_vide, 'test_obtenir_coups_planche_vide', {}, toutes_lignes))
    tests.append(
        TestSortieObjet(planche_presque_vide, 'test_obtenir_coups_planche_presque_vide', {}, presque_toutes_lignes))
    tests.append(TestSortieObjet(planche_pleine, 'test_obtenir_coups_planche_pleine', {}, aucune_ligne))
    tests.append(TestSortieObjet(planche_presque_pleine, 'test_obtenir_coups_planche_presque_pleine', {}, une_ligne))

    return GroupeTest('Planche.obtenir_coups_possibles', tests, 'obtenir_coups_possibles')


def tests_etape_2():
    print("*******TESTS ÉTAPE 2*******\n")
    testeur = Testeur(groupe_coup_dans_les_limites(), groupe_est_pleine(), groupe_jouer_coup(), groupe_valider_coup(),
                      groupe_obtenir_coups_possible())
    testeur.test()


def groupe_obtenir_idx_boites_a_valider():
    tests = []

    p_h = planche_vide()
    p_h.position_dernier_coup = (1, 1, 'H')

    tests.append(
        TestSortieObjet(obj_to_func(p_h), 'test_obtenir_idx_boites_a_valider_ligne_horizontale_milieu', {}, [(0, 1),
                                                                                                             (1, 1)]))

    p_v = planche_vide()
    p_v.position_dernier_coup = (1, 1, 'V')

    tests.append(
        TestSortieObjet(obj_to_func(p_v), 'test_obtenir_idx_boites_a_valider_ligne_verticale_milieu', {}, [(1, 0),
                                                                                                           (1, 1)]))

    p_h_haut = planche_vide()
    p_h_haut.position_dernier_coup = (0, 1, 'H')

    tests.append(
        TestSortieObjet(obj_to_func(p_h_haut), 'test_obtenir_idx_boites_a_valider_ligne_horizontale_haut', {},
                        [(0, 1)]))

    p_h_bas = planche_vide()
    p_h_bas.position_dernier_coup = (3, 1, 'H')

    tests.append(
        TestSortieObjet(obj_to_func(p_h_bas), 'test_obtenir_idx_boites_a_valider_ligne_horizontale_bas', {}, [(2, 1)]))

    p_v_gauche = planche_vide()
    p_v_gauche.position_dernier_coup = (1, 0, 'V')

    tests.append(
        TestSortieObjet(obj_to_func(p_v_gauche), 'test_obtenir_idx_boites_a_valider_ligne_verticale_gauche', {},
                        [(1, 0)]))

    p_v_droite = planche_vide()
    p_v_droite.position_dernier_coup = (1, 3, 'V')

    tests.append(
        TestSortieObjet(obj_to_func(p_v_droite), 'test_obtenir_idx_boites_a_valider_ligne_verticale_droite', {},
                        [(1, 2)]))

    return GroupeTest('Planche.obtenir_idx_boites_a_valider', tests, 'obtenir_idx_boites_a_valider')


def groupe_compter_lignes_jouees_boite():
    tests = []

    planche = planche_vide()

    tests.append(
        TestSortieObjet(obj_to_func(planche), 'test_compter_lignes_jouees_boite_sans_ligne_jouee',
                        {'idx_boite': (0, 0)}, 0))

    planche = planche_vide()
    planche.lignes[(0, 0, 'H')].jouee = True
    tests.append(
        TestSortieObjet(obj_to_func(planche), 'test_compter_lignes_jouees_boite_ligne_haut_jouee',
                        {'idx_boite': (0, 0)}, 1))

    planche = planche_vide()
    planche.lignes[(2, 1, 'H')].jouee = True
    tests.append(
        TestSortieObjet(obj_to_func(planche), 'test_compter_lignes_jouees_boite_ligne_bas_jouee', {'idx_boite': (1, 1)},
                        1))

    planche = planche_vide()
    planche.lignes[(1, 2, 'V')].jouee = True
    tests.append(
        TestSortieObjet(obj_to_func(planche), 'test_compter_lignes_jouees_boite_ligne_gauche_jouee',
                        {'idx_boite': (1, 2)}, 1))

    planche = planche_vide()
    planche.lignes[(2, 2, 'V')].jouee = True
    tests.append(
        TestSortieObjet(obj_to_func(planche), 'test_compter_lignes_jouees_boite_ligne_droite_jouee',
                        {'idx_boite': (2, 1)}, 1))

    planche = planche_pleine()
    tests.append(
        TestSortieObjet(obj_to_func(planche), 'test_compter_lignes_jouees_boite_toutes_lignes_jouees',
                        {'idx_boite': (1, 1)}, 4))

    return GroupeTest('Planche.compter_lignes_jouees_boite', tests, 'compter_lignes_jouees_boite')


def groupe_bilan_boites():
    tests = []

    tests.append(TestSortieObjet(planche_pleine, 'test_bilan_boites_5_rouges_4_bleus', {}, (4, 5)))

    planche_rouge = planche_pleine()

    for boite in planche_rouge.boites.values():
        boite.couleur = 'rouge'

    tests.append(TestSortieObjet(obj_to_func(planche_rouge), 'test_bilan_boites_planche_pleine_rouge', {}, (0, 9)))

    return GroupeTest('Planche.bilan_boites', tests, 'bilan_boites')


def tests_etape_3():
    print("*******TESTS ÉTAPE 3*******\n")
    testeur = Testeur(groupe_obtenir_idx_boites_a_valider(), groupe_compter_lignes_jouees_boite(),
                      groupe_bilan_boites())
    testeur.test()


def tests_complets():
    print("*******TESTS COMPLETS*******\n")
    testeur = Testeur(groupe_init_boites(), groupe_init_lignes(), groupe_coup_dans_les_limites(), groupe_est_pleine(),
                      groupe_jouer_coup(), groupe_valider_coup(), groupe_obtenir_coups_possible(),
                      groupe_obtenir_idx_boites_a_valider(), groupe_compter_lignes_jouees_boite(),
                      groupe_bilan_boites())
    testeur.test()


if __name__ == "__main__":
    colorama.init()
    # Commentez et décommentez les tests correspondant à l'étape à laquelle vous êtes rendu
    # pour conserver une sortie claire.
    # tests_etape_1()
    # tests_etape_2()
    # tests_etape_3()
    tests_complets()