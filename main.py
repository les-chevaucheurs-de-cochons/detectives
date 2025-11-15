class Suspect:
    def __init__(self,nom : str, prenom : str ,age : int, adresse : str):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.adresse = adresse

    def __str__(self):
        return f"Suspect(nom={self.nom},prenom={self.prenom} ,age={self.age})"

class Enquete:
    def __init__(self,suspect : str,preuves : str, date : int):
        self.suspect = suspect
        self.preuves = preuves
        self.date = date

    def afficher(self):
        print(f"Suspect : {self.suspect}")
        print(f"Preuves : {self.preuves}")
        print(f"Date : {self.date}")


e = Enquete("pierre", "couteau", 12)
e.afficher()

s = Suspect('Diego','Ducamp',21,'wavre')
print(s)