"""Tests pour le Mini-Projet A.

MGA802 - Mini-Projet A
Auteurs: Loïc Jacob, Fabien Koch, Guillaume Pissang

Objectif: Ce fichier comporte plusieurs tests automatisés afin de vérifier le bon fonctionnement du main.py

Ce fichier contient les chaînes de test officielles + quelques cas
limites. Ajoutez vos propres tests au fur et à mesure.


Pour lancer les tests :
    pip install pytest      (à ne faire qu'un fois la première fois, il faut copier cette commande dans le Terminal de PyCharm)  #permet d'installer la bibliotèque externe pytest
    pytest -v                 #À ENTRER DANS LE TERMINAL une fois l'installation de pytest faite !!! Permet de lancer les tests (le paramètre -v permet d'afficher le détail des tests

Le principe est le suivant:
Python va executer les tests, et nous dire si oui (PASSED) ou non (FAILED) les tests sont validés

Pour certains tests, nous avons décidé d'utiliser "monkeypatch". Cela va simuler ce que l'utilisateur entre sur le clavier lors d'une utilisation normale du fihcier main.py
On va donc pouvoir tester sans intervention pour les fonction input()
"""
import sys
from pathlib import Path
from main import (normaliser, enigma_dechiffrer, brute_force_enigma, brute_force_cesar, charger_bigrammes, charger_bigrammes_rares)
#importation de toutes les fonctions nécessaires depuis le main pour effectuer les tests

import pytest #va nous permettre de vérifier qu'un fonction trouve bien une erreur

# Permet d'importer main.py depuis le dossier parent
sys.path.insert(0, str(Path(__file__).parent))
from main import chiffrer, dechiffrer, enigma_chiffrer  # noqa: E402


# ---------- Chaînes de test officielles — César (spec §7) ----------

def test_cesar_officiel_cle_42():
    assert chiffrer("Veni, vidi, vici!", 42) == "Ludy, lyty, lysy!"

def test_cesar_officiel_cle_neg_42():
    assert chiffrer("Veni, vidi, vici!", -42) == "Foxs, fsns, fsms!"


# ---------- Chaîne de test officielle — Enigma César (spec §2.6) ----------
"""À du être modifié pour fonctionner avec notre version du main.py"""
def test_enigma_officiel_maison(monkeypatch):
    entrees = iter(["7", "16","9"])    #notre monkeypatch va simuler les entrées saisis pas un utilisateur
    monkeypatch.setattr(
        "builtins.input", lambda _: next(entrees)  #on remplace temporairement input() et on utilise une fonction qui renvoie les valeurs au-dessus
    )
    texte, cle = enigma_chiffrer("MAISON")   #comme à chaque fois, on utilise le chiffrement du mot de référence
    assert texte == "TQRZEW"    #résultat officiel qu'on est censé trouver si c'est focntionnel


# ---------- Cas standards (à compléter par votre équipe) ----------

def test_cesar_round_trip():
    """Chiffrer puis déchiffrer doit redonner le message original."""
    msg = "Bonjour le monde !"
    assert dechiffrer(chiffrer(msg, 7), 7) == msg


def test_cesar_cle_zero_identite():
    """Une clé de 0 ne doit rien changer."""
    assert chiffrer("Tout pareil.", 0) == "Tout pareil."


# TODO : ajoutez vos propres tests ci-dessous
#  - test pour les majuscules
#  - test pour les caractères spéciaux (accents, ponctuation)
#  - test pour les très grandes clés (positives et négatives)
#  - test pour le brute-force (César ET Enigma César)
#  - test que enigma_chiffrer rejette une clé qui n'a pas 3 nombres

# ---------- Majuscules et minuscules ----------

def test_cesar_minuscules():
    """Les lettres majuscules doivenet impérativement rester des majuscules"""
    assert chiffrer("ABC", 3) == "DEF"            #avec une clé de 3 ici

def test_cesar_minuscules_avec_retour_a_zero():
    """On va ici vérifier que lorsque'on arrive à la fin de l'alphabet (z) on retourne bien au a"""
    assert chiffrer("xyz", 3) == "abc"

def test_cesar_majuscules_minuscules():
    """on va vérifier si le chiffrement est capable de bien conserver majuscules et minuscules qd elles sont mélangées dans le meme texte"""
    assert chiffrer("ABcdEfG", 4) == "EFghIjK"        #décalage arbitraire de 4, majuscules ou minuscules doivent bien rester

# ---------- Ponctuation - espaces - déchiffrement direct ----------

def test_cesar_ponctuation_et_espaces():
    """Il ne faut pas que la ponctuation ainsi que les espaces soient modifiées"""
    assert chiffrer(" a b, c!", 1) == " b c, d!"        #seule les lettres vont bouger, alors que les espaces, ponctuations, etc. ne bougeront pas

def test_cesar_dechiffrer_direct():
    """c'est l'inverse du chiffrage exactement. C'est la reprise du test, mais à l'envers !"""
    assert dechiffrer("Ludy, lyty, lysy!", 42) == "Veni, vidi, vici!"            #exactement l'inverse qui est vérifié

# ---------- Accents + caractères spéciaux ----------

def test_normaliser_accents():
    """la fonction supprime-t-elle bien les accents sur les minuscules """
    assert normaliser("éàçèùüäöê") == "eaceuuaoe"     #ils doivent tous être remplacé par leur équivlant sans accent

def test_normaliser_accents_majuscules():
    """Idem mais pour les accents sur des majuscules"""
    assert normaliser("ÉÀÇÙ") == "EACU"      #les lettres restent en majuscules même après la suppression des accents

def test_normaliser_chaine_vide():
    """check la normalisation d'une chaine vide """
    assert normaliser("") == ""     #cas limite avec aucun caractère à traiter

def test_cesar_accents_quon_retires_avant_chiffrement():
    """On va faire attention à bien retirer tous les accents avant de chiffrer comme vu dans la consigne.
    Du coup, le é devient e, ç devient c , etc...
    Ensuite on applique la clé"""
    assert chiffrer(normaliser("éàùç"),1) == "fbvd"     #éàùç devient en premier temps eauc puis avec la clé de 1, fbvd

# ---------- Pour les très grandes clés ----------

def test_cesar_tres_grande_cle_positive():
    """on va utiliser le modulo 26 pour les très grandes clés"""
    assert chiffrer("abc", 53) == "bcd"           #ici, 53 modulo 26 = 1, donc la clé c'est 1

def test_cesar_tres_grande_cle_negative():
    """pareil mais pour les clés négatives !!"""
    assert chiffrer("bcd", -53) == "abc"      #ici, le modulo de -53 donne une clé de -1

def test_cesar_tres_grande_cle_negative_2():
    """test pour un second cas avec de très grande clé négative"""
    assert chiffrer("abc", -79) == "zab"    #-79 devient -1 en modulo 26

def test_dechiffre_cle_zero():
    """vérification qu'une clé nulle ne va pas mofifier la valeur"""
    assert chiffrer("Bonjour", 0) == "Bonjour"    #0 doit retourner aucun décalage

# ---------- Pour les cas limites ----------

def test_cesar_cle_multiple_de_26():
    """clé égale à 26 (ou multiple) ne doit pas modifier le texte"""
    assert chiffrer("Bonjour", 26) == "Bonjour"    #tour complet de l'alphabet qui revient bien au point de départ

def test_cesar_cle_52():
    """idem pour 2 tours complets"""
    assert chiffrer("Bonjour", 52) == "Bonjour"    #idem au-dessus en x2

def test_cesar_chaine_vide():
    """Si on a une chaine vide, il faut qu'une chaine vide soit renvoyé. Cela peut importe la clé."""
    assert chiffrer("", 5) == ""      #avec une chaine vide, on a bien une chaine vide peut importe la clé

def test_enigma_cle_zero_identite(monkeypatch):
    """si on a une clé ENIGMA comme ça (0, 0, 0) --> ça ne doit rien changer au message"""
    entrees = iter(["0", "0", "0"])   #simulation avec monkeypatch des input()
    monkeypatch.setattr(
        "builtins.input", lambda _: next(entrees)
    )
    texte, cle = enigma_chiffrer("MAISON")      #on effectue la recherche automatiqeu des clés
    assert texte == "MAISON"             #pas de changement ici au mot maison avec cette clé

def test_cesar_uniquement_chiffres():
    """check si les chiffres ne sont jamais modifiés par le chiffrement de César"""
    assert chiffrer("123456789", 5) == "123456789"    #les chiffres ne sont pas dans l'alphabet donc doivent rester identiques

def test_cesar_uniquement_ponctuation():
    """idem que pour les chiffres mais pour la ponctuation"""
    assert chiffrer("?.,;:-!", 12) == "?.,;:-!"    #idem que chiffres mais pour ponctuation

def test_cesar_uniquement_espaces():
    """idem pour les espaces"""
    assert chiffrer("      ", 7) == "      "   #clé arbitraire encore une fois, mais idem qu'avant pour les espaces

# ---------- Test des comportements spécifiques d'Enigma César ----------

def test_enigma_round_trip(monkeypatch):
    """vérification de si un texte chiffré puis déchiffré avec les mêmes clés retoruve le message initial"""
    entrees = iter(["7", "16", "9"])    #simulation des trois clé enigma input()
    monkeypatch.setattr("builtins.input", lambda _: next(entrees))
    message = "MAISON"               #message à tester
    message_chiffre, cles = enigma_chiffrer(message)     #chiffrement du message
    message_dechiffre = enigma_dechiffrer(message_chiffre, cles)   #on déchiffreici avec les memes clés
    assert enigma_dechiffrer(message_chiffre, cles) == message    #on s'assure comme ça que le message ne change pas suite au double chiffrement

def test_enigma_basta_les_espaces(monkeypatch):
    """Il ne faut pas que les espaces soient chiffrées et ils ne doivent pas faire avancer la clé
    On doit retoruver le meme message avec les lettres chiffrées mais les espaces qui n'ont pas bougé"""
    entrees = iter(["7", "16", "9"])       #simulation des entrées enigma
    monkeypatch.setattr(
        "builtins.input", lambda _: next(entrees)   #remplacement temporaire des inputs qui évite la saisie manuelle
    )
    texte, cle = enigma_chiffrer("MA ISON")    #chiffrement avec un espace
    assert texte == "TQ RZEW"        #l'espace est au meme endroit

def test_enigma_ponctuation(monkeypatch):
    """Il ne faut pas que la ponctuation soit modifiée lors du chiffrement Enigma"""
    entrees = iter(["1", "2", "3"])           #simulation des trois clés
    monkeypatch.setattr("builtins.input", lambda _: next(entrees))   #on remplace les inputs
    texte, cle = enigma_chiffrer("A! B?")         #chiffrement d'un texte qui comporte des espaces et de la ponctuation
    assert texte == "B! D?"     #return identique en théorie

def test_enigma_avec_espace_ne_va_pas_changer_cycle(monkeypatch):
    """On vérifie qu'on ne fait pas avancer le cycle des trois clés enigma avec un espace(en gros on consomme pas une clé Enigma avec un espace
    """
    entrees = iter(["1", "2", "3"])   #simulation des clés
    monkeypatch.setattr(
        "builtins.input", lambda _: next(entrees)    #remplacement temporaire de input()
    )
    texte, cle = enigma_chiffrer("A B")  #chiffrement d'un texte avec un espace, ou A est la clé 1, l'espace est skippé, et B est donc la clé 2
    assert texte == "B D"    #Si le test fonctionne bien, on a A+1 = B, espace inchangé, puis B+2 = D

# ---------- Brute-force, pour César et Enigma ----------

def test_brute_force_cesar_retrouve_le_message():
    """on veut que notre brute forve césar retrouve le message clair
    sans qu'on lui donne la clé.
    On va chiffrer un message connu, puis on va vérifier que le brute-force arrive bel et bien
    à récuperer le message original"""
    message_clair = "coder est ma passion au quotidien"     #texte pour référence
    message_chiffre = chiffrer(message_clair, 13)            #on chiffre avec une clé arbitraire inconnue du brute-force

    liste_bigrammes = charger_bigrammes(200)          #on charge les listes de bigrammes utiliéses pour faire une analyse statistique
    liste_bigrammes_rares = charger_bigrammes_rares()

    texte, cle = brute_force_cesar(message_chiffre, liste_bigrammes, liste_bigrammes_rares)       #ici on recherche automatiquemernt la clé
    assert texte == message_clair          #on test si c'est bien exactmeent le meme message qui est renvoyé

def test_brute_force_enigma_retrouve_le_message(monkeypatch):
    """notre brute-force pour enigma doit etre capable de retrouver le message original"""
    message_clair = "coder est vraiment ma passion au quotidien"          #texte de référence, classique, banal
    entrees = iter(["3", "7", "11"])       #on simule les trois clés en input
    monkeypatch.setattr(
        "builtins.input", lambda _: next(entrees))
    message_chiffre, cle = enigma_chiffrer(message_clair)    #on effectue le chiffrement du message
    liste_bigrammes = charger_bigrammes(200)
    liste_bigrammes_rares = charger_bigrammes_rares()      #on vient ensuite charger les bigrammes français

    texte, cle = brute_force_enigma(message_chiffre, liste_bigrammes, liste_bigrammes_rares)             #on effectue une recherche automatoqeu des trois clés
    assert texte == message_clair     #on test si c'est bien le meme message qui vient
