import numpy as np
import pandas as pda

def OpenAndStock(fileInput):
    #Avec cette fonction on récupére le tableau de contraintes qu'on va réajuster et mettre dans un tableau et donc stocker
    file=[]
    fichier = open(fileInput, "r")

    line = fichier.readline()
    line_cut = line.strip("\n")
    line_ = line_cut.split(" ")
    for j in range(0, len(line_)):
        if (line_[j] == ''):
            line_.pop()
    if (line_):
        file.append(line_)

    while line:
        line = fichier.readline()
        line_cut = line.strip("\n")
        line_ = line_cut.split(" ")
        for j in range(0,len(line_)):
            if(line_[j]==''):
                line_.pop()
        if (line_):
            file.append(line_)
    fichier.close()
    #(file)
    return file

def Sommets(mainFile):
    #On calcule le nombre de sommets
    return (len(mainFile)+2)

def reajustementTab(mainFile2):
    #Avec cette fonction on a va rajouter un 0 aux valeurs qui n'ont pas de prédécesseur dans notre tableau de contraintes
    #Car s'ils n'ont pas de prédécesseurs cela veut dire que leur prédécesseur est le sommet alpha (soit 0)
    for i in range(0,len(mainFile2)):
        if(len(mainFile2[i]) < 3):
            mainFile2[i].append('0')
    return mainFile2

def initiateMatrix(sommet):
    #Initialisation de notre matrice avec des * partout
    matrix = []
    for i in range(0,sommet):
            matrix.append(['*'] * sommet)
    return np.array(matrix)

def lock(mainFile2, caseMatrix, isLinkToEnd):
    #Cette fonction est une fonction récursive qu'on utilise dans la fonction ValuesMatrix qui nous permet de parcourir le graphe
    #en profondeur.
    y = 0
    exit = False
    verifIfLink = caseMatrix
    #print("lock verif ",verifIfLink)
    while exit == False and y < len(mainFile2):
        #print("lock ", y)
        if(verifIfLink == mainFile2[y][0]):
            if (len(mainFile2[y]) < 4):
                try:
                    isLinkToEnd.index(mainFile2[y][2])
                    exit = True
                except:
                    verifIfLink = mainFile2[y][2]
                    isLinkToEnd.append(verifIfLink)
                    y = 0
            else:
                for m in range(2, len(mainFile2[y])):
                    try:
                        isLinkToEnd.index(mainFile2[y][m])
                        if m == len(mainFile2[y])-1:
                            exit = True
                    except:
                        #print("y lock m",y, m)
                        verifIfLink = mainFile2[y][m]
                        isLinkToEnd.append(verifIfLink)
                        #print(verifIfLink)
                        lock(mainFile2=mainFile2, caseMatrix=mainFile2[y][m], isLinkToEnd=isLinkToEnd)

        else:
            y = y + 1

def ValuesMatrix(matrix, mainFile2):
    #avec cette fonction on vérifie si tous les chemins vont jusqu'au dernier sommet omega
    #si ce n'est pas le cas on rajoute artificiellement un arc sortant du sommet en question jusqu'au dernier sommet omega.
    isLinkToEnd = []
    isLinkToEnd.append(str(len(mainFile2)))
    for x in range(2, len(mainFile2[len(mainFile2) - 1])):
        verifIfLink = mainFile2[len(mainFile2) - 1][x]
        #print("verif X : ", verifIfLink)
        isLinkToEnd.append(verifIfLink)
        y = 0
        while y < len(mainFile2)-1:
            #print(isLinkToEnd)
            #print("y :",y)
            #print("first ver", verifIfLink)
            if (verifIfLink == mainFile2[y][0]):
                #print("if")
                if (len(mainFile2[y]) < 4):
                    #print("len < 4")
                    try:
                        #print("try")
                        isLinkToEnd.index(mainFile2[y][2])
                        #print("correct ?")
                        y = y + 1
                    except:
                        #print("except")
                        verifIfLink = mainFile2[y][2]
                        isLinkToEnd.append(verifIfLink)
                        #print("verifIfLink1 :", verifIfLink)
                        y = 0
                else:
                    #print("else ", mainFile2[y])
                    ifver = 1
                    for m in range(2, len(mainFile2[y])):
                        #print("m", m)
                        try:
                            isLinkToEnd.index(mainFile2[y][m])
                            #print("tryyyy")
                            if m == (len(mainFile2[y])-1):
                                #print("azeazeaz")
                                ifver = 0
                                y = y + 1
                        except:
                            #print(y)
                            #print("veriif ", mainFile2[y][2])
                            verifIfLink = mainFile2[y][m]
                            #print("mm ",mainFile2[y])
                            #print("v1",verifIfLink)
                            isLinkToEnd.append(verifIfLink)
                            lock(mainFile2=mainFile2, caseMatrix=mainFile2[y][m], isLinkToEnd=isLinkToEnd)
                            #print(isLinkToEnd)
                    if ifver != 0:
                        y = 0

            else:
                y = y + 1
    isLinkToEnd = list(set(isLinkToEnd))
    #print(isLinkToEnd)

    isNotLinktoEnd = []
    for v in range(0, len(matrix[0])):
        try:
            isLinkToEnd.index(str(v))
        except:
            if(v != len(matrix[0])-1):
                isNotLinktoEnd.append(str(v))

    #print(isNotLinktoEnd)
    nothing = 0
    isNotLinktoEnd2 = isNotLinktoEnd.copy()
    for o in range(0, len(isNotLinktoEnd)):
        for m in range(0, len(mainFile2)):
            if len(mainFile2[m]) < 4:
                if isNotLinktoEnd[o] == mainFile2[m][2]:
                    try:
                        isNotLinktoEnd2.remove(isNotLinktoEnd[o])
                    except:
                        nothing = 1
            else:
                for l in range(2, len(mainFile2[m])):
                    if isNotLinktoEnd[o] == mainFile2[m][l]:
                        try:
                            isNotLinktoEnd2.remove(isNotLinktoEnd[o])
                        except:
                            nothing = 1
    #print("Need to be link :",isNotLinktoEnd2)
    #Ici on va remplir notre matrice avec les valeurs qui nous ont été données dans le tableau de contraintes.
    for i in range(0, len(matrix)):
        for j in range(0,len(matrix[0])):
            if (str(j) == mainFile2[(len(mainFile2)-1)][0] and i==(len(matrix)-1)):
                matrix[i][j] = mainFile2[(len(mainFile2)-1)][1]
            for a in range(0, len(mainFile2)):
                for b in range(0, len(mainFile2[a])):
                    if len(mainFile2[a]) < 4:
                        if((str(i) == mainFile2[a][0]) and (str(j) == mainFile2[a][2])):
                            if(mainFile2[a][2]=='0'):
                                matrix[i][j] = '0'
                            for d in range(0,len(mainFile2)):
                                    if(mainFile2[d][0] == mainFile2[a][2]):
                                        matrix[i][j] = mainFile2[d][1]
                    else:
                        for c in range(2, len(mainFile2[a])):
                            if ((str(i) == mainFile2[a][0]) and (str(j) == mainFile2[a][c])):
                                if (mainFile2[a][c] == '0'):
                                    matrix[i][j] = '0'
                                for d in range(0, len(mainFile2)):
                                    if (mainFile2[d][0] == mainFile2[a][c]):
                                        matrix[i][j] = mainFile2[d][1]

    #Donc avec cette dernière boucle on continue de remplir la matrice mais avec les valeurs des sommets qui ne vont pas
    #jusqu'au sommet omega.
    for w in range(0, len(isNotLinktoEnd2)):
        for v in range(0, len(matrix[0])):
            if (isNotLinktoEnd2[w] == str(v)):
                g = 0
                stop = False
                while (stop == False and g < len(mainFile2)):
                    if str(v) == mainFile2[g][0]:
                        matrix[len(matrix) - 1][v] = mainFile2[g][1]
                        stop = True
                    g = g + 1

    return matrix

def verifLoop(newMainFile, mainFileSave):
    #Avec cette fonction nous vérifions si toutes les conditions sont respectées par notre graphe pour qu'il puisse être un
    #graphe d'ordonnancement
    print("\nDétection de circuit...\n")
    dependance = []
    verif = list(mainFileSave)
    #print(verif)
    b = 0
    #On commence dans un premier par voir s'il y a des circuits en utilisant la méthode de suppression des sommets
    print("Suppression du sommet : 0")
    while b < len(verif):
        #print(verif)
        if len(verif[b]) < 3:
            for a in range(0, len(verif)):
                if len(verif[a]) > 2:
                    c = 2
                    while c < len(verif[a]):
                        if (verif[b][0] == verif[a][c]):
                            verif[a].pop(c)
                            c = 2
                        else:
                            c = c + 1
            print("Suppression du sommet :",verif[b][0])
            verif.pop(b)
            b = 0
        elif len(verif[b]) >= 3:
            #print("else", verif[b])
            cont = True
            i = 2
            while cont == True and i < len(verif[b]):
                if dependance:
                    d = 0
                    stop = False
                    while stop == False and d < len(dependance):
                        if int(dependance[d]) != int(verif[b][i]) and int(verif[b][i]) < int(verif[b][0]):
                            cont = True
                        else:
                            cont = False
                            stop = True
                            dependance.append(verif[b][0])
                        d = d + 1
                else:
                    if int(verif[b][i]) < int(verif[b][0]):
                        cont = True
                    else:
                        cont = False
                        dependance.append(verif[b][0])
                i = i + 1
            if cont == False:
                b = b + 1
            else:
                for j in range(2, len(verif[b])):
                    for a in range(0, len(verif)):
                        if len(verif) > 2:
                            c = 2
                            while c < len(verif[a]):
                                if (verif[b][0] == verif[a][c]):
                                    verif[a].pop(c)
                                    c = 2
                                else:
                                    c = c + 1
                print("Suppression du sommet :",verif[b][0])
                verif.pop(b)
                b = 0
        else:
            b = b + 1
        dependance = list(set(dependance))
    if(not(verif)):
        print("Tous les sommets ont été supprimés !")
    else:
        print("Tous les sommets n'ont pas été supprimés !")
    #print(dependance)
    #print(verif)
    #Dans le if, si verif = True alors ça veut dire que notre graphe contient un ou plusieurs circuits
    if verif:
        print("\nCe graphe contient un/plusieurs circuit(s) !")
        print("Les sommets qui n'ont pas pu être supprimés, avec la méthode de suppression des points d'entrée, sont :\n")
        for j in range(0, len(dependance)):
            dependance[j] = int(dependance[j])
        dependance.sort()
        for i in range(0, len(dependance)):
           print(dependance[i], end='|',)
        print("")
        arcsNuls(newMainFile)
        #On regarde s'il y a des arcs négatifs
        if arcNegatif(newMainFile) == 0:
            print("\nIl y a des arcs négatifs")
        else:
            print("\nIl n'y a pas d'arcs négatifs")
        print("\n-> Ce n'est pas un graphe d'ordonnancement")
        return 1
    #Dans le else on prévient notre utilisateur que ce graphe ne contient pas de circuits
    else:
        print("\nCe graphe ne contient pas de circuits !")
        arcsNuls(newMainFile)
        # On regarde s'il y a des arcs négatifs, s'il y en a dans ces cas là on retourne 1 ce qui dira à l'utilisateur qu'il ne
        #peut pas continuer avec ce graphe
        if arcNegatif(newMainFile) == 0:
            print("\nIl y a des arcs négatifs")
            return 1
        else:
            print("\nIl n'y a pas d'arcs négatifs")
        print("\n-> C'est un graphe d'ordonnancement")
        return 0

def arcsNuls(newMainFile):
    #avec cette fonction nous vérifions quels arcs sont nuls
    print("\nles arcs :")
    for i in range(0, len(newMainFile)):
        if (newMainFile[i][2] == '0'):
            print(newMainFile[i][2], "->", newMainFile[i][0], end='|')
    print("sont nuls")

def arcNegatif(newMainFile):
    #avec cette fonction nous vérifions si tous les arcs sont positifs
    for i in range(0, len(newMainFile)):
            if int(newMainFile[i][1]) < 0:
                return 0

def ordonnancement(matrix, mainFile):
    print("\nTableau d'ordonnancement :\n")
    rang = {}
    labels = ["rang", "Dates au plus tôt", "Dates au plus tard", "Marge totale", "Marge libre", "Chemin critique"]
    rang[0] = ['0']
    #print(mainFile)
    refaire = []
    #On attribue les bons rangs à chaque sommet :
    for i in range(0, len(mainFile)):
            #print("1",mainFile[i])
            if len(mainFile[i]) < 4:
                #print("2",mainFile[i])
                add = False
                index = -1
                save = - 1
                nothing = 0
                for cle, valeur in rang.items():
                    try:
                        valeur.index(mainFile[i][2])
                        index = cle + 1
                        save = mainFile[i][0]
                        add = True
                    except:
                        nothing = 0
                if add:
                    #print("s", save)
                    rang.setdefault(index, [])
                    rang[index].append(save)
                else:
                    refaire.append(mainFile[i])
            else:
                #print('1.1', mainFile[i])
                add = False
                index = -1
                save = - 1
                nothing = 0
                comp = -1
                skip = []
                #print(skip)

                #print('elsee', mainFile[i])
                for b in range(2, len(mainFile[i])):
                    for cle, valeur in rang.items():
                        try:
                            valeur.index(mainFile[i][b])
                            if(cle > comp):
                                comp = cle
                                index = comp + 1
                                save = mainFile[i][0]
                                add = True
                        except:
                            nothing = 0
                if add:
                    rang.setdefault(index, [])
                    rang[index].append(save)
                else:
                    refaire.append(mainFile[i])
    comparaison = []
    for r in range(0, len(refaire)):
        for f in range(2, len(refaire[r])):
            for cle, valeur in rang.items():
                for val in range(0, len(valeur)):
                    if valeur[val] == refaire[r][f]:
                        comparaison.append(cle)
        stopKey = False
        sk = 0
        rangKey = max(comparaison)+1
        while stopKey == False and sk < len(rang):
            if rangKey == sk:
                rang[rangKey].append(refaire[r][0])
                rang[rangKey].sort()
                stopKey = True
            sk = sk + 1
        if stopKey == False:
            rang.setdefault(rangKey, [])
            rang[rangKey].append(refaire[r][0])

    for cle, valeur in rang.items():
        rang[cle] = list(map(int, valeur))
    for cle, valeur in rang.items():
        rang[cle].sort()
    rang1 = {}
    for k in sorted(rang.keys()):
        rang1[k] = rang[k]
    rang = {}
    for k in rang1.keys():
        rang[k] = rang1[k]

    for cle, valeur in rang.items():
        rang[cle] = list(map(str, valeur))

    index = -1
    save = -1
    nothing = 0
    """for cle, valeur in rang.items():
        try:
            valeur.index(str(len(mainFile)))
            index = cle + 1
            save = len(mainFile) + 1
        except:
            nothing = 0"""
    #Comme précédemment on a mis nos rangs dans un dictionnaire là nous les mettons dans un tableau. Ce sera celui qui sera affiché
    rang.setdefault(len(rang), [])
    rang[len(rang) - 1].append(str((len(mainFile) + 1)))
    finalRang = []
    for cle, valeur in rang.items():
        for e in range(0, len(valeur)):
            finalRang.append(cle)

    """tacheEtLongueur = {}
    index = 0
    tacheEtLongueur[index] = '0'
    for cle, valeur in rang.items():
        for j in range(0, len(valeur)):
            for i in range(0, len(mainFile)):
                if valeur[j] == mainFile[i][0]:
                    index = index + 1
                    tacheEtLongueur[index] = mainFile[i][1]
    for cle, valeur in tacheEtLongueur.items():
        if cle == len(mainFile):
            index = cle + 1
    tacheEtLongueur[index] = '-'
    print("tache",tacheEtLongueur)

    finalTL = []
    for cle, valeur in tacheEtLongueur.items():
        string = str(cle) + "(" + str(valeur) + ")"
        finalTL.append(string)
    print(finalRang)
    print(finalTL)"""

    EarlyDate = []
    #Pendant toute cette boucle nous allons chercher la date au plus tôt pour chaque rang.
    for cle, valeur in rang.items():
        for z in range(0, len(valeur)):
            a = 0
            stop1 = False
            if valeur[z] == '0':
                EarlyDate.append(0)
                stop1 = True
            if valeur[z] == str((len(mainFile)+1)):
                EarlyDate.append(-1)
            while (stop1 == False and a < len(mainFile)):


                save = mainFile[a][0]
                #print("value", valeur[z])
                if valeur[z] == mainFile[a][0]:
                    #print("first if")
                    if len(mainFile[a]) < 4:
                        longueurChemin = 0
                        save1 = mainFile[a][2]
                        TabLongueurChemin = []
                        c = 0
                        stop = False
                        while stop == False and c < len(mainFile):
                            #print("test")
                            #print(mainFile[c][0])
                            if mainFile[c][0] == save1:
                                if len(mainFile[c]) < 4:
                                    longueurChemin = longueurChemin + int(mainFile[c][1])
                                    save1 = mainFile[c][2]
                                    c = 0
                                elif len(mainFile[c]) >= 4:
                                    longueurChemin = longueurChemin + int(mainFile[c][1])
                                    for j in range(2, len(mainFile[c])):
                                        save = mainFile[c][j]
                                        TabLongueurChemin.append(lock2(mainFile, save))
                                    stop = True
                            else:
                                c = c + 1
                        if TabLongueurChemin:
                            longueurChemin = longueurChemin + max(TabLongueurChemin)
                        EarlyDate.append(longueurChemin)
                    else:
                        #print("First Else")
                        TablElse = []

                        for y in range(2, len(mainFile[a])):
                            save1 = mainFile[a][y]
                            longueurChemin = 0
                            TabLongueurChemin = []
                            c = 0
                            stop = False
                            while stop == False and c < len(mainFile):
                                #print("loop ")
                                #print("s1", save1)
                                if mainFile[c][0] == save1:
                                    #print("ifff")
                                    #print("mFc", mainFile[c])
                                    if len(mainFile[c]) < 4:
                                        #print("2if")

                                        longueurChemin = longueurChemin + int(mainFile[c][1])
                                        #print(longueurChemin)
                                        save1 = mainFile[c][2]
                                        c = 0
                                    elif len(mainFile[c]) >= 4:
                                        #print("elif")
                                        #print(longueurChemin)
                                        longueurChemin = longueurChemin + int(mainFile[c][1])
                                        #print("22", longueurChemin)
                                        for j in range(2, len(mainFile[c])):
                                            save = mainFile[c][j]
                                            TabLongueurChemin.append(lock2(mainFile, save))
                                        #print("tbl",TabLongueurChemin)
                                        stop = True
                                else:
                                    c = c + 1
                            #print(longueurChemin)
                            if TabLongueurChemin:
                                longueurChemin = longueurChemin + max(TabLongueurChemin)
                            TablElse.append(longueurChemin)
                            #print("TBl", TablElse)
                        if TablElse:
                            longueurChemin = max(TablElse)
                        EarlyDate.append(longueurChemin)
                    stop1 = True
                    #print(EarlyDate)
                a = a +1
    #print(EarlyDate)
    #print(finalRang)
    #Là nous cherchons la date au plus tôt mais pour le dernier rang.
    TabComp = []
    for u in range(0, len(matrix)):
        for s in range(0, len(matrix[u])):
            if(u==len(matrix)-1 and matrix[u][s] != '*'):
                save = s
                saveKey = -1
                saveValue = -1
                saveIndex = -1
                saveChemin = - 1
                Index = 0
                for cle, valeur in rang.items():
                    for t in range(0, len(valeur)):
                        if int(valeur[t]) == int(save):
                            saveKey = cle
                            saveIndex = Index
                        Index = Index + 1
                for a in range(0, len(mainFile)):
                    if save == int(mainFile[a][0]):
                        saveValue = mainFile[a][1]
                for b in range(0, len(EarlyDate)):
                    if b == saveIndex:
                        saveChemin = EarlyDate[b]
                saveChemin = int(saveChemin) + int(saveValue)
                TabComp.append(saveChemin)

    for z in range(0, len(EarlyDate)):
        if EarlyDate[z] == -1:
            EarlyDate[z] =max(TabComp)
    dicoEarlyDate = {}
    index = 0
    #Comme nous avions mis les dates au plus tôt dans un tableau, nous décidons de les mettre dans un dictionnaire pour pouvoir
    #plus facilement les associer à leurs rangs respectifs.
    for cle, valeur in rang.items():
        for v in range(0, len(valeur)):
            dicoEarlyDate.setdefault(cle, [])
            dicoEarlyDate[cle].append(EarlyDate[index])
            index = index + 1
    #print(dicoEarlyDate)
    #print(EarlyDate)
    #print(rang)
    #print(mainFile)
    DicoLateDate = {}
    #Durant cette boucle fort nous parcourons les rangs du plus grand au plus petit pour pouvoir obtenir la date au plus tard pour
    #chaque rang.
    for i in range((len(rang)-1), -1, -1):
        value = rang[i]
        index = 0
        for j in range(0, len(value)):
            if int(value[j]) == len(mainFile)+1:
                for cle,valeur in dicoEarlyDate.items():
                    if i == cle:
                        DicoLateDate.setdefault(int(value[j]), [])
                        DicoLateDate[int(value[j])].append(valeur[j])
            elif int(value[j]) == 0:
                DicoLateDate.setdefault(0, [])
                DicoLateDate[0].append(0)
            elif i == len(rang)-2:
                for c in range(0, len(mainFile)):
                    if int(mainFile[c][0]) == int(value[j]):
                        DicoLateDate.setdefault(int(value[j]), [])
                        DicoLateDate[int(value[j])].append(DicoLateDate[len(mainFile)+1][0]-int(mainFile[c][1]))
            else:
                TabComp = []
                for r in range(0, len(mainFile)):
                    if value[j] == mainFile[r][0]:
                        save = int(mainFile[r][1])
                for a in range(0, len(mainFile)):
                    for b in range(2, len(mainFile[a])):
                        if mainFile[a][b] == value[j]:
                            for cle, valeur in DicoLateDate.items():
                                if cle == int(mainFile[a][0]):
                                    TabComp.append(valeur[0]-save)
                DicoLateDate.setdefault(int(value[j]), [])
                if TabComp:
                    DicoLateDate[int(value[j])].append(min(TabComp))
                else:
                    DicoLateDate[int(value[j])].append(DicoLateDate[len(mainFile)+1][0]-save)
    #print(DicoLateDate)
    LateDate = []
    #Nous mettons nos dates au plus tard dans un tableau.
    for cle1, valeur in rang.items():
        for v in range(0, len(valeur)):
            for cle2, val in DicoLateDate.items():
                if int(valeur[v]) == cle2:
                    LateDate.append(val[0])

    tache = []
    for cle, valeur in rang.items():
        for v in range(0, len(valeur)):
            tache.append(int(valeur[v]))
    #print(tache)
    #print(finalRang)
    #print(EarlyDate)
    #print(LateDate)
    MargeT=[]
    MargeL=[]
    CritWay = []
    #Enfin durant ces deux dernières boucles for nous récupérons la marge libre et le chemin critique (durant la première boucle)
    #Et dans la deuxième boucle for nous calculons les marges libres.
    for e in range(0, len(tache)):
            MargeT.append(abs(LateDate[e] - EarlyDate[e]))
            if LateDate[e] == EarlyDate[e]:
                CritWay.append("->")
            else:
                CritWay.append("*")
    MargeL.append(0)
    #print(tache)
    for e in range(1, len(tache)):
        CompMargeL = []
        saveEarlyDate = EarlyDate[e]
        if e == len(tache)-1:
            saveLongueur = 0
            for u in range(0, len(matrix)):
                for s in range(0, len(matrix[u])):
                    if (u == len(matrix) - 1 and matrix[u][s] != '*'):
                        save = s
                        saveKey = -1
                        saveValue = -1
                        saveIndex = -1
                        saveChemin = - 1
                        Index = 0
                        for z in range(0, len(mainFile)):
                            if save == int(mainFile[z][0]):
                                saveLongueur = int(mainFile[z][1])
                        for j in range(0, len(tache)):
                            if save == tache[j]:
                                #print("zer",EarlyDate[j])
                                CompMargeL.append(saveEarlyDate - EarlyDate[j] - saveLongueur)
            MargeL.append(min(CompMargeL))
        else:
            for m in range(0, len(mainFile)):
                if tache[e] == int(mainFile[m][0]):
                    if int(mainFile[m][2]) == 0:
                        MargeL.append(0)
                    else:
                        saveLongueur = 0
                        #print(tache[e])
                        for l in range(2, len(mainFile[m])):
                            for i in range(0, len(mainFile)):
                                if int(mainFile[i][0]) == int(mainFile[m][l]):
                                    #print(mainFile[i])
                                    saveLongueur = int(mainFile[i][1])
                            for j in range(0, len(tache)):
                                if int(mainFile[m][l]) == tache[j]:
                                    #print("zer",EarlyDate[j])
                                    CompMargeL.append(saveEarlyDate - EarlyDate[j] - saveLongueur)
                        #print("c",CompMargeL)
                        MargeL.append(min(CompMargeL))

    #print(MargeL)
    #print(MargeT)
    #Nous affichons notre tableau d'ordonnancement grâce à un dataFrame que nous créons grâce à pandas.
    ListOrdonnancement = pda.DataFrame(np.array([finalRang,EarlyDate,LateDate, MargeT, MargeL, CritWay]))
    ListOrdonnancement.columns = tache
    ListOrdonnancement.index = labels
    print(ListOrdonnancement)


def grapheOrdonnance(matrix, sommets):
    #avec cette fonction nous affichons le graphe d'ordonnance, ses sommets et ses arcs.
    print("\nGraphe d'ordonnance :\n")
    graphe = []
    arcs = 0
    for i in range(0, len(matrix[0])):
        for j in range(0, len(matrix)):
            if matrix[j][i] != "*":
                graphe.append(str(i) + "->" + str(j))
                arcs = arcs + 1
    print(sommets, "sommets")
    print(arcs, "arcs\n")
    return graphe

#cette fonction est utilisée pour calculer les dates au plus tôt. C'est une fonction récursive qui permet de parcourir
#notre "graphe" en profondeur.
def lock2(mainFile, save):
    y = 0
    exit = False
    comp2 = 0
    plusGrand = []
    while exit == False and y < len(mainFile):
        if (save == mainFile[y][0]):
            if (len(mainFile[y]) < 4):
                save = mainFile[y][2]
                comp2 = comp2 + int(mainFile[y][1])
                y = 0
            else:
                comp2 = comp2 + int(mainFile[y][1])
                for m in range(2, len(mainFile[y])):
                    plusGrand.append(lock2(mainFile, mainFile[y][m]))
                exit = True
        else:
            y = y + 1
    if plusGrand:
        comp2 = comp2 + max(plusGrand)
        #print("cp22", comp2)
        return comp2
    else:
        #print("cp2", comp2)
        return comp2