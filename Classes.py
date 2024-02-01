# Correction de G. Poux-Médard, 2021-2022

# =============== 2.1 : La classe Document ===============
class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte="", numDoc=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.numDoc = numDoc

# =============== 2.2 : REPRESENTATIONS ===============
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"

    #TD5 Fonction qui retourne le type
    def getType(self):
        return self.type
        #pass

# =============== 2.4 : La classe Author ===============
class Author:
    # Initialisation des variables de la classe
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []

# =============== 2.5 : ADD =============================
    #Fonction qui ajoute une production à la liste des productions de l'auteur
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"
    