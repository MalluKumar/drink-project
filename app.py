from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(100))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def home():
    return "Hello!!"


@app.route('/drinks')
def get_all_drinks():
    drinks = Drink.query.all()

    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}
        output.append(drink_data)

    return {"drinks": output}


@app.route('/drinks', methods=['POST'])
def post_drink():
    drink = Drink(name=request.json['name'],
                  description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    drink = Drink.query.get_or_404(drink_id)
    if drink:
        db.session.delete(drink)
        db.session.commit()
        return {"Message": "Successfully Deleted!!"}
    else:
        return {"Error": "Drink ID does not exists!!"}


@app.route('/drinks/<int:drink_id>')
def get_drink(drink_id):
    drink = Drink.query.get_or_404(drink_id)
    return {'name': drink.name, 'description': drink.description}


if __name__ == '__main__':
    app.run(debug=True)
