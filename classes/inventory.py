
class Item:
    def __init__(self, name: str, type: str, description: str, prop: int,
                 quantity: int):
        self.name = name
        self.type = type
        self.description = description
        self.prop = prop
        self.quantity = quantity

    def add_quantity(self, addition):
        self.quantity += addition

    def reduce_quantity(self, reduction):
        self.quantity -= reduction

