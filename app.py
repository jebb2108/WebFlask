import sqlite3
from flask import Flask, request, jsonify, abort, g
from pathlib import Path
from werkzeug.exceptions import HTTPException
# from flask_sqlalchemy import SQLAlchemy

BASE_DIR = Path(__name__).parent
DATABASE = BASE_DIR / 'test.db'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e


@app.route("/quotes")
def get_all_quotes():
    connection = get_db()
    cursor = connection.cursor()
    select_quotes = " SELECT * FROM quotes "
    cursor.execute(select_quotes)
    quotes_db = cursor.fetchall()
    # Правильная распаковка.
    keys = ['id', 'author', 'text']
    quotes = []
    for quote_db in quotes_db:
        quote_db = dict(zip(keys, quote_db))
        quotes.append(quote_db)
    cursor.close()
    connection.close()
    return jsonify(quotes), 200


@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    connection = get_db()
    cursor = connection.cursor()
    get_quote = f""" SELECT * FROM quotes WHERE id={quote_id} """
    cursor.execute(get_quote)
    quote_db = cursor.fetchone()
    keys = ['id', 'author', 'text']
    if quote_db is None:
        abort(404, f"The quote with id={quote_id} is not found.")
    quote = dict(zip(keys, quote_db))
    return jsonify(quote), 200



# @app.route("/quotes/filter")
# def get_quotes_by_filter():
#     args = request.args
#     res = []
#     for quote in quotes:
#         if all(args.get(key, type=type(quote[key])) == quote[key] for key in args):
#             res.append(quote)
#
#     return jsonify(res)


@app.route("/quotes", methods=["POST"])
def create_quotes():
    new_data = request.json
    connection = get_db()
    cursor = connection.cursor()
    create_quote = """ INSERT INTO quotes  (author, text) VALUES (?, ?) """
    cursor.execute(create_quote, (new_data['author'], new_data['text']))
    connection.commit()
    new_id = cursor.lastrowid
    new_data['id'] = new_id
    return jsonify(new_data), 201


# noinspection All
@app.route("/quotes/<int:id>", methods=["PUT"])
def edit_quote(quote_id):
    new_data = request.json
    connection = get_db()
    cursor = connection.cursor()
    update_quote = """ UPDATE quotes SET author=?, text=?, WHERE id=? """
    cursor.execute(
        update_quote, (new_data['author'], new_data['text'], quote_id))
    connection.commit()
    if cursor.rowcount > 0:
        new_data['id'] = quote_id
        return jsonify(new_data), 200
    abort(404, f"Quote with {quote_id} is not found")


@app.route('/quotes/<int:quote_id>', methods=["DELETE"])  # Берет int из URL.
def delete(quote_id):
    connection = get_db()
    cursor = connection.cursor()
    delete_quote = """ DELETE FROM quotes WHERE id=? """
    cursor.execute(delete_quote, (quote_id))
    connection.commit()
    if cursor.rowcount > 0:
        return jsonify({'message': f"The quote with id= {quote_id} has been deleted."})
    abort(404, f"The quotes with id= {quote_id} is not found.")


if __name__ == "__main__":
    app.run(debug=True)
