import json
from pathlib import Path
from uuid import uuid4

DATA_DIR = Path(__file__).resolve().parent / "data"
INVENTORY_FILE = DATA_DIR / "inventory.json"
BOOKINGS_FILE = DATA_DIR / "bookings.json"


def load_inventory():
    with INVENTORY_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_item_by_id(item_id):
    for item in load_inventory():
        if item["id"] == item_id:
            return item
    return None


def load_bookings():
    if not BOOKINGS_FILE.exists():
        return []
    with BOOKINGS_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, list) else []


def save_bookings(bookings):
    with BOOKINGS_FILE.open("w", encoding="utf-8") as f:
        json.dump(bookings, f, indent=2)


def get_available_stock(item_id, event_date):
    item = get_item_by_id(item_id)
    if not item:
        return 0

    # Subtract already-booked quantities for the requested item and date
    booked_qty = sum(
        b.get("quantity", 0)
        for b in load_bookings()
        if b.get("item_id") == item_id and b.get("event_date") == event_date
    )
    return max(0, item["total_stock"] - booked_qty)


def create_booking(item_id, event_date, quantity, customer_name):
    item = get_item_by_id(item_id)
    if not item:
        return None, "Selected item was not found."

    if quantity <= 0:
        return None, "Quantity must be at least 1."

    available = get_available_stock(item_id, event_date)
    if quantity > available:
        return None, f"Only {available} unit(s) of {item['name']} available on {event_date}."

    booking = {
        "booking_id": str(uuid4())[:8],
        "item_id": item_id,
        "item_name": item["name"],
        "event_date": event_date,
        "quantity": quantity,
        "customer_name": customer_name.strip() or "Guest",
        "total_price": round(item["price_per_day"] * quantity, 2),
    }

    bookings = load_bookings()
    bookings.append(booking)
    save_bookings(bookings)
    return booking, None