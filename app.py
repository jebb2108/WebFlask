from random import choice
from flask import Flask, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

about_me = {
    "name": "Габриэль",
    "surname": "Бушар",
    "email": "gabouchard2002@gmail.com"
}

quotes = [
    {
        "id": 3,
        "author": "Rick Cook",
        "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
    },
    {
        "id": 5,
        "author": "Waldi Ravens",
        "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
    },
    {
        "id": 6,
        "author": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
    },
    {
        "id": 8,
        "author": "Yoggi Berra",
        "text": "В теории, теория и практика неразделимы. На практике это не так."
    },

]


@app.route("/")
def hello_world():
    return "Hello, world!"


@app.route("/about")
def about():
    return about_me


# Сериализация list -> str. Под капотом преобразует в json строку.
@app.route("/quotes")
def quotes_all_quotes():
    return quotes


@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    for quote in quotes:
        if quote['id'] == quote_id:
            return quote
        return f"Quotes with id={quote_id} not found", 404


@app.route("/quotes/random", methods=["GET"])
def random_quote():
    return choice(quotes)


@app.get("/quotes/count")
def goutes_count():
    return {
        "count": len(quotes)
    }


@app.route("/quotes", methods=["POST"])
def create_quote():
    new_quote = request.json
    last_quote = quotes[-1]
    new_id = last_quote["id"] + 1
    new_quote['id'] = new_id
    quotes.append(new_quote)
    return new_quote, 201


@app.route("/quotes/<id>", methods=["PUT"])
def edit_quote(id):
    new_data = request.json
    quote = get_quote_by_id(id)
    if quote['text'] == new_data['text']:
        quote['text'] = new_data['text']
        return "Successfully replaced.", 200

    return "Error", 404


@app.route('/quotes/<id>', methods=["DELETE"])
def delete(id):
    quote = get_quote_by_id(id)
    quotes.remove(quote)
    return f"The {quote} is deleted."


if __name__ == "__main__":
    app.run(debug=True)
