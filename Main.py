from CSP_Wordle import *
from Genetic_Wordle import *

functionList = [Solve_Genetic,SolveA1,SolveA2,Solve_RAC,Solve_RACAC]

def mainMenu():
    all_words = parse()
    print("Projet de RP 2022 - Algo de recherche de mots")

    print("1-Séléctionnez une fonction :")
    for i in range(len(functionList)):
        print(str(i+1)+"- "+functionList[i].__name__)
    functionNum = int(input("Votre choix : "))
    while functionNum < 1 or functionNum > len(functionList):
        print("Veuillez entrer un nombre entre 1 et "+str(len(functionList)))
        functionNum = int(input("Votre choix : "))
    function = functionList[functionNum-1]

    print("2-Proposez un mot contenue dans le dictionnaire (uniquement les lettres de l'alphabet sans accent)")
    prop = input("Proposition: ")
    while prop.lower() not in all_words[len(prop)]:
        print(f"{prop} n'est pas dans le dictionnaire")
        prop = input("Proposition: ")
    print("\n")

    iter = function(prop,all_words[len(prop)])
    print(f"votre mot, \"{prop}\" à été trouvé par {function.__name__} en {iter} itérations")


######################    MAIN   ######################

mainMenu()

######################    MAIN   ######################