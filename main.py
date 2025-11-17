class Suspect:
    def __init__(self,nom : str, prenom : str ,age : int, adresse : str):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.adresse = adresse

    def __str__(self):
        return f"Suspect(nom={self.nom},prenom={self.prenom} ,age={self.age})"

class Preuve:
    def __init__(self, description : str,lieu : str,element_sup : str = None):
        self.description = description
        self.lieu = lieu
        self.element_sup = element_sup

    def __str__(self):
        print(f"Preuve({self.description}, lieu={self.lieu})")


class Enquete:
    def __init__(self, titre: str, date_ouverture: int, statut: str = "ouverte"):
        self.titre = titre
        self.date_ouverture = date_ouverture
        self.statut = statut
        self.suspects: list[Suspect] = []
        self.preuves: list[Preuve] = []

    def ajouter_suspect(self, suspect: Suspect):
        self.suspects.append(suspect)

    def ajouter_preuve(self, preuve: Preuve):
        self.preuves.append(preuve)

    def afficher(self):
        print("Suspects")
        for s in self.suspects:
            print(f" - {s.nom} , {s.prenom}")
        print(f"Date d'ouverture : {self.date_ouverture}")



#e = Enquete("pierre", "couteau", 12)
#e.afficher()

#s = Suspect('Diego','Ducamp',21,'wavre')
#print(s)

s1 = Suspect("Pierre" , "Lee" , 19 , "Louv")
s2 = Suspect('Diego','Ducamp',21,'wavre')

e1 = Enquete("Braquage" , 2025)
e1.ajouter_suspect(s1)
e1.ajouter_suspect(s2)

p1 = Preuve('Couteau resté sur place', 'devant la banque')
e1.ajouter_preuve(p1)

for s in e1.suspects:
    print(s.nom , s.prenom)

for p in e1.preuves:
    print(p.description,' / ',p.lieu)


