import json

INVENTORY_FILE = "data/inventory.json"
BOOKINGS_FILE = "data/bookings.json"


def load_inventory():
    with open(INVENTORY_FILE, "r") as file:
        return json.load(file)


def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=2)


def load_bookings():
    with open(BOOKINGS_FILE, "r") as file:
        return json.load(file)


def save_bookings(bookings):
    with open(BOOKINGS_FILE, "w") as file:
        json.dump(bookings, file, indent=2)


if __name__ == "__main__":
    items = load_inventory()
    bookings = load_bookings()
    print("Inventory items loaded:", len(items))
    print("Bookings loaded:", len(bookings))