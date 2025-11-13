suspects_lst = ['Thomas', 'Pierre', 'Louis', 'Max', 'Luc']

def TrouverLeCoupable(suspects):
    for nom in suspects:
        if len(nom) == 5:
            return(nom)

def texte(coupable):
    return 'Le coupable est ' + coupable

coupable = TrouverLeCoupable(suspects_lst)
print(texte(coupable))