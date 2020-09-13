# Player

from modules.item import Item

class Player():

    def __init__(self, name="Unnamed Player"):
        self.name = name
        self.items = [Item(103, "Nacho Chips")]
        self.valor = 0
        self.honesty = 0
        self.mercy = 0
        self.talking = None


    def see_items(self):
        count = 0
        print("[Your Inventory]")
        for i in self.items:
            print("[" + str(count) + "] " + i.name, end=", ")
            count += 1
        print("")


    def add_item(self, item):
        self.items.append(item)
        print("[" + item.name + " has added to your inventory.]")


    def remove_item(self, item):
        self.items.remove(item)
        print("[" + item.name + " has removed from your inventory.]")


