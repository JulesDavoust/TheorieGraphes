import fonctions as fc
import pandas as pda

x = "Oui"
while x == "Oui":
    print("Veuillez rentrer le chemin de votre fichier s'il vous plaît :")
    fileInput = input()
    cont = True
    try:
        #On essaye d'ouvrir le fichier avec le chemin qui a été donné. Si le programme ne le trouve il passe dans except
        #Il demande ensuite si nous voulons réessayer de mettre un chemin.
        mainFile = list(fc.OpenAndStock(fileInput))
    except:
        print("Impossible de trouver votre fichier... Assurez-vous d'avoir entré le bon chemin s'il vous plaît.")
        print("Voulez-vous essayer de nouveau ? (Oui ou Non) :")
        x = input()
        cont = False
    #Si le fichier a pu être bien lu est stocké nous passons dans le if Sinon on retourne au début du while
    if cont == True:
        # print(mainFile)
        #On récupére le nombre de sommets qu'on stocke dans la variable "sommets"
        sommets = fc.Sommets(mainFile)
        # print(somme)ts)
        mainFile2 = list(mainFile)
        #On appelle la fonction reajustementTab qui va rajouter les ou le "0" aux sommets qui n'ont pas de prédécesseurs.
        mainFile2 = list(fc.reajustementTab(mainFile2))
        # print(mainFile)
        #On initialiser notre matrice avec des "*"
        matrix = pda.DataFrame(fc.initiateMatrix(sommets))
        #Puis on met les valeurs, tirées de notre tableau de contraintes, dans notre matrice.
        matrix = fc.ValuesMatrix(matrix, mainFile2)
        print("Matrice des valeurs :")
        print(matrix)
        newMainFile = list(fc.OpenAndStock(fileInput))
        newMainFile = list(fc.reajustementTab(newMainFile))
        #On vérifie si avec le graphe qui a été donné nous pouvons faire le tableau d'ordonnancement
        #print(newMainFile)
        #print(mainFile2)
        verif = fc.verifLoop(newMainFile, mainFile2)
        #Si verifLoop retourne 0 on passe dans le if Sinon on demande à l'utilisateur s'il souhaite sélectionner un autre tableau de contraintes
        if verif == 0:
            #Si la fonction verifLoop a retourné 0 alors on va créer notre tableau d'ordonnancement et notre graphe d'ordonnancement
            graphe = fc.grapheOrdonnance(matrix, sommets)
            for g in range(0, len(graphe)):
                print(graphe[g])
            fc.ordonnancement(matrix, newMainFile)
            print("\nVoulez vous changer de tableau de contraintes ? (Oui ou Non) :")
            x = input()
        else:
            print("\nNous ne pouvons pas faire l'ordonnancement de ce tableau car ce dernier ne respecte pas les régles.")
            print("Voulez vous changer de tableau de contraintes ? (Oui ou Non) :")
            x = input()

print("\nAu revoir !")




