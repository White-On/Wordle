
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