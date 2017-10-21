
import os
from datetime import date

def getList(dossier, extension):
    listElement = []
    if not os.path.isdir(dossier) and dossier.endswith(extension):
        listElement.append(dossier)
        return (listElement)
    try:
        for element in os.listdir(dossier):
            if not os.path.isdir(element) and element.endswith(extension):
                listElement.append(element)
    except Exception as E:
        listElement = None
    return (listElement)

def parsingFile(element, dic):
    print("Parsing {}".format(element))
    try:
        f = open(element, 'r')
        for line in f:
            if line in dic:
                dic[line] = dic[line] + 1
            else:
                dic[line] = 1
    except Exception as E:
        print("parsingFile", E)
        return (None)
    return (dic)

def saveDic(dic):
    name = "CHECK_EXCEPTION_"
    now = date.today()
    name += str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    nb_time = 0
    dic = sorted(dic.items(), key=lambda t:t[1], reverse=True)
    try:
        for element in os.listdir('.'):
            if element == name:
                nb_time += 1
        name += str(nb_time) + ".exception"
        f = open(name, 'a')
        
        for element in dic:
            f.write("L'exception '{}' est apparue {} fois.\n".format(str(element[0][:-1]), str(element[1])))
        f.close()
        print("Sauvegarde réussie! Trouvez toutes les infos ici: {}".format(name))
    except Exception as E:
        print("Sauvegarde échouée: ", E)
        return False
    return True

def parseDir(element, extension):
    dic = {}
    listFile = getList(element, extension)
    if listFile == None:
        print("Erreur: {} n'est pas un dossier!".format(element))
    elif len(listFile) == 0:
        print("Aucun fichier {} n'as été trouvé dans '{}'".format(extension, element))
    else:
        for files in listFile:
            if element[-1] == '/':
                files = element + '' + files
            else:
                files = element + '/' + files
            dic = parsingFile(files, dic)
            if (dic):
                print("Analyse de '{}' Réussie!".format(files))
            else:
                print("Analyse de '{}' échouée!".format(files))
        a = saveDic(dic)
        if (a == False):
            sys.exit(1)


if __name__ == "__main__":
    import sys
    extension = ".log"
    
    try:
        if (len(sys.argv) > 1):
            if sys.argv[1].startswith("-ext="):
                extension = sys.argv[1][len("-ext="):]
            for element in sys.argv:
                if not (element.startswith("-ext=")):
                    parseDir(element, extension)
        else:
            parseDir('.', extension)
    except Exception as E:
        print("Erreur: ", E)
        sys.exit(1)
    print("Fin du programme d'analyse d'Exception")
