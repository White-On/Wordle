import random
import os
from numpy import number

def parse(filename=os.path.dirname(os.path.abspath(__file__))+"\dico.txt")->list:
    """
    Permet de récupérer les mots du document dico.txt 
    """
    words = {}
    file = open(filename,'r')
    try :
        for l in file.readlines():
            # permet de passer outre les retours chariot
            line= l[0:-1]

            # si le nombre de lettre n'est pas encore répertoriée, on l'ajoute.
            if len(line) not in words.keys():
                words[len(line)] = []

            words[len(line)].append(line)
    finally:
        file.close()
    
    return words

def give_random_word(words,number_letter:int):
    """
    Donne un mot aléatoire parmis une liste de mots et un nombre de lettre souhaité.
    """
    return words[number_letter][random.randint(0,len(words[number_letter])-1)]


######################    Test des commandes    ######################

#print(parse())
#print(give_random_word(parse(),22),end="")



