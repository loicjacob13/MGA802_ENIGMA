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
chiffrer(texte_original, cle)
dechiffrer(texte_chiffree, cle)

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

enigma_chiffrer(texte_original)