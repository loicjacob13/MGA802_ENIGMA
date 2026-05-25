"""
MGA802 - Mini-Projet A
Script de perf_counter & time_it
"""

# On importe les fonctions dont on a besoin

from time import perf_counter
from timeit import timeit
from main import (brute_force_cesar, brute_force_enigma,
                  chiffrer, enigma_chiffrer,
                  charger_bigrammes, charger_bigrammes_rares)

# On prépare les paramètres dont on va avoir besoin pour enigma

liste_bigrammes = charger_bigrammes(200) # On prend les 200 bigrammes les plus courant en français
liste_bigrammes_rares = charger_bigrammes_rares() #Renvoie les bigrammes les plus rares du francais (set up aux 50 plus rares cf main)

# Le message à chiffrer

message_chiffre = chiffrer("Le chien du père de mon copain est grand.", 25) #Message à brute force César
message_chiffre_enigma, _ = enigma_chiffrer("Le chien du père de mon copain est grand.") #Message à brute force Enigma

print("=" * 60)
print("  Script perf_counter & time_it  ")
print("=" * 60)
print(f"Message César  chiffré : {message_chiffre}")
print(f"Message Enigma chiffré : {message_chiffre_enigma}")
print()

# 1. perf_counter (une seule exécution)

tic = perf_counter() #On lance le timer avant
texte_cesar, cle_cesar = brute_force_cesar(message_chiffre, liste_bigrammes, liste_bigrammes_rares)
toc = perf_counter() #On lance le timer après
print(f"Temps d'exécution César  : {toc - tic:.4f} [s]")  #On fait la différence des 2 pour obtenir le temps d'exécution
print(f"Clé trouvée : {cle_cesar}")
print(f"Texte déchiffré : {texte_cesar}")
print()

#De même chose que pour César
tic = perf_counter() #On lance le timer avant
texte_enigma, cle_enigma = brute_force_enigma(message_chiffre_enigma, liste_bigrammes, liste_bigrammes_rares)
toc = perf_counter() #On lance le timer après
print(f"Temps d'exécution Enigma : {toc - tic:.4f} [s]") #On fait la différence des 2 pour obtenir le temps d'exécution
print(f"Clé trouvée : {cle_enigma}")
print(f"Texte déchiffré : {texte_enigma}")
print()

# 2. time it (on execute pour 100 répétitions)

REPETITIONS = 100 #Nombre de répétitions pour la fonction timeit

total_cesar = timeit("brute_force_cesar(message_chiffre, liste_bigrammes, liste_bigrammes_rares)",
    globals=globals(), # donne accès aux variables du script à timeit
    number=REPETITIONS)

print(f"time_it César  ({REPETITIONS}x) : {total_cesar:.4f} [s]  |  moyenne : {total_cesar / REPETITIONS:.4f} [s]")
print()

total_enigma = timeit("brute_force_enigma(message_chiffre_enigma, liste_bigrammes, liste_bigrammes_rares)",
    globals=globals(), # donne accès aux variables du script à timeit
    number=REPETITIONS)

print(f"time_it Enigma ({REPETITIONS}x) : {total_enigma:.4f} [s]  |  moyenne : {total_enigma / REPETITIONS:.4f} [s]")
print()