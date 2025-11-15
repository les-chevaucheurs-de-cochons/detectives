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