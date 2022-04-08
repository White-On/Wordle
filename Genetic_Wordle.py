from Parse_Wordle import *
import string
import time
import matplotlib.pyplot as plt
from Tools_Wordle import *

alph = string.ascii_lowercase
vowels = ["a","e","i","o","u"]

class Genetic_Word:
    MAX_SIZE = 50
    MAX_GEN = 30
    MUTATION_PROB = 0.2
    

    # ensemble des mots compatibles avec les essais précedent
    E = []

    TAILLE_POP = 200
    population = []

    def __init__(self,word:str) -> None:
        self.word = word
        self.fitness = self.evalutation()
        Genetic_Word.population.append(self)
    
    def __eq__(self, __o: object) -> bool:
        return self.word == __o.word
    
    def __repr__(self) -> str:
        return f"{self.word} : {self.fitness}"

    def evalutation(self) -> float:
        """
        Fonction qui calcule le score d'un mot
        """
        # On pars sur une heristique basé sur le nombre de 
        # lettre compatible lors des essais précedents
        return sum([Genetic_Word.Score_Caracter[c] for c in self.word])
    
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
            self.crossover(random.choice(Genetic_Word.population))
        

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
        j = random.randint(i+1,len(self.word)-1)
        self.word = self.word[:i] + self.word[j] + self.word[i+1:j] + self.word[i] + self.word[j+1:]
    
    def crossover(self,other) -> None:
        """
        Fonction qui effectue un crossover entre deux mots
        """
        if len(self.word) != len(other.word):
            raise Exception(f"Les deux mots doivent avoir la meme taille ({self.word} et {other.word})")
        else:
            i = random.randint(0,len(self.word)-1)
            self.word = self.word[:i] + other.word[i:]
        
    def setCompatible(self):
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
        
        self.fitness = self.evalutation()

        if len(Genetic_Word.E) >= Genetic_Word.MAX_SIZE:
                    raise Exception("La taille de l'ensemble de solution à atteind la limite")
    
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
    def set_UnAuthaurised_Word(cls,words:list) -> None:
        """
        Permet de definir le mot non autorise
        """
        cls.UnAuthaurised_Words = words
    
    @classmethod
    def set_Score_Caracter(cls,score:list) -> None:
        """
        Permet de definir le score des caracteres
        """
        cls.Score_Caracter = score
    
    @classmethod
    def reset_Class(cls)->None:
        """
        Permet de reinitialiser la classe
        """
        cls.Authaurised_Words = []
        cls.UnAuthaurised_Words = []
        cls.Score_Caracter = []
        cls.Authaurised_Caracters = []
        cls.population = []
        cls.E = []
        cls.MAX_SIZE = 50
        cls.MAX_GEN = 30

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
    
    

def algo_genetique(words:list,Unauthorised_words:list,Authorised_Caracters:list,Score:list) -> list:
    Genetic_Word.reset_Class()
    Genetic_Word.set_Authaurised_Word(words)
    Genetic_Word.set_Authaurised_Caracters(Authorised_Caracters)
    Genetic_Word.set_UnAuthaurised_Word(Unauthorised_words)
    Genetic_Word.set_Score_Caracter(Score)

    Genetic_Word.generate_initial_population(words)

    for _ in range(0,Genetic_Word.MAX_GEN):
        parents = Genetic_Word.get_N_best_word(int(Genetic_Word.TAILLE_POP/2))
        Genetic_Word.resetPopulation()
        for _ in range(0,int(Genetic_Word.TAILLE_POP/2)):
            Genetic_Word.breed(random.choice(parents),random.choice(parents))
        for i in range(0,int(Genetic_Word.TAILLE_POP/2)):
            if random.random() < Genetic_Word.MUTATION_PROB:
                Genetic_Word.population[i].mutation()
            try:
                Genetic_Word.population[i].setCompatible()
            except Exception as e:
                #print(e)
                return Genetic_Word.getE()
        Genetic_Word.population.extend(parents)
    return Genetic_Word.getE()


def Solve_Genetic(correct_word:str,words:list):
    """ Cherche à résodre le problème du wordle avec l'algorithme génétique """
    Unauthorised_words = []
    Authorised_Caracters = list(alph)
    Unauthorised_Caracters = []
    Score = {c:1 for c in alph}
    n = len(correct_word)
    Authorised_Word = words.copy()

    iteration = 0

    while True:
        sol = random.choice(algo_genetique(Authorised_Word,Unauthorised_words,Authorised_Caracters,Score))

        iteration += 1
        print(f"iteration {iteration}"+"\tsolution "+sol)

        # on teste le mot
        check = check_correct2(correct_word,sol) 
        Unauthorised_words.append(sol)
        Authorised_Word.remove(sol)

        if check[0] == n:
            print(f"Le mot cherchée était \"{correct_word}\", le mot retrouvée est \"{sol}\"")
            return iteration
        
        elif  check[2] == n:
            for l in list(set(sol)):
                try:
                    # donc on retire les lettres du champs des lettres possible et on les ajoute aux lettre impossibles
                    Authorised_Caracters.remove(l)
                    Unauthorised_Caracters.append(l)
                    
                except:
                    continue
            Authorised_Word = remove_impossible(Unauthorised_Caracters,Authorised_Word)
        
        # si toutes les lettre sont au moins dans le mot que l'on cherche, notre liste de lettre 
        # possible est celle des lettres du mot que l'on viens de proposer
        elif check[2] == 0:
            Authorised_Caracters = list(set(sol))
            Unauthorised_Caracters = [c for c in alph if c not in Authorised_Caracters]
            Authorised_Word = remove_impossible(Unauthorised_Caracters,Authorised_Word)

        # on calcule le score des lettres
        
        for l in list(set(sol)):
            try:
                Score[l] += check[1] + check[0]
            except:
                continue
        
        """if check[0] + check[1] >= n/2:
            for c in sol:
                Score[c] += check[0] + check[1] 
        else:
            for c in sol:
                Score[c] -= check[2]"""
        
    
def plot_result2(spectre:range,words:list)->None:
    """
    Permet de tracer les resultats de l'algorithme génétique
    """
    list_time = []
    iteration = []

    for n in spectre:
        start = time.time()
        iteration.append(Solve_Genetic(give_random_word(words,n),words[n]))
        end = time.time()
        list_time.append(end-start)
        plt.scatter(n,len(words[n]),label=f"{n} lettres")
        

    
    # on tracer le graphique de la vitesse de résolution de l'algorithme génétique
    plt.plot(spectre,list_time,label="temps")
    plt.xlabel("taille du mot en nombre de lettre")
    plt.ylabel("temps d'execution en sec")
    plt.title(f"Vitesse de résolution de l'algorithme génétique")
    plt.legend()
    plt.show()

    # on tracer le graphique de la vitesse de résolution de l'algorithme génétique
    plt.plot(spectre,iteration,label="itération")
    plt.xlabel("taille du mot en nombre de lettre")
    plt.ylabel("itérations")
    plt.title(f"Nombre d'itération de l'algorithme génétique ")
    plt.legend()
    plt.show()

##########   MAIN   ##########


all_words = parse()
#Nombre de lettre dans le mot que l'on cherche
N = 5

#Genetic_Word.generate_initial_population(all_words[N])
"""
Genetic_Word.set_Authaurised_Word(all_words[N])
Genetic_Word.set_Authaurised_Caracters(alph)
parent1 = Genetic_Word("coucou")
parent2 = Genetic_Word("pommes")
print(Genetic_Word.getPopulation())
Genetic_Word.breed(parent1,parent2)
print(Genetic_Word.getPopulation())

for p in Genetic_Word.getPopulation():
    p.mutation()
print(Genetic_Word.get_best_word().fitness)
print(Genetic_Word.getPopulation())
print(Genetic_Word.getE())

score = {c:1 for c in alph }
E = algo_genetique(all_words[N],[],alph,score)
print(E)

"""

#print(Solve_Genetic(give_random_word(all_words,N),all_words[N]))

plot_result_intervalle(range(3,6),all_words,Solve_Genetic,5)

