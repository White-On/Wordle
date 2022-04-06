
import string

from Tools_Wordle import *

alph = string.ascii_lowercase


def compatible(word:str,words)->list:
    """
    Permet de vérifier la compatibilité d'un mot avec une liste de mots
    """
    res = []
    for w in words:
        # si le début du mot correspond au mot partiellement construit alors on l'ajoute
        if list(w[0:len(word)]) == word:
            res.append(w)

    return res 

def gener_compatible(profondeur:int,mot:list,mots_possible:list,lettre_dispo:list,liste_solution:list)->list:

    """
    Permet de générer une liste de mot compatible avec une liste de lettre 
    """
    #on arrête la recherche si on a atteint la profondeur maximale
    if profondeur == 0:
        return 
    for lettre in lettre_dispo:
        nv_mot = mot.copy()
        # on ajoute la lettre au mot
        nv_mot.append(lettre)
        # on vérifie si le mot est compatible avec les mots restants
        tmp = compatible(nv_mot,mots_possible)
        #print("tmp: ",tmp)
        #print("mot: ",nv_mot)

        #si il ne reste qu'un seul mot dispo plus besoin d'aller cherche plus loin
        if len(tmp) == 1:
            liste_solution.append(tmp[0])
            continue
        #si il n'y a plus de mot on arrête la recherche
        elif len(tmp) == 0:
            continue 
        
        # on continue la génération des mots à la profondeur suivante
        gener_compatible(profondeur-1,nv_mot,tmp,lettre_dispo,liste_solution)
    
    return liste_solution

def gener_single_compatible(profondeur:int,mot:list,mots_possible:list,lettre_dispo:list)->list:
    """
    Permet de générer un mot compatible avec une liste de lettre 
    """
    solution = None
    
    #on arrête la recherche si on a atteint la profondeur maximale
    if profondeur == 0:
        return 
    for lettre in lettre_dispo:
        nv_mot = mot.copy()
        # on ajoute la lettre au mot
        nv_mot.append(lettre)
        # on vérifie si le mot est compatible avec les mots restants
        tmp = compatible(nv_mot,mots_possible)
        #print("tmp: ",tmp)
        #print("mot: ",nv_mot)

        # si il ne reste qu'un seul mot dispo plus besoin d'aller cherche plus loin
        # on arrete la récursion si on a trouvé un mot

        if len(tmp) == 1:
            return tmp[0]
        #si il n'y a plus de mot on arrête la recherche
        elif len(tmp) == 0:
            continue 
        
        # on continue la génération des mots à la profondeur suivante
        solution = gener_single_compatible(profondeur-1,nv_mot,tmp,lettre_dispo)
        if solution != None:
            return solution
    
    return solution

def gener_single_compatible_forward(profondeur:int,mot:list,mots_possible:list,lettre_dispo:list,liste_indispo:list)->list:
    solution = None
    
    #on arrête la recherche si on a atteint la profondeur maximale
    if profondeur == 0:
        return 
    for lettre in lettre_dispo:
        nv_mot = mot.copy()
        # on ajoute la lettre au mot
        nv_mot.append(lettre)
        # on vérifie si le mot est compatible avec les mots restants
        tmp = compatible_lettre_interdites(nv_mot,mots_possible,liste_indispo)
        #print("tmp: ",tmp)
        #print("mot: ",nv_mot)

        # si il ne reste qu'un seul mot dispo plus besoin d'aller cherche plus loin
        # on arrete la récursion si on a trouvé un mot

        if len(tmp) == 1:
            return tmp[0]
        #si il n'y a plus de mot on arrête la recherche
        elif len(tmp) == 0:
            continue 
        
        # on continue la génération des mots à la profondeur suivante
        solution = gener_single_compatible_forward(profondeur-1,nv_mot,tmp,lettre_dispo,liste_indispo)
        if solution != None:
            return solution
    
    return solution

def compatible_lettre_interdites(word:str,words,prohibed_caract)->list:
    """
    Permet de vérifier la compatibilité d'un mot avec une liste de mots avec une contrainte de lettres interdites
    """
    
    res = []
    not_the_word = False
    for w in words:
        # si le début du mot correspond au mot partiellement construit 
        if list(w[0:len(word)]) == word:
            # on vérifie si ce mot n'est pas pas composée avec des lettres prohibés dans la suite
            for caract in prohibed_caract:
                if caract in list(w):
                    not_the_word = True
                    break
            if not_the_word:
                not_the_word = False
                continue
            else:
                res.append(w)

    return res 

def gener_compatible_forward(profondeur:int,mot:list,mots_possible:list,lettre_dispo:list,liste_solution:list,liste_indispo:list)->list:
    """
    Permet de générer une liste de mot compatible avec une liste de lettre 
    """
    #on arrête la recherche si on a atteint la profondeur maximale
    if profondeur == 0:
        return 
    for lettre in lettre_dispo:
        nv_mot = mot.copy()
        nv_mot.append(lettre)
        tmp = compatible_lettre_interdites(nv_mot,mots_possible,liste_indispo)
        #print("tmp: ",tmp)
        #print("mot: ",nv_mot)

        #si il ne reste qu'un seul mot dispo plus besoin d'aller cherche plus loin
        if len(tmp) == 1:
            liste_solution.append(tmp[0])
            continue
        #si il n'y a plus de mot on arrête la recherche
        elif len(tmp) == 0:
            continue 
        
        # 
        gener_compatible_forward(profondeur-1,nv_mot,tmp,lettre_dispo,liste_solution,liste_indispo)
    
    return liste_solution

def Solve_RAC(correct_word:str,all_words)->None:
    """
    Retour arrière chronologique
    """
    #dimmension du probleme
    n = len(correct_word)
    words_tried = []
    possible_words = all_words.copy()
    iteration = 0
    available_caracter = list(alph)
    

    # On cherche a avoir une valeur assigné aux lettres pour avoir une indications des
    # lettre qui semblent présentent dans le mot

    caract_weight = {}

    for c in alph:
        caract_weight[c] = 0

    while True:
        iteration += 1
        generated_words = gener_compatible(n,[],possible_words,available_caracter,[])

        # On dois prendre un solution en fonction des poids des lettres
        tmp = list(caract_weight.values())
        tmp.sort(reverse=True)
        tmp = tmp[0:int(n/2)]
        most_value_caract = [c for c in caract_weight if caract_weight[c] in tmp][0:int(n/2)]
        #print("tmp: ",tmp)
        #print("most_value_caract: ",most_value_caract)

        try:
            plausible_words = caract_in_words(generated_words,most_value_caract)
            sol = plausible_words[random.randint(0,len(plausible_words)-1)]
        except:
            #print("no solution found")
            sol = generated_words[random.randint(0,len(generated_words)-1)]

        #sol = generated_words[random.randint(0,len(generated_words)-1)]

        # On retire les mots testés pour ne pas les réutiliser dans la suite
        possible_words.remove(sol)
        
        check = check_correct2(correct_word,sol) 
        words_tried.append(sol)   

        # si le nombre de lettre bien placé est égale au nombre de lettre du mot chercher, on a donc trouvée notre mot
        if check[0] == n:
            print(f"Le mot cherchée était \"{correct_word}\", le mot retrouvée est \"{sol}\"")
            return iteration

        # si le nombre de lettre mal placée est égale au nombre de lettres total du mot testé, 
        # alors on sais que aucune des lettres composant le mot n'est dans le mot que l'on cherche
        elif  check[2] == n:
            for l in list(set(sol)):
                try:
                    # donc on retire les lettres du champs des lettres possible et on les ajoute aux lettre impossibles
                    available_caracter.remove(l)
                    
                except:
                    continue
        
        # si toutes les lettre sont au moins dans le mot que l'on cherche, notre liste de lettre 
        # possible est celle des lettres du mot que l'on viens de proposer
        elif check[2] == 0:
            available_caracter = list(set(sol))
        
        if check[0] + check[1] >= n/2:
            for c in sol:
                caract_weight[c] += check[0] + check[1] 
        else:
            for c in sol:
                caract_weight[c] -= check[2]


    # affichage des resultats mais servait pour les tests
    for c in alph:
        if caract_weight[c] == 0:
            caract_weight.pop(c)
        
        if c not in available_caracter and c in caract_weight.keys():
            caract_weight.pop(c)

    print(f"mots testé : {words_tried}.\nlettre dispo : {available_caracter}")
    print(f"mot correct : {correct_word}")
    #print(caract_weight)
    assert(correct_word not in words_tried)
    
def Solve_RACAC(correct_word:str,all_words)->None:
    """
    retour arrière chronologique avec arc cohérence
    """

    #dimmension du probleme
    n = len(correct_word)
    words_tried = []
    possible_words = all_words.copy()
    iteration = 0
    available_caracter = list(alph)
    unavailable_caracter = []

    # On cherche a avoir une valeur assigné aux lettres pour avoir une indications des
    # lettre qui semblent présentent dans le mot

    caract_weight = {}

    for c in alph:
        caract_weight[c] = 0

    while True:

        iteration += 1

        # on génère tout les mots possibles avec les lettres à notre disposition
        generated_words = gener_compatible_forward(n,[],possible_words,available_caracter,[],unavailable_caracter)

        
        # On dois prendre un solution en fonction des poids des lettres
        tmp = list(caract_weight.values())
        tmp.sort(reverse=True)
        tmp = tmp[0:int(n/2)]
        most_value_caract = [c for c in caract_weight if caract_weight[c] in tmp][0:int(n/2)]
        #print("tmp: ",tmp)
        #print("most_value_caract: ",most_value_caract)

        try:
            plausible_words = caract_in_words(generated_words,most_value_caract)
            sol = plausible_words[random.randint(0,len(plausible_words)-1)]
        except:
            #print("no solution found")
            sol = generated_words[random.randint(0,len(generated_words)-1)]

        #sol = generated_words[random.randint(0,len(generated_words)-1)]

        # On retire les mots testés pour ne pas les réutiliser dans la suite
        possible_words.remove(sol)
        
        # on teste le mot
        check = check_correct2(correct_word,sol) 
        words_tried.append(sol)   

        # si le nombre de lettre bien placé est égale au nombre de 
        # lettre du mot chercher, on a donc trouvée notre mot
        if check[0] == n:
            print(f"Le mot cherchée était \"{correct_word}\", le mot retrouvée est \"{sol}\"")
            return iteration

        # si le nombre de lettre mal placée est égale au nombre de lettres total du mot testé, 
        # alors on sais que aucune des lettres composant le mot n'est dans le mot que l'on cherche
        elif  check[2] == n:
            for l in list(set(sol)):
                try:
                    # donc on retire les lettres du champs des lettres possible et on les ajoute aux lettre impossibles
                    available_caracter.remove(l)
                    unavailable_caracter.append(l)
                    
                except:
                    continue
            #on retire les mots contenant les lettres impossible
            possible_words = remove_impossible(unavailable_caracter,possible_words)
        
        # si toutes les lettre sont au moins dans le mot que l'on cherche, notre liste de lettre 
        # possible est celle des lettres du mot que l'on viens de proposer
        
        elif check[2] == 0:
            available_caracter = list(set(sol))
            unavailable_caracter = [c for c in alph if c not in available_caracter] 
            possible_words = remove_impossible(unavailable_caracter,possible_words)
        
        if check[0] + check[1] >= n/2:
            for c in sol:
                caract_weight[c] += check[0] + check[1] 
        else:
            for c in sol:
                caract_weight[c] -= check[2]

    for c in alph:
        if caract_weight[c] == 0:
            caract_weight.pop(c)
        
        if c not in available_caracter and c in caract_weight.keys():
            caract_weight.pop(c)
        
    # affichage des resultats mais servait pour les tests
    print(f"mots testé : {words_tried}.\nlettre dispo : {available_caracter}")
    print(f"mot correct : {correct_word}")
    assert(correct_word not in words_tried)
    print(unavailable_caracter)
    
def SolveA1(correct_word:str,all_words)->None:
    """
    Fonction qui permet de résoudre le problème A1
    """
    n = len(correct_word)
    words_tried = []
    possible_words = all_words.copy()
    iteration = 0
    available_caracter = list(alph)

    while True:
        iteration += 1
        solution = gener_single_compatible(n,[],possible_words,available_caracter)

        check = check_correct2(correct_word,solution) 
        words_tried.append(solution)
        possible_words.remove(solution)

        # si le nombre de lettre bien placé est égale au nombre de lettre du mot chercher, on a donc trouvée notre mot
        if check == (n,0,0):
            print(f"Le mot cherchée était \"{correct_word}\", le mot retrouvée est \"{solution}\"")
            return iteration

        # si le nombre de lettre mal placée est égale au nombre de lettres total du mot testé, 
        # alors on sais que aucune des lettres composant le mot n'est dans le mot que l'on cherche
        elif  check == (0,0,n):
            for l in list(set(solution)):
                try:
                    # donc on retire les lettres du champs des lettres possible et on les ajoute aux lettre impossibles
                    available_caracter.remove(l)
                except:
                    continue
        
        # si toutes les lettre sont au moins dans le mot que l'on cherche, notre liste de lettre 
        # possible est celle des lettres du mot que l'on viens de proposer
        elif check[2] == 0:
            available_caracter = list(set(solution))
            
def SolveA2(correct_word:str,all_words)->None:
    """
    Fonction qui permet de résoudre le problème A1
    """
    n = len(correct_word)
    words_tried = []
    possible_words = all_words.copy()
    iteration = 0
    available_caracter = list(alph)
    unavailable_caracter = []

    while True:
        iteration += 1
        solution = gener_single_compatible_forward(n,[],possible_words,available_caracter,unavailable_caracter)

        check = check_correct2(correct_word,solution) 
        words_tried.append(solution)
        possible_words.remove(solution)

        # si le nombre de lettre bien placé est égale au nombre de lettre du mot chercher, on a donc trouvée notre mot
        if check == (n,0,0):
            print(f"Le mot cherchée était \"{correct_word}\", le mot retrouvée est \"{solution}\"")
            return iteration

        # si le nombre de lettre mal placée est égale au nombre de lettres total du mot testé, 
        # alors on sais que aucune des lettres composant le mot n'est dans le mot que l'on cherche
        elif  check == (0,0,n):
            for l in list(set(solution)):
                try:
                    # donc on retire les lettres du champs des lettres possible et on les ajoute aux lettre impossibles
                    available_caracter.remove(l)
                    unavailable_caracter.append(l)
                    
                except:
                    continue
            #on retire les mots contenant les lettres impossible
            possible_words = remove_impossible(unavailable_caracter,possible_words)
        
        # si toutes les lettre sont au moins dans le mot que l'on cherche, notre liste de lettre 
        # possible est celle des lettres du mot que l'on viens de proposer
        elif check[2] == 0:
            available_caracter = list(set(solution))
            unavailable_caracter = [c for c in alph if c not in available_caracter] 
            possible_words = remove_impossible(unavailable_caracter,possible_words)


##########   MAIN   ##########

all_words = parse()
#Nombre de lettre dans le mot que l'on cherche
N = 4

#print(check_correct("eeh","hhh"))
#print(check_correct2(['e','e','h'],['h','h','h']))

#SolveA1(give_random_word(all_words,N),all_words[N])

#SolveA2(give_random_word(all_words,N),all_words[N])

#Solve_RAC(give_random_word(all_words,N),all_words[N])

#Solve_RACAC(give_random_word(all_words,N),all_words[N])

#print(compatible(['a'],all_words[N]))
#res = gener_compatible(N,[],all_words[N],list(alph),[])
#print(res)


#print(compatible_lettre_interdites(['z'],all_words[5],['a','x','y']))
#print(compatible(['z'],all_words[5]))

"""
test = give_random_word(all_words,N)

tp1 = time.time()
Solve_RAC(test,all_words[N])
tpRAC = time.time() - tp1

tp1 = time.time()
Solve_RACAC(test,all_words[N])
tpRACAC = time.time() - tp1

print(f"temps RAC: {tpRAC} sec, temps RACAC: {tpRACAC} sec")"""

#print(caract_in_words(["anubis","ane","nubian"],["a","n","u"]))

#Compare(SolveA1,SolveA2,range(4,9),20)

#plot_result(range(4,9),all_words,SolveA2)

#plot_result_intervalle(range(4,9),all_words,Solve_RACAC,20)

Compare4(Solve_RAC,Solve_RACAC,SolveA1,SolveA2,range(7,9),2)