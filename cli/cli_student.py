#!/usr/bin/env python3
def new_file():
    pass


def delete_file():
    pass


def file_change_script_attribute():
    pass


def file_add_course():
    pass


def file_add_tag():
    pass


def file_remove_course():
    pass


def file_remove_tag():
    # ### --all
    pass


def move_file():
    pass


def open_file_in_graphical_user_interface_editor():
    pass


def open_file_in_vi():
    pass


def list_courses():
    # ### --subbed
    pass


def list_owned_files():
    pass


def list_sorted_files_on_tags(tags):
    """
    Fonction permettant generer les lignes de chaines de caracteres a afficher en console
        comme resultat du tri sur un ou plusieurs tags

    :param tags: list
        Liste des tags sur base desquels il faut trier les fichiers
    :return content_do_display: list
        Liste des lignes de fichier (sous forme de string) a afficher en console
        Chaque ligne presente plusieurs champs :
            * id={File.file_id}
            * pathname={File.pathname}
            * course={course_name}
                    on trouve course_name grace a File.course_id en allant chercher dans le fichier courses.pkl
                    grace a la fonction cli.cli_misc.pickle_get()
                        persistent_data = cli.cli_misc.pickle_get(all_courses=True)
                        all_courses = persistent_data[3]
                        course_name = all_course["objects_dict"][File.course_id]
            * script={File.script}
    """

    # RECUPERER L'ENTIERETE DES FICHIERS GRACE A LA FONCTION cli.cli_misc.pickle_get()
    # CFR EXPLICATION POUR RECUPERER all_courses DANS LA DOCSTRING
    # NB: tu peux faire en sorte de recupere les deux en une seule ligne :
    #           persistent_data = cli.cli_misc.pickle_get(all_files=True, all_courses=True)
    #           all_files = persistent_data[2]
    #           all_courses = persistent_data[3]

    # UNE FOIS FAIT, IL NE FAUT GARDER QUE LES FICHIERS QUE L'UTILISATEUR CONNECTE POSSEDE
    #   TU PEUX LE SAVOIR GRACE A File.user_id
    #   File.user_id DOIT CORRESPONDRE A current_user_instance.user_id
    #   current_user_instance est normalement defini dans cli.temp_main grace a la fonction cli.cli_misc.login

    # UNE FOIS FAIT, IL NE FAUT GARDER QUE LES FICHIERS QUI POSSEDENT LE (OU LES) TAG(S) SPECIFIES

    content_to_display = []
    # GENERER, POUR CHAQUE FICHIER SELECTIONE, UNE CHAINE DE CARACTERE REPONDANT AUX CONDITIONS DECRITES
    #   DANS LA DOCSTRING AU NIVEAU DE LA DESCRIPTION DE content_to_display ET
    #   LES ENREGISTRER DANS content_to_display

    # RETOURNER content_to_display
    return content_to_display


def list_sorted_files_on_course(course_name):
    """
        Fonction permettant generer les lignes de chaines de caracteres a afficher en console
            comme resultat du tri sur un cours

        :param course_name: str
            Nom du cours sur base duquel il faut trier les fichiers
        :return content_do_display: list
            Liste des lignes de fichier (sous forme de string) a afficher en console
            Chaque ligne presente plusieurs champs :
                * id={File.file_id}
                * pathname={File.pathname}
                * course={course_name}
                        NB :    ici course_name est donne, mais pour effectuer le tri, il sera necessaire de connaitre
                                    course_id (vu que c'est course_id qui est enregistre dans un fichier pour
                                    specifier son appartenance a un cours)
                                on trouve course_id en allant chercher dans le fichier courses.pkl
                                    grace a la fonction cli.cli_misc.pickle_get()
                                        persistent_data = cli.cli_misc.pickle_get(all_courses=True)
                                        all_courses = persistent_data[3]
                                        course_id = all_course["name_id_dict"][course_name]
                * script={File.script}
        """

    # RECUPERER L'ENTIERETE DES FICHIERS GRACE A LA FONCTION cli.cli_misc.pickle_get()
    # CFR EXPLICATION POUR RECUPERER all_courses DANS LA DOCSTRING
    # NB: tu peux faire en sorte de recupere les deux en une seule ligne :
    #           persistent_data = cli.cli_misc.pickle_get(all_files=True, all_courses=True)
    #           all_files = persistent_data[2]
    #           all_courses = persistent_data[3]

    # UNE FOIS FAIT, IL NE FAUT GARDER QUE LES FICHIERS QUE L'UTILISATEUR CONNECTE POSSEDE
    #   TU PEUX LE SAVOIR GRACE A File.user_id
    #   File.user_id DOIT CORRESPONDRE A current_user_instance.user_id
    #   current_user_instance est defini dans cli.temp_main grace a la fonction cli.cli_misc.login

    # UNE FOIS FAIT, IL NE FAUT GARDER QUE LES FICHIERS QUI SONT ASSOCIES AU COURS SPECIFIE

    content_to_display = []
    # GENERER, POUR CHAQUE FICHIER SELECTIONE, UNE CHAINE DE CARACTERE REPONDANT AUX CONDITIONS DECRITES
    #   DANS LA DOCSTRING AU NIVEAU DE LA DESCRIPTION DE content_to_display ET
    #   LES ENREGISTRER DANS content_to_display

    # RETOURNER content_to_display
    return content_to_display
