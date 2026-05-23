import string

#CONSTANTES

alphabet = string.ascii_lowercase
liste_chiffres= list(range(10))

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
    return liste_bigrammes


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
    mot="" #pour initialiser le mot qui sera vide au départ
    #NOS LISTE BIGRAMME EST EN MINUSCULE et sans accent, donc on normalise
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
                    if paire in liste_bigramme:
                        score=score+1
                    elif paire in liste_bigrammes_rares:
                        score=score-1
            mot="" #on repart de 0 pour le prochain mot
    return score

def brute_force_cesar(texte_chiffree,liste_bigramme,liste_bigrammes_rares):
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

def cas_du_e(texte_chiffree,liste_bigrammes,liste_bigrammes_rares):

    if len(texte_chiffree)>= 300:
        #si le texte est assez long, on essaie de supposer que la lettre la plus récurrente est le "e" et on appelle directemenr la fonction score en plus
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

    else: #si jamais le texte est pas assez long
        return None


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

# on a donc la bonen clé, on va appeler la fonction scorer et la fonction dechiffrer
    texte_dechiffre=dechiffrer(texte_chiffree,cle)
    score=scorer(texte_dechiffre,liste_bigrammes,liste_bigrammes_rares)

    if score>int(0.2 * (nombre_total_lettres/2) ): #si le score est assez élévé
        return texte_dechiffre, cle, score
    else:
        return None #pour sortir de cette boucle



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

