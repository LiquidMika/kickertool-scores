#!/usr/bin/env python

import json
import sys


def xor(x, y):
    return bool((x and not y) or (not x and y))


def list_match_joueur(joueur, matches):
    liste_matchs_joueur = "\n"
    liste_matchs_joueur += joueur + "\n"
    liste_matchs_joueur += "=" * len(joueur) + "\n"
    for match in matches:
        if joueur in match:
            vainqueur_joueur1 = True
            nb_victoire_p1 = 0
            nb_victoire_p2 = 0
            for a, b in match[3]:
                if a > b:
                    nb_victoire_p1 += 1
                else:
                    nb_victoire_p2 += 1
            if xor(nb_victoire_p1 > nb_victoire_p2, joueur == match[1]):
                liste_matchs_joueur += "Défaite    "
            else:
                liste_matchs_joueur += "Victoire   "

            if joueur == match[1]:
                liste_matchs_joueur += str(nb_victoire_p1) + " - "
                liste_matchs_joueur += str(nb_victoire_p2) + "   "
                liste_matchs_joueur += match[2] + "\t"
                for a, b in match[3]:
                    liste_matchs_joueur += str(a) + "-" + str(b) + "\t"
                liste_matchs_joueur += "\n"

            if joueur == match[2]:
                liste_matchs_joueur += str(nb_victoire_p2) + " - "
                liste_matchs_joueur += str(nb_victoire_p1) + "   "
                liste_matchs_joueur += match[1] + "\t"
                for a, b in match[3]:
                    liste_matchs_joueur += str(b) + "-" + str(a) + "\t"
                liste_matchs_joueur += "\n"
    return liste_matchs_joueur


try:
    chemin = sys.argv[1]
except:
    print("Manque le chemin du .csv")


with open(chemin, "r") as read_file:
    data = json.load(read_file)


dict_players = {}
for i in data["players"]:
    dict_players[i["_id"]] = i["_name"]

list_matchs = []
for tour in data["rounds"]:
    for match in tour["plays"]:
        if match["valid"] == True:
            ce_match = []
            division = dict_players[match["team1"]["_id"]][0:2]
            joueur1 = dict_players[match["team1"]["_id"]][3:]
            joueur2 = dict_players[match["team2"]["_id"]][3:]
            score = []
            ce_match.append(division)
            ce_match.append(joueur1)
            ce_match.append(joueur2)
            for discipline in match["disciplines"]:
                for manche in discipline["sets"]:
                    score.append((manche["team1"], manche["team2"]))
            ce_match.append(score)
            list_matchs.append(ce_match)

list_players = []
for player in dict_players.values():
    list_players.append(player[3:])

for player in sorted(list_players):
    print(list_match_joueur(player, list_matchs))
