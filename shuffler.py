#!/usr/bin/env python
"""
Dominion Board Shuffler

This project has a detailed README on https://github.com/thalom/dominion_randomizer/
Use it for whatever you want, I guess.
Change it, commercialize it, sure.
I'm not making any guarantees about it though.
"""
from random import shuffle, randint, random
import sys
import getopt
import config as cf

def pick_n(deck, n):
    shuffle(deck)
    return deck[:n]

def read_deck(filename):
    with open("card_categories/" + filename) as infile:
        deck = infile.readlines()
    for i in range(len(deck)):
        deck[i] = deck[i].strip()
    return list(set(deck))

## Implemented to only ever include up to 1 Way
def pick_lands(ddeck, deck, landDeck, max_landscapes=2, landProbability=0.5):
    ldeck = []
    ddeck = set(ddeck)
    event_deck = set(read_deck("adventures.txt"))
    if not event_deck & ddeck:
        deck.remove("events_adventures")
    proj_deck = set(read_deck("renaissance.txt"))
    if not proj_deck & ddeck:
        deck.remove("projects")
    way_deck = set(read_deck("menagerie.txt"))
    if not way_deck & ddeck:
        deck.remove("ways")
        deck.remove("events_menagerie")
    mark_deck = set(read_deck("empires.txt"))
    if not mark_deck & ddeck:
        deck.remove("landmarks")
        deck.remove("events_empires")
    ally_deck = set(read_deck("allies.txt"))
    if not ally_deck & ddeck:
        deck.remove("allies")
        deck.remove("allies_landscapes")

    for _ in range(max_landscapes):
        rand1 = random()
        if rand1 < landProbability and len(deck) > 1:
            rand2 = randint(1, len(deck)-1)
            lands = deck[rand2]
            ldeck.extend(pick_n(landDeck[lands], 1))
            landDeck[lands].remove(ldeck[-1])
            if ldeck[-1].startswith("Way "):
                deck.remove("ways")

    return ldeck

def setup_young_witch(deck, already_used):
    cost_2_3 = set(read_deck("cost_2.txt"))
    cost_2_3 = cost_2_3 | set(read_deck("cost_3.txt"))
    cost_2_3 = cost_2_3 & set(deck)
    cost_2_3 = list( cost_2_3 - set(already_used) )
    shuffle(cost_2_3)
    return cost_2_3[0]

def setup_way_mouse(deck, already_used):
    treasures = set(read_deck("dedicated_treasures.txt"))
    victories = set(read_deck("dedicated_victories.txt"))
    cost_2_3 = set(read_deck("cost_2.txt"))
    cost_2_3 = cost_2_3 | set(read_deck("cost_3.txt"))
    cost_2_3 = cost_2_3 & set(deck)
    cost_2_3 = cost_2_3 - treasures
    cost_2_3 = cost_2_3 - victories
    cost_2_3 = list( cost_2_3 - set(already_used) )
    shuffle(cost_2_3)
    return cost_2_3[0]

def setup_obelisk(deck):
    treasure = read_deck("treasures.txt")
    victory = read_deck("victories.txt")
    looter = read_deck("looters.txt")
    deck = set(deck) - set(treasure)
    deck -= set(victory)
    if set(looter) & deck:
        deck.add("Ruins")
    deck = list(deck)
    shuffle(deck)
    return deck[0]

def use_plat_col(deck, plat_col_probability=0.5, require_prosperity=True):
    deck2 = read_deck("prosperity.txt")
    rand = random()
    if rand >= plat_col_probability:
        return False
    if require_prosperity:
        return set(deck) & set(deck2)
    else:
        return True

def use_shelters(deck, shelter_probability=0.5, require_dark_ages=True):
    deck2 = read_deck("dark_ages.txt")
    rand = random()
    if rand >= shelter_probability:
        return False
    if require_dark_ages:
        return set(deck) & set(deck2)
    else:
        return True

def display_deck(deck, card_dict, sort="cost", for_online_client=False):
    if for_online_client:
        line_len = 0
        for card in sorted(deck, key=lambda entry: str(card_dict[entry][1])):
            line_len += len(card) + 1
            if sys.platform == "win32" and line_len >= cf.windows_max_terminal_line_length:
                print()
                line_len = 0
            print(card, end=",")
    else:
        print("{:19} {:>4} {:.11}".format("Card", "Cost", "Expansion"))
        if sort == "cost":
            for card in sorted(deck, key=lambda entry: str(card_dict[entry][1])):
                print("{:19} {:>4} {:.11}".format(card, card_dict[card][1], \
                        card_dict[card][0].capitalize()))
        elif sort == "expansion":
            for card in sorted(deck, key=lambda entry: str(card_dict[entry][0])):
                print("{:19} {:>4} {:.11}".format(card, card_dict[card][1], \
                        card_dict[card][0].capitalize()))
        else:
            for card in sorted(deck):
                print("{:19} {:>4} {:.11}".format(card, card_dict[card][1], \
                        card_dict[card][0].capitalize()))

def display_landscapes(deck, for_online_client=False):
    str_builder = ""
    if for_online_client:
        for i, card in enumerate(sorted(deck)):
            if i < len(deck) - 1:
                str_builder += card + ","
            else:
                str_builder += card
        return str_builder
    else:
        if len(deck) == 0:
            str_builder += ("No landscapes\n")
        else:
            str_builder += ("Landscapes\n")
            for card in sorted(deck):
                str_builder += ("{:19}\n".format(card))
        return str_builder

def display_colonies_shelters(deck, plat_col_probability=0.5, \
                              shelter_probability=0.5, \
                              require_prosperity=True, require_dark_ages=True):
    str_builder = ""
    if use_plat_col(deck, plat_col_probability, require_prosperity):
        str_builder += ("Use platina and colonies.\n")
    if use_shelters(deck, shelter_probability, require_dark_ages):
        str_builder += ("Use shelters.\n")
    return str_builder

def display_tutorial(boolean, verbose=1):
    # a:w:r:p:h:i:c:b:d:g:s:t:v:T:V:L:C:S:e:
    print("Use the following options to customize your randomizer:",
        # "{} - {} {} {} {}".format("-O {y, i, n, x, <N>, <N>a, <N>s} where O is one of the below options", \
        # "y/i to require one interaction card;", "n/x to exclude any attack cards;", \
        # "N represents an int, N/Na to require N many interaction cards;", \
        # "Ns to require S many interaction cards."),
        "-a attacks and interactions",
        "-w turn-worsening attacks",
        "-r trashing attacks",
        "-p topdeck attacks",
        "-h handsize attacks",
        "-i deck inspection attacks",
        "-c junking attacks",
        "-b +buys",
        "-d draws",
        "-g gainers",
        "-s sifters",
        "-t trashers",
        "-v villages",
        "-T treasure cards",
        "-V victory cards",
        "-L <landscape probability>",
        "-C <colony/platinum probability",
        "-S <shelter probability>",
        "-e <expansions>",
        sep="\n"
    )
    if verbose >= 1:
        pass
    if verbose >= 2:
        pass

if __name__ == "__main__":

    if cf.show_tutorial:
        display_tutorial(cf.show_tutorial)
    deckFiles = ["base.txt", "intrigue.txt", "seaside.txt", "prosperity.txt", \
            "cornucopia.txt", "hinterlands.txt", "dark_ages.txt", \
            "guilds.txt", "adventures.txt", "empires.txt", "nocturne.txt", \
            "renaissance.txt", "menagerie.txt", "alchemy.txt", "allies.txt"]
    # typeFiles = ["cursers.txt", "deck_inspection_attacks.txt", "medium_draw.txt", \
    #         "handsize_attacks.txt", "secondary_cursers.txt", "sifters.txt", \
    #         "topdeck_attacks.txt", "trashers.txt", "trashing_attacks.txt", \
    #         "turn_worsening_attacks.txt", "villages.txt", "buys.txt", \
    #         "gainers.txt", "dedicated_treasures.txt", "dedicated_victories.txt", \
    #         "remodelers.txt", "thrones.txt", "attacks.txt", "interactions.txt", \
    #         'cantrips.txt', 'durations.txt']
    costFiles = ["cost_1.txt", "cost_2.txt", "cost_3.txt", "cost_4.txt", \
            "cost_5.txt", "cost_6.txt", "cost_7.txt", "cost_8.txt", ]
    altCostFiles = ["cost_1p.txt", "cost_2_1p.txt", "cost_3_1p.txt", \
            "cost_4_1p.txt", "cost_6_1p.txt", "cost_4d.txt", "cost_8d.txt"]
    landscapes = ["none", "projects", "landmarks", "ways", \
            "events_adventures", "events_empires", "events_menagerie", "allies_landscapes"]
    landDeck = {"projects": read_deck("projects.txt"), \
            "landmarks": read_deck("landmarks.txt"), \
            "ways": read_deck("ways.txt"), \
            "events_adventures": read_deck("events_adventures.txt"), \
            "events_empires": read_deck("events_empires.txt"), \
            "events_menagerie": read_deck("events_menagerie.txt"), \
            "allies_landscapes": read_deck("allies_landscapes.txt")}
    xdeck = []
    a = w = r = p = h = i_ = c = D = False
    aDeg = cDeg = 'a'
    u = n = b = d = g = s = t = v = T = V = False
    bDeg = dDeg = gDeg = sDeg = tDeg = vDeg = TDeg = VDeg = 'a'
    L = 0.5
    C = 0.5
    S = 0.5
    if len(sys.argv) > 1:
        # Only grab expansions used in command line
        try:
            opts, args = getopt.getopt(sys.argv[1:], "u:n:a:w:r:p:h:i:c:b:d:g:s:t:v:D:T:V:L:C:S:e:")
        except getopt.GetoptError:
            print("shuffler.py -u -n -a -w -r -p -h -i -c -b -d -g -s -t -v -D -T -V -L <landscape probability> -C <platina/colony probability> -S <shelter probability> -e <expansions>")
            sys.exit(2)
        for opt, arg in opts:
            if opt == "-u":
                if arg.startswith("-") or arg == 'n' or arg == 'x':
                    xdeck.extend(read_deck("durations.txt"))
                elif len(arg) == 1:
                    if arg == "y" or arg == "i":
                        u = 1
                    else:
                        u = int(arg[0])
                else:
                    u = int(arg)
            elif opt == "-n":
                if arg.startswith("-") or arg == 'n' or arg == 'x':
                    xdeck.extend(read_deck("cantrips.txt"))
                elif len(arg) == 1:
                    if arg == "y" or arg == "i":
                        n = 1
                    else:
                        n = int(arg[0])
                else:
                    n = int(arg)
            elif opt == "-a":
                if arg.startswith("-") or arg == 'n' or arg == 'x':
                    xdeck.extend(read_deck("attacks.txt"))
                elif len(arg) == 1:
                    if arg == "y" or arg == "i":
                        a = 1
                    else:
                        a = int(arg[0])
                else:
                    a = int(arg[0])
                    aDeg = arg[1]
            elif opt == "-c":
                if arg.startswith("-") or arg == 'n' or arg == 'x':
                    xdeck.extend(read_deck("cursers.txt"))
                elif len(arg) == 1:
                    if arg == "y" or arg == "i":
                        c = 1
                    else:
                        c = int(arg[0])
                else:
                    c = int(arg[0])
                    cDeg = arg[1]
            elif opt == "-i":
                if arg.startswith("-") or arg == 'n' or arg == 'x':
                    xdeck.extend(read_deck("deck_inspection_attacks.txt"))
                else:
                    if arg == "y" or arg == "i":
                        i_ = 1
                    else:
                        i_ = int(arg[0])
            elif opt == "-h":
                if arg.startswith("-") or arg == 'n' or arg == 'x':
                    xdeck.extend(read_deck("handsize_attacks.txt"))
                else:
                    if arg == "y" or arg == "i":
                        h = 1
                    else:
                        h = int(arg[0])
            elif opt == "-p":
                if arg.startswith("-") or arg == 'n' or arg == 'x':
                    xdeck.extend(read_deck("topdeck_attacks.txt"))
                else:
                    if arg == "y" or arg == "i":
                        p = 1
                    else:
                        p = int(arg[0])
            elif opt == "-r":
                if arg.startswith("-") or arg == 'n' or arg == 'x':
                    xdeck.extend(read_deck("trashing_attacks.txt"))
                else:
                    if arg == "y" or arg == "i":
                        r = 1
                    else:
                        r = int(arg[0])
            elif opt == "-w":
                if arg.startswith("-") or arg == 'n' or arg == 'x':
                    xdeck.extend(read_deck("turn_worsening_attacks.txt"))
                else:
                    if arg == "y" or arg == "i":
                        w = 1
                    else:
                        w = int(arg[0])
            ## "true_buys" and "buys"
            ## degrees may be None or 'a' for any, 's' for strong
            elif opt == "-b":
                if arg.startswith("-"):
                    b = 1
                else:
                    if len(arg) == 1:
                        if arg == "y" or arg == "i":
                            b = 1
                        elif arg == "n" or arg == "x":
                            xdeck.extend(read_deck("buys.txt"))
                        else:
                            b = int(arg[0])
                    else:
                        b = int(arg[0])
                        bDeg = arg[1]
            ## Strong gainers come from "strong_gainers.txt"
            ## degrees may be None or 'a' for any, 's' for strong
            elif opt == "-g":
                if arg.startswith("-"):
                    g = 1
                else:
                    if len(arg) == 1:
                        if arg == "y" or arg == "i":
                            g = 1
                        elif arg == "n" or arg == "x":
                            xdeck.extend(read_deck("gainers.txt"))
                        else:
                            g = int(arg[0])
                    else:
                        g = int(arg[0])
                        gDeg = arg[1]
            ## draws range from "very_strong_draw.txt" to
            ## "strong_draw.txt" to "medium_draw.txt" to "weak_draw.txt"
            ## degrees may be None or 'a' for any,
            ## 'w' for weak, 'm' for medium, 's' for strong, 'v' for very strong
            elif opt == "-d":
                if arg.startswith("-"):
                    d = 1
                else:
                    if len(arg) == 1:
                        if arg == "y" or arg == "i":
                            d = 1
                        elif arg == "n" or arg == "x":
                            xdeck.extend(read_deck("medium_draw.txt"))
                        else:
                            d = int(arg[0])
                    else:
                        d = int(arg[0])
                        dDeg = arg[1]
            ## "true_sifters.txt" and "sifters.txt"
            ## degrees may be None or 'a' for any, 's' for strong
            elif opt == "-s":
                if arg.startswith("-"):
                    s = 1
                else:
                    if len(arg) == 1:
                        if arg == "y" or arg == "i":
                            s = 1
                        elif arg == "n" or arg == "x":
                            xdeck.extend(read_deck("sifters.txt"))
                        else:
                            s = int(arg[0])
                    else:
                        s = int(arg[0])
                        sDeg = arg[1]
            ## "strong_trashers.txt" and "trashers.txt"
            ## degrees may be None or 'a' for any, 's' for strong,
            ## 'r' for remodelers
            elif opt == "-t":
                if arg.startswith("-"):
                    t = 1
                else:
                    if len(arg) == 1:
                        if arg == "y" or arg == "i":
                            t = 1
                        elif arg == "n" or arg == "x":
                            xdeck.extend(read_deck("trashers.txt"))
                        else:
                            t = int(arg[0])
                    else:
                        t = int(arg[0])
                        tDeg = arg[1]
            ## "true_villages.txt" and "villages.txt" and 'thrones.txt'
            ## degrees may be None or 'a' for any, 's' for strong,
            ## 't' for thrones
            elif opt == "-v":
                if arg.startswith("-"):
                    v = 1
                else:
                    if len(arg) == 1:
                        if arg == "y" or arg == "i":
                            v = 1
                        elif arg == "n" or arg == "x":
                            xdeck.extend(read_deck("villages.txt"))
                        else:
                            v = int(arg[0])
                    else:
                        v = int(arg[0])
                        vDeg = arg[1]
            elif opt == "-D":
                if arg.startswith("-"):
                    D = 1
                else:
                    if len(arg) == 1:
                        if arg == "y" or arg == "i":
                            D = 1
                        elif arg == "n" or arg == "x":
                            xdeck.extend(read_deck("defense.txt"))
                        else:
                            D = int(arg[0])
                    else:
                        D = int(arg[0])
            elif opt == "-T":
                if arg.startswith("-"):
                    T = 1
                else:
                    if len(arg) == 1:
                        if arg == "y" or arg == "i":
                            T = 1
                        elif arg == "n" or arg == "x":
                            xdeck.extend(read_deck("dedicated_treasures.txt"))
                        else:
                            T = int(arg[0])
                    else:
                        T = int(arg[0])
                        TDeg = arg[1]
            elif opt == "-V":
                if arg.startswith("-"):
                    V = 1
                else:
                    if len(arg) == 1:
                        if arg == "y" or arg == "i":
                            V = 1
                        elif arg == "n" or arg == "x":
                            xdeck.extend(read_deck("dedicated_victories.txt"))
                        else:
                            V = int(arg[0])
                    else:
                        V = int(arg[0])
                        VDeg = arg[1]
            elif opt == "-L":
                L = float(arg)
            elif opt == "-C":
                C = float(arg)
            elif opt == "-S":
                S = float(arg)
            elif opt == "-e":
                deckFiles2 = []
                for file in deckFiles:
                    for arg2 in sys.argv[sys.argv.index('-e')+1:]:
                        if arg2.lower() == file[:file.find(".txt")]:
                            deckFiles2.append(file)
                deckFiles = deckFiles2

    ddeck = []
    card_dict = {}
    for file in deckFiles:
        this_expansion = read_deck(file)
        ddeck.extend(this_expansion)
        for card in this_expansion:
            card_dict[card] = (file[:file.find(".txt")],)
    for i, file in enumerate(costFiles):
        i += 1
        this_cost = read_deck(file)
        for card in ddeck:
            if card in this_cost:
                card_dict[card] += (i,)
        ddeck = list(set(ddeck) - set(xdeck))
    for file in altCostFiles:
        this_cost = read_deck(file)
        parse_str = file[:file.find(".txt")].split("_")
        parsed_cost = ""
        for part in parse_str[1:]:
            parsed_cost += part.upper() + ","
        parsed_cost = parsed_cost.strip(",")
        for card in ddeck:
            if card in this_cost:
                card_dict[card] += (parsed_cost,)

    the_deck = pick_n(ddeck, cf.BOARD_SIZE)
    include_dict = {"true_buys.txt" if bDeg == 's' else 'buys.txt': b, \
            # "medium_draw.txt": d,
            'strong_gainers.txt' if gDeg == 's' else "gainers.txt": g, \
            'true_sifters.txt' if sDeg == 's' else "sifters.txt": s, \
            'strong_trashers.txt' if tDeg == 's' else \
                    ('remodelers.txt' if tDeg == 'r' else "trashers.txt"): t, \
            'true_villages.txt' if vDeg == 's' else \
                    ('thrones.txt' if vDeg == 't' else "villages.txt"): v, \
            'dedicated_alt_treasures.txt' if TDeg == 's' else 'dedicated_treasures.txt': T, \
            'dedicated_alt_victories.txt' if VDeg == 's' else 'dedicated_victories.txt': V, \
            'attacks.txt' if aDeg == 's' else 'interactions.txt': a, \
            'cursers.txt' if cDeg == 's' else 'secondary_cursers.txt': c, \
            'deck_inspection_attacks.txt': i_, \
            'handsize_attacks.txt': h, 'topdeck_attacks.txt': p, \
            'trashing_attacks.txt': r, 'turn_worsening_attacks.txt': w, \
            'cantrips.txt': n, 'durations.txt': u, 'defense.txt': D
    }
    # CODE FOR DRAWS ENTRY
    if dDeg == 'v':
        include_dict['very_strong_draw.txt'] = d
    elif dDeg == 's':
        include_dict['strong_draw.txt'] = d
    # elif dDeg == 'm':
    #     include_dict['medium_draw.txt'] = d
    elif dDeg == 'w':
        include_dict['weak_draw.txt'] = d
    else:
        include_dict['medium_draw.txt'] = d
    ## Do it twice to double check that you haven't pushed out
    ## a card that was previously satisfying a condition
    counter = 0
    for _ in range(2):
        for file, choice in include_dict.items():
            draw_deck = read_deck(file)
            if type(choice) == int:
                boolean = len(set(the_deck) & set(draw_deck)) >= choice
            else:
                boolean = choice
            while choice and not boolean:
                draw_deck = list(set(draw_deck) & set(ddeck))
                shuffle(draw_deck)
                mini_counter = 0
                while draw_deck[0] in the_deck:
                    shuffle(draw_deck)
                    mini_counter += 1
                    if mini_counter > len(the_deck):
                        print("Could not satisfy all options.")
                        sys.exit(2)
                the_deck = the_deck[:len(the_deck)-1]
                the_deck.insert(0, draw_deck[0])
                counter += 1
                if counter > len(the_deck):
                    print("Could not satisfy all options.")
                    sys.exit(2)
                if type(choice) == int:
                    boolean = len(set(the_deck) & set(draw_deck)) >= choice
                else:
                    boolean = set(the_deck) & set(draw_deck)
                # print(draw_deck[0], file)
    if "Young Witch" in the_deck and cf.automate_young_witch:
        bane = setup_young_witch(ddeck, the_deck)
        the_deck.append(bane)

    the_landscapes = pick_lands(the_deck, landscapes, landDeck, cf.MAX_LANDSCAPES, L)

    display_deck(the_deck, card_dict, sort=cf.sort, \
            for_online_client=cf.terminal_output_for_online_client)
    lands_message = display_landscapes(the_landscapes, \
            for_online_client=cf.terminal_output_for_online_client)
    print(lands_message)

    if "Young Witch" in the_deck and cf.automate_young_witch:
        print("Bane card: {}".format(bane))
    if "Obelisk" in the_landscapes and cf.automate_obelisk:
        obelisk = setup_obelisk(the_deck)
        print("Obelisk card: {}".format(obelisk))
    if "Way of the Mouse" in the_landscapes and cf.automate_way_of_the_mouse:
        mouse = setup_way_mouse(ddeck, the_deck)
        print("Way of the Mouse card: {}".format(mouse))
    col_shelt_message = display_colonies_shelters(the_deck, C, S, \
            cf.plat_col_require_ge_1_prosperity_card, cf.shelters_require_ge_1_dark_ages_card)
    print(col_shelt_message)

    if cf.output_file:
        outfile = open(cf.output_path, "w")
        for i, card in enumerate(the_deck + the_landscapes):
            if i == len(the_deck + the_landscapes) - 1:
                outfile.write(card)
            else:
                outfile.write(card + ",")
        outfile.write("\n\n" + col_shelt_message)
        outfile.close()


## TODO:
## - Option to INCLUDE a range of different cost cards.
## (e.g. 2-5 requires at least one 2-, 3-, 4-, and 5-cost card)
