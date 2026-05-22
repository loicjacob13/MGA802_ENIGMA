import string

def normaliser(texte):
    """Renvoie une lettre sans accent par l'intermédiaire d'un dictionnaire"""
    accents = {
        'à': 'a', 'â': 'a', 'á': 'a', 'ä': 'a',
        'è': 'e', 'ê': 'e', 'é': 'e', 'ë': 'e',
        'î': 'i', 'ï': 'i', 'í': 'i', 'ì': 'i',
        'ô': 'o', 'ó': 'o', 'ö': 'o', 'ò': 'o',
        'û': 'u', 'ú': 'u', 'ü': 'u', 'ù': 'u',
        'ç': 'c', 'ñ': 'n',
    }
    resultat =""
    for lettre in texte.lower():
        if lettre in accents:
            resultat += accents[lettre]
        else:
            resultat += lettre
    return resultat

def lire_texte(fichier_a_lire):
    while True:
        print("Voulez-vous écrire votre texte ou ouvrir un fichier ?")
        print("1- Écrire votre texte")
        print("2- Ouvrir un fichier")

        try:
            choix = int(input("1 ou 2 ? ").strip())
        except ValueError:  #Si l'utilisateur tape "a" au lieu de 1 ou 2
            print("Erreur : entrez uniquement 1 ou 2.\n")
            continue  #On recommence la boucle

        if choix == 1:
            texte_original = input("Écrivez votre texte ici : ")
            return normaliser(texte_original)

        elif choix == 2: #On boucle jusqu'à ce que le fichier existe
            while True:
                chemin = input("Nom du fichier ? ").strip()
                try:
                    with open(chemin, "r", encoding="utf-8") as fichier:
                        contenu = fichier.read()
                        return normaliser(contenu)
                except FileNotFoundError:  #Si le fichier n'existe pas
                    print(f"Erreur : le fichier '{chemin}' est introuvable, réessayez.\n")
                except PermissionError:  #Si l'accès au fichier n'est pas autorisé
                    print(f"Erreur : accès refusé au fichier '{chemin}'.\n")

        else:
            print("Erreur : entrez uniquement 1 ou 2.\n")  # si l'utilisateur tape 5 par exemple

alphabet = string.ascii_lowercase
liste_chiffres= list(range(10))
texte_original = "abc ab"
cle = 1

def chiffrer(texte_original, cle):
    texte_chiffree = [" "] * len(texte_original)
    liste_index_original = [" "] * len(texte_original)
    liste_index_chiffree = [" "] * len(texte_original)
    for i in range(len(texte_original)):
        if texte_original[i] in alphabet:
            liste_index_original[i] = alphabet.find(texte_original[i]) #aprés le for, on aura notre liste d'index
            liste_index_chiffree[i] = (liste_index_original[i] + cle) % 25
            texte_chiffree[i] = alphabet[liste_index_chiffree[i]]
        elif texte_original[i] in liste_chiffres:
            texte_chiffree[i] = liste_chiffres[liste_index_chiffree[i]]
    print(texte_chiffree)

    '''#on sort de la boucle, et donc on va mtn utiliser la clé
    for i in range(len(texte_original)):
        if liste_index_original[i] in liste_chiffres:
            liste_index_chiffree[i]=liste_index_original[i]+cle%26
    print(liste_index_chiffree)
    #on sort de cette boucle et mtn on remplit la liste du mot
    for i in range(len(liste_index_chiffree)):
        if texte_original[i] in alphabet:
            texte_chiffree[i]=alphabet[liste_index_chiffree[i]]
    print(texte_chiffree)'''

def dechiffrer(texte_chiffree, cle):
    texte_original = [" "] * len(texte_chiffree)
    liste_index_original = [" "] * len(texte_original) #variables de transition # pas nécessaire
    liste_index_chiffree = [" "] * len(texte_original)
    for i in range(len(texte_original)):
        if texte_chiffree[i] in alphabet:
            liste_index_chiffree[i] = alphabet.find(texte_chiffree[i]) #aprés le for, on aura notre liste d'index
            liste_index_original[i] = (liste_index_chiffree[i] - cle) % 26
            texte_original[i] = alphabet[liste_index_original[i]]
    print(texte_original)

texte_chiffree = "bcd bc"
#chiffrer(texte_original, cle)
#dechiffrer(texte_chiffree, cle)

def enigma_chiffrer(texte_original,cle):
    cle=[input("saisis ta première clé: "),input("saisis ta deuxième clé: "),input("saisis ta troisème clé: ")]

def enigma_chiffrer(texte_original):
    cle = [int(input("saisis ta première clé: ")), int(input("saisis ta deuxième clé: ")),int( input("saisis ta troisème clé: "))]

    # contrôle : on vérifie que chaque clé est bien un entier compris dans liste_chiffres (0 à 9)
    liste_chiffres = list(range(10))
    for k in range(len(cle)): #on vérifie l'input afin de ne pas mettre d'input qui ne marcherait pas
        while cle[k] not in liste_chiffres:
            print("\n")
            print("attention, veilles bien à mettre un nombre entier compris entre 0 et 9")
            cle[k] = int(input(f"saisis à nouveau ta clé numéro {k + 1}: "))

    texte_chiffree = [" "] * len(texte_original)
    liste_index_original = [" "] * len(texte_original)
    liste_index_chiffree = [" "] * len(texte_original)
    j=0
    for i in range(len(texte_original)):
        if texte_original[i] in alphabet:
            liste_index_original[i] = alphabet.find(texte_original[i]) #aprés le for, on aura notre liste d'index
            liste_index_chiffree[i] = (liste_index_original[i] + (cle[j%3])) % 26
            texte_chiffree[i] = alphabet[liste_index_chiffree[i]]
            j=j+1
    print(texte_chiffree)

#enigma_chiffrer(texte_original)


#on rechange d'idée, je vais importer des bi-grammes le splus communément utilisées dans la la langue fr
#
def charger_bigrammes(nombre_de_bigramme):
    liste_bigrammes=[] #liste vide qui stockera nos bigrammes
    nom_fichier="french_bigrams.txt"
    with open (nom_fichier,"r", encoding="utf-8") as fichier:
        for i in range (nombre_de_bigramme+1):
            liste_bigrammes.append(((fichier.readline()).split()[0]).lower()) #ici l'ajout de [0] permet de prendfe suelement le premier bout
    #return liste_bigrammes
    print(liste_bigrammes)

charger_bigrammes(300)

def charger_bigrammes_rares():
    liste_bigrammes_rare=["qz","qx","qy","jx","wx","zx","qw","hx","vz","jq","qk","qh","qn","qg","qv","qb","qj","jz","jw","jv","jf","jg","wq","wz","wv","kx","kz","fz","fx","xz"]
    return liste_bigrammes_rare


#on va essyaer de faire un pseudo-code pour la fonction brut force
#on va essayer
#on va faire une fonction qui va découper le texte avce espaces en une liste qui contient chaque mots sans espaces.

def scorer(texte_teste,liste_bigramme,liste_bigrammes_rares):
    score=0 #initialisation du score
    #on va créer une liste qui stocke chaque mot du texte,
    liste_mots="" #liste vide au départ
    #NOS LISTE BIGRAMME EST EN MINUSCULE et sans accent, donc on normalise
    texte_teste=normaliser(texte_teste)
    for caractere in texte_teste + " ": #on parcourt tous les caracteres du texte un par un
        #l'ajout de " " sert à ajouter un espace à la fin du dernier mot du texte pour qu'il soit ajouté comme un mot
        if caractere in alphabet: #si le caractere apparait ds l'alphabet alors ça siginfiera qu'il faut ce caractère comme constituant d'un mot
            mot=mot+caractere #ainsi on va remplir ce mot par ce caractère
        else:
            #ce else caracterise la fin du mot car on rencontre soit un chiffre, soit un espace, soit un caractere alpha numerique
            if len(mot)>=2: #ce if est pour ne pas prendre en compte les mot à 1 carctere pour le score
                for i in range(len(mot)-1): #ici on met le -1 pour que l'indce i+1 du mot existe bien
                    paire=mot[i]+mot[i+1]
                    if paire in liste_bigramme:
                        score=score+1
                    elif paire in liste_bigrammes_rares:
                        score=score-1
            mot="" #on repart de 0 pour le prochain mot

def brute_force_cesar(texte_chiffre,liste_bigramme,liste_bigrammes_rares):
    #bete et mechant, on va tester les differentes cles et identifier laquelle est la meilleure selon le score
    meileur_cle=0
    meilleur_score=-5
    meilleur_texte=""
    for cle in range(26): #26 lettres de l'alphabet
        texte_teste=dechiffrer(texte_chiffree,cle)
        score=scorer(texte_teste, liste_bigramme, liste_bigrammes_rares)
        if score>meilleur_score:
            meilleur_cle=cle
            meilleur_score=score
            meilleur_texte=texte_teste
    return meilleur_texte, meilleur_cle

