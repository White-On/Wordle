from Parse_Wordle import *
import string

alph = string.ascii_lowercase

def caract_in_words(words,list_caract):
    """
    Find the word(s) that can be build with a list of caracters
    """
    res = []
    for word in words:
        if set(word) == set(list_caract):
            res.append(word)
    return res

def distance_edition(word1, words2):
    """
    calculate the evaluation of the distance edition between two words
    """
    dist = { (-1,-1): 0 }
    for i,c in enumerate(word1) :
        dist[i,-1] = dist[i-1,-1] + 1
        dist[-1,i] = dist[-1,i-1] + 1
        for j,d in enumerate(words2) :
            opt = [ ]
            if (i-1,j) in dist : 
                x = dist[i-1,j] + 1
                opt.append(x)
            if (i,j-1) in dist : 
                x = dist[i,j-1] + 1
                opt.append(x)
            if (i-1,j-1) in dist :
                x = dist[i-1,j-1] + (1 if c != d else 0)
                opt.append(x)
            dist[i,j] = min(opt)
    return dist[len(word1)-1,len(words2)-1]

def closest_word(word:str,list_word)->str:
    """
    Find the closest word from a list of words
    """
    score = []
    for w in list_word:
        score.append(distance_edition(word,w))
    return list_word[score.index(min(score))]

def check_correct(correct_word:str,proposition:str):
    """
    On part du principe que les mots proposée sont de même taille que le mot solution
    """
    #taille du mot
    n = len(correct_word)
    #liste contenant les connaisance de résultats
    #chacune de ses cases s'apparente à une de nos lettre prends une valeurs de 0 à 2 
    #0 si la lettre n'est pas de le mot,1 si elle est mal positionée, 2 si elle est bien positionée
    res = [0] * n

    for i in range(n):
        if correct_word[i] == proposition[i]:
            res[i] = 2

    if res.count(2) == n:
        return (res.count(2),res.count(1),res.count(0))

    unique = list(set(correct_word))

    for i in range(n):
        if res[i] == 2:
            continue
        elif proposition[i] in unique:
            res[i] = 1

    return (res.count(2),res.count(1),res.count(0))

def check_correct2(correct_word:str,proposition:str):
    """
    On part du principe que les mots proposée sont de même taille que le mot solution.

    Ici la différence c'est que deux lettres identiques mais leur quantitée est trop importante
    donc on dois considéré que l'une d'elle n'est ni bien placé ni présente.
    """
    #taille du mot
    n = len(correct_word)
    tmp1,tmp2 = [],[]
    for i in range(n):
        tmp1.append(proposition[i])
        tmp2.append(correct_word[i])
    proposition,correct_word = tmp1,tmp2

    res = [0,0,0]
    copy_correct_word = correct_word

    for i in range(n):
        if correct_word[i] == proposition[i]:
            res[0] += 1
            proposition[i] = "/"
            copy_correct_word[i] = "&"

    if res[0] == n:
        return tuple(res)
    
    for i in range(n):
        for j in range(n):
            if proposition[i] == copy_correct_word[j]:
                proposition[i] = "/"
                copy_correct_word[j] = "&"
                res [1] += 1
    for l in proposition:
        if l != "/":
            res[2] += 1

    return tuple(res)

def compatible(word:str,words)->bool:
    """
    Permet de vérifier la compatibilité d'un mot avec une liste de mots
    """
    n = len(word)
    res = []
    for w in words:
        if list(w[0:n]) == word:
            res.append(w)

    return res 

def gener_compatible(profondeur:int,mot:list,mots_possible:list,lettre_dispo:list,liste_solution:list):
    """
    Permet de générer une liste de mot compatible avec une liste de lettre 
    """
    #on arrête la recherche si on a atteint la profondeur maximale
    if profondeur == 0:
        return 
    for lettre in lettre_dispo:
        nv_mot = mot.copy()
        nv_mot.append(lettre)
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
        
        gener = gener_compatible(profondeur-1,nv_mot,tmp,lettre_dispo,liste_solution)
    
    return liste_solution

def Solve_RAC(word:str,all_words):
    #dimmension du probleme
    n = len(word)
    words_tried = []
    possible_words = all_words.copy()
    itermax = 200
    available_caracter = list(alph)

    for _ in range(itermax):
        
        generated_words = gener_compatible(n,[],possible_words,available_caracter,[])

        sol = generated_words[random.randint(0,len(generated_words)-1)]
        
        check = check_correct2(word,sol) 
        words_tried.append(sol)   

        if  check == (0,0,n):
            for l in list(set(sol)):
                try:
                    available_caracter.remove(l)
                except:
                    continue

        elif check == (n,0,0):
            print(f"Le mot cherchée était \"{word}\", le mot retrouvée est \"{sol}\"")
            return 

    print(f"mots testé : {words_tried}, lettre dispo : {available_caracter}")
    print(f"mot correct : {word}")
    assert(word not in words_tried)
    

def Solve_CSP_A2(gest_word:str):
    pass

def Solve_Genetic(gest_word:str,all_words):
    MAX_SIZE = 100
    MAX_GEN = 100
    E = []
    Population = []

#print(check_correct("eeh","hhh"))
#print(check_correct2(['e','e','h'],['h','h','h']))

all_words = parse()
#Nombre de lettre dans le mot que l'on cherche
N = 8

Solve_RAC(give_random_word(all_words,N),all_words[N])

#print(compatible(['a'],all_words[N]))
#res = gener_compatible(N,[],all_words[N],list(alph),[])
#print(res)
