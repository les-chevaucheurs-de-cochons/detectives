"""

Ce fichier a été commenté par une intelligence artificielle (ChatGpt)

"""

# Exception personnalisée pour signaler
# qu'une PRE-condition n'est pas respectée
class PreconditionError(ValueError):
    """
    Exception levée lorsqu'une condition
    préalable à l'exécution d'une action
    n'est pas respectée.
    Exemple : titre vide avant un INSERT.
    """
    pass


# Exception personnalisée pour signaler
# qu'une POST-condition n'est pas respectée
class PostconditionError(RuntimeError):
    """
    Exception levée lorsqu'une condition
    attendue après une action n'est pas atteinte.
    Exemple : id non généré après un INSERT.
    """
    pass

