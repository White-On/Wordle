from Parse_Wordle import *
import string
import time
import matplotlib.pyplot as plt
from Tools_Wordle import *

alph = string.ascii_lowercase

class Genetic_Word:
    MAX_SIZE = 250
    MAX_GEN = 10

    # ensemble des mots compatibles avec les essais précedent
    E = []

    TAILLE_POP = 100
    population = []

    def __init__(self,word:str) -> None:
        self.word = word
        self.fitness = self.evalutation(self.word)
        Genetic_Word.population.append(self)
        Genetic_Word.population.sort(reverse=True,key=lambda x:x.fitness)
    
    def __eq__(self, __o: object) -> bool:
        return self.word == __o.word
    
    def __repr__(self) -> str:
        return f"{self.word} : {self.fitness}"

    def evalutation(self,word:str) -> float:
        """
        Fonction qui calcule le score d'un mot
        """
        return len(word)
    
    def mutation(self) -> None:
        """
        Fonction qui effectue une mutation aleatoire
        """
        r =random.random()
        if r < 0.33:
            self.randomCaracterChange()
        elif r > 0.66:
            self.exchangeCaracter()
        else:
            self.crossover(random.choice(self.population))
        
        # On dois maintenant faire en sorte que le nouveau mot soit 
        # compatible avec les mots possibles et qu'il n'y ait 
        # pas de doublon dans la population.

        
        if self.word in Genetic_Word.Authaurised_Words:
            if self.word not in Genetic_Word.E:
                Genetic_Word.E.append(self.word)
        else:
            self.word = closest_word(self.word,Genetic_Word.Authaurised_Words)
            if self.word not in Genetic_Word.E:
                Genetic_Word.E.append(self.word)
        
        self.fitness = self.evalutation(self.word)

    def randomCaracterChange(self) -> None:
        """
        Fonction qui change un caractere aleatoire
        """
        i = random.randint(0,len(self.word)-1)
        self.word = self.word[:i] + random.choice(Genetic_Word.Authaurised_Caracters) + self.word[i+1:]
    
    def exchangeCaracter(self) -> None:
        """
        Fonction qui effectue un echange de caractere aleatoire
        """
        i = random.randint(0,len(self.word)-2)
        j = random.randint(i,len(self.word)-1)
        self.word = self.word[:i] + self.word[j] + self.word[i+1:j] + self.word[i] + self.word[j+1:]
    
    def crossover(self,other) -> None:
        """
        Fonction qui effectue un crossover entre deux mots
        """
        if len(self.word) != len(other.word):
            raise Exception("Les deux mots doivent avoir la meme taille")
        else:
            i = random.randint(0,len(self.word)-1)
            self.word = self.word[:i] + other.word[i:]
    
    @classmethod
    def breed(cls,parent1, parent2) -> None:
        """
        Permet de faire croiser la population
        """
        cls(parent1.word).crossover(parent2)

    @classmethod
    def resetPopulation(cls) -> None:
        """
        Réinitialise la population
        """
        cls.population = []
    
    @classmethod
    def getPopulation(cls) -> list:
        """
        Retourne la population
        """
        return cls.population

    @classmethod
    def get_best_word(cls) -> str:
        """
        Renvoie le meilleur individu de la population
        """
        Genetic_Word.population.sort(reverse=True,key=lambda x:x.fitness)
        return cls.population[0]
    
    @classmethod
    def get_worst_word(cls) -> str:
        """
        Renvoie le pire individu de la population
        """
        Genetic_Word.population.sort(reverse=True,key=lambda x:x.fitness)
        return cls.population[-1]
    
    @classmethod
    def get_N_best_word(cls,N:int) -> list:
        """
        Renvoie les N meilleurs individus de la population
        """
        Genetic_Word.population.sort(reverse=True,key=lambda x:x.fitness)
        return cls.population[:N]
    
    @classmethod
    def get_N_worst_word(cls,N:int) -> list:
        """
        Renvoie les N pires individus de la population
        """
        Genetic_Word.population.sort(reverse=True,key=lambda x:x.fitness)
        return cls.population[-N:]
    
    @classmethod
    def set_Authaurised_Word(cls,words:list) -> None:
        """
        Permet de definir le mot autorise
        """
        cls.Authaurised_Words = words

    @classmethod
    def set_Authaurised_Caracters(cls,caracters:list) -> None:
        """
        Permet de definir les caracteres autorises
        """
        cls.Authaurised_Caracters = caracters
    
    @classmethod
    def getE(cls) -> list:
        """
        Retourne la liste des mots compatibles
        """
        return cls.E
    
    
        
    @staticmethod
    def generate_initial_population(words:list) -> list:
        """
        Génère une population de taille size
        """
        for _ in range(0,Genetic_Word.TAILLE_POP):
            Genetic_Word(random.choice(words))
    
    

def algo_genetique(words:list,N:int,Authorised_Caracters) -> list:
    Genetic_Word.generate_initial_population(words[N])
    Genetic_Word.set_Authaurised_Word(words[N])

    Genetic_Word.set_Authaurised_Caracters(Authorised_Caracters)

    for _ in range(0,Genetic_Word.MAX_GEN):
        for i in range(0,Genetic_Word.TAILLE_POP):
            Genetic_Word.population[i].mutation()
        Genetic_Word.population.sort(reverse=True,key=lambda x:x.fitness)
    
    return Genetic_Word.getE()

        
##########   MAIN   ##########


all_words = parse()
#Nombre de lettre dans le mot que l'on cherche
N = 4

#Genetic_Word.generate_initial_population(all_words[N])
Genetic_Word.set_Authaurised_Word(all_words[N])
Genetic_Word.set_Authaurised_Caracters(alph)
parent1 = Genetic_Word("coucou")
parent2 = Genetic_Word("pommes")
print(Genetic_Word.getPopulation())
Genetic_Word.breed(parent1,parent2)
print(Genetic_Word.getPopulation())

"""
for p in Genetic_Word.getPopulation():
    p.mutation()
print(Genetic_Word.get_best_word().fitness)
print(Genetic_Word.getPopulation())
print(Genetic_Word.getE())
"""
