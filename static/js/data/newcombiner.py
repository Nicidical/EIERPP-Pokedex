import json
from copy import deepcopy

def returnSortedList(toSort,moveList,index):
    toSort = sorted(toSort, key=lambda x: x[index])

if __name__ == "__main__":
    data = ""

    # Loading just 2.5
    with open('formatted2.5.txt', 'r', encoding='utf8') as file: data = json.load(file)

    # Getting Moves and organizing them (2.5)
    moveList = [""] * len(data["moves"])
    for move in data["moves"]:
        # Removing stat ignoring flags
        if 17 in move["flags"]: move["flags"].remove(17)
        if move["name"] == "Freezy Frost": move["lDesc"] = "Attack with crystal made of cold frozen haze."
        if move["name"] == "Cross Chop": move["lDesc"] = "The foe is hit with double chops. Hits twice. High crit ratio."
        if move["name"] == "Aerial Ace": move["lDesc"] = "An extremely fast attack. It can't be evaded. Always crits. Keen Edge boost."
        moveList[move["id"]] = [move["name"], move["pwr"], move["acc"], move["prio"]]

    # Changing ability descriptions
    for ability in data["abilities"]:
        if ability["name"] == "Gunman": ability["desc"] = "Mega Launcher + Status moves are Mega Launcher boosted."
        
    # Going through every mon and:
    # Combining every move in a set
    # Creating a new set replacing the numbers with move names
    # Ordering it alphabetically
    # Replacing the move names with numbers once again
    # Putting everything into a massive list of tutor moves, with all other move categories blank
    moveSets = dict()
    convergenceMoveSets = dict()
    silvallyTutor = set()

    bannedSpecies = ["Arceus", 
                     "Burmy Eterna",
                     "Calyrex Cloud Rider",
                     "Calyrex Ice Rider",
                     "Calyrex Shadow Rider",
                     "Cascoon Primal",
                     "Castform Foggy",
                     "Castform Rainy",
                     "Castform Sandy",
                     "Castform Snowy",
                     "Castform Sunny",
                     "Chien Pao Mega",
                     "Dawn Wings",
                     "Deoxys",
                     "Deoxys Attack",
                     "Dialga",
                     "Dusk Mane",
                     "Espeon Primal",
                     "Eternatus",
                     "Kartana Fallen",
                     "Giratina",
                     "Groudon",
                     "Ho-Oh",
                     "Hoopa",
                     "Kecleong",
                     "Koraidon",
                     "Kyogre",
                     "Kyurem",
                     "Lugia",
                     "Lunala",
                     "Magearna",
                     "Melmetal Mega",
                     "Mew",
                     "Mimikyu Apex",
                     "Mimikyu Primal",
                     "Miraidon",
                     "Necrozma Ultra",
                     "Palkia",
                     "Rayquaza",
                     "Regigigas",
                     "Reshiram",
                     "Smeargle",
                     "Silvally",
                     "Solgaleo",
                     "Solrock System",
                     "Terapagos",
                     "Urshifu Mega",
                     "Urshifu Rapid Strike Style Mega",
                     "Wigglytuff Primal",
                     "Victini Primal",
                     "Xerneas"
                     "Yveltal",
                     "Zacian",
                     "Zamazenta",
                     "Zekrom",
                     "Zygarde Complete"]

    # Creating all possible type combinations for convergenceMoveSets
    for i in range(21):
        for j in range(i,21):
            convergenceMoveSets[(i,j)] = set()


    for pokemon in data["species"]:
        # print(f"{pokemon["name"]}: {pokemon["id"]}")
        tempSet = set()
        for move in pokemon["levelUpMoves"]:
            if (move["lv"] <= 100): tempSet.add(move["id"])
            else: print(f"{pokemon['name']} can't learn {move['id']}.")
        for move in pokemon["tutor"]:
            if (pokemon["name"] == "Silvally"): silvallyTutor.add(move)
            tempSet.add(move)
        
        tempSet2 = set()
        if ("Silvally " in pokemon["name"]): tempSet = tempSet.union(silvallyTutor)
        for id in tempSet:
            tempSet2.add(moveList[id][0])
        tempSet2.add("Protect")
        tempSet2.add("Secret Power")
        tempSet2.add("Hidden Power")
        tempSet2.add("Substitute")
        moveSets[pokemon["id"]] = tempSet2

        validConverge = True
        for mon in bannedSpecies:
            if mon in pokemon["name"] and pokemon["name"] != "Deoxys Speed" and pokemon["name"] != "Deoxys Defense":
                validConverge = False
                print(f"Invalid species: {pokemon['name']}")

        if validConverge:
            type1 = pokemon["stats"]["types"][0]
            type2 = pokemon["stats"]["types"][1]
            convergenceMoveSets[(min(type1, type2),max(type1,type2))] = convergenceMoveSets[(min(type1, type2),max(type1,type2))].union(tempSet2)

    # Edge Cases for Partner/Battle Bond/Alternate Form Pokemon   
    moveSets[1852] = moveSets[1852].union(moveSets[25]) # Pikachu
    moveSets[1854] = moveSets[1854].union(moveSets[52]) # Meowth   
    moveSets[1853] = moveSets[1853].union(moveSets[133]) # Eevee  
    moveSets[1857] = moveSets[1857].union(moveSets[884]) # Duraludon  
    moveSets[1859] = moveSets[1859].union(moveSets[926]) # Fidough
    moveSets[1862] = moveSets[1862].union(moveSets[655]) # Delphox 
    moveSets[1860] = moveSets[1860].union(moveSets[652]) # Chesnaught 
    moveSets[1687] = moveSets[1687].union(moveSets[658]) # Greninja
    moveSets[1678] = moveSets[1678].union(moveSets[645]) # Landorus-Therian
    moveSets[1677] = moveSets[1677].union(moveSets[642]) # Thundurus-Therian
    moveSets[1676] = moveSets[1676].union(moveSets[641]) # Tornadus-Therian
    moveSets[1844] = moveSets[1844].union(moveSets[905]) # Enamorus-Therian
    moveSets[1649] = moveSets[1649].union(moveSets[492]) # Shaymin-Sky
    moveSets[1681] = moveSets[1681].union(moveSets[647]) # Keldeo-Resolute

    # Comment this out if you do not want to create a new dex
    # Standard Alphabetical
    for id, moveset in moveSets.items():
        namedTempMoveset = list(moveset)
        namedTempMoveset.sort()
        alphabetizedMoveset = []
        for move in namedTempMoveset:
            newID = 0
            # Wrote a for loop because the find functions were annoying me
            for move2 in moveList:
                if (move2[0] != move): newID += 1
                else: break
            if (newID < 1000): alphabetizedMoveset.append(newID)
        moveSets[id] = alphabetizedMoveset

    for pokemon in data["species"]:
        pokemon["levelUpMoves"] = []
        pokemon["tutor"] = moveSets[pokemon["id"]]

    with open('gameDataV2.5.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        print("Finished standard sorting in gameDataV2.5.json.")
    
    # Standard Alphabetical (Convergence)
    for id, moveset in convergenceMoveSets.items():
        namedTempMoveset = list(moveset)
        namedTempMoveset.sort()
        alphabetizedMoveset = []
        for move in namedTempMoveset:
            newID = 0
            # Wrote a for loop because the find functions were annoying me
            for move2 in moveList:
                if (move2[0] != move): newID += 1
                else: break
            if (newID < 1000): alphabetizedMoveset.append(newID)
        convergenceMoveSets[id] = alphabetizedMoveset

    for pokemon in data["species"]:
        pokemon["levelUpMoves"] = []

        type1 = pokemon["stats"]["types"][0]
        type2 = pokemon["stats"]["types"][1]
        pokemon["tutor"] = convergenceMoveSets[(min(type1, type2),max(type1,type2))]

    with open('gameDataV1.6.1.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        print("Finished standard convergence sorting in gameDataV1.6.1.json.")
    
    newData = deepcopy(data)
    illegalSpecies = set()
    
    # Running once to find all Pokemon that are evolved
    for pokemon in data["species"]:
        for evo in pokemon["evolutions"]:
            illegalSpecies.add(data["species"][evo["in"]]["id"])
        bst = 0
        for stat in pokemon["stats"]["base"]:
            bst += stat
        if bst > 420 or len(pokemon["evolutions"]) == 0 and pokemon["id"] != -1:
            illegalSpecies.add(pokemon["id"])
    
    # Running a loop to only have 1st stage pokemon with a bst <= 420
    newData["species"] = [item for item in newData["species"] if item["id"] not in illegalSpecies]
    for mon in newData["species"]: mon["evolutions"] = []
    for location in newData["locations"]["maps"]:
        if "land" in location: location["land"] = [2, 2, 1]
        if "honey" in location: location["honey"] = [2, 2, 1]
        if "water" in location: location["water"] = [2, 2, 1]
        if "fish" in location: location["fish"] = [2, 2, 1]
        if "hidden" in location: location["hidden"] = [2, 2, 1]
        if "rock" in location: location["rock"] = [2, 2, 1]
        if "given" in location: location["given"] = [2, 2, 1]
    newData["trainers"] = []
    {
      "name": "Sickle",
      "tclass": 54,
      "db": False,
      "party": [
        {
          "spc": 2,
          "abi": 2,
          "ivs": [
            31,
            31,
            31,
            31,
            31,
            31
          ],
          "evs": [
            0,
            252,
            0,
            4,
            0,
            252
          ],
          "item": 194,
          "nature": 11,
          "moves": [
            187,
            299,
            337,
            9
          ]
        }
      ]
    }
    
    with open('gameDataVBeta2.0.json', 'w', encoding='utf-8') as file:
        json.dump(newData, file, ensure_ascii=False, indent=2)
        print("Finished LC sorting in gameDataVBeta2.0.json.")
    
    alphabetizedMoveset = dict()
    for id, moveset in moveSets.items():
        tempMoveset = list()
        for move in moveset:
            if (move > 999): 
                print ("Nope")
                continue
            tempMoveset.append(moveList[move])
        alphabetizedMoveset[id] = tempMoveset
    
    bpMovesets = dict()
    accMovesets = dict()
    prioMovesets = dict()
    
    
    
    # Sorted by Base Power
    for id, moveset in alphabetizedMoveset.items():
        tempMoveset = sorted(moveset, key=lambda x: x[1], reverse=True)
        newMoveset = list()
        for move in tempMoveset:
            newID = moveList.index(move)
            newMoveset.append(newID)
        moveSets[id] = newMoveset
    
    for pokemon in data["species"]:
        pokemon["levelUpMoves"] = []
        pokemon["tutor"] = moveSets[pokemon["id"]]

    with open('gameDataV2.2.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        print("Finished base power sorting in gameDataV2.2.json.")
    
    
    
    # Sorted by Accuracy
    for id, moveset in alphabetizedMoveset.items():
        tempMoveset = sorted(moveset, key=lambda x: x[2], reverse=True)
        newMoveset = list()
        for move in tempMoveset:
            newID = moveList.index(move)
            newMoveset.append(newID)
        moveSets[id] = newMoveset
    
    for pokemon in data["species"]:
        pokemon["levelUpMoves"] = []
        pokemon["tutor"] = moveSets[pokemon["id"]]

    with open('gameDataV2.1.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        print("Finished accuracy sorting in gameDataV2.1.json.")
    
    
    
    # Sorted by Priority
    for id, moveset in alphabetizedMoveset.items():
        tempMoveset = sorted(moveset, key=lambda x: x[3], reverse=True)
        newMoveset = list()
        for move in tempMoveset:
            newID = moveList.index(move)
            newMoveset.append(newID)
        moveSets[id] = newMoveset
    
    for pokemon in data["species"]:
        pokemon["levelUpMoves"] = []
        pokemon["tutor"] = moveSets[pokemon["id"]]

    with open('gameDataVBeta2.1.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        print("Finished priority sorting in gameDataVBeta2.1.json.")       

    """
    fullMovelist = set()
    illegalMoves = ["Absorb", "Acupressure", "Attract", "Clear Smog", "Destiny Bond", "Double Team", "Encore", "Explosion", "Final Gambit", "Guard Split", "Guard Swap", "Lunar Dance", "Haze", "Healing Wish", "Heart Swap", "Helping Hand", "Imprison", "Inverse Room", "Lash Out", "Magic Room", "Memento", "Minimize", "Misty Explosion", "Mud Sport", "Outburst", "Perish Song", "Power Split", "Power Swap", "Power Trip", "Psych Up", "Punishment", "Quash", "Salt Cure", "Self-Destruct", "Simple Beam", "Smokescreen", "Spectral Thief", "Spotlight", "Stored Power", "Topsy-Turvy", "Water Sport", "Wonder Room"]
    
    with open('moveset.txt', 'w', encoding='utf-8') as file:
        ids = [343]
        for id, moveset in moveSets.items():
            if id not in ids: continue
            
            for move in moveset:
                fullMovelist.add(move)
        
        alphabeticalMoves = list(fullMovelist)
        
        for move in illegalMoves:
            if move in alphabeticalMoves: alphabeticalMoves.remove(move)
        alphabeticalMoves.sort()
        
        firstMove = True
        for move in alphabeticalMoves:
            if firstMove: 
                file.write(f"{move}")
                firstMove = False
            else: file.write(f", {move}")
        
        file.close()
    """ 
            
            
            