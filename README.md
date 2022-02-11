# polymorphic-shellcode

## Prérequis:
- Python3
- nasm

## Objectifs
Transformer un code assembleur pour exécuter la même fonction mais avec des instructions différentes 

## Développement
Etapes:
[ ] Rechercher des marqueurs pouvant être changé
[ ] Associer un label de `dico.json` à ce marqueur
[ ] Remplacer le marqueur par l'une des alternatives proposées dans le `dico.json`

## Utilisation:
1. Peupler le fichier `dico.json`
2. Mettre le fichier assembleur à polymorpher dans le dossier input
3. Lancer le programme, choisir le fichier assembleur dans le menu puis choisir `Go polymorphism`.
4. Récupérer le résultat dans le dossier output.