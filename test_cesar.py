"""Tests pour le Mini-Projet A.

Ce fichier contient les chaînes de test officielles + quelques cas
limites. Ajoutez vos propres tests au fur et à mesure.

Pour lancer les tests :
    pip install pytest
    pytest -v
"""
import sys
from pathlib import Path

import pytest #va nous permettre de vérifier qu'un fonction trouve bien une erreur

# Permet d'importer main.py depuis le dossier parent
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import chiffrer, dechiffrer, enigma_chiffrer  # noqa: E402


# ---------- Chaînes de test officielles — César (spec §7) ----------

def test_cesar_officiel_cle_42():
    assert chiffrer("Veni, vidi, vici!", 42) == "Ludy, lyty, lysy!"


def test_cesar_officiel_cle_neg_42():
    assert chiffrer("Veni, vidi, vici!", -42) == "Foxs, fsns, fsms!"


# ---------- Chaîne de test officielle — Enigma César (spec §2.6) ----------

def test_enigma_officiel_maison():
    assert enigma_chiffrer("MAISON", (7, 16, 9)) == "TQRZEW"


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

# ---------- Ponctuation - espaces - déchiffrement direct ----------

def test_cesar_ponctuation_et_espaces():
    """Il ne faut pas que la ponctuation ainsi que les espaces soient modifiées"""
    assert chiffrer(" a b, c!", 1) == "b c, d!"        #seule les lettres vont bouger, alors que les espaces, ponctuations, etc. ne bougeront pas

def test_cesar_dechiffrer_direct():
    """c'est l'inverse du chiffrage exactement. C'est la reprise du test, mais à l'envers !"""
    assert dechiffrer("Ludy, lyty, lysy!", 42) == "Veni, vidi, vici!"            #exactement l'inverse qui est vérifié

# ---------- Accents + caractères spéciaux ----------

def test_cesar_accents_quon_retires_avant_chiffrement():
    """On va faire attention à bien retirer tous les accents avant de chiffrer comme vu dans la consigne.
    Du coup, le é devienbt e, ç devient c , etc...
    Ensuite on applique la clé"""
    assert chiffrer("éàùç",1) == "fbvd"     #éàùç devient en premier temps eauc puis avec la clé de 1, fbvd

# ---------- Pour les très grandes clés ----------

def test_cesar_tres_grande_cle_positive():
    """on va utiliser le modulo 26 pour les très grandes clés"""
    assert chiffrer("abc", 53) == "bcd"           #ici, 53 modulo 26 = 1, donc la clé c'est 1

def test_cesar_tres_grande_cle_negative():
    """pareil mais pour les clés négatives !!"""
    assert chiffrer("bcd", -53) == "abc"      #ici, le modulo de -53 donne une clé de -1

# ---------- Pour les cas limites ----------

def test_cesar_chaine_vide():
    """Si on a une chaine vide, il faut qu'une chaine vide soit renvoyé. Cela peut importe la clé."""
    assert chiffrer("", 5) == ""      #avec une chaine vide, on a bien une chaine vide peut importe la clé

def test_enigma_cle_zero_identite():
    """si on a une clé ENIGMA comme ça (0, 0, 0) --> ça ne doit rien changer au message"""
    assert enigma_chiffrer("MAISON", (0, 0, 0)) == "MAISON"             #pas de changement ici au mot maison avec cette clé

# ---------- TEst des comportement s spécifiques d'Enigma César ----------

def test_enigma_round_trip():
    """si on chiffre avec des inverses (soit 7, 16 ,9) puis on rechiffre en imverse (-7, -16, -9)
    On doit bien obtenir le message original"""
    cles = (7 , 16, 9)
    cles_inverse = (-7, -16, -9)                       #les clés et leur inverses
    message = "MAISON"                                       #message à tester
    message_chiffre = enigma_chiffrer(message, cles)                            #premeir chiffrement
    assert enigma_chiffrer(message_chiffre, cles_inverse) == message     #on s'assure comme ça que le message ne change pas suite au double chiffrement

def test_enigma_basta_les_espaces():
    """Il ne faut pas que les espaces soient chiffrées et ils ne doivent pas faire avancer la clé
    On doit retoruver le meme message avec les lettres chiffrées mais les espaces qui n'ont pas bougé"""
    assert enigma_chiffrer("MA ISON", (7, 16, 9)) == "TQ RZEW"        #l'espace est au meme endroit

# ---------- Si clé Enigma invalide --> rejet ----------

def test_enigma_rejette_cle_qui_na_pas_trois_nombres():
    """Il faut que la clé est exactement 3 nombres
    Si c'est pas le cas --> erreur"""
    with pytest.raises(ValueError):
        enigma_chiffrer("MAISON", (7, 16))       #cas ou on a pas assez de nombres, ici 2
    with pytest.raises(ValueError):
        enigma_chiffrer("MAISON", (7, 16, 9, 4))      #cas ou on a trop de nombres, ici 4

# ---------- Brute-force, pour César et Enigma ----------

def test_brute_force_cesar_retrouve_le_message():
    """on veut que notre brute forve césar retrouve le message clair
    sans qu'on lui donne la clé.
    On va chiffrer un message connu, puis on va vérifier que le brute-force arrive bel et bien
    à récuperer le message original"""
    from main import brute_force_cesar     #on est obliger de faire un import local au cas ou brute_force_cesar n'existe pas encore au début du porjet

    message_clair = "coder est ma passion au quotidien"
    message_chiffre = chiffrer(message_clair, 13)
    assert brute_force_cesar(message_chiffre) == message_clair          #on test si c'est bien exactmeent le meme message qui est renvoyé

def test_brute_force_enigma_retrouve_le_message():
    """notre brute-force pour enigma doit etre capable de balayer toutes les combinaisons possibles (soit 17575)
    et quand meme retrouver le message original"""
    from main import brute_force_enigma     #idem qu'avant

    message_clair = "coder est vraiment ma passion au quotidien"
    cles = (3, 7, 11)
    message_chiffre = enigma_chiffrer(message_clair, cles)
    assert brute_force_enigma(message_chiffre) == message_clair     #on test si c'est bien le meme message qui vient

