from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from resources import *
from models.tables import *


class DataService:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        data = {
            'Models': {},
            'Customers': {}
        }
        models = self.db.session.query(Models).all()
        customers = self.db.session.query(Customers).all()
        for model in models:
            data['Models'][int(model.id)] = model
        for customer in customers:
            data['Customers'][int(customer.id)] = customer
        return jsonify(data)

    def get_tables(self, table):
        return self.db.session.query(table).all()

    def table_by_id(self, table, id_model):
        return self.db.session.query(table).get(id_model)

    def add(self, table, json_data):
        table_return = []
        if table == Models:
            if json_data['customer_id'] == '':
                table_return = Models(manufacturer=json_data['manufacturer'], year=json_data['year'],
                                      customer_id=None)
            else:
                table_return = Models(manufacturer=json_data['manufacturer'], year=json_data['year'],
                                      customer_id=json_data['customer_id'])
        elif table == Customers:
            table_return = Customers(first_name=json_data['first_name'], family_name=json_data['family_name'],
                                     age=json_data['age'])
        self.db.session.add(table_return)
        self.db.session.commit()
        return table_return

    def update(self):
        self.db.session.commit()

    def delete(self, model):
        self.db.session.delete(model)
        self.db.session.commit()


class server:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.route("/", methods=['GET', 'POST', 'PUT'])
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite"
        api = Api(self.app)
        self.db = SQLAlchemy(self.app)
        data = DataService(self.db)

        api.add_resource(DataList, '/', resource_class_args=[data])
        api.add_resource(ModelList, '/models/', resource_class_args=[data])
        api.add_resource(Model, '/models/<id_model>/', resource_class_args=[data])

        api.add_resource(CustomerList, '/customers/', resource_class_args=[data])
        api.add_resource(Customer, '/customers/<id_customer>/', resource_class_args=[data])

        self.app.run(debug=True)


if __name__ == '__main__':
    server()
