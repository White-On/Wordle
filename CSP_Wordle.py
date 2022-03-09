from Parse_Wordle import *
from constraint import *
import string

alph = string.ascii_uppercase


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
            if proposition[i] == copy_correct_word[i]:
                proposition[i] = "/"
                copy_correct_word[j] = "&"
                res [1] += 1
    for l in proposition:
        if l != "/":
            res[2] += 1

    return tuple(res)

def Solve_RAC(word:str):
    #dimmension du probleme
    n = len(word)
    RAC = Problem()
    RAC.addVariables(range(n),alph)
    # Recuperation de l’ensemble des solutions possibles
    s = RAC.getSolutions()
    print("Nombre de solutions = ", len(s))


def Solve_CSP_A2(gest_word:str):
    pass

print(check_correct("eeh","hhh"))
print(check_correct2("eeh","hhh"))

Solve_RAC(give_random_word(parse(),4))