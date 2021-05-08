from flask import request, jsonify
from flask_restful import Resource
from werkzeug.exceptions import *

from models.tables import *


class DataList(Resource):
    def __init__(self, data):
        self.data = data

    def get(self):
        return self.data.get()


class ModelList(Resource):
    def __init__(self, data):
        self.model_list = data

    def get(self):
        return jsonify(self.model_list.get_tables(Models))

    def post(self):
        model = self.model_list.add(Models, request.json)
        return jsonify(model)


class Model(Resource):
    def __init__(self, data):
        self.data = data

    def get(self, id_model):
        model = self.data.table_by_id(Models, id_model)
        return jsonify(model)

    def put(self, id_model):
        model = self.data.table_by_id(Models, id_model)
        if not model:
            raise NotFound('Invalid ID, model not found')
        json_data = request.get_json()

        model.manufacturer = json_data['manufacturer']
        model.year = json_data['year']
        if json_data['customer_id'] == "":
            model.customer_id = None
        else:
            model.customer_id = json_data['customer_id']
        self.data.update()

        return jsonify(model)

    def delete(self, id_model):
        model = self.data.table_by_id(Models, id_model)
        if not model:
            raise NotFound('Invalid ID, model not found')
        self.data.delete(model)

        return jsonify(model)


class CustomerList(Resource):
    def __init__(self, data):
        self.model_list = data

    def get(self):
        return jsonify(self.model_list.get_tables(Customers))

    def post(self):
        model = self.model_list.add(Customers, request.json)
        return jsonify(model)


class Customer(Resource):
    def __init__(self, data):
        self.data = data

    def get(self, id_customer):
        model = self.data.table_by_id(Customers, id_customer)
        return jsonify(model)

    def put(self, id_customer):
        model = self.data.table_by_id(Customers, id_customer)
        if not model:
            raise NotFound('Invalid ID, model not found')
        json_data = request.get_json()

        model.first_name = json_data['first_name']
        model.family_name = json_data['family_name']
        model.age = json_data['age']
        self.data.update()

        return jsonify(model)

    def delete(self, id_customer):
        model = self.data.table_by_id(Customers, id_customer)
        if not model:
            raise NotFound('Invalid ID, customer not found')
        self.data.delete(model)

        return jsonify(model)
