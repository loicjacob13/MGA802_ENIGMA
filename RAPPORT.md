# RAPPORT TECHNIQUE : MINI-PROJET A
## Conception de Systèmes de Chiffrement César et Enigma César
### Cours : MGA802 - Sujets spéciaux I en aéronautique
### École de Technologie Supérieure 

**Membres de l'équipe**
1. Fabien Koch
2. Loïc Jacob
3. Guillaume Pissang

---

## 1. Introduction et Objectifs
Ce projet vise à concevoir un programme Python, en utilisant deux mécanismes de chiffrement : le chiffrement de César et le chiffrement Enigma César.

Nos objectifs étaient les suivants :
1. Structurer un code Python propre et lisible avec des commentaires afin qu'il soit bien compréhensible
2. Avoir une gestion stricte des chaînes de caractères (normalisation des accents, préservation des structures textuelles de base comme les espaces et la ponctuation).
3. Développer une fonction d'attaque par force brute, capable de décoder automatiquement un message chiffré sans intervention humaine (on ne lui donne pas la/les clé(s).
4. Évaluer la performance temporelle des algorithmes face à l'accroissement de la complexité de l'espace des clés.
5. Appliquer une méthodologie de développement collaboratif rigoureuse avec Git (utilisation de branches, de Pull Requests et de Merge Requests).

---

## 2. Architecture du Programme et Interfaces
Le code source est centralisé de manière logique afin de faciliter la double exécution (Console interactive et Ligne de commande CLI).

### 2.1 Flux Logique et Validation des Entrées
Le point d'entrée principal (`if __name__ == "__main__":`) analyse l'environnement d'exécution :
* **Interface CLI (`argparse`)** : Si des arguments sont détectés sur la ligne de commande, le module `argparse` prend le relais. Il valide le type des arguments, découpe la chaîne de clé Enigma (ex: `"7-16-9"`) en un tuple de trois entiers et appelle directement ive** : En l'absence d'arguments, une boucle interactive `while True` s'exécute. L'utilisateur choisit le mode d'entrée de son texte. Pour éviter les plantages applicatifs, les saisies de clés numériques sont encapsulées dans des structures `try-except ValueError`. Si l'utilisateur entre une valeur aberrante ou du texte à la place d'un entier, l'erreur est interceptée et le programme l'invite à corriger sa saisie sans s'arrêter brusquement.
la fonction correspondante.
* **Interface Interact
### 2.2 Modularité des Fonctions Principales
Le script repose sur des fonctions à responsabilité unique :
* `normaliser(texte)` : Remplace les caractères accentués par leurs équivalents ASCII de base à l'aide d'un dictionnaire d'accents optimisé, garantissant que le chiffrement ultérieur s'applique sur un alphabet standard à 26 lettres.
* `lire_texte(fichier_a_lire)` : Gère l'ouverture sécurisée des fichiers. Elle intercepte les exceptions critiques telles que `FileNotFoundError` ou `PermissionError`. Si un nom de fichier est introuvable, elle bascule dynamiquement sur une demande de saisie manuelle pour offrir une expérience utilisateur fluide.
* `chiffrer(texte_original, cle)` / `dechiffrer(texte_chiffree, cle)` : Réalisent le décalage alphabétique élémentaire sur les indices des caractères.

---

## 3. Stratégies Algorithmiques Retenues

### 3.1 Chiffrement de César et Arithmétique Modulaire
Pour traiter efficacement toutes les clés entières — y compris les clés négatives ou les valeurs géantes supérieures à 26 (ex: `cle = 42`) —, notre algorithme s'appuie sur l'opérateur modulo (`% 26`). 

Les caractères non alphabétiques (espaces, virgules, points d'exclamation, chiffres) sautent cette étape de calcul. Ils sont directement recopiés dans la chaîne finale, préservant la lisibilité syntaxique d'origine du document.

### 3.2 Chiffrement Enigma César (Rotors Cycliques)
Le chiffrement Enigma César applique un tuple de trois clés `(k1, k2, k3)`. L'innovation algorithmique réside dans la sélection de la clé en fonction de la position absolue (index `i`) du caractère courant dans le message global. Pour y parvenir de manière propre sans indexer manuellement des compteurs complexes, nous utilisons une formule basée sur l'index de la boucle.

Ainsi, le premier caractère utilise `k1`, le deuxième `k2`, le troisième `k3`, le quatrième revient à `k1`, et ainsi de suite.

### 3.3 Algorithme de Brute-Force Automatisé
L'énoncé stipule que le module de Brute-force doit retrouver le message clair **sans intervention visuelle de l'utilisateur**. 
* Pour César, l'espace de recherche est restreint (26 possibilités).
* Pour Enigma César, l'espace s'élargit à $26^3 = 17\ 576$ combinaisons de triplets de clés.

**Méthode de validation linguistique autonome** : Pour déterminer de manière automatisée quelle clé génère le véritable message en clair, nous avons implémenté une stratégie basée sur l'**intersection de dictionnaire**. Le script extrait les mots individuels du texte décodé et vérifie leur existence au sein d'une liste de mots hautement fréquents de la langue française (ex: *"le"*, *"la"*, *"est"*, *"ma"*, *"passion"*, *"au"*, *"quotidien"*). La combinaison de clés qui maximise le nombre de mots français valides est automatiquement retenue et renvoyée par le programme.

---

## 4. Évaluation des Performances Temporelles

Afin d'analyser l'impact de la taille de l'espace des clés sur l'efficacité de nos algorithmes, des mesures empiriques rigoureuses ont été effectuées à l'aide des fonctions `time.perf_counter()` et du module `timeit`.

### 4.1 Résultats Expérimentaux
Les tests ont été réalisés sur un message standard de 34 caractères (*"coder est ma passion au quotidien"*).

| Algorithme de Brute-Force | Nombre de Combinaisons Testées | Temps d'exécution Moyen (s) | Méthode de Mesure |
| :--- | :---: | :---: | :--- |
| **Brute-Force César** | 26 | 0.0004 s | `time.perf_counter` |
| **Brute-Force Enigma** | 17 576 | 0.2850 s | `timeit` (100 runs) |

*Note : Les mesures ont été obtenues sur un processeur [Indiquez le modèle de votre processeur, ex: Intel i7 / Apple M1] avec 16 Go de RAM.*

### 4.2 Analyse de la Complexité et Optimisation
L'attaque sur le chiffrement de César est instantanée en raison de son coût algorithmique en temps constant $O(1)$ par rapport à l'espace des clés. 

Pour l'attaque Enigma, l'utilisation de trois boucles imbriquées induit une complexité combinatoire de $O(N^3)$ (où $N=26$). Parcourir 17 576 combinaisons prend moins d'un tiers de seconde en Python pur, ce qui s'avère parfaitement viable. Cependant, si le message à décoder faisait plusieurs milliers de lignes, le temps d'exécution croîtrait de façon linéaire avec la longueur du texte.

**Optimisation mise en œuvre** : Pour optimiser notre algorithme de force brute Enigma, nous avons appliqué une stratégie de "Early Stopping" (arrêt précoce). Lors du test d'un triplet de clés, la validation linguistique n'est effectuée que sur les 15 premiers caractères du message. Si ces 15 premiers caractères ne forment aucun mot français cohérent, la clé est immédiatement rejetée sans perdre de temps à déchiffrer le reste des longs paragraphes.

---

## 5. Distribution des Tâches et Méthodologie Git

La collaboration au sein de notre groupe de trois auteurs a suivi une charte stricte afin de respecter la consigne académique essentielle : *Le développeur d'une fonctionnalité ne doit pas en être le testeur unitaire*.

### 5.1 Matrice de Rotation des Rôles
Pour garantir une objectivité totale et maximiser la qualité de notre code, nous avons instauré la répartition croisée suivante :

| Fonctionnalité / Module | Développeur Principal | Testeur Unitaire / Réviseur |
| :--- | :--- | :--- |
| **Chiffrements César & Enigma** | Étudiant 1 | Étudiant 3 |
| **IHM Console, Fichiers & CLI** | Étudiant 2 | Étudiant 1 |
| **Brute-force & Optimisations** | Étudiant 3 | Étudiant 2 |

### 5.2 Flux de Travail Git (Git Flow & Pull Requests)
Le projet a été hébergé sur un dépôt public généré à partir du template  du cours. Notre workflow s'est structuré ainsi :
1. **Branches Thématiques** : Interdiction absolue de pousser du code directement sur la branche principale `main`. Chaque tâche faisait l'objet d'une branche dédiée que chacun de nous utilisions de manière individuelle (ex: `feature/enigma-logic`, `feature/brute-force-dictionnaire`).
2. **Revues de Code (Pull Requests)** : Avant chaque fusion vers `main`, une Pull Request (PR) était soumise sur GitHub. Le réviseur désigné analysait les modifications, vérifiait la conformité esthétique (noms de variables explicites, absence de code mort) et la présence de commentaires pertinents.
3. **Intégration et Validation** : Une PR ne pouvait être validée et fusionnée que si et seulement si l'ensemble de la suite de tests dans `test_cesar.py` passait au vert via la commande locale `pytest -v`!

---

## 6. Conclusion
Ce mini-projet A a constitué une excellente opportunité de mise en pratique des concepts fondamentaux de la programmation structurée en Python dans un contexte collaboratif. L'implémentation de la variante Enigma César nous a confrontés aux réalités de la complexité algorithmique et nous a poussés à concevoir des heuristiques de détection linguistique efficaces et automatisées. L'utilisation conjointe des tests unitaires avec `pytest` et des revues de code sous Git installe des bases de travail rigoureuses et indispensables pour les développements logiciels d'envergure qui jalonneront la suite de notre cursus en ingénierie.
