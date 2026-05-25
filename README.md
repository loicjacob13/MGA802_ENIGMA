# Mini-Projet A : Chiffrement César & Enigma César
### MGA802 - Sujets spéciaux I en aéronautique
### École de Technologie Supérieure  

## Description du projet
Ce projet consiste à coder en Python un programme capable de chiffrer et de déchiffrer des textes, à l'aide de deux algorithmes :
1. **Le Chiffrement de César** : clé = 1 entier.
2. **Le Chiffrement Enigma César** : clé = 3 entiers.

## Utilisation

### Mode interactif (via la console)
Lancez le script main.py
Le programme vous guidera à travers les différentes étapes.

### Prérequis

Les fichiers `french_bigrams.txt`et `Les_Miserables.txt` doivent être présent dans le même dossier que le `main.py`.

### Lancer les tests unitaires

Voir les instructions dans le fichier `test_cesar.py`.

## Nos fichiers

| Fichier | Rôle |
|---|---|
| `main.py` | Script principal contenant toutes les fonctions de chiffrement, déchiffrement, brute-force et l'interface utilisateur |
| `test_cesar.py` | Suite de tests unitaires (avec pytest) qui convrent tous les cas de fonctionnement possible |
| `perf_counter_et_time_it.py` | Script qui mesure les performances des fonctions de brute-force |
| `french_bigrams.txt` | Liste de bigrammes français classés par fréquence, utilisée pour le brute-force |
| `Les_Miserables.txt` | Texte en français utilisé pour avoir des proportions de bigrammes récurents, que nous utilisons dans notre analyse |
| `RAPPORT.md` | Rapport technique du projet |
| `README.md` | Ce fichier |

## Membres de l'équipe
* **Auteur 1** : Fabien Koch (KOCF83320301)
* **Auteur 2** : Loïc Jacob (JACL93280301) 
* **Auteur 3** : Guillaume Pissang (PISG89300201) 

## Structure de notre dépôt
```text
├── main.py              # Script principal 
├── test_cesar.py        # Suite de tests unitaires (pytest) pour valider le fonctionnement du main.py
├── perf_counter_et_time_it.py   # Mesures de performance (perf_counter et timeit)
├── french_bigrams.txt   # Fichier de bigrammes utilisé pour le brute force
├── Les_Miserables.txt   # Corpus de référence pour le seuil d'arrêt
├── RAPPORT.md           # Rapport du projet en .md
└── README.md            # Fichier README expliquant globalement le projet et le contenu de notre dépot GitHub
