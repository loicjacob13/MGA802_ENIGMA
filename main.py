"""
MGA802 - Mini-Projet A
Auteurs: Loïc Jacob, Fabien Koch, Guillaume Pissang

Description:
Programme de chiffrement et de déchiffement avec la méthode de César et de Enigma-César

Objectif:
Etre capable de chiffrer un texte, de le déchiffre avec ou sans la clé (utilisation de méthodes de brute-force)
en utilisant l'une des deux méthodes
"""

import string

#CONSTANTES

alphabet = string.ascii_lowercase #renvoie l'alphabet
liste_chiffres= list(range(10)) #renvoie les chiffres

def normaliser(texte):
    """Renvoie une lettre sans accent par l'intermédiaire d'un dictionnaire"""
    accents = { #création du dico accents
        'à': 'a', 'â': 'a', 'á': 'a', 'ä': 'a',
        'è': 'e', 'ê': 'e', 'é': 'e', 'ë': 'e',
        'î': 'i', 'ï': 'i', 'í': 'i', 'ì': 'i',
        'ô': 'o', 'ó': 'o', 'ö': 'o', 'ò': 'o',
        'û': 'u', 'ú': 'u', 'ü': 'u', 'ù': 'u',
        'ç': 'c', 'ñ': 'n',
    }
    resultat =""
    for lettre in texte:
        minuscule = lettre.lower()
        if minuscule in accents:
            sans_accent = accents[minuscule]
            resultat += sans_accent.upper() if lettre.isupper() else sans_accent
        else:
            resultat += lettre
    return resultat

def lire_texte(fichier_a_lire):

    while True:
        print("=" * 60)
        print("Voulez-vous écrire votre texte ou ouvrir un fichier ?")
        print("1- Écrire votre texte")
        print("2- Ouvrir un fichier")
        print("3- Coller un texte multiligne")
        print("=" * 60)
        try:
            choix = int(input("1, 2 ou 3 ? ").strip())
        except ValueError:  #Si l'utilisateur tape "a" au lieu de 1, 2 ou 3
            print("Erreur : entrez uniquement 1, 2 ou 3.\n")
            continue  #On recommence la boucle

        if choix == 1:        #Cas 1 pour un texte avec une seule ligne (trivial)
            texte_original= input("Écrivez votre texte ici (pas de retour à la ligne possible) : ")
            return normaliser(texte_original)

        elif choix == 2: #Cas 2 avec un fichier, on boucle jusqu'à ce que le fichier existe
            while True:
                chemin = input("Nom du fichier au format .txt (il faut le path complet du fichier) ? ").strip().strip('"')
                try:
                    with open(chemin, "r", encoding="utf-8") as fichier:
                        contenu = fichier.read()
                        return normaliser(contenu)
                except FileNotFoundError:  #Si le fichier n'existe pas
                    print(f"Erreur : le fichier '{chemin}' est introuvable, réessayez.\n")
                except PermissionError:  #Si l'accès au fichier n'est pas autorisé
                    print(f"Erreur : accès refusé au fichier '{chemin}'.\n")

        elif choix == 3:       #Cas 3 avec le collage d'un texte multiligne
            print("Collez votre texte, puis (obligatoire) tapez FIN sur une ligne seule pour terminer votre saisie :")
            lignes = []    # création d'une liste qui stockera toutes les lignes de la saisie
            while True:
                ligne = input() #on lie une seule ligne à la fois
                if ligne.strip() == "FIN":      #quand on tape FIN spécifiquement, on arrête la saisie
                    break
                lignes.append(ligne)  #sinon on continue à ajouter les lignes à la lister, donc au texte complet
            texte_original = "\n".join(lignes)
            return normaliser(texte_original)

        else:
            print("Erreur : entrez uniquement 1,2 ou 3.\n")  # si l'utilisateur tape 5 par exemple


def chiffrer(texte_original, cle):
    texte_original = normaliser(texte_original)
    texte_chiffree = [" "] * len(texte_original)
    liste_index_original = [0] * len(texte_original)
    liste_index_chiffree = [0] * len(texte_original)
    for i in range(len(texte_original)):
        if texte_original[i].lower() in alphabet:
            liste_index_original[i] = alphabet.find(texte_original[i].lower()) #aprés le for, on aura notre liste d'index
            liste_index_chiffree[i] = (liste_index_original[i] + cle) % 26
            nouvelle_lettre = alphabet[liste_index_chiffree[i]]
            texte_chiffree[i] = nouvelle_lettre.upper() if texte_original[i].isupper() else nouvelle_lettre
        else:
            texte_chiffree[i] = texte_original[i]
    return "".join(texte_chiffree)

def dechiffrer(texte_chiffree, cle):
    texte_original = [" "] * len(texte_chiffree)
    liste_index_original = [0] * len(texte_original) #variables de transition # pas nécessaire
    liste_index_chiffree = [0] * len(texte_original)
    for i in range(len(texte_original)):
        if texte_chiffree[i].lower() in alphabet:
            liste_index_chiffree[i] = alphabet.find(texte_chiffree[i].lower()) #aprés le for, on aura notre liste d'index
            liste_index_original[i] = (liste_index_chiffree[i] - cle) % 26

            nouvelle_lettre = alphabet[liste_index_original[i]]
            texte_original[i] = nouvelle_lettre.upper() if texte_chiffree[i].isupper() else nouvelle_lettre
        else:
            texte_original[i] = texte_chiffree[i]
    return "".join(texte_original)


def enigma_chiffrer(texte_original):
    cle = [0, 0, 0]          #on crée la liste qui contient les 3 clés
    for k in range(len(cle)):        #on parcourt les 3 emplacements de la liste des clés
        while True:               #ici, c'est une boucle infinie, on n'en sort que si l'utilisateur met une clé valide
            try:
                cle[k] = int(input(f"Saisis ta clé numéro {k+1}: ")) % 26      #on demande unbe clé à user, le int vérifie que c'est bien un entier et modulo 26 pour l'alphabet
                break       #si pas d'erreur, on passe à la clé suivant
            except ValueError:           #cette partie ne s'active que si l'utilisateur ne met pas un entier (ex: "abc", "3.2", blablabla...)
                print("Ta clé n'est pas bonne, mets uniquement des nombres entiers")
    texte_chiffree = [" "] * len(texte_original)
    liste_index_original = [0] * len(texte_original)
    liste_index_chiffree = [0] * len(texte_original)
    j=0
    for i in range(len(texte_original)):
        if texte_original[i].lower() in alphabet:
            liste_index_original[i] = alphabet.find(texte_original[i].lower()) #aprés le for, on aura notre liste d'index
            liste_index_chiffree[i] = (liste_index_original[i] + (cle[j%3])) % 26
            nouvelle_lettre = alphabet[liste_index_chiffree[i]]
            texte_chiffree[i] = nouvelle_lettre.upper() if texte_original[i].isupper() else nouvelle_lettre
            j=j+1
        else:
            texte_chiffree[i] = texte_original[i]
    return "".join(texte_chiffree),cle

def definir_seuil(nom_fichier,liste_bigrammes,liste_bigrammes_rares):
    with open(nom_fichier, "r",encoding="utf-8") as fichier:
        lignes=fichier.readlines()
    texte_reference="".join(lignes)
    score,nombre_de_bigrammes_testes,proportion=scorer(texte_reference,liste_bigrammes,liste_bigrammes_rares)
    return score, nombre_de_bigrammes_testes, proportion




def enigma_dechiffrer(texte_chiffree,cle):

    texte_original = [" "] * len(texte_chiffree)
    liste_index_original = [0] * len(texte_chiffree)
    liste_index_chiffree = [0] * len(texte_chiffree)
    j=0
    for i in range(len(texte_chiffree)):
        if texte_chiffree[i].lower() in alphabet:
            liste_index_chiffree[i] = alphabet.find(texte_chiffree[i].lower()) #aprés le for, on aura notre liste d'index
            liste_index_original[i] = (liste_index_chiffree[i] - (cle[j%3])) % 26
            nouvelle_lettre = alphabet[liste_index_original[i]]
            texte_original[i] = nouvelle_lettre.upper() if texte_chiffree[i].isupper() else nouvelle_lettre
            j=j+1
        else:
            texte_original[i] =texte_chiffree[i]
    return "".join(texte_original)


#on rechange d'idée, je vais importer les bigrammes les plus communément utilisées de la langue française

def charger_bigrammes(nombre_de_bigramme):
    liste_bigrammes=[] #liste vide pour stocker nos bigrammes
    nom_fichier="french_bigrams.txt"
    with open (nom_fichier,"r", encoding="utf-8") as fichier:
        for ligne in fichier:
            if len(liste_bigrammes) >= nombre_de_bigramme:
                break
            bigramme = ligne.split()[0].lower()
            if all(lettre in alphabet for lettre in bigramme):
                liste_bigrammes.append(bigramme)
    return liste_bigrammes

def charger_bigrammes_rares(nombre_de_bigrammes_rares=50):
    liste_bigrammes_rares=[] #liste vide pour stocker nos bigrammes
    nom_fichier="french_bigrams.txt"
    toutes_les_lignes=[]
    with open (nom_fichier,"r", encoding="utf-8") as fichier:
        for ligne in fichier:
            parties = ligne.split()
            if len(parties) >= 1: #on vérifie que la partie n'est pas vide
                    bigramme = parties[0].lower()
                    if all(lettre in alphabet for lettre in bigramme) and len(bigramme) == 2:
                        toutes_les_lignes.append(bigramme)
    liste_bigrammes_rares = toutes_les_lignes[-nombre_de_bigrammes_rares:]
    return liste_bigrammes_rares


#on va essayer de faire un pseudo-code pour la fonction brute force
#on va faire une fonction qui va découper le texte avec des espaces en une liste qui contient chaque mot sans espace.

def scorer(texte_teste,liste_bigramme,liste_bigrammes_rares):
    score=0 #initialisation du score
    #on va créer une liste qui stocke chaque mot du texte,
    liste_mots="" #liste vide au départ
    mot="" #pour initialiser le mot qui sera vide au départ
    #NOS LISTE BIGRAMME EST EN MINUSCULE et sans accent, donc on normalise
    nombre_de_bigrammes_testes=0 #nombre de paire de lettre examiné
    nombre_de_bigrammes_rares=0
    texte_teste=normaliser(texte_teste)
    for caractere in texte_teste + " ": #on parcourt tous les caracteres du texte un par un
        #l'ajout de " " sert à ajouter un espace à la fin du dernier mot du texte pour qu'il soit ajouté comme un mot
        if caractere in alphabet: #si le caractere apparait ds l'alphabet alors ça siginfiera qu'il faut ce caractère comme constituant d'un mot
            mot=mot+caractere.lower() #ainsi on va remplir ce mot par ce caractère en mettant tout en minuscule
        else:
            #ce else caracterise la fin du mot car on rencontre soit un chiffre, soit un espace, soit un caractere alpha numerique
            if len(mot)>=2: #ce if est pour ne pas prendre en compte les mot à 1 carctere pour le score
                for i in range(len(mot)-1): #ici on met le -1 pour que l'indce i+1 du mot existe bien
                    paire=mot[i]+mot[i+1]
                    nombre_de_bigrammes_testes+=1
                    if paire in liste_bigramme:
                        score=score+1
                    elif paire in liste_bigrammes_rares:
                        score=score-3 #le -3 permet de faire plus baisser le score
                        nombre_de_bigrammes_rares+=1
                        if nombre_de_bigrammes_rares>=3:
                            break #on sort ainsi de cette boucle, on sairt que ça ne sera pas cette clé
            mot="" #on repart de 0 pour le prochain mot
    #Calcul proportion de bigramme dans le texte
    if nombre_de_bigrammes_testes > 0:
        proportion = score / nombre_de_bigrammes_testes
    else:
        proportion = 0
    return score,nombre_de_bigrammes_testes,proportion

def brute_force_cesar(texte_chiffree,liste_bigramme,liste_bigrammes_rares):
    #bete et mechant, on va tester les differentes cles et identifier laquelle est la meilleure selon le score
    meileur_cle=0
    meilleur_score=-5
    meilleur_texte=""
    for cle in range(26): #26 lettres de l'alphabet
        texte_teste=dechiffrer(texte_chiffree,cle)
        score,nb,proportion=scorer(texte_teste, liste_bigramme, liste_bigrammes_rares)
        if score>meilleur_score:
            meilleur_cle=cle
            meilleur_score=score
            meilleur_texte=texte_teste
    return meilleur_texte, meilleur_cle

def cas_du_e(texte_chiffree,liste_bigrammes,liste_bigrammes_rares):
    """cette fonction agit comme un raccourci, donc on teste le cas "e"."""
    nombre_du_caractere_le_plus_redondant=0 #init de cette variable
    texte_chiffree=normaliser(texte_chiffree)
    nombre_total_lettres=0
    compteur={} #dictionnaire des lettres, donc clé: lettre et valeur: nombre de cette lettre dans le texte

    #on va d'abord compter chaque lettre de l'alphabet dans le texte
    for caractere in texte_chiffree: #on parcourt chaque carectere du texte
        lettre_minuscule=caractere.lower() #grâce à ça on a que des minsucules
        if lettre_minuscule in alphabet: #donc forcement minusucule alphabet est deja en minsuscule
            nombre_total_lettres+=1

            if lettre_minuscule in compteur:
                compteur[lettre_minuscule]+=1 #cette lettre existe déjà comme clé du dictionnaire, donc sa valeur augmente
            else:
                compteur[lettre_minuscule]=1 #nouvelle clé car nouvelle lettre

    if nombre_total_lettres==0:
        print("il y a aucune lettre de l'alphabet dans ton texte, celà ne va pas fonctionner")
        return None

#mtn on va trouver quelle est la lettre qui est la plus redondante


    lettre_la_plus_redondante=""
    for lettre in compteur:
        if compteur[lettre]>nombre_du_caractere_le_plus_redondant:
            nombre_du_caractere_le_plus_redondant=compteur[lettre]
            lettre_la_plus_redondante=lettre

#mtn on va essyaer de fixer une part de présence afin de s'assurer que ça soit bien un bon critere

    proportion=nombre_du_caractere_le_plus_redondant/nombre_total_lettres
    if proportion<0.15: #en utilisant ce critère (une proportion de 15%) on s'assure que c'est vraiment redondant
        print("la lettre la plus fréquente représente moins de 15% donc on ne peut pas utiliser l'hypothèse que cette lettre est la lettre e")
        return None

#mtn, vu que c'est supérieur à 15%, on peut supposer que c'est bien un e
# le e est référencé par le chiffre 4 dans l'alphabet, donc on se sert de ça pour calculer la clé de e
    index_lettre_la_plus_redondante=alphabet.find(lettre_la_plus_redondante)
    cle=(index_lettre_la_plus_redondante-alphabet.find("e")) % 26

# on a donc la bonne clé, on va appeler la fonction scorer et la fonction dechiffrer
    texte_dechiffre=dechiffrer(texte_chiffree,cle)
    score,nb,proportion=scorer(texte_dechiffre,liste_bigrammes,liste_bigrammes_rares)

    if score>int(0.2 * (nombre_total_lettres/2) ): #si le score est assez élévé
        return texte_dechiffre, cle, score
    else:
        return None #pour sortir de cette boucle



def brute_force_enigma(texte_chiffree,liste_bigrammes,liste_bigrammes_rares):


# on va gérer le cas des textes courts
    meilleur_cle=[0,0,0]
    meilleur_score=-100 #de façon à ce que le score soit bien bas
    meilleur_texte=""
    nombre_bigrammes_examines=scorer(texte_chiffree,liste_bigrammes,liste_bigrammes_rares)[1] #on calcule juste une fois le nombre de bigrammes examinés dans le texte
    texte_court=nombre_bigrammes_examines<10 #booléen qui renvoie True si le nb de bigrammes examinés est inférieur à 10

    if not texte_court: #si le texte est court, ça ne sert à rien d'appeler definir_seuil()
        seuil_ideal=definir_seuil("Les_Miserables.txt",liste_bigrammes,liste_bigrammes_rares)[2]
#le seuil ideal correspond à la proportion ideale

    #triple_boucle des indices
    for premiere_cle in range(26):
        for deuxieme_cle in range(26):
            for troisieme_cle in range(26):
                texte_teste=enigma_dechiffrer(texte_chiffree,[premiere_cle,deuxieme_cle,troisieme_cle])
                score,nombre_bigrammes_examines,proportion=scorer(texte_teste,liste_bigrammes,liste_bigrammes_rares) #permet d'appeler la fonction une seule fois


                if score>meilleur_score:
                    meilleur_score=score #pour prendre en compte le meilleur score
                    meilleur_cle=[premiere_cle,deuxieme_cle,troisieme_cle]
                    meilleur_texte=texte_teste

                if not texte_court and proportion>= seuil_ideal*0.9: #si ça rentre dedans, on arrête la boucle interminable
                    #Pour que ça rentre dedans, le texte doit contenir au moins 10 bigrammes examinés
                    #sinon le code fait toutes les possibilités et renvoie celle avec le meilleur score
                    #le seuil qui se base sur un vrai texte francais est ideal, donc on prend 90% de ce seuil pour le vrai bon seuil
                    return meilleur_texte, meilleur_cle

    return meilleur_texte, meilleur_cle


if __name__ == "__main__":
    print("="*60)
    print(" BIENVENUE DANS CE PROGRAMME DE CHIFFREMENT / DÉCHIFFREMENT ")
    print("="*60)
    print()
    print("Ce programme va vous permettre de chiffrer ou de déchiffre un texte")
    print("à l'aide de deux méthodes qui sont basées sur le chiffrement de César :")
    print()
    print(" - César classique : qui n'utilise qu'une seule clé de décalage")
    print(" - Enigma-César : qui utilise trois clés de décalage successive")
    print()
    print("Le programme vous permet aussi de retrouver automatiquement la clé")
    print("d'un texte chiffré par par l'une des deux méthodes grâce à une méthode d'analyse.")
    print()
    print("A vous de jouer!")
    print()

    #Lecture du texte
    resultat = lire_texte(None)
    print(f"\ntexte:{resultat}")

    #Choix du mode
    while True:
        print("=" * 60)
        print("Quel mode de chiffrement voulez-vous utiliser ?")
        print("1- César (une seule clé)")
        print("2- Enigma (un triplet de clés)")
        print("=" * 60)
        try:
            mode = int(input("1 ou 2 ?").strip())
            if mode in [1,2]:
                break
            else:
                 print("Erreur : entrez uniquement 1 ou 2.")
        except ValueError:
            print("Erreur : entrez uniquement 1 ou 2.")

    #Choix de l'action
    while True:
        print("=" * 60)
        print("Quelle action voulez-vous effectuer ?")
        print("1- Chiffrer")
        print("2- Déchiffrer (avec la clé)")
        print("3- Déchiffrer automatiquement (brute force)")
        print("=" * 60)
        try:
            action = int(input("1, 2 ou 3 ?").strip())
            if action in [1,2,3]:
                break
            else:
                print("Erreur : entrez uniquement 1, 2 ou 3.")
        except ValueError:
            print("Erreur : entrez uniquement 1, 2 ou 3.")

    #Chargement des bigrammes si on réalise l'action brute force
    if action == 3:
        liste_bigrammes = charger_bigrammes(200) #On charge les 200 bigrammes les plus courants de la langue française
        liste_bigrammes_rares = charger_bigrammes_rares()

    #Mode César
    if mode == 1:
        if action == 1: #Chiffrement de César
            while True:
                try:
                    cle=int(input("Saisis de la cle: ").strip())
                    break
                except ValueError:
                    print("Erreur : saisissez une clé entière uniquement.")
            texte_chiffree = chiffrer(resultat, cle)
            print(f"\ntexte encrypté:\n{texte_chiffree}")

        elif action == 2: #Déchiffrement de César
            while True:
                try:
                    cle=int(input("Saisis de la cle: ").strip())
                    break
                except ValueError:
                    print("Erreur : saisissez une clé entière uniquement.")
            texte_original = dechiffrer(resultat, cle)
            print(f"\ntexte décrypté:\n{texte_original}")

        elif action == 3:
            #Essai avec la méthode du "e" d'abord (plus rapide)
            resultat_e = cas_du_e(resultat,liste_bigrammes, liste_bigrammes_rares)

            if resultat_e is not None:
                texte_dechiffree, cle, score = resultat_e
                print(f" \n Clé trouvée par méthode du 'e' : {cle}")
                print(f"Score : {score}")
                print(f"\ntexte décrypté :\n{texte_dechiffree} ")
            else:
                #Si la méthode du "e" n'aboutit pas, on réalise le brut force complet du texte
                print("\nMéthode du 'e' insuffisante, utilisation du brute force complet")
                texte_dechiffree, cle = brute_force_cesar(resultat,liste_bigrammes, liste_bigrammes_rares)
                print(f"\nClé trouvée ≡ {cle} [26]")
                print(f"\ntexte décrypté :\n{texte_dechiffree} ")

    #Mode Enigma
    if mode == 2:
        if action == 1:  # Chiffrement Enigma
            texte_chiffree, cle = enigma_chiffrer(resultat)
            print(f"\ntexte encrypté:\n{texte_chiffree}")

        elif action == 2:  # Déchiffrement Enigma
            cle = [0,0,0]
            for k in range(3):
                while True:
                    try:
                        cle[k] = int(input(f"Saisis de la cle numéro {k+1}: ")) % 26
                        break
                    except ValueError:
                        print("Entier uniquement")
            texte_original = enigma_dechiffrer(resultat,cle)
            print(f"\ntexte décrypté:\n{texte_original}")

        elif action == 3: #Brute force Enigma
            print("\nBrute force Enigma")
            texte_dechiffree, cle = brute_force_enigma(resultat, liste_bigrammes, liste_bigrammes_rares)
            score, nb, proportion = scorer(texte_dechiffree, liste_bigrammes, liste_bigrammes_rares)
            print(f"\ntexte décrypté :\n{texte_dechiffree} ")
            print(f"\nClé trouvée ≡ {cle} [26]")
            print(f"Proportion de bigrammes reconnus : {proportion*100:.1f}%") #un chiffre après la virgule
