# RAPPORT TECHNIQUE : MINI-PROJET A
## Conception de Systèmes de Chiffrement César et Enigma César
### Cours : MGA802 - Sujets spéciaux I en aéronautique
### École de Technologie Supérieure 

**Membres de l'équipe**
1. Fabien Koch (KOCF83320301)
2. Loïc Jacob (JACL93280301)
3. Guillaume Pissang (PISG89300201)

---

## 1. Introduction et Objectifs
Ce projet vise à concevoir un programme Python, en utilisant deux mécanismes de chiffrement : le chiffrement de César et le chiffrement Enigma César.

Nos objectifs étaient les suivants :
1. Structurer un code Python propre et lisible avec des commentaires afin qu'il soit bien compréhensible
2. Avoir une gestion stricte des chaînes de caractères (normalisation des accents, préservation des structures textuelles de base comme les espaces et la ponctuation).
3. Développer une fonction d'attaque par force brute, capable de décoder automatiquement un message chiffré sans intervention humaine (on ne lui donne pas la/les clé(s).
4. Évaluer la performance temporelle des algorithmes à l'aide de `perf_counter` et `timeit`.
5. Appliquer une méthodologie de développement collaboratif rigoureuse avec Git (utilisation de branches, de Pull Requests et de Merge Requests).

---

## 2. Architecture du Programme et Interfaces
Le code source est centralisé dans `main.py` et peux être utiliser avec deux modes d'exécution : une console interactive et une interface en ligne de commande (CLI).

### 2.1 Flux Logique et Validation des Entrées
Le point d'entrée principal (`if __name__ == "__main__":`) analyse l'environnement d'exécution.
En l'absence d'arguments, une boucle interactive `while True` s'exécute quand on est en mode console interactif. L'utilisateur choisit le mode d'entrée de son texte (3 différents). Pour éviter les plantages applicatifs, les saisies de clés numériques sont encapsulées dans des structures `try/except ValueError`. Si l'utilisateur entre une valeur aberrante ou du texte à la place d'un entier, l'erreur est interceptée et le programme l'invite à corriger sa saisie sans s'arrêter brusquement. Trois modes sont supportés : l'entrée directe, la lecture depuis un fichier `.txt` (qui comporte aussi un système de gestion des erreurs) et le collage multiligne, dont la saisie prend fin par l'entrée du mot-clé `FIN`.

### 2.2 Modularité des Fonctions Principales
Le script repose sur des fonctions à responsabilité unique. En voici les principales :
| Fonction | Rôle |
|---|---|
| `normaliser(texte)` | Remplace les caractères accentués par leurs équivalents ASCII via un dictionnaire |
| `lire_texte(fichier_a_lire)` | Gère les trois modes de saisie du texte avec gestion des erreurs pour chacuns |
| `chiffrer(texte_original, cle)` | Applique le décalage alphabétique de César, en conservant les caractères non alphabétiques |
| `dechiffrer(texte_chiffree, cle)` | Inverse du chiffrement César |
| `enigma_chiffrer(texte_original)` | Chiffrement Enigma avec un triplet de clés saisi par l'utilisateur |
| `enigma_dechiffrer(texte_chiffree, cle)` | Déchiffrement Enigma avec le triplet fourni |
| `scorer(texte, bigrammes, bigrammes_rares)` | Calcule un score de vraisemblance à la lange française par analyse des bigrammes |
| `brute_force_cesar(texte_chiffree,liste_bigramme,liste_bigrammes_rares)` | Parcourt les 26 clés possibles et retourne celle avec le meilleur score |
| `brute_force_enigma(texte_chiffree,liste_bigrammes,liste_bigrammes_rares)` | Utilise des méthodes d'analyse pour trouver les trois clés |
| `cas_du_e(texte_chiffree,liste_bigrammes,liste_bigrammes_rares)` | Raccourci statistique pour César basé sur la fréquence de la lettre "e" |

---

## 3. Stratégies Algorithmiques Retenues

### 3.1 Chiffrement de César et Arithmétique Modulaire
Pour traiter efficacement toutes les clés entières — y compris les clés négatives ou les valeurs géantes supérieures à 26 (ex: `cle = 42`) —, notre algorithme s'appuie sur l'opérateur modulo (`% 26`). 

Les caractères non alphabétiques (espaces, virgules, points d'exclamation, chiffres) sautent cette étape de calcul. Ils sont directement recopiés dans la chaîne finale, préservant la lisibilité syntaxique d'origine du document.

### 3.2 Chiffrement Enigma César
Le chiffrement Enigma César applique un tuple de trois clés `[k1, k2, k3]`. L'innovation algorithmique réside dans la sélection de la clé en fonction de la position absolue (index `i`) du caractère courant dans le message global. Pour y parvenir de manière propre sans indexer manuellement des compteurs complexes, nous utilisons une formule basée sur l'index de la boucle.

Ainsi, le premier caractère utilise `k1`, le deuxième `k2`, le troisième `k3`, le quatrième revient à `k1`, et ainsi de suite.

### 3.3 Algorithme de brute-force César
Deux stratégies ont été implémentées pour le déchiffrement de César automatique :

**Méthode du "e" (raccourci statistique)** : En français, la lettre "e" est la plus fréquente. Si la lettre la plus représentée dans le texte chiffré dépasse 15% de toutes les lettres, on suppose qu'elle correspond au "e" et on déduit directement la clé. Un appel à la fonction `scorer` valide ensuite cette hypothèse.

**Brute-force complet** : Si la méthode du "e" échoue (texte trop court ou distribution atypique), les clés possibles sont testées et évaluées avec la fonction `scorer`. On retiendra la clé qui produit le meilleur score.

### 3.4 Algorithme de brute-force Enigma
Il y a 17 576 combinaisons. Pour accélerer le processus, on va utiiser une méthode d'analyse linguistique reposantr sur les bigrammes français.
Les bigrammes sont des paires de deux lettres consécutive au sein d'un mot. 
On utilise le fichier `french_bigrams.txt` qui contient les birammes classés par fréquence décroissante d'utilisation. On va choisir les 200 premiers plus utilisés et les 50 plus rares (ce premier choix est arbitraire).
Ensuite, pour chaque texte, notre fonction extrait tous les bigrammes du texte. Elle va ensuite ajouter +1 points si la paire est fréquente, -3 si c'est un bigramme rare. Si 3 des 50 bigrammes rares sont détectés, il y a un arrêt précoce.

On a au final un ratio qui est calculé : `score / nombre_de_bigrammes_testés`.

Le seuil d'arrêt précoce est pas arbitraire. Il est calculé dynamiquement à l'aide d'un vrai texte français, ici *Les Misérables*. Le seuil est fixé à 85% de cette proportion de référence. Ainsi, lorsqu'on parcours les 17 576 combinaisons, si une combinaison de clés atteint ce seuil, on retourne directement le résultat. 

Pour le petit textes, nous avions des soucis car plusieurs combinaisons de vrais bigrammes en même nombres étaient la meilleure solution. Dans ce cas là, le return était possiblement la meilleur phrase.
On a utilisé une comparaison avec tous les mots du dictionnaire français pour trouver la bonne phrase.
Cette méthode est beaucoup plus longue mais viable que si le nombre de mots est petit.

---

## 4. Évaluation des Performances Temporelles

Afin d'analyset l'efficacité de nos algorithmes, des mesures empiriques rigoureuses ont été effectuées à l'aide des fonctions `time.perf_counter` et du module `timeit`.

On remarque que le brute-force César est presque instantané, alors que le Enigma César est plus long (ce qui est normal).

---

## 5. Distribution des Tâches et Méthodologie Git

### 5.1 Flux de Travail Git (Git Flow & Pull Requests)
Le projet a été hébergé sur un dépôt public généré à partir du template  du cours. Notre workflow s'est structuré ainsi :
1. **Branches Thématiques** : Interdiction absolue de pousser du code directement sur la branche principale `main`. Chaque tâche faisait l'objet d'une branche dédiée que chacun de nous utilisions de manière individuelle (ex: `feature/enigma-logic`, `feature/brute-force-dictionnaire`).
2. **Revues de Code (Pull Requests)** : Avant chaque fusion vers `main`, une Pull Request (PR) était soumise sur GitHub. Le réviseur désigné analysait les modifications, vérifiait la conformité esthétique (noms de variables explicites, absence de code mort) et la présence de commentaires pertinents.
3. **Intégration et Validation** : Une PR ne pouvait être validée et fusionnée que si et seulement si l'ensemble de la suite de tests dans `test_cesar.py` passait au vert via la commande locale `pytest -v`!

---

## 6. Distribution des tâches

1. Loïc --> Principalement la construction du main
2. Fabien --> Principalement la construction des tests 
3. Guillaume --> Principalement la construction des fontions d'input et les fonctions de temps

---

## 7. Conclusion
Ce mini-projet A a été une très bone opportunité de mise en pratique des concepts fondamentaux de la programmation structurée en Python dans un contexte collaboratif. L'implémentation de la variante Enigma César nous a confrontés aux réalités de la complexité algorithmique et nous a poussés à trouver des systèmes d'analyse plus ou moins poussés pour améliorer l'efficacité et l'automatisation. L'utilisation de `pytest` et de GitHub ont été très pédagogiques.
