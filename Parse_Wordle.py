import random
import os
from numpy import number

def parse(filename=os.path.dirname(os.path.abspath(__file__))+"\dico.txt"):
    words = {}
    file = open(filename,'r')
    try :
        for line in file.readlines():

            if len(line) not in words.keys():
                words[len(line)] = []

            words[len(line)].append(line)
    finally:
        file.close()
    
    return words

def give_random_word(words,number_letter:int):
    return words[number_letter][random.randint(0,len(words[number_letter])-1)]

#Test des commandes


#print(parse())
print(give_random_word(parse(),22),end="")



