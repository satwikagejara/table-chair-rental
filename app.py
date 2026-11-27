from flask import Flask, render_template, request
import storage

app = Flask(__name__)


@app.route("/")
@app.route("/catalog")
def catalog():
    items = storage.load_inventory()
    bookings = storage.load_bookings()
    return render_template("catalog.html", items=items, bookings=bookings)


@app.route("/book", methods=["POST"])
def book():
    item_id = request.form.get("item_id", "").strip()
    event_date = request.form.get("event_date", "").strip()
    customer_name = request.form.get("customer_name", "").strip()

    try:
        quantity = int(request.form.get("quantity", "0"))
    except ValueError:
        quantity = 0

    if not event_date:
        booking = None
        error = "Please choose an event date."
    else:
        booking, error = storage.create_booking(item_id, event_date, quantity, customer_name)

    items = storage.load_inventory()
    bookings = storage.load_bookings()
    return render_template(
        "catalog.html",
        items=items,
        bookings=bookings,
        booking=booking,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)