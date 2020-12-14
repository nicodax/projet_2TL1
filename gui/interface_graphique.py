#!/usr/bin/env python3
from gui.exceptions import WrongExtensionException
########################################################################################################
# LOGIN WINDOW
########################################################################################################

def connexion():
    """
    POST: Lance tool.window si username et mot de passe existe et corresponde.
    RAISES: Affiche un message d erreur si username et mot de passe ne sont pas reconnu.
    """

    # Cette fonction est liee a un bouton(submit) pour verifier le nom utilisateur
    #   et le mot de passe present dans des zone de texte.
    # Si ca correspond, la fenetre ce ferme et ouvre la fenetre tool_window. Sinon
    #   une zone de texte error apparait et dit de verifier le nom utilisateur et le
    #   mot de passe.
    pass


########################################################################################################
# TOOL WINDOW
########################################################################################################

def new():
    """
    POST: Ouvre editor_window (zone de texte vide).
    """
    # Cette fonction est liee a un bouton qui ouvre une seconde page avec un
    #   editeur de texte vide.
    pass


def verify_extension(fichier):
    try:
        extension = fichier.split(".")[-1]
        if extension == "py" or extension == "txt":
            return True
        else:
            raise WrongExtensionException
    except WrongExtensionException:
        pass #affiche erreur


def open():
    """
    POST: Ouvre un navigateur de fichier, puis après avoir choisis un fichier,
        ouvre editor_window avec son contenu (dans la zone de texte).
    RAISES: Affiche un message d erreur si le fichier n'a ni l'extension .txt, ni
        l'extension .py.
    """
    # Cette fonction est liee a un bouton qui ouvre une seconde page avec un
    #   editeur de texte qui contient un fichier deja existant.
    pass


def delete():
    """
    POST: Ouvre un navigateur de fichier, puis après avoir choisis un fichier,
        supprime ce dernier.
     RAISES: Affiche un message d erreur si le fichier n'a ni l'extension .txt, ni
        l'extension .py.
    """
    # Cette fonction est liee a un bouton qui ouvre un navigateur de fichier et
    # supprime le fichier selectionner
    pass


def get_list():
    """
    POST: Affiche la liste des fichiers, des cours ou des utilisateurs recenses
        apres avoir clique sur le bouton submit, dans l espace prevu pour cela selon
        l'element (a affiche) selectionne dans la liste deroulante.
    """
    # Cette fonction est liee a un bouton(submit) qui une fois clique envoie la liste des fichiers
    #   , des cours ou des utilisateurs recenses en fonction a une zone de texte/une liste deroulante
    #   contenu sur la meme fenetre.
    pass


def sort():
    """
    POST: Affiche la liste des fichiers, apres avoir clique sur le bouton submit,
        dans l espace prevu pour cela selon le(s) etiquette(s)/cours defini dans
        la zone de texte/liste.
    """
    # Cette fonction est liee a un bouton(submit) qui en fonction du cours/tag ecrit/selectionne dans un(e)
    #   zone de texte/liste affichera les fichiers appartenant a ce cours/tag dans une zone de texte.
    pass


########################################################################################################
# EDITOR WINDOW
########################################################################################################

def leave():
    """
    POST: Ferme la fenetre editor_window apres avoir cliquer sur le bouton quitter.
    """
    # Cette fonction est liee a une liste deroulante (onglet quitter) qui ferme la fenetre editor_window.
    pass


def enregistrer():
    """
    POST: Ouvre le navigateur de fichier apres avoir cliquer sur l'onglet
        enregistrer et sauvegarde le fichier a l endroit choisi.
    """
    # Cette fonction est liee a une liste deroulante (onglet enregistrer) qui ouvre le navigateur de fichier
    #   et sauvegarde le fichier a l endroit choisi.
    pass


def deplacer():
    """
    POST: Ouvre le navigateur de fichier apres avoir cliquer sur l'onglet
        deplacer et deplace le fichier a l endroit choisi.
    """
    # Cette fonction est liee a une liste deroulante (onglet deplacer) qui ouvre le navigateur de fichier
    #    et deplace le fichier a l endroit choisi.
    pass


def attribute_tag_or_course():
    """
    POST: Attribue un(e) cours/etiquette au fichier ouvert apres avoir cliquer sur le bouton submit qui
        recupere la valeur de la liste/zone de texte. Dans le cas d'un cours, si le cours existe deja, remplace
        ce cours sans problemes.
    """
    # Cette fonction est liee un bouton qui une fois clique attribue l etiquette encodee dans une zone de texte
    #   au fichier ouvert.
    pass


if __name__ == "__main__":
    pass
