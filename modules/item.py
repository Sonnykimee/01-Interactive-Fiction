# Items

'''
[ID List]
Unnamed Item : 100
Empty Bottle : 101
A Bottle of Drinkable : 102
Edible : 103
Golden Whistle : 104
'''
class Item():

    def __init__(self, item_id=100, name="Unnamed Item"):
        self.item_id = item_id
        self.name = name