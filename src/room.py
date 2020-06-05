# Implement a class to hold room information. This should have name and
# description attributes.

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.n_to = "wall"
        self.s_to = "wall"
        self.e_to = "wall"
        self.w_to = "wall"