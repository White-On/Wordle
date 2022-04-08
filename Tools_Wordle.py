from Parse_Wordle import *
import time
import matplotlib.pyplot as plt
import numpy as np

def caract_in_words(words,list_caract):
    """
    Trouve le ou les mots pouvant etre construit à partir d'une liste de lettres
    """
    res = []
    test = True
    for word in words:
        for c in list_caract:
            # si la lettre n'est pas dans le mot, on ne peux donc pas le construire à partir de notre liste de lettre
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

def distance_edition_recursive(mot1, mot2):
    if len(mot1) == 0 : return len(mot2)
    elif len(mot2) == 0 : return len(mot1)
    else :
        return min ( distance_edition_recursive(mot1[:-1], mot2) + 1,
                     distance_edition_recursive(mot1, mot2[:-1]) + 1,
                     distance_edition_recursive(mot1[:-1], mot2[:-1]) + \
                          (1 if mot1[-1] != mot2[-1] else 0))

def closest_word(word:str,list_word)->str:
    """
    Trouve le mot le plus proche parmis une liste de mot
    """
    score = []
    for w in list_word:
        # on calcule la distance d'édition entre les deux mots
        score.append(distance_edition(word,w))
    # on retourne le mot le plus proche
    return list_word[score.index(min(score))]

def closest_word_recursive(word:str,list_word)->str:
    """
    Trouve le mot le plus proche parmis une liste de mot
    """
    score = []
    for w in list_word:
        # on calcule la distance d'édition entre les deux mots
        score.append(distance_edition_recursive(word,w))
    # on retourne le mot le plus proche
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

def remove_impossible(unavailable_caracters,list_words):
    """
    Supprime les mots impossible d'une liste pour une litste de lettre interdites
    """
    res = list_words.copy()
    for c in unavailable_caracters:
        for w in res:
            if c in set(w):
                res.remove(w)
    return res

def plot_result(spectre:range,words:list,function,maxiter=False)->None:
    """
    Permet de tracer les resultats de l'algorithme génétique
    """
    list_time = []
    iterations = []

    for n in spectre:
        start = time.time()
        iterations.append(function(give_random_word(words,n),words[n]))
        end = time.time()
        list_time.append(end-start)
        
        

    
    # on tracer le graphique de la vitesse de résolution de l'algorithme génétique
    plt.plot(spectre,list_time,label="temps")
    plt.xlabel("taille du mot en nombre de lettre")
    plt.ylabel("temps d'execution en sec")
    plt.title(f"Vitesse de résolution de {function.__name__}")
    plt.legend()
    plt.show()

    if maxiter:
        for n in spectre:
            plt.scatter(n,len(words[n]),label=f"{n} lettres")
    
    # on tracer le graphique de la vitesse de résolution de l'algorithme génétique
    plt.plot(spectre,iterations,label="itération")
    plt.xlabel("taille du mot en nombre de lettre")
    plt.ylabel("itérations")
    plt.title(f"Nombre d'itération de {function.__name__}")
    plt.legend()
    plt.show()

def Compare(function1,function2,n_caracter,instance,maxiter=False)->None:



    """
    Compare le temps d'execution de deux fonctions pour une certain nombre d'itération
    """
    function1_time = []
    function2_time = []

    function1_iter = []
    function2_iter = []

    all_words = parse()

    if type(n_caracter).__name__ == "range":
        function1_time = {n:[0] for n in n_caracter}
        function2_time = {n:[0] for n in n_caracter}
        function1_mean_time = []
        function2_mean_time = []

        function1_iter = {n:[0] for n in n_caracter}
        function2_iter = {n:[0] for n in n_caracter}
        function1_mean_iter = []
        function2_mean_iter = []

        for _ in range(instance):
            for n in n_caracter:
                word = give_random_word(all_words,n)
                start = time.time()
                function1_iter[n].append(function1(word,all_words[n]))
                function1_time[n].append(time.time()-start)
                start = time.time()
                function2_iter[n].append(function2(word,all_words[n]))
                function2_time[n].append(time.time()-start)
        
        for n in n_caracter:
            function1_mean_time.append(sum(function1_time[n])/instance)
            function2_mean_time.append(sum(function2_time[n])/instance)
            function1_mean_iter.append(sum(function1_iter[n])/instance)
            function2_mean_iter.append(sum(function2_iter[n])/instance)

        
        plt.plot(n_caracter,function1_mean_time,label=function1.__name__)
        plt.plot(n_caracter,function2_mean_time,label=function2.__name__)
        plt.title(f"Comparaison du temps d'execution de {function1.__name__} et {function2.__name__}")
        plt.xlabel("taille du mot en nombre de lettre")
        plt.ylabel("temps d'execution en sec")
        plt.legend()
        plt.show()

        if maxiter:
            for n in n_caracter:
                plt.scatter(n,len(all_words[n]),label=f"{n} lettres")

        plt.plot(n_caracter,function1_mean_iter,label=function1.__name__)
        plt.plot(n_caracter,function2_mean_iter,label=function2.__name__)
        plt.title(f"Comparaison du nombre d'itération de {function1.__name__} et {function2.__name__}")
        plt.xlabel("taille du mot en nombre de lettre")
        plt.ylabel("itérations")
        plt.legend()
        plt.show()

    else:
        for _ in range(instance):
            word = give_random_word(all_words,n_caracter)
            start = time.time()
            function1_iter.append(function1(word,all_words[n_caracter]))
            end = time.time()
            function1_time.append(end-start)

            start = time.time()
            function2_iter.append(function2(word,all_words[n_caracter]))
            end = time.time()
            function2_time.append(end-start)
        
        print(f"{function1.__name__} : {sum(function1_time)/len(function1_time)}")
        print(f"{function2.__name__} : {sum(function2_time)/len(function2_time)}")
        print(f"{function1.__name__} : {sum(function1_iter)/len(function1_iter)}")
        print(f"{function2.__name__} : {sum(function2_iter)/len(function2_iter)}")

def plot_result_intervalle(spectre:range,all_words:list,function,intervalle=None,maxiter=False):
    function1_time = {n:[0] for n in spectre}
    function1_mean_time = []

    function1_iter = {n:[0] for n in spectre}
    function1_mean_iter = []

    for _ in range(intervalle):
        for n in spectre:
            word = give_random_word(all_words,n)
            start = time.time()
            function1_iter[n].append(function(word,all_words[n]))
            function1_time[n].append(time.time()-start)

    
    for n in spectre:
        function1_mean_time.append(sum(function1_time[n])/intervalle)
        function1_mean_iter.append(sum(function1_iter[n])/intervalle)

    plt.plot(spectre,function1_mean_time,label=function.__name__)
    plt.title(f"Temps d'execution de {function.__name__}")
    plt.xlabel("taille du mot en nombre de lettre")
    plt.ylabel("temps d'execution en sec")
    plt.legend()
    plt.show()

    if maxiter:
        for n in spectre:
            plt.scatter(n,len(all_words[n]),label=f"{n} lettres")

    plt.plot(spectre,function1_mean_iter,label=function.__name__)
    plt.title(f"Nombre d'itération de {function.__name__} ")
    plt.xlabel("taille du mot en nombre de lettre")
    plt.ylabel("itérations")
    plt.legend()
    plt.show()

def Compare4(function1,function2,function3,function4,n_caracter,instance,maxiter=False)->None:

    """
    Compare le temps d'execution de quatres fonctions pour une certain nombre d'itération
    """
    function1_time = []
    function2_time = []
    function3_time = []
    function4_time = []

    function1_iter = []
    function2_iter = []
    function3_iter = []
    function4_iter = []

    all_words = parse()

    function1_time = {n:[0] for n in n_caracter}
    function2_time = {n:[0] for n in n_caracter}
    function3_time = {n:[0] for n in n_caracter}
    function4_time = {n:[0] for n in n_caracter}
    function1_mean_time = []
    function2_mean_time = []
    function3_mean_time = []
    function4_mean_time = []

    function1_iter = {n:[0] for n in n_caracter}
    function2_iter = {n:[0] for n in n_caracter}
    function3_iter = {n:[0] for n in n_caracter}
    function4_iter = {n:[0] for n in n_caracter}
    function1_mean_iter = []
    function2_mean_iter = []
    function3_mean_iter = []
    function4_mean_iter = []

    for _ in range(instance):
        for n in n_caracter:
            word = give_random_word(all_words,n)

            start = time.time()
            function1_iter[n].append(function1(word,all_words[n]))
            function1_time[n].append(time.time()-start)
            start = time.time()
            function2_iter[n].append(function2(word,all_words[n]))
            function2_time[n].append(time.time()-start)
            start = time.time()
            function3_iter[n].append(function3(word,all_words[n]))
            function3_time[n].append(time.time()-start)
            start = time.time()
            function4_iter[n].append(function4(word,all_words[n]))
            function4_time[n].append(time.time()-start)
    
    for n in n_caracter:
        function1_mean_time.append(sum(function1_time[n])/instance)
        function1_mean_iter.append(sum(function1_iter[n])/instance)
        function2_mean_time.append(sum(function2_time[n])/instance)
        function2_mean_iter.append(sum(function2_iter[n])/instance)
        function3_mean_time.append(sum(function3_time[n])/instance)
        function3_mean_iter.append(sum(function3_iter[n])/instance)
        function4_mean_time.append(sum(function4_time[n])/instance)
        function4_mean_iter.append(sum(function4_iter[n])/instance)

    
    plt.plot(n_caracter,function1_mean_time,label=function1.__name__)
    plt.plot(n_caracter,function2_mean_time,label=function2.__name__)
    plt.plot(n_caracter,function3_mean_time,label=function3.__name__)
    plt.plot(n_caracter,function4_mean_time,label=function4.__name__)
    plt.title(f"Temps d'execution de {function1.__name__} , {function2.__name__} , {function3.__name__} , {function4.__name__}")
    plt.xlabel("taille du mot en nombre de lettre")
    plt.ylabel("temps d'execution en sec")
    plt.legend()
    plt.show()

    if maxiter:
        for n in n_caracter:
            plt.scatter(n,len(all_words[n]),label=f"{n} lettres")

    plt.plot(n_caracter,function1_mean_iter,label=function1.__name__)
    plt.plot(n_caracter,function2_mean_iter,label=function2.__name__)
    plt.plot(n_caracter,function3_mean_iter,label=function3.__name__)
    plt.plot(n_caracter,function4_mean_iter,label=function4.__name__)
    plt.title(f"Comparaison du nombre d'itération de {function1.__name__} , {function2.__name__} , {function3.__name__} , {function4.__name__}")
    plt.xlabel("taille du mot en nombre de lettre")
    plt.ylabel("itérations")
    plt.legend()
    plt.show()

    # plus belle affichage
    fit_25 = [];fit_75 = [];median_max = []
    for n in n_caracter:
        fit_25.append(np.quantile(function1_iter[n],25))
        fit_75.append(np.quantile(function1_iter[n],75))
        median_max.append(np.mean(function1_iter[n]))
        
    plt.fill_between(n_caracter, fit_25, fit_75, alpha=0.25, linewidth=0)
    plt.plot(n_caracter,median_max,label="{}".format(function1.__name__))

    fit_25 = [];fit_75 = [];median_max = []
    for n in n_caracter:
        fit_25.append(np.quantile(function2_iter[n],25))
        fit_75.append(np.quantile(function2_iter[n],75))
        median_max.append(np.mean(function2_iter[n]))
        
    plt.fill_between(n_caracter, fit_25, fit_75, alpha=0.25, linewidth=0)
    plt.plot(n_caracter,median_max,label="{}".format(function2.__name__))

    fit_25 = [];fit_75 = [];median_max = []
    for n in n_caracter:
        fit_25.append(np.quantile(function3_iter[n],25))
        fit_75.append(np.quantile(function3_iter[n],75))
        median_max.append(np.mean(function3_iter[n]))
        
    plt.fill_between(n_caracter, fit_25, fit_75, alpha=0.25, linewidth=0)
    plt.plot(n_caracter,median_max,label="{}".format(function3.__name__))

    fit_25 = [];fit_75 = [];median_max = []
    for n in n_caracter:
        fit_25.append(np.quantile(function4_iter[n],25))
        fit_75.append(np.quantile(function4_iter[n],75))
        median_max.append(np.mean(function4_iter[n]))
        
    plt.fill_between(n_caracter, fit_25, fit_75, alpha=0.25, linewidth=0)
    plt.plot(n_caracter,median_max,label="{}".format(function4.__name__))

    plt.xlabel("taille du mot en nombre de lettre")
    plt.ylabel("itérations")
    plt.legend()
    plt.show()




def check_correct3(correct_word:str,proposition:str):
    #taille du mot
    n = len(correct_word)
    res = [0,0,0]
    word = list(correct_word)
    print(proposition)
    proposition = list(proposition)

    for i in range(n):
        if proposition[i] in list(set(word)):
            if correct_word[i] == proposition[i]:
                res[0] += 1
            else:
                res[1] += 1
            word.remove(proposition[i])
        else:
            res[2] += 1
    
    return tuple(res)

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]
