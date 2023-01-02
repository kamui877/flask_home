from flask import Flask
from views import AdvertView, register


app = Flask("app")


app.add_url_rule("/register/", view_func=register, methods=["POST"])
app.add_url_rule("/advert/<int:id>", view_func=AdvertView.as_view("advert"), methods=["GET", "PATCH", "DELETE"])
app.add_url_rule("/advert/", view_func=AdvertView.as_view("advert_create"), methods=["POST"])


app.run(host="127.0.0.1", port=5000)
