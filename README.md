# Projet RP 2022

Le projet est répartie sur 5 fichiers :
* CSP_Wordle.py
* Genetic_Wordle.py
* Tools_Wordle.py
* Parse_Wordle.py
* Main.py

**Tools_Wordle.py** contient les fonctions utiles pour les différents algorithmes de résolution de Wordle. Vous pouvez y trouver les fonctions de test suivantes :
* plot_result(spectre:range,words:list,function,maxiter=False) permet de tracer le temps de résolution et le nombre de tentatives pour un nombre de lettres donné.
* plot_result_intervalle(spectre:range,all_words:list,function,intervalle=None,maxiter=False) permet de tracer le temps de résolution et le nombre de tentatives moyen pour un nombre de lettres donné et un nombre de fois que l'action sera répété.
* Compare(function1,function2,n_caracter,instance,maxiter=False) permet de comparer les deux fonctions passées en paramètre.
* Compare4(function1,function2,function3,function4,n_caracter,instance,maxiter=False) permet de comparer les quatre fonctions passées en paramètre.

**Parse_Wordle.py** contient les fonctions utiles pour parser les fichiers de données.
Main.py contient les fonctions utiles pour lancer les différents algorithmes de résolution de Wordle pour des essais rapides.

**Generate_Wordle.py** et **CSP_Wordle.py** contiennent les fonctions de résolution de Wordle. Vous y trouverez des tests déjà près a l'emploit à la fin des fichiers.