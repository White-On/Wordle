from Parse_Wordle import *
import string
import time
import matplotlib.pyplot as plt
from Tools_Wordle import *

alph = string.ascii_lowercase



def compatible(word:str,words)->list:
    """
    Permet de vérifier la compatibilité d'un mot avec une liste de mots
    """
    n = len(word)
    res = []
    for w in words:
        # si le début du mot correspond au mot partiellement construit alors on l'ajoute
        if list(w[0:n]) == word:
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

def compatible_lettre_interdites(word:str,words,prohibed_caract)->list:
    """
    Permet de vérifier la compatibilité d'un mot avec une liste de mots avec une contrainte de lettres interdites
    """
    n = len(word)
    res = []
    not_the_word = False
    for w in words:
        # si le début du mot correspond au mot partiellement construit 
        if list(w[0:n]) == word:
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
        gener_compatible(profondeur-1,nv_mot,tmp,lettre_dispo,liste_solution)
    
    return liste_solution

def Solve_RAC(correct_word:str,all_words)->None:
    """
    Retour arrière chronologique
    """
    #dimmension du probleme
    n = len(correct_word)
    words_tried = []
    possible_words = all_words.copy()
    itermax = 2000
    available_caracter = list(alph)

    # On cherche a avoir une valeur assigné aux lettres pour avoir une indications des
    # lettre qui semblent présentent dans le mot

    caract_weight = {}

    for c in alph:
        caract_weight[c] = 0

    for _ in range(itermax):
        
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
        if check == (n,0,0):
            print(f"Le mot cherchée était \"{correct_word}\", le mot retrouvée est \"{sol}\"")
            return 

        # si le nombre de lettre mal placée est égale au nombre de lettres total du mot testé, 
        # alors on sais que aucune des lettres composant le mot n'est dans le mot que l'on cherche
        elif  check == (0,0,n):
            for l in list(set(sol)):
                try:
                    # donc on retire les lettres du champs des lettres possible et on les ajoute aux lettre impossibles
                    available_caracter.remove(l)
                except:
                    continue
        
        # si toutes les lettre sont au moins dans le mot que l'on cherche, notre liste de lettre 
        # possible est celle des lettres du mot que l'on viens de proposer
        elif check == (_,_,0):
            available_caracter = list(set(sol))
        
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

    print(f"mots testé : {words_tried}.\nlettre dispo : {available_caracter}")
    print(f"mot correct : {correct_word}")
    #print(caract_weight)
    assert(correct_word not in words_tried)
    
def Solve_RACAC(word:str,all_words)->None:
    """
    retour arrière chronologique avec arc cohérence
    """

    #dimmension du probleme
    n = len(word)
    words_tried = []
    possible_words = all_words.copy()
    itermax = 2000
    available_caracter = list(alph)
    unavailable_caracter = []

    # On cherche a avoir une valeur assigné aux lettres pour avoir une indications des
    # lettre qui semblent présentent dans le mot

    caract_weight = {}

    for c in alph:
        caract_weight[c] = 0

    for _ in range(itermax):
        
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
        check = check_correct2(word,sol) 
        words_tried.append(sol)   

        # si le nombre de lettre bien placé est égale au nombre de 
        # lettre du mot chercher, on a donc trouvée notre mot
        if check == (n,0,0):
            print(f"Le mot cherchée était \"{word}\", le mot retrouvée est \"{sol}\"")
            return 

        # si le nombre de lettre mal placée est égale au nombre de lettres total du mot testé, 
        # alors on sais que aucune des lettres composant le mot n'est dans le mot que l'on cherche
        elif  check == (0,0,n):
            for l in list(set(sol)):
                try:
                    # donc on retire les lettres du champs des lettres possible et on les ajoute aux lettre impossibles
                    available_caracter.remove(l)
                    unavailable_caracter.append(l)
                except:
                    continue
        
        # si toutes les lettre sont au moins dans le mot que l'on cherche, notre liste de lettre 
        # possible est celle des lettres du mot que l'on viens de proposer
        
        elif check == (_,_,0):
            available_caracter = list(set(sol))
            unavailable_caracter = [c for c in alph if c not in available_caracter] 
        
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
        

    print(f"mots testé : {words_tried}.\nlettre dispo : {available_caracter}")
    print(f"mot correct : {word}")
    assert(word not in words_tried)
    print(unavailable_caracter)

def CompareTime(function1,function2,n_caracter,iteration)->None:
    """
    Compare le temps d'execution de deux fonctions pour une certain nombre d'itération
    """
    function1_time = []
    function2_time = []

    all_words = parse()

    if type(n_caracter).__name__ == "range":
        function1_time = {n:[0] for n in n_caracter}
        function2_time = {n:[0] for n in n_caracter}
        function1_mean_time = []
        function2_mean_time = []

        for _ in range(iteration):
            for n in n_caracter:
                word = give_random_word(all_words,n)
                start = time.time()
                function1(word,all_words[n])
                function1_time[n].append(time.time()-start)
                start = time.time()
                function2(word,all_words[n])
                function2_time[n].append(time.time()-start)
        
        for n in n_caracter:
            function1_mean_time.append(sum(function1_time[n])/iteration)
            function2_mean_time.append(sum(function2_time[n])/iteration)

        
        plt.plot(n_caracter,function1_mean_time,label=function1.__name__)
        plt.plot(n_caracter,function2_mean_time,label=function2.__name__)
        plt.title(f"Comparaison du temps d'execution de {function1.__name__} et {function2.__name__}")
        plt.legend()
        plt.show()

    else:
        for _ in range(iteration):
            word = give_random_word(all_words,n_caracter)
            start = time.time()
            function1(word,all_words[n_caracter])
            end = time.time()
            function1_time.append(end-start)

            start = time.time()
            function2(word,all_words[n_caracter])
            end = time.time()
            function2_time.append(end-start)
        
        print(f"{function1.__name__} : {sum(function1_time)/len(function1_time)}")
        print(f"{function2.__name__} : {sum(function2_time)/len(function2_time)}")
    


    
##########   MAIN   ##########


#print(check_correct("eeh","hhh"))
#print(check_correct2(['e','e','h'],['h','h','h']))

all_words = parse()
#Nombre de lettre dans le mot que l'on cherche
N = 4

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

CompareTime(Solve_RAC,Solve_RACAC,range(4,9),1)

# je dois maintenant faire des retours plus concret pour les algos 
# pour pouvoir affichier leurs résultats plus clairement et 
# egalement ajouter le systeme de timeout

