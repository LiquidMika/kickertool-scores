#!/usr/bin/env python

import json
import sys


def xor(x, y):
    return bool((x and not y) or (not x and y))


def list_match_joueur(joueur, matches, longest_string):
    liste_matchs_joueur = "\n"
    liste_matchs_joueur += joueur + "\n"
    liste_matchs_joueur += "=" * len(joueur) + "\n"
    for match in matches:
        if joueur in match:
            nb_victoire_p1 = 0
            nb_victoire_p2 = 0
            for a, b in match[3]:
                if a > b:
                    nb_victoire_p1 += 1
                else:
                    nb_victoire_p2 += 1
            if xor(nb_victoire_p1 > nb_victoire_p2, joueur == match[1]):
                vainq_or_defait =  "Défaite"
            else:
                vainq_or_defait = "Victoire"

            if joueur == match[1]:
                score = str(nb_victoire_p1) + " - " + str(nb_victoire_p2)
                opponent = match[2]
                lst_manches = []
                for a, b in match[3]:
                    lst_manches.append(str(a) + "-" + str(b))
                str_manches = '   '.join(lst_manches)
            
            if joueur == match[2]:
                score = str(nb_victoire_p2) + " - " + str(nb_victoire_p1)
                opponent = match[1]
                lst_manches = []
                for a, b in match[3]:
                    lst_manches.append(str(b) + "-" + str(a))
                str_manches = '   '.join(lst_manches)

            str_ligne = f"{vainq_or_defait.ljust(12)}{score}   {opponent.ljust(longest_string + 4)}{str_manches}"
            liste_matchs_joueur += str_ligne + '\n'
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

car_max = len(max(list_players, key=len))

for player in sorted(list_players):
    print(list_match_joueur(player, list_matchs, longest_string=car_max))
