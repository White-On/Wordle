from Parse_Wordle import *
import string
import time

alph = string.ascii_lowercase

def caract_in_words(words,list_caract):
    """
    Trouve le ou les mots pouvant etre construit à partir d'une liste de lettres
    """
    res = []
    test = True
    for word in words:
        for c in list_caract:
            if c not in set(word):
                test = False
                break
        if test:
            res.append(word)
        test = True
    return res

def distance_edition(word1, words2):
    """
    Calcul la distance d'édition entre deux mots
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
    Trouve le mot le plus proche parmis une liste de mot
    """
    score = []
    for w in list_word:
        score.append(distance_edition(word,w))
    return list_word[score.index(min(score))]

def check_correct(correct_word:str,proposition:str):
    """
    Ancienne version archive, elle ne prenais pas en compte toutes les contraines de l'enoncée
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

    """tmp1,tmp2 = [],[]
    for i in range(n):
        tmp1.append(proposition[i])
        tmp2.append(correct_word[i])
    proposition,correct_word = tmp1,tmp2"""

    proposition,correct_word = list(proposition),list(correct_word)

    res = [0,0,0]
    copy_correct_word = correct_word

    # on parcours le mot pour faire une première vérification sur les lettres bien placés
    for i in range(n):
        if correct_word[i] == proposition[i]:
            res[0] += 1
            # les lettres sont ensuite remplacée par des caractères impossible a trouvée dans
            # les mots pour ne pas les traitée de nouveau mais concervé l'indexion actuelle
            proposition[i] = "/"
            copy_correct_word[i] = "&"

    # on vérifie si on à pas déja trouvée de mot que l'on cherchais 
    if res[0] == n:
        return tuple(res)
    
    #on cherche maintenant les lettres mal placé dans le mots
    for i in range(n):
        for j in range(n):
            if proposition[i] == copy_correct_word[j]:
                proposition[i] = "/"
                copy_correct_word[j] = "&"
                res [1] += 1
    
    # le reste sont des lettres qui ne sont pas dans le mot
    for l in proposition:
        if l != "/":
            res[2] += 1

    # format de retour (bonne lettre,lettre mal placé,mauvaise lettre)
    return tuple(res)

def compatible(word:str,words)->bool:
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

def compatible_lettre_interdites(word:str,words,prohibed_caract)->bool:
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

def gener_compatible_forward(profondeur:int,mot:list,mots_possible:list,lettre_dispo:list,liste_solution:list,liste_indispo:list):
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
        
        gener = gener_compatible(profondeur-1,nv_mot,tmp,lettre_dispo,liste_solution)
    
    return liste_solution

def Solve_RAC(word:str,all_words):
    """
    Retour arrière chronologique
    """
    #dimmension du probleme
    n = len(word)
    words_tried = []
    possible_words = all_words.copy()
    itermax = 20
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
            print("no solution found")
            sol = generated_words[random.randint(0,len(generated_words)-1)]

        #sol = generated_words[random.randint(0,len(generated_words)-1)]

        # On retire les mots testés pour ne pas les réutiliser dans la suite
        possible_words.remove(sol)
        
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
    #print(caract_weight)
    assert(word not in words_tried)
    
def Solve_RACAC(word:str,all_words):
    """
    retour arrière chronologique avec arc cohérence
    """

    #dimmension du probleme
    n = len(word)
    words_tried = []
    possible_words = all_words.copy()
    itermax = 20
    available_caracter = list(alph)
    unavailable_caracter = []

    for _ in range(itermax):
        
        # on génère tout les mots possibles avec les lettres à notre disposition
        generated_words = gener_compatible_forward(n,[],possible_words,available_caracter,[],unavailable_caracter)

        # on pioche une solution possible parmis les mots générés
        sol = generated_words[random.randint(0,len(generated_words)-1)]
        
        # on teste le mot
        check = check_correct2(word,sol) 
        words_tried.append(sol)   

        # si le nombre de lettre mal placée est égale au nombre de lettres total du mot testé, *
        # alors on sais que aucune des lettres composant le mot n'est dans le mot que l'on cherche
        if  check == (0,0,n):
            for l in list(set(sol)):
                try:
                    # donc on retire les lettres du champs des lettres possible et on les ajoute aux lettre impossibles
                    available_caracter.remove(l)
                    unavailable_caracter.append(l)
                except:
                    continue

        # avec la même logique, si le nombre de lettre bien placé est égale au nombre de lettre du mot chercher, on a donc trouvée notre mot
        elif check == (n,0,0):
            print(f"Le mot cherchée était \"{word}\", le mot retrouvée est \"{sol}\"")
            return 
        

    print(f"mots testé : {words_tried}.\nlettre dispo : {available_caracter}")
    print(f"mot correct : {word}")
    assert(word not in words_tried)
    print(unavailable_caracter)
    
def Solve_Genetic(gest_word:str,all_words):
    MAX_SIZE = 100
    MAX_GEN = 100
    E = []
    Population = []


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


test = give_random_word(all_words,N)

tp1 = time.time()
Solve_RAC(test,all_words[N])
tpRAC = time.time() - tp1

tp1 = time.time()
Solve_RACAC(test,all_words[N])
tpRACAC = time.time() - tp1

print(f"temps RAC: {tpRAC} sec, temps RACAC: {tpRACAC} sec")

#print(caract_in_words(["anubis","ane","nubian"],["a","n","u"]))