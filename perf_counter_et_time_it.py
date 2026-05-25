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

liste_bigrammes       = charger_bigrammes(200)
liste_bigrammes_rares = charger_bigrammes_rares()

# Le message à chiffrer

message_chiffre = chiffrer("Veni, vidi, vici!", 13)
message_chiffre_enigma, _ = enigma_chiffrer("Veni, vidi, vici!")

print("=" * 60)
print("  Script perf_counter & time_it  ")
print("=" * 60)
print(f"Message César  chiffré : {message_chiffre}")
print(f"Message Enigma chiffré : {message_chiffre_enigma}")
print()

# 1. perf_counter (une seule exécution)

tic = perf_counter()
brute_force_cesar(message_chiffre, liste_bigrammes, liste_bigrammes_rares)
toc = perf_counter()
print(f"Temps d'execution César  : {toc - tic} [s]")

tic = perf_counter()
brute_force_enigma(message_chiffre_enigma, liste_bigrammes, liste_bigrammes_rares)
toc = perf_counter()
print(f"Temps d'execution Enigma : {toc - tic} [s]")
print()

# 2. timeit (on execute pour 100 répétitions)

REPETITIONS = 100

total_cesar = timeit(
    "brute_force_cesar(message_chiffre, liste_bigrammes, liste_bigrammes_rares)",
    globals=globals(),
    number=REPETITIONS,
)
print(f"timeit César  (100x) : {total_cesar} [s]  |  moy : {total_cesar / REPETITIONS} [s]")

total_enigma = timeit(
    "brute_force_enigma(message_chiffre_enigma, liste_bigrammes, liste_bigrammes_rares)",
    globals=globals(),
    number=REPETITIONS,
)
print(f"timeit Enigma (100x) : {total_enigma} [s]  |  moy : {total_enigma / REPETITIONS} [s]")
print()