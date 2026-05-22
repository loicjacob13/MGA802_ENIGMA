import string

#CONSTANTES

alphabet = string.ascii_lowercase
liste_chiffres= list(range(10))

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
                chemin = input("Nom du fichier ? ").strip().strip('"')
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


def chiffrer(texte_original, cle):
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
    cle = [int(input("saisis ta première clé: ")), int(input("saisis ta deuxième clé: ")),int( input("saisis ta troisème clé: "))]

    # contrôle : on vérifie que chaque clé est bien un entier compris dans liste_chiffres (0 à 9)
    liste_chiffres = list(range(10))
    for k in range(len(cle)): #on vérifie l'input afin de ne pas mettre d'input qui ne marcherait pas
        while cle[k] not in liste_chiffres:
            print("\n")
            print("Attention, veille bien à mettre un nombre entier compris entre 0 et 9")
            cle[k] = int(input(f"saisis à nouveau ta clé numéro {k + 1}: "))

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

def enigma_dechiffrer(texte_chiffree,cle):

    # contrôle : on vérifie que chaque clé est bien un entier compris dans liste_chiffres (0 à 9)
    liste_chiffres = list(range(10))
    for k in range(len(cle)): #on vérifie l'input afin de ne pas mettre d'input qui ne marcherait pas
        while cle[k] not in liste_chiffres:
            print("\n")
            print("Attention, veille bien à mettre un nombre entier compris entre 0 et 9")
            cle[k] = int(input(f"saisis à nouveau ta clé numéro {k + 1}: "))

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
            texte_original[i] = texte_chiffree[i]
    return "".join(texte_original)


if __name__ == "__main__":
    #Lecture du texte
    resultat = lire_texte(None)
    print(f"\ntexte:{resultat}")

    #Demande du mode
    while True:
        print("Quel mode de chiffrement voulez-vous utiliser ?")
        print("1- César (une seule clé)")
        print("2- Enigma (un triplet de clés)")
        try:
            mode = int(input("1 ou 2 ?").strip())
            if mode in [1,2]:
                break
            else:
                 print("Erreur : entrez uniquement 1 ou 2.")
        except ValueError:
            print("Erreur : entrez uniquement 1 ou 2.")

    if mode == 1:
        while True:
            try:
                cle=int(input("saisis de la cle: ").strip())
                break
            except ValueError:
                print("Erreur : saisissez une clé entière.")
        #Chiffrement Cesar
        texte_chiffree = chiffrer(resultat, cle)
        print(f"\ntexte encrypté:{texte_chiffree}")
        #Dechiffrement Cesar
        texte_original = dechiffrer(texte_chiffree, cle)
        print(f"\ntexte décrypté:{texte_original}")
    elif mode == 2:
        #Dechiffrement Enigma_Cesar
         texte_chiffree, cle = enigma_chiffrer(resultat)
         print(f"\ntexte encrypté:{texte_chiffree}")
        #Dechiffrement Enigma_Cesar
         texte_original = enigma_dechiffrer(texte_chiffree, cle)
         print(f"\ntexte décrypté:{texte_original}")